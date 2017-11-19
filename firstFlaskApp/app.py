from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators, IntegerField
import pickle
import pandas as pd
import sqlite3
import os
import numpy as np

#We ran our application as a single module; thus we initialized a new Flask instance with the argument __name__ to let Flask know that it can find the #HTML template folder (templates) in the same directory where it is located.
app = Flask(__name__)

#Preparing the recommender
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
db = os.path.join(cur_dir, 'recipes_db.db')

def recommend(user_id):
    # TODO get it from db
    recipes_df = pd.read_csv('datasets/recipes.csv', index_col='recipes_id')
    user_ratings = predicted_ratings[user_id - 1]
    recipes_df['rating'] = user_ratings
    recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)
    return recipes_df

#####Flask
class ReviewForm(Form):
    recommendForUserWithID = IntegerField('user id', [validators.DataRequired()])

#Next, we used the route decorator (@app.route('/')) to specify the URL that #should trigger the execution of the index function.
@app.route('/')
def index():
    # index f. renders .html
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = int(request.form['recommendForUserWithID'])
        recommendation = recommend(user_id)
        return render_template('results.html',
                               content=user_id,
                               prediction = recommendation)
    return render_template('reviewform.html', form=form)
"""
@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']
    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
    y = int(not(y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('thanks.html')
"""
if __name__ == '__main__':
    #run app on the server this script is directly executed by the Python interpreter, which we ensured using the if statement with __name__ == '__main__'.
    app.run(debug=True)