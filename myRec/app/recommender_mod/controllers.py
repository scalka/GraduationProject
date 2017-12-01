# Import flask dependencies
import pickle
import pandas as pd
import os
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from flask_login import login_required, current_user

# Import module forms
from app import User
from app.recommender_mod.forms import ReviewForm

# Import module models (i.e. User)
#from app.recommender_mod.recommender import recommend
from app.recommender_mod.recommender import recommend

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




# Define the blueprint: 'auth', set its url prefix: app.url/auth
recommender_mod = Blueprint('recommender_mod', __name__, url_prefix='/recom')

@recommender_mod.route('/reviewform')
@login_required
def index():
    # index f. renders .html
    form = ReviewForm(request.form)
    return render_template('recom/reviewform.html', form=form)

@recommender_mod.route('/results', methods=['POST'])
@login_required
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST':
        user_id = current_user.get_id()
        recommendation = recommend(int(user_id)).head(10)
        print(recommendation)
        return render_template('recom/results.html',
                               userId=user_id,
                               recommendations=recommendation,
                               title=recommendation[['title']],
                               category=recommendation[['category']],
                               rating=recommendation[['rating']],
                               )



"""
@recom.route('/thanks', methods=['POST'])
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