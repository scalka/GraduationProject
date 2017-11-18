import pickle
import pandas as pd

# Load prediction rules from data files
U = pickle.load(open("pickled/user_features_recipes.dat", "rb"))
M = pickle.load(open("pickled/product_features_recipes.dat", "rb"))
predicted_ratings = pickle.load(open("pickled/predicted_ratings_recipes.dat", "rb"))

# Load recipe titles
recipes_df = pd.read_csv('datasets/recipes.csv', index_col='recipes_id')

print("Enter a user_id to get recommendations (Between 1 and 100):")
user_id_to_search = int(input())

print("Recipes we will recommend:")

user_ratings = predicted_ratings[user_id_to_search - 1]
recipes_df['rating'] = user_ratings
recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)

print(recipes_df[['title', 'category', 'rating']].head(15))