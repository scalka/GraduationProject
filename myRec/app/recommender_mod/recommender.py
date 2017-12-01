#Preparing the recommender
import os
import pickle

import pandas as pd

from app import engine
from app.mod_auth.models import Recipe

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
    #http://shichaoji.com/2016/10/10/database-python-connection-basic/
    # Open engine connection
    con = engine.connect()

    # Perform query: rs
    recipe_query = con.execute('select * from recipe')

    # Save results of the query to list: ll
    recipes = recipe_query.fetchall()

    # Close connection
    con.close()

    recipes_df = pd.DataFrame(recipes)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipe_query.keys()

    recipes_df.head()
    #recipes_df = pd.read_csv('C:\\Users\\calka\\Documents\\Y4\\Recommender\\myRec\\app\\recommender_mod\\datasets\\recipes.csv', index_col='recipes_id')
    user_ratings = predicted_ratings[user_id - 1]

    #TODO workaround for now https://stackoverflow.com/questions/42382263/valueerror-length-of-values-does-not-match-length-of-index-pandas-dataframe-u
    user_ratings_df = pd.DataFrame(user_ratings, dtype='str' )
    recipes_df['rating'] = user_ratings_df

    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)


    return recipes_df