from flask import g

from app import db
from app.services.custom_errors import NoContent, Forbidden, Conflict
from app.services.custom_errors import (BadRequest, Unauthorized, InternalError, Forbidden)
from app.models import User, remove_user_token
from app import redis_obj
import json




class AuthService(object):
    @staticmethod
    def forgot_password(email: str, expires_in=4000) -> tuple:
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user:
            raise NoContent("Please enter valid email")
        if not user.registered:
            raise Forbidden("Please Register")
        token = user.generate_auth_token(expires_in)
        return user.name, token
    
def verify_password(email: str, password: str) -> bool:
    """User password verification"""
    user = User.query.filter_by(email=email).first()
    if not user:
        raise BadRequest("Incorrect Email")
    if not user.is_active:
        raise Forbidden("Your account has been suspended")
    if not user.registered: 
        raise Unauthorized("Please Register")
    if user.check_password(password):
        g.user = user
        return True
    else:
        raise BadRequest("Wrong Password")
def verify_token(token: str):
    """Verify token"""
    token_key = f"auth_token:{token}"  
    user_data = redis_obj.get(token_key)
    
    if user_data:
        user_data = json.loads(user_data)
        user_id = user_data.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            if user:
                g.user = user  
                return True
    return False 
def store_token_in_redis(user_id, token, expires_in=86400):
    """Store user token in Redis"""
    user_data = {
        "user_id": user_id
    }
    
    token_key = f"auth_token:{token}" 

    redis_obj.setex(token_key, expires_in, json.dumps(user_data))
    print(f"Token stored in Redis: {token_key}")  

@staticmethod
def new_invitee(data: dict) -> bool:
    user_obj = User.query.filter_by(id=g.user['id']).first()
    if user_obj.registered:
        raise Conflict('User already registered')
        
    user_obj.hash_password(data.pop('passowrd'))
    user_obj.registered = True
    user_obj.is_active = True

    db.session.commit()
    remove_user_token(g.user['id'])
    return True