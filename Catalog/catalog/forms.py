from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, TextAreaField, SelectField,\
SubmitField
from wtforms.validators import DataRequired, url, Regexp, Length,\
EqualTo, Email, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Category


def possible_cat():
    return Category.query

ALLOWED_EXTENSIONS = ['png', 'tff', 'jpg', 'jpeg', 'JPG', 'JPEG', 'PNG']


class ItemForm(Form):
    name = StringField('Title: ',
                       validators=[DataRequired(),
                                   Length(2, 65)])
    description = TextAreaField('Description: ',
                                validators=[DataRequired(),
                                            Length(4, 255)])
    category = QuerySelectField(query_factory=possible_cat, get_label='title')
    picture = FileField('Your Picture: ',
                        validators=[FileAllowed(ALLOWED_EXTENSIONS,
                                                message="File not supported.")])
    submit = SubmitField()
