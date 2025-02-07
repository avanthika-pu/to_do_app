from app.models import User
from app import db
from flask import jsonify
from app.services import custom_errors

def create_user(email: str, first_name: str, last_name: str, password: str) -> bool:
    try:
        if not first_name:
            raise ValueError("First name is required.")
        if len(first_name) > 128:
            raise ValueError("First name cannot exceed the length of 128 characters.")
        if not last_name:
            raise ValueError("Last name is required.")
        if len(last_name) > 64:
            raise ValueError("Last name cannot exceed the length of 64 characters.")
        if not password:
            raise ValueError("Password is required.")
        if len(password) < 8 or len(password) > 128:
            raise ValueError("Password must be between 8 and 128 characters.")
        if User.query.filter_by(email=email).first():
            raise ValueError("A user with this email already exists.")
        
       
        user = User(email=email, first_name=first_name, last_name=last_name,password=password)
        user.hash_password(password)
        db.session.commit()

        return True

    except Exception as e:
        return {"message": str(e)}


def update_user(user_id: int, updates: dict) -> dict:
    """Update user"""
    try:
        result = User.query.filter_by(id=user_id).update(updates)
        db.session.commit()

        return jsonify({"message": "User updated successfully", "status": 200})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "User not found", "error": str(e), "status": 404})
