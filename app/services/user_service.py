from flask import jsonify, request


from app import db
from app.models.users import User
from app.services import custom_errors

def create_user(email: str, first_name: str, last_name: str, password: str) -> bool:
    """Create User"""
    try:
        if not first_name:
            raise ValueError("First name is required.")
        # if len(first_name) > 128:
        #     raise ValueError("First name cannot exceed the length of 128 characters.")
        if not last_name:
            raise ValueError("Last name is required.")
        # if len(last_name) > 64:
        #     raise ValueError("Last name cannot exceed the length of 64 characters.")
        if not password:
            raise ValueError("Password is required.")
        
        if len(password) < 8 or len(password) < 38:
            raise ValueError("Password must be between 8 and 38 characters")
        
        if User.query.filter_by(email=email).count():
            raise ValueError("A user with this email already exists.")
        

        # user = User(email=email, first_name=first_name, last_name=last_name,password=password)
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

def delete_user(user_id: int) -> dict:
    """Delete user"""
    try:
        result = User.query.filter(User.id == user_id).update({"is_deleted": True})
        db.session.commit() 
        return jsonify({"message": "User deleted successfully", "status": 200})

    except Exception as e:
        db.session.rollback()
        return ({"message": "user not found", "error": str(e)})

    

