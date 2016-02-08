from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, FileField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Regexp, Length, EqualTo, Email, ValidationError

from ..models import User


class LoginForm(Form):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    username = StringField('Username: ',
                           validators=[DataRequired(),
                                       Length(5, 45),
                                       Regexp('^[A-Z,a-z0-9_]{3,}$')])
    name = StringField('Full name: ', validators=[DataRequired(),
                                                  Length(4, 65)])
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    picture = URLField('URL for your photo: ', validators=[DataRequired(),
                                                           url()])
    password = PasswordField('Password: ', validators=[DataRequired(),
                                                       Length(7, 45),
                                                       EqualTo('confirmPassword')])
    confirmPassword = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError(
                'An account with this email has already been created.')

    def validate_user(self, name_field):
        if User.query.filter_by(name=name_field.data).first():
            raise ValidationError('This username is taken')
