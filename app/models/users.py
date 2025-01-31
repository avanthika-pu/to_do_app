from datetime import datetime
from datetime import timedelta
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import (generate_password_hash, check_password_hash)

from app import db
from config import Config
from app.models import BaseModel
from itsdangerous import URLSafeTimedSerializer
from app import redis_obj


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

        
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.id,
            'name': self.name,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data

    @staticmethod
    def get_hashed_password(password: str):
        """
        Hash the password
        """
        return generate_password_hash(password)

    def hash_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str):
        """
        Check password with the hashed password
        """
        return check_password_hash(self.hashed_password, password)

    def generate_auth_token(self, expiration: int = Config.AUTH_TOKEN_EXPIRES):
        """
        Generate user token and store the value in redis
        """
        s = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = s.dumps(
            {'id': self.id, 'name': self.name, 'role_id': self.role_id, 'email': self.email})
        add_user_token_in_cache(self.id, expiration, token)
        return token

    @staticmethod
    def verify_auth_token(token: str, expires_in: int = Config.AUTH_TOKEN_EXPIRES):
        """
        Verifying the user token valid or not
        """
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(token, max_age=expires_in)
            if verify_user_token_in_cache(data['id'], token):
                return data
        except Exception as e:
            print(e)
        return False


def add_user_token_in_cache(user_id: int, expiry_at: int, user_auth_token: str) -> bool:
    redis_obj.setex(f"{user_id}", timedelta(seconds=expiry_at), user_auth_token)
    return True


def verify_user_token_in_cache(user_id: int, user_auth_token: str):
    if redis_obj.get(f"{user_id}") == user_auth_token:
        return True
    return False


def remove_user_token(user_id: int, user_auth_token: str = None):
    """
    Remove user token from redis
    """
    if redis_obj.get(f"{user_id}") == user_auth_token or not user_auth_token:
        redis_obj.delete(f"{user_id}")
    return True
