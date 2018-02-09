import pickle
import os
import pandas as pd
from app import engine

def mf_recommend(user_id):
    # Open engine connection
    con = engine.connect()
    # Perform query: rs to get recipe data from database
    recipe_query = con.execute('select * from recipe')
    # Save results of the query to list: ll
    recipes = recipe_query.fetchall()
    # Close connection
    con.close()
    # create data frame from recipes from database
    recipes_df = pd.DataFrame(recipes)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipe_query.keys()

    print(recipes_df)



    return recipes_df