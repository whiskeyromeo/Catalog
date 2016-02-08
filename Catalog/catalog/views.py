from flask import Flask, render_template, url_for, redirect, request,\
session, flash, json, abort
from werkzeug import secure_filename
from ..models import Category, Item
import forms
import os

from . import catalog
from .. import db

#Image files uploaded to the following path
file_path = 'Catalog/static/uploads/'

#Commit an item to the database
def commitItem(name, description, category_id, user_id, photo_path=None):
    newItem = Item(name=name,
                   description=description,
                   category_id=category_id,
                   user_id=user_id,
                   photo_path=photo_path)
    db.session.add(newItem)
    db.session.commit()

#grab an item
def getItemByID(item_id):
    return Item.query.filter_by(id=item_id).first()


#Show all of the Items in the category
@catalog.route('/<category_name>')
def showCategory(category_name):
    categories = Category.getCategories()
    category = Category.query.filter_by(title=category_name).first()
    category_items = Item.query.filter_by(category_id=category.id).all()
    return render_template('showContents.html', items=category_items,\
                           categories=categories, title=category_name)

#Add a new item
@catalog.route('/new', methods=['GET', 'POST'])
def newItem():
    if session['name']:
        form = forms.ItemForm()
        if form.validate_on_submit():
            photo_path = None
            if form.picture.data:
                file = request.files['picture']
                filename = secure_filename(file.filename)
                file.save(os.path.join(file_path, filename))
                photo_path = filename
            name = form.name.data
            description = form.description.data
            user_id = session['user_id']
            category_id = form.category.data.id
            commitItem(name, description, category_id, user_id, photo_path)
            flash('\'{}\' successfully added'.format(name))
            return redirect('/')
        return render_template('addItem.html', form=form, title="Add an Item: ")
    else:
        flash('Please log in to add items.')
        return redirect(url_for('auth.showLogin'))

#Show a given item
@catalog.route('/<category_name>/<item_name>')
def showItem(category_name, item_name):
    item = Item.query.filter_by(name=item_name).first()
    return render_template('showItem.html', item=item)

#Edit an item
@catalog.route('/<category_id>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_name):
    if 'name' not in session:
        flash('You must be logged in to edit items')
        return redirect(url_for('auth.showLogin'))
    item = Item.query.filter_by(name=item_name).first_or_404()
    if item.user_id != session['user_id']:
        abort(403)
    form = forms.ItemForm(obj=item)
    print item
    if form.validate_on_submit():
        #if a picture was submitted, add it to the uploads if it doesnt exist.
        if form.picture.data:
            file = request.files['picture']
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_path, filename))
            item.photo_path = filename
        form.populate_obj(item)
        db.session.commit()
        flash("Stored '{}'".format(item.name))
        return redirect('/')
    return render_template('addItem.html', form=form, title="Edit Item: ")

# Delete an item
@catalog.route('/<int:category_id>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_name):
    # redirect if not logged in
    if 'name' not in session:
        flash('You must be logged in to delete items')
        return redirect(url_for('auth.showLogin'))
    item = Item.query.filter_by(name=item_name).first_or_404()
    # abort, unauthorized if user_id's not equivalent
    if item.user_id != session['user_id']:
        abort(403)
    if request.method == 'POST':
        # if photo_path exists, get the number of accounts dependent on the
        # photo
        if item.photo_path != None:
            dependents = Item.query.filter_by(
                photo_path=item.photo_path).count()
            # if there is only one dependent, remove the photo from the uploads
            # folder
            if dependents == 1:
                os.remove(os.path.join(file_path, item.photo_path))
        db.session.delete(item)
        db.session.commit()
        flash("Deleted '{}'".format(item.name))
        return redirect('/')
    return render_template('deleteItem.html', item=item)
