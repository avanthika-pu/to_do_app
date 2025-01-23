from flask import (Blueprint, request, jsonify)
from app.services.user_service import create_user

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    create_user(request.json) 

    return jsonify({"message": "Successfully created user", "status": 200}), 200


    
    
