# app/api/user_api.py
from flask import Blueprint, request, jsonify
from app.services.user_service import create_user

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    data = request.json  
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    create_user(email, first_name, last_name, password)  
    return jsonify({"message": "Successfully created user", "status": 200}), 200
    
    
