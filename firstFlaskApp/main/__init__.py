#This file initializes application and brings together all of the various components
# Import flask and template operators
from flask import Flask, render_template


#from main.models import User

app = Flask(__name__)
# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from main.controllers import main as main

#app.register_blueprint(main, url_prefix='/')

#initialize the LoginManager
from flask_login import LoginManager
from main.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


# Register blueprint(s)
#app.register_blueprint(main)
# main.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.init_app(app)
db.create_all()
