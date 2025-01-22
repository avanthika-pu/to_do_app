from app import db
from app.models.users import Users 
from flask_httpauth import HTTPBasicAuth
from app import db
from .base import BaseModel
from config import Config

auth = HTTPBasicAuth()


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.Text, nullable=False)
    description = db.Column(db.Text(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
