#Holds our form definitions created by flask-wtf.

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField

class SignupForm(Form):
    email = StringField('email')
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('SignIn')