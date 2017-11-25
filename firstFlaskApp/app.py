#Contains the application together with routes and login facilities created by flask-login.
from model import db, User
from flask import Flask, render_template, request, redirect, url_for
from wtforms import TextAreaField, validators, IntegerField, form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import Form
from forms import SignupForm
from flask_login import LoginManager, login_user, login_required, logout_user
import pickle
import pandas as pd
import sqlite3
import os
import numpy as np

#We ran our application as a single module; thus we initialized a new Flask instance with the argument __name__ to let Flask know that it can find the #HTML template folder (templates) in the same directory where it is located.
app = Flask(__name__)
#login
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/database.sqlite'

#initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

#Preparing the recommender
cur_dir = os.path.dirname(__file__)
U = pickle.load(open(os.path.join(cur_dir,
                                            'pkl_objects',
                                            'user_features_recipes.dat'), 'rb'))
R = pickle.load(open(os.path.join(cur_dir,
                                            'pkl_objects',
                                            'product_features_recipes.dat'), 'rb'))
predicted_ratings = pickle.load(open(os.path.join(cur_dir,
                                            'pkl_objects',
                                            'predicted_ratings_recipes.dat'), 'rb'))
#db = os.path.join(cur_dir, 'recipes_db.db')

def recommend(user_id):
    # TODO get it from db
    recipes_df = pd.read_csv('datasets/recipes.csv', index_col='recipes_id')
    user_ratings = predicted_ratings[user_id - 1]
    recipes_df['rating'] = user_ratings
    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)

    return recipes_df

#####Flask
class SignupForm(Form):
    username = StringField('username',
                           validators=[DataRequired()])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired()])
    submit = SubmitField("Sign In")

class ReviewForm(Form):
    recommendForUserWithID = IntegerField('', [validators.DataRequired()])


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()


@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


#Next, we used the route decorator (@app.route('/')) to specify the URL that #should trigger the execution of the index function.
@app.route('/')
def index():
    # index f. renders .html
    #form = ReviewForm(request.form)
    #return render_template('reviewform.html', form=form)
    form = SignupForm(request.form)
    return render_template('signup.html', form=form)


# methods=['GET', 'POST'] tells Flask, that only GET and POST methods should be accepted
@app.route('/signup', methods=['GET', 'POST'])
def register():
    return "Signup"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupForm = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', signupForm = form)
    elif request.method == 'POST':
        if signupForm.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                # login when user signs up
                login_user(newuser)

                return "User created!!!"
    else:
            return "signupForm didn't validate"

@app.route('/login', methods=['GET','POST'])
def login():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return "User logged in"
                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
        else:
            return "form not validated"


@app.route('/results', methods=['POST'])
@login_required
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = int(request.form['recommendForUserWithID'])
        recommendation = recommend(user_id).head(5)

        print(recommendation[['title']])

        return render_template('results.html',
                               userId=user_id,
                               recommendations = recommendation,
                               title = recommendation[['title']],
                               category = recommendation[['category']],
                               rating=recommendation[['rating']],
                               )
    return render_template('reviewform.html', form=form)


"""
@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']
    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
    y = int(not(y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('thanks.html')
"""

if __name__ == '__main__':
    #run app on the server this script is directly executed by the Python interpreter, which we ensured using the if statement with __name__ == '__main__'.
    app.init_db()
    app.run(port=5000, host='localhost', debug=True)