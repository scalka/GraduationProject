#Preparing the recommender
import pickle

import os

import pandas as pd

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
