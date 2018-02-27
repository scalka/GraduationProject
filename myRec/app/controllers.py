"""
Route to index page
"""
from flask import Flask, render_template, app, Blueprint
from flask_login import current_user

views = Blueprint('views', __name__, url_prefix='')

@views.route('/')
def index():
    return render_template(
        'index.html'
    )
