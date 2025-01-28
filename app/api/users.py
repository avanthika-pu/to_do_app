from flask import (Blueprint, request, jsonify)

from app import db
from app.services.user_service import create_user
from app.models.users import User


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create', methods=['POST'])
def creating_user():
    create_user(request.json) 
    return jsonify({"message": "Successfully created user", "status": 201})

    
    

# """update user"""

# @user_blueprint.route('/update/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     try:
#         data = request.get_json()
#         user = User.query.get(user_id)
#         user.name = data.get('name', user.name)
#         user.email = data.get('email', user.email)
#         user.first_name = data.get('first_name', user.first_name)
#         user.last_name = data.get('last_name', user.last_name)
#         db.session.commit()

#         return jsonify({"message": "User updated successfully", "status": 200})

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": "An error occurred", "error": str(e), "status": 500})

