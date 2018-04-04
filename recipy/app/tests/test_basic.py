# project/test_basic.py
import os
import unittest

from flask import url_for

from app import app, db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
  ############################
  #### setup and teardown ####
  ############################

  ########################
  #### helper methods ####
  ########################

  def register(self, email, username, password):
    return self.app.post(
      'auth/register',
      data=dict(email=email, username=username, password=password, authenticated=True),
      follow_redirects=True
    )

  def login(self, email, password):
    return self.app.post(
      'auth/login',
      data=dict(email=email, password=password, authenticated=True),
      follow_redirects=True
    )

  def logout(self):
    return self.app.get(
      'auth/logout',
      follow_redirects=True
    )
  # executed prior to each test

  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                            os.path.join(app.config['BASE_DIR'], TEST_DB)
    self.app = app.test_client()
    db.drop_all()
    db.create_all()

    # Disable sending emails during unit testing
    self.assertEqual(app.debug, False)

  # executed after each test
  def tearDown(self):
    db.session.remove()
    db.drop_all()


  ###############
  #### tests ####
  ###############



  def test_main_page(self):
    response = self.app.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)


  def test_valid_user_registration(self):
    response = self.register('sylwia@gmail.com', 'Username', 'FlaskIsAwesome')
    self.assertEqual(response.status_code, 200)

  def test_invalid_user_registration_duplicate_email(self):
    response = self.register('sylwia@gmail.com', 'Username', 'FlaskIsAwesome')
    self.assertEqual(response.status_code, 200)
    response = self.register('sylwia@gmail.com', 'Username', 'FlaskIsReallyAwesome')
    self.assertIn('Email address already exists'.encode(), response.data)

  def logout(self):
    return self.app.get('/logout', follow_redirects=True)





if __name__ == "__main__":
  unittest.main()


