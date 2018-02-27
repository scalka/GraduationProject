"""
Popularity recommender that recommends the most popular recipes
"""
import pandas as pd
from app import engine


def pop_recommend():
    # Open engine connection
    con = engine.connect()
    # Perform query: rs
    recipe_query = con.execute('select * from recipe')
    ratings_query = con.execute('select * from ratings')
    # Save results of the query to list: ll
    recipes = recipe_query.fetchall()
    ratings = ratings_query.fetchall()
    recipes_df = pd.DataFrame(recipes)
    ratings_df = pd.DataFrame(ratings)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipe_query.keys()
    ratings_df.columns = ratings_query.keys()
    # Close connection
    con.close()

    # recommendation based on counts of ratings (from users)
    # rating_count = pd.DataFrame(ratings_df.groupby('recipe_id')['rating'].count())
    # rating_count = rating_count.sort_values('rating', ascending=False).head()
    # print("The most popular recipes in the db " + rating_count)
    # Most popular based on the review_count from dataset
    most_ratings = recipes_df.sort_values(['review_count'], ascending=[False])

    return most_ratings
