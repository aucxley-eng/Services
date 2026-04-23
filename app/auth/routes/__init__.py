from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.auth.service import AuthService
from app.auth.schema import UserSchema
from app.api_response import APIResponse

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json() or {}
    
    auth_service = AuthService()
    user, access_token, error = auth_service.register(data)
    
    if error:
        if 'already taken' in error.lower() or 'already registered' in error.lower():
            return APIResponse.conflict(error)
        return APIResponse.error(error, "Validation Error", 400)
    
    user_data = user_schema.dump(user)
    
    return APIResponse.success(
        data={"user": user_data, "access_token": access_token},
        message="User registered successfully",
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    auth_service = AuthService()
    user, access_token, error = auth_service.login(email, password)
    
    if error:
        if "no account found" in error.lower():
            return APIResponse.unauthorized(error)
        if "incorrect password" in error.lower():
            return APIResponse.unauthorized(error)
        return APIResponse.error(error, "Validation Error", 400)
    
    user_data = user_schema.dump(user)
    
    return APIResponse.success(
        data={"access_token": access_token, "user": user_data},
        message="Login successful"
    )


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info"""
    user_id = int(get_jwt_identity())
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    user_data = user_schema.dump(user)
    return APIResponse.success(data=user_data)


@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required()
def refresh_token():
    """Generate new JWT token for current user"""
    user_id = int(get_jwt_identity())
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    
    return APIResponse.success(
        data={"access_token": access_token},
        message="Token refreshed successfully"
    )