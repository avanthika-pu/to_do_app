from functools import wraps

import jwt
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import (generate_password_hash)
from flask import g, current_app as app

from app import db
from app.models import User, remove_user_token
from app.services.custom_errors import (
    NoContent, Forbidden, Unauthorized)
from app.services.user_service import User
from config import Config


class AuthService(object):
    @staticmethod
    def forgot_password(email: str, expires_in=3600) -> tuple:
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user:
            print(user)
            raise NoContent("Please enter a valid email address.")
        if not user.registered:
            print(user.registered)
            raise Forbidden("Please register first")
        token = user.generate_auth_token(expires_in)
        return user.first_name, token
    
    @staticmethod
    def new_password(user_id, new_password):
        hashed_password = generate_password_hash(new_password)
        user = User.query.get(user_id)
        user.password = hashed_password
        db.session.commit()
        return True

    
    
def admin_authorizer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user['role_id'] == 1:
            return func(*args, **kwargs)
        raise Forbidden()

    return inner