import json
import redis
from datetime import timedelta

from flask_httpauth import HTTPBasicAuth
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import (
    generate_password_hash, check_password_hash)

from app import db, redis_obj
from .base import BaseModel
from config import Config

auth = HTTPBasicAuth()


class User(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.TEXT)
    # User information
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))

    # User state
    registered = db.Column(db.Boolean, default=True)

  

    def login_to_dict(self):
        """
        Logged-in user info from object to dict
        """
        data = dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )
        return data

    def to_dict(self, tz: str):
        data = dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )
        return data

    def basic_to_dict(self):
        data = dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        return data

    @staticmethod
    def get_hashed_password(password: str):
        """
        Hash the password
        """
        return generate_password_hash(password)

    def hash_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        if self.password is None:
            print("Error: Password is None in the database")
            return False
    
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration: int = Config.AUTH_TOKEN_EXPIRES):
        """
        Generate user token and store the value in redis
        """

        s = URLSafeTimedSerializer(Config.SECRET_KEY)
        print(s)
        print(self.first_name)
        token = s.dumps(
            {'id': self.id, 'first_name': self.first_name, 'last_name':self.last_name, 'email': self.email})
        print(token)
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
            print(data)
            if verify_user_token_in_cache(data['id'], token):
                return data
        except Exception as e:
            print(e)
        return False


def add_user_token_in_cache(user_id: int, expiry_at: int, user_auth_token: str) -> bool:
    """Store the auth token in Redis with an expiration time"""

    if expiry_at is None or not isinstance(expiry_at, int):
        raise ValueError("Expiry time cannot be None or invalid")

    redis_obj.setex(f"auth_token:{user_id}", timedelta(seconds=int(expiry_at)), user_auth_token)
    return True



def verify_user_token_in_cache(user_id: int, user_auth_token: str):
    if redis_obj.get(f"auth_token:{user_id}") == user_auth_token:
        return True
    return False


def remove_user_token(user_id: int, user_auth_token: str = None):
    """
    Remove user token from redis
    """
    if redis_obj.get(f"auth_token:{user_id}") == user_auth_token or not user_auth_token:
        redis_obj.delete(f"auth_token:{user_id}")
    return True
