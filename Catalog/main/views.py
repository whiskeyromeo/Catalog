from flask import render_template, session
from ..models import Category, Item
from . import main


#When rendering the index, grab the whole list of categories along with the 10 newest items

@main.route('/index')
@main.route('/')
def index():
    categories = Category.getCategories()
    return render_template('index.html', session=session, categories=categories, items=Item.newest(10))


# Error handling

@main.app_errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html', error=e), 500
