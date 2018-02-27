# Import flask dependencies
import pandas as pd
from flask import Blueprint, request, render_template, \
                  redirect, url_for
# Import the database object from the main app module
from flask_login import login_required, current_user
from app import engine
from app.recommender_comp.categories import find_categories, display_recipes_from_category
from app.recommender_comp.contentbased_recommender import contentbased_tfidf_recommend, metadata_recommend, \
  get_last_rated_recipe, get_last_bookmarked
# Import module models (i.e. User)
from app.recommender_comp.mf_recommender import mf_recommend
# Define the blueprint: 'auth', set its url prefix: app.url/auth
import app.recommender_comp.pop_recommender
import datetime

recommender_mod = Blueprint('recommender_comp', __name__, url_prefix='/recom')


@recommender_mod.route('/')
@login_required
def index():
    user_id = current_user.get_id()
    assert isinstance(engine, object)
    conn = engine.connect()
    n = conn.execute("select username from user where user.id == " + user_id)  # get user name
    rr = conn.execute("select recipe_id, rating from ratings where user_id == " + user_id)  # rated_recipes by a user
    bm = conn.execute("SELECT * from recipe where recipe.id in ( SELECT recipe_id from bookmarks where user_id == ? )",
                      (user_id,))  # bookmarked recipes by a user

    """ The result of the query is being represented as a Python list of Python tuples [('Philip',)]
    The tuples contained in the list represent the rows returned by your query.
    Each value contained in a tuple represents the corresponding field, 
    of that specific row, in the order you selected it"""
    name_tuple = n.fetchall()  # get user name
    name = name_tuple[0][0]
    # get recently rated recipes to use in content based recommender
    rated_recipes = rr.fetchall()
    bookmarked_recipes = bm.fetchall()
    conn.close()

    last_rated_title = get_last_rated_recipe(rated_recipes, 4.0)
    last_bookmarked = get_last_bookmarked(bookmarked_recipes)

    # Content based algorithms
    no_rated_msg = True
    recommender_tfidf_recipes = pd.DataFrame()
    if last_rated_title != 0:
        # Term Frequency-Inverse Document Frequency (TF-IDF) in ingredients for recipe rated at 5.0
        recommender_tfidf_recipes = contentbased_tfidf_recommend(last_rated_title)
        no_rated_msg = False

    # Metadata terms based on category, ingredients and description for recipe rated at 4.0
    no_bookmarked_msg = True
    metadata_recommend_recipes = pd.DataFrame()
    if last_bookmarked != 0:
        metadata_recommend_recipes = metadata_recommend(last_bookmarked)
        no_bookmarked_msg = False

    recommendation = pd.DataFrame()
    no_mf_msg = True

    if int(user_id) <= 942:
        no_mf_msg = False
        # Matrix factorization recommendation
        recommendation = mf_recommend(int(user_id)).head(10)

    # Popularity recommendation
    popular_recipe = app.recommender_comp.pop_recommender.pop_recommend().head(10)

    # Get all categories from db
    categories = find_categories()

    return render_template('recom/results.html',
                           userId=user_id,
                           name=name,
                           popular_recipes=popular_recipe,
                           recommendations=recommendation,
                           last_bookmarked=last_bookmarked,
                           last_rated_title=last_rated_title,
                           metadata_recommend_recipes=metadata_recommend_recipes,
                           recommender_tfidf_recipes=recommender_tfidf_recipes,
                           categories=categories,
                           no_mf_msg=no_mf_msg,
                           no_rated_msg=no_rated_msg,
                           no_bookmarked_msg=no_bookmarked_msg
                           )


