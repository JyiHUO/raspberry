# encoding=utf-8
import os

# sqlite
SECRET_KEY = os.urandom(24)
# HOSTNAME = '127.0.0.1'
# PORT = '5000'
DATABASE = 'hi_movie'
# USERNAME = 'root'
# PASSWORD = 'root'
# DB_URI = ""
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/{}.db'.format(DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True