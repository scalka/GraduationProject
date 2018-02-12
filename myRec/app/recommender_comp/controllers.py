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

from app import User, engine, app
from app.pagination.Pagination import Pagination
from app.recommender_comp.categories import find_categories, display_recipes_from_category
from app.recommender_comp.contentbased_recommender import contentbased_tfidf_recommend, metadata_recommend, get_last_rated_recipe
from app.recommender_comp.forms import ReviewForm

# Import module models (i.e. User)
#from app.recommender_comp.recommender import recommend
from app.recommender_comp.mf_recommender import mf_recommend

# Define the blueprint: 'auth', set its url prefix: app.url/auth
from app.recommender_comp.pop_recommender import pop_recommend
from datetime import timedelta

recommender_mod = Blueprint('recommender_comp', __name__, url_prefix='/recom')

@recommender_mod.route('/reviewform')
@login_required
def index():
    user_id = current_user.get_id()
    #Get user name
    conn = engine.connect()
    n = conn.execute('select username from user where user.id == ' + user_id) # get user name
    rr = conn.execute('select recipe_id, rating from ratings where user_id == ' + user_id) # rated_recipes by a user
    """The result of the query is being represented as a Python list of Python tuples [('Philip',)]
        The tuples contained in the list represent the rows returned by your query.
        Each value contained in a tuple represents the corresponding field, of that specific row, in the order you selected it"""
    name_tuple = n.fetchall() # get user name
    name = name_tuple[0][0]
    # get recently rated recipes to use in content based recommender
    rated_recipes = rr.fetchall()
    conn.close()

    last_rated_title5 = get_last_rated_recipe(rated_recipes, 5.0)
    last_rated_title4 = get_last_rated_recipe(rated_recipes, 4.0)

    # Content based algorithms
    # Term Frequency-Inverse Document Frequency (TF-IDF) in ingredients for recipe rated at 5.0
    recommender_tfidf_recipes = contentbased_tfidf_recommend(last_rated_title5)
    # Metadata terms based on category, ingredients and description for recipe rated at 4.0
    metadata_recommend_recipes = metadata_recommend(last_rated_title4)

    # Matrix factorization recommendation
    recommendation = mf_recommend(int(user_id)).head(10)

    # Popularity recommendation
    popular_recipe = pop_recommend().head(10)

    # Get all categories from db
    categories = find_categories()

    return render_template('recom/results.html',
                           userId=user_id,
                           name=name,
                           popular_recipes=popular_recipe,
                           recommendations=recommendation,
                           last_rated_title=last_rated_title5,
                           last_rated_title2 = last_rated_title4,
                           metadata_recommend_recipes = metadata_recommend_recipes,
                           recommender_tfidf_recipes=recommender_tfidf_recipes,
                           categories=categories
                           )


@recommender_mod.route('/<recipe_id>', methods=['POST', 'GET'])
@login_required
# Detail page
def recipe_details(recipe_id):
    conn = engine.connect()
    # s = select(* from 'user').where('user.id' == user_id)
    r = conn.execute('select * from recipe where recipe.id == ' + recipe_id)
    r_tuple = r.fetchall()
    ratings_num = conn.execute('select count(rating) from ratings where recipe_id == ' + recipe_id)
    ratings_num_tuple = ratings_num.fetchall()

    prep_time = str(timedelta(minutes=r_tuple[0][7]))[:-3]
    total_time = str(timedelta(minutes=r_tuple[0][8]))[:-3]

    if request.method == 'POST':
        rating = request.form.get('test_name')
        userId = current_user.get_id()
        recipeId = recipe_id
        ratings_num = conn.execute('select count(rating) from ratings where recipe_id == ' + recipe_id)
        ratings_num_tuple = ratings_num.fetchall()
        #q = conn.execute('select * from ratings where ratings.recipe_id == ' + recipeId + ' and ratings.user_id == ' + userId)
        #check = q.fetchall()

        #if :
        #    print("update")
       # else:
           # print("insert")
        conn.execute('insert into ratings (user_id, recipe_id, rating) values (? , ? , ? )', (userId, recipeId, rating, ))

    conn.close()
    return render_template('recipe_detail.html',
                           recipe_details = r_tuple,
                           ratings_num = ratings_num_tuple[0][0],
                           prep_time = prep_time,
                           total_time = total_time
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



@recommender_mod.route('/category/<category>/', defaults={'page': 1})
@recommender_mod.route('/category/<category>/<int:page>')
@login_required
def display_category(category, page):
    #PER_PAGE = 5
    #count = len(recipes_cat)
    recipes_cat = display_recipes_from_category(category)
    #pagination = Pagination(page, PER_PAGE, count)
    return render_template('category_page.html',
                           recipes = recipes_cat,
                           cat=category,
                           #pagination=pagination
                            )
