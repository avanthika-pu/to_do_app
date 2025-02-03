from flask import Blueprint,request, jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api import bp
from app import db
from app.services.custom_errors import (BadRequest, Unauthorized, InternalError, Forbidden)
from werkzeug.security import check_password_hash,generate_password_hash
from app.services.auth import AuthService
from app.models import User, remove_user_token
from config import Config

auth_bp = Blueprint('auth', __name__)

auth = HTTPBasicAuth()
tokenAuth = HTTPTokenAuth(scheme='Token')
auth_service = AuthService()


from app.models.users import User
from app.services.custom_errors import Unauthorized

@auth.verify_password
def verify_password(email: str, password: str) -> bool:
    """Verify user email and password"""
    user = User.query.filter_by(email=email).first()
    print(user)
    if not user:
        raise BadRequest("Incorrect Email")
    if not user.is_active:
        raise Forbidden('Your account has been suspended')
    if not user.registered:
        print(user.registered)
        raise Unauthorized("Please register first and try again")
    if user.check_password(password):
        g.user = user
        return True
    else:
        raise BadRequest('Wrong password')
    
@tokenAuth.verify_token
def verify_token(token: str) -> bool:
    if not token:
        token = str(request.headers.get('Authorization', ''))
    token = token.split('Token ')[-1]
    if token:
        user_is = User.verify_auth_token(token)
        if user_is:
            g.user = user_is
            return True
    raise Unauthorized()


@auth_bp.route('/login', methods=['POST'])
def login_user():
    """
    Login to the application with email address and password in
    """
    verify_password(request.json.get('email', ' ').lower().strip(), request.json.get('password', ' ').strip())
    token = g.user.generate_auth_token()
    return jsonify({'data': g.user.login_to_dict(), 'auth_token': token, 'status': 200}), 200


@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('first_name') or not data.get('last_name'):
        return jsonify({"message": "Email, password, first name, and last name are required", "status": 400})
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists", "status": 400})
    hashed_password = generate_password_hash(data['password'])
    new_user = User(**{**data, 'password': hashed_password, 'registered': True})

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "status": 201})






