# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
# Import SQLAlchemy

# Define the WSGI application object
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import Cache
from flask import Flask
from flask.ext.cache import Cache
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
# Configurations
app.config.from_object('config')
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# Create engine: engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.signin"

from app.authorisation_comp.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


@login_manager.unauthorized_handler
def unauthorized():
    # when unauthorised
    return redirect(url_for('views.index'))


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (auth_comp)
from app.controllers import views
from app.authorisation_comp.controllers import mod_auth as auth_module
from app.recommender_comp.controllers import recommender_mod as rcmdr

# Register blueprint(s)
app.register_blueprint(views)
app.register_blueprint(auth_module)
app.register_blueprint(rcmdr)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
