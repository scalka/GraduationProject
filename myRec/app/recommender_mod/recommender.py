#Preparing the recommender
import os
import pickle

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

def recommend(user_id, pd=None):
    # TODO get it from db
    recipes_df = pd.read_csv('C:\\Users\\calka\\Documents\\Y4\\Recommender\\myRec\\app\\recommender_mod\\datasets\\recipes.csv', index_col='recipes_id')
    user_ratings = predicted_ratings[user_id - 1]
    recipes_df['rating'] = user_ratings
    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)

    return recipes_df