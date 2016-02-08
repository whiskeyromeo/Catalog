from flask import Flask, render_template, request, url_for, redirect,\
flash, jsonify, json, make_response

from . import auth
from .. import db
from ..models import User, LoginUser

# Oauth imports
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# General User authentication
from .forms import LoginForm, RegisterForm


CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


############################
# Handler Functions
############################

# Commit a new user to the database
def commitUser(name, picture, email):
    db.session.add(User(name=name, picture=picture, email=email))
    db.session.commit()

# Output a welcome message to the user before redirecting back to the home
# page.
def returnHTMLOutput(login_session):
    print 'Returning output...'
    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['name'])
    return output

# Make a json response
def makeJSONResponse(string, code):
    response = make_response(json.dumps(string), code)
    response.headers['Content-Type'] = 'application/json'
    return response

# Create a user based on data and return their new id
def createUser(data):
    commitUser(data['name'], data['picture'], data['email'])
    user = User.query.filter_by(name=data['name']).first()
    return user.id

# Get the user object associated with a particular user from the db
def getUserInfo(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

# Retrieve a user's id number based on their username
def getUserID(name):
    try:
        user = User.query.filter_by(name=name).first()
        return user.id
    except:
        return None

# Completely clear the login_session
def clearSession(login_session):
    del login_session['name']
    del login_session['user_id']
    del login_session['email']
    del login_session['picture']
    del login_session['provider']
    del login_session['state']
    del login_session['access_token']
    login_session.clear


#Login a traditional user
@auth.route('/login', methods=['GET', 'POST'])
def showLogin():
    if 'name' in login_session:
        flash('You are already logged in as {}. Logout First.'.format(
            login_session['name']))
        return redirect('/')
    form = LoginForm()
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.ascii_lowercase + string.digits)\
                    for x in xrange(32))
    login_session['state'] = state
    if form.validate_on_submit():
        user_login = LoginUser.get_by_username(form.username.data)
        if user_login is not None and\
        user_login.check_password(form.password.data):
            user = getUserInfo(user_login.user_id)
            login_session['name'] = user.name
            login_session['email'] = user.email
            login_session['picture'] = user.picture
            login_session['user_id'] = user.id
            login_session['provider'] = None
            login_session['access_token'] = None
            flash('Logged in successfully as {}'.format(user.name))
            return redirect('/')
    return render_template('login.html', STATE=state, form=form)

#Register a new user

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'name' in login_session:
        flash('You are already logged in as \'{}\'. Logout First.'.format(
            login_session['name']))
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        commitUser(form.name.data, form.picture.data, form.email.data)
        user_id = getUserID(form.name.data)
        if user_id is None:
            flash('There was a problem with registration. Please try again.')
            return redirect(url_for('auth.signup'))
        user_login = LoginUser(username=form.username.data,
                               password=form.password.data,
                               user_id=user_id)
        db.session.add(user_login)
        db.session.commit()

        flash('Welcome, {}! Please login'.format(form.username.data))
        return redirect(url_for('auth.showLogin'))
    return render_template('signup.html', form=form)


#########################################
# Facebook Pathways
########################################
@auth.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        return makeJSONResponse('Invalid state parameter.', 401)
    access_token = request.data
    print 'access-token established'
    print access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    # Get user picture
    pic_url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    pic_result = h.request(pic_url, 'GET')[1]
    pic_data = json.loads(pic_result)

    # Check for the user in the database
    user_id = getUserID(data['name'])
    # If the user does not exist, create the user, return their id
    if user_id == None:
        data['picture'] = pic_data['data']['url']
        createUser(data)
        user_id = getUserID(data['name'])

    # Get the user information from the db and set the login_session values
    user = getUserInfo(user_id)
    login_session['name'] = user.name
    login_session['picture'] = user.picture
    login_session['email'] = user.email
    login_session['user_id'] = user.id
    login_session['provider'] = 'facebook'

    # Properly store the token in the login_session for future logout
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Ouput a message to the user before redirecting back to the home page.
    return returnHTMLOutput(login_session)


#########################################
# Google Pathways
########################################

@auth.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        return makeJSONResponse('Invalid state parameter.', 401)
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return makeJSONResponse('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return makeJSONResponse(result.get('error'), 500)
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return makeJSONResponse("Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return makeJSONResponse("Token's client ID does not match app's.", 401)

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return makeJSONResponse('Current user is already connected.', 200)

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    user_id = getUserID(data['name'])

    if user_id == None:
        createUser(data)
        user_id = getUserID(data['name'])

    user = getUserInfo(user_id)
    login_session['name'] = user.name
    login_session['picture'] = user.picture
    login_session['email'] = user.email
    login_session['user_id'] = user.id
    login_session['provider'] = 'google'

    return returnHTMLOutput(login_session)


#######################
# Disconnect
######################

@auth.route('/disconnect')
def disconnect():
    if 'access_token' not in login_session:
        flash('You are not currently logged in. Log in to log out.')
        redirect(url_for('auth.showLogin'))
    access_token = login_session['access_token']
    if access_token is not None:
        # user is logged in through social media
        provider = login_session['provider']
        if access_token is None:
            return makeJSONResponse('Current User not connected.', 401)
        if provider == 'google':
            url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
            h = httplib2.Http()
            result = h.request(url, 'GET')[0]
            if result['status'] == '200':
                clearSession(login_session)
                flash('You have successfully disconnected.')
                return redirect('/')
            else:
                flash('There was a problem disconnecting. Please Try again.')
                return redirect('/')
        elif provider == 'facebook':
            url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % access_token
            h = httplib2.Http()
            result = h.request(url, 'DELETE')[1]
            clearSession(login_session)
            flash('You have successfully logged out.')
            return redirect('/')
    else:
        # User is a local login
        flash('Congratulations. You have escaped the system.')
        clearSession(login_session)
        return redirect('/')
