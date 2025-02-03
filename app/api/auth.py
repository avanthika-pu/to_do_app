from flask import request, jsonify, g, Blueprint
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api import bp
import json
from werkzeug.security import check_password_hash,generate_password_hash
from app.models import User, remove_user_token
from app import db, redis_obj 
from app.services.auth import AuthService, verify_password
from config import Config
import uuid

auth_bp = Blueprint('auth', __name__)

auth = HTTPBasicAuth()
tokenAuth = HTTPTokenAuth(scheme='Token')
auth_service = AuthService()


@bp.route('/get_token/<user_id>', methods=['GET'])
def get_token_from_redis(user_id):
    """token stored in Redis."""
    token = redis_obj.get(user_id)  
    if token:
        return jsonify({"message": "Token found Successfully", "status": 200})
    else:
        return jsonify({"error": "Token not found", "status": 404})
    


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(data.get(field) for field in ['first_name', 'last_name', 'email', 'password']):
        return jsonify({"message": "All fields are required", "status": 404})
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists", "status":400})
    
    hashed_password = generate_password_hash(data['password'])
    print(f"Hashed password: {hashed_password}")
    new_user = User(**{**data, 'password': hashed_password})

    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return jsonify({"message": "User Registered successfully", "status": 201})


@bp.route('/login', methods=['POST']) 
def login():
    data = request.get_json()

    if not all(data.get(field) for field in ['email', 'password']):
        return jsonify({"message": "Email and password are required", "status": 400})

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials", "status": 401})

    return jsonify({"message": "Login successful", "status": 200})
