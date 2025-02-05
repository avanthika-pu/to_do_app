from flask import Blueprint,request, jsonify, g, render_template
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api import bp
from app import db
from app import redis_obj
from app.services.custom_errors import (BadRequest, Unauthorized, InternalError, Forbidden)
from app.services.sendgrid_email import send_email
from werkzeug.security import check_password_hash,generate_password_hash
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
        print(g.user, "111111111234") 
        return True
    raise BadRequest('Wrong password')

@tokenAuth.verify_token
def verify_token(token: str) -> bool:
    if not token:
        token = str(request.headers.get('Authorization', ''))
    token = token.split('Token ')[-1]
    print(token, "###########")
    if token:
        user_is = User.verify_auth_token(token)
        print(user_is, '@@@@@@@@@@@@@@@@')
        if user_is:
            g.user = user_is
            return True
    raise Unauthorized()




@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    """
    Login to the application with email address and password in
    """
    verify_password(request.json.get('email', ' ').lower().strip(), request.json.get('password', ' ').strip())
    token = g.user.generate_auth_token()
    print(g.user, "222234454")
    return jsonify({'data': g.user.login_to_dict(), 'auth_token': token, 'status': 200})


@auth_blueprint.route('/register', methods=['POST'])
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

@auth_blueprint.route('/forgot_password', methods=['POST'])
def forgot_password():
    print(request.json.get('email', ''))
    email = request.json.get('email', '').strip().lower()
    print(email)
    if not email:
        return jsonify({"message": "Email is required", "status": 400})
    print(email)
    try:
        token = auth_service.forgot_password(email)
        print(token)
        reset_url = f"{Config.FRONT_END_PASSWORD_RESET_URL}/{token}"
        print(reset_url)
        send_an_email = send_email(to_email=email, html_content=f"Click here to reset: {reset_url}", subject='Reset Password')
        print(send_an_email)
        if send_an_email:
            return jsonify({"message": "Please check your inbox", "status": 200})
        raise InternalError()
    except Exception as e:
        return jsonify({"message": str(e), "status": 500})
    

@auth_blueprint.route('/reset_password', methods=['PATCH'])
def reset_password_req():
    token = request.headers.get('Authorization')
    print(f"Extracted Token: {token}")
    verify_token(token)
    print(token)
    if len(request.json.get('new_password', '')) < 5:
        raise BadRequest('Password length is short. Please try another password')
    if request.json.get('new_password') != request.json.pop('confirm_password', None):
        raise BadRequest('Enter the password correctly.')
    if auth_service.new_password(g.user['id'], request.json['new_password']):
        return jsonify({'message': 'Password has been changed successfully', 'status': 200}), 200
    return InternalError()


@auth_blueprint.route('/logout', methods=['GET'])
@tokenAuth.login_required()
def logout():
    token = request.headers.get('Authorization')
    print(f"Extracted Token: {token}")
    verify_token(token)
    remove_user_token(g.user['id'], request.headers.get('Authorization', '').replace('Token ', '').strip())
    return jsonify({'message': 'Logout Successfully', 'status': 200}), 200

