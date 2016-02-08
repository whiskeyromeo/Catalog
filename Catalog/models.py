from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy import desc

from Catalog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), nullable=False, unique=True)
    picture = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'picture': self.picture,
            'email': self.email,
            'items': self.serialize_items
        }

    @property
    def serialize_items(self):
        return [item.serialize for item in self.items]

    @staticmethod
    def __repr__(self):
        return '<User %r>' % self.name


class LoginUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: is a write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return LoginUser.query.filter_by(username=username).first()

    def __repr__(self):
        return '<LoginUser %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(65), nullable=False, unique=True)
    items = db.relationship('Item', backref="category", lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'items': self.serialize_items}

    @property
    def serialize_items(self):
        return [item.serialize for item in self.items]

    @staticmethod
    def getCategories():
        return Category.query.all()

    def __repr__(self):
        return '<Category %r>' % self.title


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=False)
    photo_path = db.Column(db.String(125))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    db.relationship('User')
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    db.relationship('Category')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'photo_path': self.photo_path,
            'user_id': self.user_id,
            'category_id': self.category_id
        }

    @staticmethod
    def newest(num):
        return Item.query.order_by(desc(Item.date)).limit(num)

    def __repr__(self):
        return '<Item %r>' % self.name
