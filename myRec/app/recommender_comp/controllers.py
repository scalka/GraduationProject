# Import flask dependencies
import pickle
import pandas as pd
import os
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from flask_login import login_required, current_user

# Import module forms
from sqlalchemy import literal_column, select

from app import User, engine
from app.recommender_comp.categories import find_categories
from app.recommender_comp.forms import ReviewForm

# Import module models (i.e. User)
#from app.recommender_comp.recommender import recommend
from app.recommender_comp.mf_recommender import mf_recommend

# Define the blueprint: 'auth', set its url prefix: app.url/auth
from app.recommender_comp.pop_recommender import pop_recommend

recommender_mod = Blueprint('recommender_comp', __name__, url_prefix='/recom')

@recommender_mod.route('/reviewform')
@login_required
def index():
    user_id = current_user.get_id()
    #Get user name
    conn = engine.connect()
    #s = select(* from 'user').where('user.id' == user_id)
    n = conn.execute('select username from user where user.id == ' + user_id)
    """The result of the query is being represented as a Python list of Python tuples [('Philip',)]
        The tuples contained in the list represent the rows returned by your query.
        Each value contained in a tuple represents the corresponding field, of that specific row, in the order you selected it"""
    name_tuple = n.fetchall()
    name = name_tuple[0][0]

    conn.close()
    #matrix factorization recommendation
    recommendation = mf_recommend(int(user_id)).head(5)
    #popularity recommendation
    popular_recipe = pop_recommend().head(5)
    print(popular_recipe[['title']])

    #get categories
    categories = find_categories()
    print(categories)
    return render_template('recom/results.html',
                           userId=user_id,
                           name=name,
                           popular_recipes=popular_recipe,
                           recommendations=recommendation,
                           id=recommendation[['id']],
                           title=recommendation[['title']],
                           category=recommendation[['category']],
                           photo_url=recommendation[['photo_url']],
                           rating=recommendation[['rating']],
                           categories=categories
                           )

# @recommender_comp.route('/results', methods=['POST'])
# @login_required
# def results():
#     form = ReviewForm(request.form)
#     if request.method == 'POST':
#         user_id = current_user.get_id()
#         recommendation = recommend(int(user_id)).head(10)
#         print(recommendation)
#         return render_template('recom/results.html',
#                                userId=user_id,
#                                recommendations=recommendation,
#                                id=recommendation[['id']],
#                                title=recommendation[['title']],
#                                category=recommendation[['category']],
#                                photo_utl=[['photo_utl']],
#                                rating=recommendation[['rating']],
#                                )

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