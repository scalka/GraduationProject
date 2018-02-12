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
from app.recommender_comp.contentbased_recommender import contentbased_tfidf_recommend
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
    #s = select(* from 'user').where('user.id' == user_id)
    n = conn.execute('select username from user where user.id == ' + user_id)

    rr = conn.execute('select recipe_id, rating from ratings where user_id == ' + user_id)

    """The result of the query is being represented as a Python list of Python tuples [('Philip',)]
        The tuples contained in the list represent the rows returned by your query.
        Each value contained in a tuple represents the corresponding field, of that specific row, in the order you selected it"""
    # get user name
    name_tuple = n.fetchall()
    name = name_tuple[0][0]
    # get recently rated recipes to use in content based recommender
    rated_recipes = rr.fetchall()
    print(len(rated_recipes))
    i = len(rated_recipes)
    print('i ' + str(i))
    # reversed loop from highest to lowest
    for i in reversed(range(i)):
        print('this is i ' + str(i))
        if (rated_recipes[i][1] >= 4.0):
            rq = conn.execute('select title from recipe where recipe.id == ' + str(rated_recipes[i][0]))
            rec = rq.fetchone()
            print(rec[0])
            recommender_tfidf_recipes = contentbased_tfidf_recommend(rec[0])
            break

    conn.close()
    #matrix factorization recommendation
    recommendation = mf_recommend(int(user_id)).head(10)
    #popularity recommendation
    popular_recipe = pop_recommend().head(10)
    #print(popular_recipe[['title']])

    #get categories
    categories = find_categories()
    return render_template('recom/results.html',
                           userId=user_id,
                           name=name,
                           popular_recipes=popular_recipe,
                           recommendations=recommendation,
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
