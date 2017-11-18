import sqlite3
import os

if os.path.exists('recipes.sqlite'):
    os.remove('recipes.sqlite')
conn = sqlite3.connect('recipes.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE recipes_db'\
          ' (recipes_id INTEGER, title TEXT, category TEXT)')

example1 = 'Pumpkin soup'
c.execute('INSERT INTO recipes_db'\
          '(recipes_id, title, category) VALUES'\
          ' (?, ?, ?)', (9999999, example1, 'soup'))

conn.commit()
conn.close()

