from flask import Blueprint,request, jsonify, g

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import (
    check_password_hash,generate_password_hash)

from app import db
from app.api import bp
from app.services.custom_errors import (
    BadRequest, Unauthorized, InternalError, Forbidden)
from app.services.sendgrid_email import send_email
from app.services.auth import AuthService
from app.models import User, remove_user_token
from config import Config



auth_blueprint = Blueprint('auth', __name__)
auth = HTTPBasicAuth()
tokenAuth = HTTPTokenAuth(scheme='Token')
auth_service = AuthService()


@auth.verify_password
def verify_password(email: str, password: str) -> bool:
    """Verify user email and password"""
    user = User.query.filter_by(email=email).first()
    if not user:
        raise BadRequest("Incorrect Email")
    if not user.is_active:
        raise Forbidden('Your account has been suspended')
    if not user.registered:
        raise Unauthorized("Please register first and try again")
    if user.check_password(password):
        g.user = user
        print(g.user) 
        return True
    raise BadRequest('Wrong password')

@tokenAuth.verify_token
def verify_token(token: str) -> bool:
    if not token:
        token = str(request.headers.get('Authorization', ''))
    token = token.split('Token ')[-1]
    print(token)
    if token:
        user_is = User.verify_auth_token(token)
        print(user_is)
        if user_is:
            g.user = user_is
            return True
    raise Unauthorized()


@auth_blueprint.route('/login', methods=['POST'])
@bp.route('/login', methods=['POST'])
def login_user():
    """
    Login to the application with email address and password 
    """
    verify_password(request.json.get('email', ' ').lower().strip(), request.json.get('password', ' ').strip())
    token = g.user.generate_auth_token()
    print(g.user)
    return jsonify({'data': g.user.login_to_dict(), 'auth_token': token, 'status': 200})


@auth_blueprint.route('/register', methods=['POST'])
@bp.route('/login', methods=['POST'])
def register_user():
    """"register user"""
    try:
        data = request.json
        required_fields = ['first_name', 'last_name', 'email', 'password']
        missing_field = next((field for field in required_fields if field not in data), None) 
        if missing_field:
            return jsonify({"error": f"{missing_field} is required", "status": 400})

        if User.query.filter_by(email=data['email']).count(): 
            return jsonify({"message": "User already exists", "status": 400})

        hashed_password = generate_password_hash(data['password'])
        
        new_user = User(**{**data, 'password': hashed_password, 'registered': True})
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "status": 201})
    except Exception as e:
        db.session.rollback() 
        return jsonify({"message": str(e), "status": 500})


@auth_blueprint.route('/forgot_password', methods=['POST'])
@bp.route('/login', methods=['POST'])
def forgot_password():
    """Forgot password request"""
    try:
        token = auth_service.forgot_password(request.json.get('email', '').strip().lower(),)
        print(token)
        send_an_email = send_email(to_email=request.json.get('email', '').strip().lower(),
                                    html_content="Click here to reset<html>",
                                    subject='Reset Password')                                                                                                                                                                                                                                    
        if send_an_email:                                                                                                                                                                                                                                                                                                                                                   
            return jsonify({"message": "Please check your inbox", "status": 200})
        raise InternalError()
    except Exception as e:
        return jsonify({"message": str(e), "status": 500})
    

@auth_blueprint.route('/reset_password', methods=['PATCH'])
@bp.route('/login', methods=['POST'])
def reset_password_req():
    """reset password request"""
    token = request.headers.get('Authorization')
    print(f"Extracted Token: {token}")
    verify_token(token)
    print(token)
    if len(request.json.get('new_password', '')) < 5:
        raise BadRequest('Password length is short. Please try another password')
    if request.json.get('new_password') != request.json.pop('confirm_password', None):
        raise BadRequest('Enter the password correctly.')
    if auth_service.new_password(g.user['id'], request.json['new_password']):
        return jsonify({'message': 'Password has been changed successfully', 'status': 200})
    return InternalError()


@auth_blueprint.route('/logout', methods=['GET'])
@tokenAuth.login_required()
def logout():
    """logout user"""
    remove_user_token(g.user['id'], request.headers.get('Authorization', '').replace('Token ', '').strip())
    return jsonify({'message': 'Logout Successfully', 'status': 200})

