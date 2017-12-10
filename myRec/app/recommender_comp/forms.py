# Import Form and RecaptchaField (optional)


# Import Form elements such as TextField and BooleanField (optional)
from flask_wtf import Form, validators
from wtforms import TextField, PasswordField, StringField, SubmitField, IntegerField  # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, DataRequired


# Define the login form (WTForms)

class ReviewForm(Form):
    recommendForUserWithID = IntegerField('', [DataRequired()])