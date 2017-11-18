from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np

class HelloForm(Form):
    sayhello = TextAreaField('', [validators.DataRequired()])

#We ran our application as a single module; thus we initialized a new Flask instance with the argument __name__ to let Flask know that it can find the #HTML template folder (templates) in the same directory where it is located.
app = Flask(__name__)

#Next, we used the route decorator (@app.route('/')) to specify the URL that #should trigger the execution of the index function.
@app.route('/')
def index():
    # index f. renders .html
    form = HelloForm(request.form)
    return render_template('first_app.html', form=form)

@app.route('/hello', methods=['POST'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['sayhello']
        return render_template('hello.html', name=name)
    return render_template('first_app.html', form=form)

if __name__ == '__main__':
    #run app on the server this script is directly executed by the Python interpreter, which we ensured using the if statement with __name__ == '__main__'.
    app.run(debug=True)