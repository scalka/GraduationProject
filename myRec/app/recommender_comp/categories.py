"""
Functions related to the categories page
"""
import pandas as pd
from app import engine


def find_categories():
    con = engine.connect()    # Open engine connection
    # Perform query:
    recipes_query = con.execute('select * from recipe')
    # Save results of the query to list
    recipes = recipes_query.fetchall()
    recipes_df = pd.DataFrame(recipes)
    # Using the recipes object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipes_query.keys()
    # get only unique values
    categories = recipes_df.category.unique()
    # order categories alphabetically
    categories = pd.np.sort(categories)
    # Close connection
    con.close()
    return categories


def display_recipes_from_category(cat):
    # Open engine connection
    con = engine.connect()
    # Perform query:
    # filter query based on http://programminghistorian.github.io/ph-submissions/lessons/creating-apis-with-python-and-flask
    category_name = cat
    sql = "select * from recipe where"
    to_filter = []
    if category_name:
        sql += ' category=?'
        to_filter.append(category_name)

    recipes_query = con.execute(sql, to_filter)
    # Save results of the query to list: ll
    recipes = recipes_query.fetchall()
    recipes_df = pd.DataFrame(recipes)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes_df.columns = recipes_query.keys()

    # Close connection
    con.close()
    return recipes_df
