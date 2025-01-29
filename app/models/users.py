from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import (generate_password_hash, check_password_hash)

from app import db
from config import Config
from app.models import BaseModel


auth = HTTPBasicAuth()

class User(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(128), index=True, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(64))
    password = db.Column(db.TEXT(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data

    def get_hashed_password(self, password):
        return generate_password_hash(password)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    