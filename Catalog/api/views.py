from . import api
from ..models import Category, User, Item
from flask import jsonify, redirect, flash, json, render_template


@api.route('/catalog.json')
@api.route('/catalog.JSON')
def showJSONCatalog():
    categories = Category.getCategories()
    return jsonify(Categories=[i.serialize for i in categories])


@api.route('/catalog.xml')
@api.route('/catalog.XML')
def showXMLCatalog():
    categories = Category.getCategories()
    return render_template('catalog.xml', categories=categories)


@api.route('/category/<category_title>.json')
@api.route('/category/<category_title>.JSON')
def showJSONCategory(category_title):
    category = Category.query.filter(Category.title.ilike(category_title))\
        .first_or_404()
    return jsonify(category_title=category.serialize)


@api.route('/users.json')
@api.route('/users.JSON')
def showJSONUsers():
    users = User.query.all()
    return jsonify(Users=[i.serialize for i in users])


@api.route('/user<user_id>.json')
@api.route('/user<user_id>.JSON')
def showJSONUser(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(User=user.serialize)


@api.route('/item/<item_name>.json')
@api.route('/item/<item_name>.JSON')
def showJSONItem(item_name):
    item = Item.query.filter(Item.name.ilike(item_name))\
        .first_or_404()
    return jsonify(Item=item.serialize)
