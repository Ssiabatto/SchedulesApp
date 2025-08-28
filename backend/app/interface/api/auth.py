import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.application.services import UserService
from app.infrastructure.database import DatabaseSession, SQLUserRepository

auth_bp = Blueprint('auth', __name__)

# Initialize database and repositories
db_session_manager = DatabaseSession(os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/gestion_turnos_vigilantes'))
db_session = db_session_manager.get_session()
user_repository = SQLUserRepository(db_session)
user_service = UserService(user_repository)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    user = user_service.get_user_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        user_service.update_last_login(user.id)
        
        access_token = create_access_token(identity={
            'username': user.username, 
            'user_id': user.id,
            'role': user.role
        })
        return jsonify({
            "success": True,
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "full_name": user.full_name
            }
        }), 200

    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    password_hash = generate_password_hash(data['password'])
    data['password'] = password_hash
    
    result = user_service.register_user(data)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "success": True,
        "message": "Access granted",
        "user": current_user
    }), 200