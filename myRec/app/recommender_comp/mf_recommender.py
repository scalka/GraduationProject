"""
Matrix Factorisation recommender
"""
# Preparing the recommender
import os
import pickle
import pandas as pd
from app import engine


cur_dir = os.path.dirname(__file__)
U = pickle.load(open(os.path.join(cur_dir,
                                  'pkl_objects',
                                  'user_features_recipes2.dat'), 'rb'))
R = pickle.load(open(os.path.join(cur_dir,
                                  'pkl_objects',
                                  'product_features_recipes2.dat'), 'rb'))
predicted_ratings = pickle.load(open(os.path.join(cur_dir,
                                    'pkl_objects',
                                    'predicted_ratings_recipes2.dat'), 'rb'))


def mf_recommend(user_id):
    #http://shichaoji.com/2016/10/10/database-python-connection-basic/
    # Open engine connection
    con = engine.connect()
    # Perform query: rs to get recipe data from database
    recipe_query = con.execute('select * from recipe')
    # ratings_query = con.execute('select * from ratings')
    # Save results of the query to list: ll
    recipes = recipe_query.fetchall()
    #ratings = ratings_query.fetchall()
    # Close connection
    con.close()
    # create data frame from recipes from datbase
    recipes_df = pd.DataFrame(recipes)
    # ratings_df = pd.DataFrame(ratings)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.

    recipes_df.columns = recipe_query.keys()
    # recipes_df = recipes_df.rename(columns={'id': 'recipe_id'})
    # ratings_df.columns = ratings_query.keys()

    # ratings_df.head()
    # check for already reviewed recipes
    # reviewed_recipes_df = ratings_df[ratings_df['user_id'] == user_id]
    # print(recipes_df.head())
    # reviewed_recipes_df = reviewed_recipes_df.join(recipes_df, on='recipe_id')

    # print("Recipe previously reviewed by user_id {}:" + reviewed_recipes_df[['title', 'rating']])

    user_ratings = predicted_ratings[user_id]
    user_ratings_df = pd.DataFrame(user_ratings, dtype='str')
    recipes_df['rating'] = user_ratings_df

    # already_reviewed = reviewed_recipes_df['id']
    # recommended_df = recipes_df[recipes_df.index.isin(already_reviewed) == False]
    # recommended_df = recommended_df.sort_values(by=['rating'], ascending=False)

    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)
    return recipes_df
