# Import the database object (db) from the main application module
# defined inside /main/__init__.py in the next sections.
from main import db

#The baseclass for all your models is called db.Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.id


    #Flask-login requires our User class to contain certain methods: is_authenticated, is_active, is_anonymous and get_id
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)