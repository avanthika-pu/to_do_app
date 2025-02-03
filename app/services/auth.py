from functools import wraps
from flask import g

from app.services.custom_errors import NoContent, Forbidden, Conflict
from app.models import User, remove_user_token
from app.services.user_service import User


class AuthService(object):
    @staticmethod
    def forgot_password(email: str, expires_in=3600) -> tuple:
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user:
            raise NoContent("Please enter a valid email address.")
        if not user.registered:
            raise Forbidden("Please register first")
        token = user.generate_auth_token(expires_in)
        return user.name, token
    
