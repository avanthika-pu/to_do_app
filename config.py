import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    FRONT_END_PASSWORD_RESET_URL = os.environ[('FRONT_END_PASSWORD_RESET_URL')]
    DEBUG  = os.environ[('DEBUG')] or True
    SECRET_KEY = os.environ[('SECRET_KEY')]
    PASSSWORD_RESET_SALT = os.environ[('PASSWORD_RESET_SALT')]
    SQLALCHEMY_DATABASE_URI = os.environ[('DATABASE_URL') ]or 'sqlite:///app.db'
    PORT = os.environ[('PORT')]
    AUTH_TOKEN_EXPIRES = 3600 
    REDIS_URL = "redis://localhost:6379/0" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_EMAIL_ADDRESS = os.environ[('SENDGRID_EMAIL_ADDRESS')]
    SENDGRID_API_KEY = os.environ[('SENDGRID_API_KEY')]
    PER_PAGE = os.environ[('PER_PAGE')]