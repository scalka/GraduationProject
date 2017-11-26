#configuration variables
# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for signing cookies
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test3.db')
DATABASE_CONNECT_OPTIONS = {}
