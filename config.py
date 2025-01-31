import redis
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG  = os.environ.get('DEBUG') or True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #PASSSWORD_RESET_SALT = os.environ.get('PASSWORD_RESET_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    PORT = os.environ.get('PORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_TOKEN_EXPIRES = os.environ.get('AUTH_TOKEN_EXPIRES')
    PER_PAGE = os.environ.get('PER_PAGE')
    REDIS_URL = "redis://localhost:6379/0"  
    REDIS = redis.StrictRedis.from_url(REDIS_URL)
 