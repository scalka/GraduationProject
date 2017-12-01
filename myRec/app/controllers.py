
from flask import Flask, render_template, app, Blueprint

views = Blueprint('views', __name__, url_prefix='')

@views.route('/')
def index():
    print("print")
    return render_template(
        'index.html'
    )