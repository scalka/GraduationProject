# Import Form and RecaptchaField (optional)


# Import Form elements such as TextField and BooleanField (optional)
from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, SubmitField  # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, DataRequired


# Define the login form (WTForms)

class LoginForm(Form):
    email    = StringField('Email Address', [Email(),
                DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a password. ;-)')])

class SignupForm(Form):
    email = StringField('email',
                validators=[DataRequired(),Email()])
    password = PasswordField(
                'password',
                validators=[DataRequired()])
    submit = SubmitField("Sign In")