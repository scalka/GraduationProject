"""
Content Based Recommender
1. Term Frequency-Inverse Document Frequency (TF-IDF)
2. Metadata recommendatins
Based on the tutorial from https://www.datacamp.com/community/tutorials/recommender-systems-python
"""
import os
import pandas as pd
from app import engine
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from functools import reduce

cur_dir = os.path.dirname(__file__)


def fetch_data():
    # Open engine connection
    con = engine.connect()
    # Perform query: rs to get recipe data from database
    recipe_query = con.execute('select * from recipe ')
    # Save results of the query to list
    recipes = recipe_query.fetchall()
    # Close connection
    con.close()
    # create data frame from recipes from database
    recipes = pd.DataFrame(recipes)
    # Using the rs object, set the DataFrame's column names to the corresponding names of the table columns.
    recipes.columns = recipe_query.keys()
    return recipes


def contentbased_tfidf_recommend(find_similar_to):    # Term Frequency-Inverse Document Frequency (TF-IDF)
    recipes = fetch_data()
    # Replace NaN with an empty string
    recipes['ingredients'] = recipes['ingredients'].fillna('')
    # remove metacharacters (\W+) and remove numbers (\d+)
    recipes['ingredients'] = recipes['ingredients'].str.strip().str.replace('(\W+)', ' ').str.replace('(\d+)', '')
    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')
    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(recipes['ingredients'])
    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Construct a reverse map of indices and recipe titles
    indices = pd.Series(recipes.index, index=recipes['title']).drop_duplicates()

    return get_contentbased_recommendations(find_similar_to, recipes, indices, cosine_sim)


def metadata_recommend(find_similar_to):
    recipes = fetch_data()
    # data with description column
    description = pd.read_csv(os.path.join(cur_dir,
                     'datasets',
                     'data_description.csv'), sep=",", error_bad_lines=False, encoding="latin-1")
    # merge recipes with description
    recipes = pd.merge(recipes, description.iloc[:, [0, 4]], how='left', on='id')
    # metadata to be used to describe recipe
    features = ['ingredients', 'category', 'description']
    # clean data
    for feature in features:
        recipes[feature] = recipes[feature].apply(clean_data).\
          str.strip().str.replace('(\W+)', ' ').str.replace('(\d+)', '')
    # Create a new metadata soup
    recipes['soup'] = recipes.apply(create_soup, axis=1)
    # use CountVectorizer() instead of tf-idf
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(recipes['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    # Reset index of your main DataFrame and construct reverse mapping as before
    indices = pd.Series(recipes.index, index=recipes['title']).drop_duplicates()
    return get_contentbased_recommendations(find_similar_to, recipes, indices, cosine_sim2)


def create_soup(x):  # function to join all the strings that contains metadata to be fed to vectorizer
    return ' '.join(x['ingredients']) + ' ' + x['category'] + ' ' + ' '.join(x['description'])


# function to clean data - convert to lower case, remove unnecessary words
def clean_data(x):
    # Function to convert all strings to lower case and strip names of spaces
    repls = ('cups', ''), ('cup', ''), ('tablespoons', ''), ('pounds', ''), ('pound', ''), \
            ('saucepan', ''), ('discard', ''), \
            ('medium', ''), ('peel', ''), ('combine', ''), ('half', ''), ('place', ''), ('add', ''), ('pound', '')
    if isinstance(x, list):
        return [str.lower(reduce(lambda a, kv: a.replace(*kv), repls, x)) for i in x]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(reduce(lambda a, kv: a.replace(*kv), repls, x))
        else:
            return ''


def get_contentbased_recommendations(title, recipes, indices, cosine_sim):
    # Function that takes in recipe title as input and outputs most similar recipes
    # Get the index of the recipe that matches the title
    idx = indices[title]
    # Get the pairwise similarity scores of all recipes with that recipe
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the recipes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar recipes
    sim_scores = sim_scores[1:11]
    # Get the recipe indices
    recipe_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar recipes
    recipes_df = recipes.iloc[recipe_indices]

    return recipes_df


def get_last_rated_recipe(rated_recipes, rating):
    i = len(rated_recipes)
    con = engine.connect()
    last_rated_t = 0
    # reversed loop from highest to lowest
    for i in reversed(range(i)):
        if rated_recipes[i][1] >= rating:
            rq = con.execute('select title from recipe where recipe.id == ' + str(rated_recipes[i][0]))
            rec = rq.fetchone()
            last_rated_t=rec[0]
            break
    con.close()
    return last_rated_t


def get_last_bookmarked(bookmarked):
    i = len(bookmarked)
    con = engine.connect()
    last_bookmarked = 0
    # reversed loop from highest to lowest
    for i in reversed(range(i)):
      rq = con.execute('select title from recipe where recipe.id == ' + str(bookmarked[i][0]))
      rec = rq.fetchone()
      last_bookmarked = rec[0]
      break
    con.close()
    return last_bookmarked


# contentbased_tfidf_recommend('Maple Roast Turkey')
# metadata_recommend('Maple Roast Turkey')
