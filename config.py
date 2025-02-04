import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    FRONT_END_PASSWORD_RESET_URL = os.environ.get('FRONT_END_PASSWORD_RESET_URL')
    DEBUG  = os.environ.get('DEBUG') or True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PASSSWORD_RESET_SALT = os.environ.get('PASSWORD_RESET_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    PORT = os.environ.get('PORT')
    AUTH_TOKEN_EXPIRES = 3600 
    REDIS_URL = "redis://localhost:6379/0" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_EMAIL_ADDRESS = os.environ.get('SENDGRID_EMAIL_ADDRESS')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    PER_PAGE = os.environ.get('PER_PAGE')