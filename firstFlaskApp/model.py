#Holds our database model(s) created by flask-sqlalchemy.
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(80), primary_key=True, unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.email
    #Flask-login requires our User class to contain certain methods: is_authenticated, is_active, is_anonymous and get_id
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)