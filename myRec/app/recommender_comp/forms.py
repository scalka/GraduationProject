# Import Form and RecaptchaField (optional)


# Import Form elements such as TextField and BooleanField (optional)
from flask_wtf import Form, validators
from wtforms import TextField, PasswordField, StringField, SubmitField, IntegerField  # BooleanField

# Import Form validators

from wtforms.validators import Required, Email, EqualTo, DataRequired, number_range


class ReviewForm(Form):

    #min – The minimum required value of the number. If not provided, minimum value will not be checked.
    #max – The maximum value of the number. If not provided, maximum value will not be checked.
    #message – Error message to raise in case of a validation error. Can be interpolated using %(min)s and %(max)s if desired. Useful defaults are provided depending on the existence of min and max.

    userId = IntegerField('user id', validators=[DataRequired()])
    recipeId = IntegerField('recipe id', validators=[DataRequired()])
    rating = IntegerField('rating', validators=[number_range(min=1, max=5, message='unacceptable.')])