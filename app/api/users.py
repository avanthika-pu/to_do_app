from flask import (Blueprint, request, jsonify)

from app import db
from app.services.user_service import create_user
from app.models.users import User


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    create_user(request.json) 
    return jsonify({"message": "Successfully created user", "status": 201})

    
    
user_blueprint.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """update user"""
    data = request.get_json()
    user = User.query.get(user_id)
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully", "status": 200})
    
