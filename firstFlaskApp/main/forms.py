# Holds our form definitions created by flask-wtf.
# Import Form and RecaptchaField (optional)
from flask_wtf import Form, validators

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField, SubmitField, IntegerField

# Import Form validators
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(Form):
    email = StringField('Email Address', [Email(),
                                          DataRequired(message='Forgot your email address?')])
    username = StringField('username',
                           validators=[DataRequired()])
    password = PasswordField('password', [ DataRequired(message='Must provide a password')])
    submit = SubmitField('SignIn')


class ReviewForm(Form):
    recommendForUserWithID = IntegerField('', [DataRequired()])