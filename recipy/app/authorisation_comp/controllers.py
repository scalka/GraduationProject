"""
Authorisation controllers
"""

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, redirect, url_for

# Import password / encryption helper tools
from flask_login import login_user, current_user, login_required, logout_user

# Import the database object from the main app module
from app import db

# Import module forms
from app.authorisation_comp.forms import LoginForm, SignupForm

# Import module models (i.e. User)
from app.authorisation_comp.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route(',')
@mod_auth.route('/login', methods=['GET', 'POST'])
# Set the route and accepted methods
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first_or_404()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                print("login successful")
                return redirect(url_for('recommender_comp.index'))
            else:
              return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = User(form.email.data, form.username.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                print(newuser)
                return redirect(url_for('recommender_comp.index'))
        else:
            return "Form didn't validate"


@mod_auth.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('auth.login'))
