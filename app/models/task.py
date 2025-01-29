from datetime import datetime
from flask_httpauth import HTTPBasicAuth

from flask_httpauth import HTTPBasicAuth
from datetime import datetime

from app import db
from app.models.users import User 
from .base import BaseModel
from config import Config

auth = HTTPBasicAuth()


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.Text, nullable=False)
    description = db.Column(db.Text(255))
    archived = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data