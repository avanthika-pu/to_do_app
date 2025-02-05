from flask import (Blueprint, request, jsonify)

from app import db
from app.services.user_service import (
    create_user, update_user)
from app.models.users import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    create_user(request.json) 
    return jsonify({"message": "Successfully created user", "status": 200})

    
@user_blueprint.route('/<int:user_id>', methods=['PUT'])
def updating_user(user_id):
    update_user(user_id, request.json)  
    return jsonify({"message": "User updated successfully","status": 200})