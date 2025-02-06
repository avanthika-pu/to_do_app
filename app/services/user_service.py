from app.models import User
from app import db
from flask import jsonify, request
from app.services import custom_errors

def create_user(email: str, first_name: str, last_name: str, password: str) -> bool:
    """Create User"""
    try:
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        if not password:
            raise ValueError("Password is required.")
        
        if len(password) < 8 or len(password) < 38:
            raise ValueError("Password must be between 8 and 38 characters")
        
        if User.query.filter_by(email=email).count():
            raise ValueError("A user with this email already exists.")
        data = request.json
        db.session.add(User(**{**data, "password": User.hash_password(data["password"])}))
        db.session.commit()
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False 
    
    except Exception as e:
        db.session.rollback()
        print(f"An unexpected error occurred: {e}")
        return False

def update_user(user_id: int, updates: dict) -> dict:
    """Update user"""
    try:
        result = User.query.filter_by(id=user_id).update(updates)
        db.session.commit()

        return jsonify({"message": "User updated successfully", "status": 200})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "User not found", "error": str(e), "status": 404})
