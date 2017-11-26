# Import flask dependencies
from flask import Blueprint, request, render_template
# Define the blueprint: 'auth', set its url prefix: main.url/auth
from flask_login import login_required, login_user
# Import the database object from the main main module
from flask_wtf import form

#from main import db
#from main.models import User
from main.recommender import recommend
from main.forms import ReviewForm
# Import module forms
from main.forms import SignupForm
# Import module models (i.e. User)
#from main.models import User
from main import app as main

# TODO Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

#Next, we used the route decorator (@main.route('/')) to specify the URL that #should trigger the execution of the index function.
@main.route('/')
def index():
    # index f. renders .html
    #form = ReviewForm(request.form)
    #return render_template('reviewform.html', form=form)
    form = SignupForm(request.form)
    return render_template('login.html', form=form)


# methods=['GET', 'POST'] tells Flask, that only GET and POST methods should be accepted
@main.route('/signup', methods=['GET', 'POST'])
def register():
    return "Signup"

@main.route('/signup', methods=['GET', 'POST'])
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

@main.route('/login', methods=['GET', 'POST'])
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


@main.route('/results', methods=['POST'])
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
@main.route('/thanks', methods=['POST'])
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
