from typing import Dict
from flask import jsonify

from app import db
from app.models import User
from app.services import custom_errors

def create_user(data: dict) -> bool:
    """Create user"""
    for k in ['email', 'first_name', 'last_name', 'password']:
        print(f"Checking field: {k}, Value: {data.get(k)}")
        if not data.get(k):
            raise ValueError(f"Missing required field: {k}")
        
    email = data.get('email', "")
    if User.query.filter_by(email=email).count():
        raise ValueError("A user with this email already exists.")
    
    password = data.get("password", "")
    if not (8 <= len(password) <= 36):
        raise ValueError("Password must be between 8 and 36 characters")
    
    try:  
        user = User(**data)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return {"message": f"An unexpected error occurred: {str(e)}", "status": 500}



def update_user(user_id: int, data: Dict) -> Dict:
    """Update user"""
    try:
        result = User.query.filter_by(id=user_id).update(data)
        if not result:
            return False
        db.session.add()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return {"message":f"An unexpected error occurred: {str(e)}", "status": 500}
