from flask import (Blueprint, request, jsonify)

from app import db
from app.services.user_service import create_user, delete_user
from app.models.users import User


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    create_user(request.json) 
    return jsonify({"message": "Successfully created user", "status": 201})



@user_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        result = delete_user(user_id) 
        
        if result.get('success'):
            return jsonify({"message": "User deleted successfully", "status": 200})
        
        return jsonify({"message": "User not found", "status": 404})
    
    except Exception as e:
        return jsonify({"message": "internal server error", "error": str(e)})
