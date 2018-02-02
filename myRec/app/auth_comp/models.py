# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from sqlalchemy import Table, Column, Integer, ForeignKey, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship

from app import db

Base = declarative_base()

#http://flask-appbuilder.readthedocs.io/en/latest/relations.html
#http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html#association-object

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    recipe_id = db.Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship("Recipe")
    rating = db.Column(REAL)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_plaintext = db.Column(db.String, nullable=False)  # TEMPORARY - TO BE DELETED IN FAVOR OF HASHED PASSWORD
    authenticated = db.Column(db.Boolean, default=False)

    #https://pythontips.com/2013/08/07/the-self-variable-in-python-explained/
    def __init__(self, email, username, password_plaintext):
        self.email = email
        self.username = username
        self.password_plaintext = password_plaintext
        self.authenticated = False

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return self.password_plaintext == plaintext_password

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    cook_time = db.Column(Integer)
    ingredients = db.Column(db.String)
    instructions = db.Column(db.String)
    photo_url =  db.Column(db.String)
    prep_time_minutes = db.Column(Integer)
    total_time_minutes = db.Column(Integer)
    rating_stars = db.Column(REAL)
    review_count = db.Column(Integer)
    calories = db.Column(Integer)
    url = db.Column(db.String)

    def __init__(self, title, cook_time, ingredients, instructions, photo_url, url, prep_time_minutes,
                 total_time_minutes, rating_stars, review_count, category, calories):

        self.title - title
        self.category = category
        self.cook_time = cook_time
        self.ingredients = ingredients
        self.instructions = instructions
        self.photo_url = photo_url
        self.prep_time_minutes = prep_time_minutes
        self.total_time_minutes = total_time_minutes
        self.rating_stars = rating_stars
        self.review_count = review_count
        self.calories = calories
        self.url = url

