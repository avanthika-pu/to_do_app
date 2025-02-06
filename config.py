import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG  = os.environ['DEBUG'] or True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'sqlite:///app.db'
    AUTH_TOKEN_EXPIRES = 604800
    REDIS_URL = "redis://localhost:6379/0" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
