# Import flask dependencies
import pickle
import pandas as pd
import os
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from flask_login import login_required

# Import module forms
from app.recommender_mod.forms import ReviewForm

# Import module models (i.e. User)
#from app.recommender_mod.recommender import recommend

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

def recommend(user_id):
    # TODO get it from db
    recipes_df = pd.read_csv(
        'C:\\Users\\calka\\Documents\\Y4\\Recommender\\myRec\\app\\recommender_mod\\datasets\\recipes.csv',
        index_col='recipes_id')
    user_ratings = predicted_ratings[user_id - 1]
    recipes_df['rating'] = user_ratings
    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)

    return recipes_df


# Define the blueprint: 'auth', set its url prefix: app.url/auth
recommender_mod = Blueprint('recommender_mod', __name__, url_prefix='/recom')

@recommender_mod.route('/reviewform')
#@login_required
def index():
    # index f. renders .html
    form = ReviewForm(request.form)
    return render_template('recom/reviewform.html', form=form)

@recommender_mod.route('/results', methods=['POST'])
#@login_required
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST':
        user_id = int(request.form['recommendForUserWithID'])
        recommendation = recommend(user_id).head(5)

        print(recommendation[['title']])

        return render_template('recom/results.html',
                               userId=user_id,
                               recommendations = recommendation,
                               title = recommendation[['title']],
                               category = recommendation[['category']],
                               rating=recommendation[['rating']],
                               )
    return render_template('recom/reviewform.html', form=form)


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