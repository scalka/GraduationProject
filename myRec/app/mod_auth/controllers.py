# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, SignupForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('recommender_mod.index'))
            else:
                print("login unsuccessful")
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('auth/login.html', form=form)

@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    print("1")
    form = SignupForm()
    if request.method == 'GET':
        print("2")
        return render_template('auth/register.html', form = form)
    if request.method == 'POST':
        print("3")
        if form.validate_on_submit():
            print("4")
            if User.query.filter_by(email=form.email.data).first():
                print("5")
                return "Email address already exists"
            else:
                print("6")
                newuser = User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                print(newuser)
                return redirect(url_for('recommender_mod.index'))
        else:
            print("7")
            return "Form didn't validate"

@mod_auth.route('/protected')
@login_required
def protected():
    return "protected area"

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