@recommender_mod.route('/cookbook')
@login_required
def cookbook():
    user_id = current_user.get_id()
    conn = engine.connect()

    rr = conn.execute('SELECT * from recipe where recipe.id in ( select recipe_id from ratings where user_id == ? )',
                      (user_id,))
    bm = conn.execute('SELECT * from recipe where recipe.id in ( SELECT recipe_id from bookmarks where user_id == ? )',
                      (user_id,))

    # get recently rated recipes to use in content based recommender
    rated_recipes = rr.fetchall()
    bookmarked = bm.fetchall()
    conn.close()

    # Rated recipes
    no_rated_msg = True
    rated_recipes_df = pd.DataFrame()
    if len(rated_recipes) > 0:
        no_rated_msg = False
        rated_recipes_df = pd.DataFrame(rated_recipes)
        rated_recipes_df.columns = rr.keys()
    # Bookmarked recipes
    bookmarked_df = pd.DataFrame()
    no_bookmarks_msg = True
    if len(bookmarked) > 0:
        no_bookmarks_msg = False
        bookmarked_df = pd.DataFrame(bookmarked)
        bookmarked_df.columns = bm.keys()

    return render_template('recom/cookbook.html',
                           rated_recipes=rated_recipes_df,
                           bookmarked_recipes=bookmarked_df,
                           no_bookmarks_msg=no_bookmarks_msg,
                           no_rated_msg=no_rated_msg
                           )


@recommender_mod.route('/<recipe_id>', methods=['POST', 'GET'])
@login_required
# Detail page
def recipe_details(recipe_id):
    user_id = current_user.get_id()
    conn = engine.connect()
    # s = select(* from 'user').where('user.id' == user_id)
    r = conn.execute('select * from recipe where recipe.id == ' + recipe_id)
    r_tuple = r.fetchall()
    ratings_num = conn.execute('select count(rating) from ratings where recipe_id == ' + recipe_id)
    ratings_num_tuple = ratings_num.fetchall()

    b = conn.execute('SELECT recipe_id from bookmarks where user_id == ' + user_id + ' and recipe_id == ' + recipe_id)
    bookmarked = b.fetchall()

    if len(bookmarked) < 1:
        show_bookmark = False
    else:
        show_bookmark = True

    prep_time = str(datetime.timedelta(minutes=r_tuple[0][7]))[:-3]
    total_time = str(datetime.timedelta(minutes=r_tuple[0][8]))[:-3]

    if request.method == 'POST':
        rating = request.form.get('rating_name')
        user_id = current_user.get_id()
        recipe_id = recipe_id
        ratings_num = conn.execute('select count(rating) from ratings where recipe_id == ' + recipe_id)
        ratings_num_tuple = ratings_num.fetchall()
        q = conn.execute('select * from ratings where ratings.recipe_id == ' + recipe_id + ' and ratings.user_id == ' + user_id)
        check = q.fetchall()
        if len(check) < 1:
            conn.execute('insert into ratings (user_id, recipe_id, rating) values (? , ? , ? )',
                        (user_id, recipe_id, rating,))
        else:
            conn.execute('update ratings set rating == ' + rating +' where ratings.recipe_id == ' + recipe_id + ' and ratings.user_id == ' + user_id)

        # conn.execute('insert into ratings (user_id, recipe_id, rating) values (? , ? , ? )', (user_id, recipe_id, rating, ))

    conn.close()
    return render_template('recipe_detail.html',
                           recipe_details=r_tuple,
                           ratings_num=ratings_num_tuple[0][0],
                           prep_time=prep_time,
                           total_time=total_time,
                           show_bookmark=show_bookmark
                           )


@recommender_mod.route('/<recipe_id>/m', methods=['POST', 'GET'])
@login_required
def bookmark(recipe_id):
    conn = engine.connect()

    user_id = current_user.get_id()
    recipe_id = recipe_id
    date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    c = conn.execute('select * from bookmarks where user_id == ' + user_id + ' and recipe_id == ' + recipe_id)
    cursor = c.fetchall()
    # if not bookmarked - do it, else delete bookmark
    if len(cursor) < 1:
        conn.execute('insert into bookmarks (user_id, recipe_id, date) values (? , ? , ? )',
                     (user_id, recipe_id, date, ))
    else:
        conn.execute('delete from bookmarks where user_id == ' + user_id + ' and recipe_id == ' + recipe_id)
    conn.close()
    return redirect(url_for('recommender_comp.recipe_details', recipe_id=recipe_id))
