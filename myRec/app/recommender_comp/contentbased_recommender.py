import pickle
import os
import numpy as np
import pandas as pd
from app import engine
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval
from functools import reduce
from string import digits


def fetch_data():
    # Open engine connection
    con = engine.connect()
    # Perform query: rs to get recipe data from database
    recipe_query = con.execute('select * from recipe')
    # Save results of the query to list
    recipes = recipe_query.fetchall()
    # Close connection
    con.close()
    # create data frame from recipes from database
    recipes = pd.DataFrame(recipes)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes.columns = recipe_query.keys()
    return recipes



# Term Frequency-Inverse Document Frequency (TF-IDF)
def contentbased_tfidf_recommend(find_similar_to):
    recipes = fetch_data()
    # Replace NaN with an empty string
    recipes['ingredients'] = recipes['ingredients'].fillna('')
    # remove metacharacters (\W+) and remove numbers (\d+)
    recipes['ingredients'] = recipes['ingredients'].str.strip().str.replace('(\W+)', ' ').str.replace('(\d+)', '')
    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')
    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(recipes['ingredients'])
    # Output the shape of tfidf_matrix
    tfidf_matrix.shape
    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Construct a reverse map of indices and movie titles
    indices = pd.Series(recipes.index, index=recipes['title']).drop_duplicates()

    return get_contentbased_recommendations(find_similar_to, recipes, indices, cosine_sim)

def metadata_recommend(find_similar_to):
    recipes = fetch_data()
    # data with description column
    description = pd.read_csv('datasets/data_description.csv', sep=",",
                              error_bad_lines=False, encoding="latin-1")
    # merge recipes with description
    recipes = pd.merge(recipes, description.iloc[:, [0, 4]], how='left', on='id')
    # metadata to be used to describe recipe
    features = ['ingredients', 'category', 'description']
    # clean data
    for feature in features:
        recipes[feature] = recipes[feature].apply(clean_data).str.strip().str.replace('(\W+)', ' ').str.replace('(\d+)', '')
    # Create a new metadata soup
    recipes['soup'] = recipes.apply(create_soup, axis=1)
    # use CountVectorizer() instead of TF-IDF
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(recipes['soup'])
    # Compute the Cosine Similarity matrix based on the count_matrix
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    # Reset index of your main DataFrame and construct reverse mapping as before
    indices = pd.Series(recipes.index, index=recipes['title']).drop_duplicates()

    return get_contentbased_recommendations(find_similar_to, recipes, indices, cosine_sim2)

# function to create metadata soup - string that contains metadata to be fed to vectorizer
def create_soup(x):
    return ' '.join(x['ingredients']) + ' ' + x['category'] + ' ' + ' '.join(x['description'])


# function to clean data - convert to lower case, remove unnecessary words
def clean_data(x):
    # Function to convert all strings to lower case and strip names of spaces
    repls = ('cups', ''), ('cup', ''), ('tablespoons', ''), ('pounds', ''), ('pound', ''), ('saucepan', ''), ('discard', ''), \
            ('medium', ''), ('peel', ''), ('combine', ''), ('half', ''), ('place', ''), ('add', ''), ('pound', '')
    if isinstance(x, list):
        return [str.lower(reduce(lambda a, kv: a.replace(*kv), repls, x)) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(reduce(lambda a, kv: a.replace(*kv), repls, x))
        else:
            return ''

# Function that takes in movie title as input and outputs most similar movies
def get_contentbased_recommendations(title, recipes, indices, cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    recipe_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    print(recipes['title'].iloc[recipe_indices])
    return recipes['title'].iloc[recipe_indices]


contentbased_tfidf_recommend('Maple Roast Turkey')
metadata_recommend('Maple Roast Turkey')