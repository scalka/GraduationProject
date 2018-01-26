import pandas as pd

from app import engine

def find_categories():
    # Open engine connection
    con = engine.connect()

    # Perform query:
    recipes_query = con.execute('select * from recipe')

    # Save results of the query to list: ll
    recipes = recipes_query.fetchall()
    recipes_df = pd.DataFrame(recipes)


    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipes_query.keys()

    print(recipes_df.category.unique())
    categories = recipes_df.category.unique()
    # Close connection
    con.close()

    #recommendation based on counts of ratings (from users)
    #rating_count = pd.DataFrame(ratings_df.groupby('recipe_id')['rating'].count())
    #rating_count = rating_count.sort_values('rating', ascending=False).head()

    #print("The most popular recipes in the db " + rating_count)

    #Most popular based on the review_count from dataset
    #most_ratings = recipes_df.sort_values(['review_count'], ascending=[False])

    return categories
