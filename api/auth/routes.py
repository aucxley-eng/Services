from flask import Blueprint, request
from services import AuthService
from schemas import UserSchema
from middleware import require_auth
from responses import APIResponse

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json() or {}
    
    auth_service = AuthService()
    user, error = auth_service.register(data)
    
    if error:
        if 'already taken' in error.lower() or 'already registered' in error.lower():
            return APIResponse.conflict(error)
        return APIResponse.error(error, "Validation Error", 400)
    
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    
    return APIResponse.success(
        data={"user": user_data},
        message="User registered successfully",
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get API key"""
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    auth_service = AuthService()
    user, error = auth_service.login(email, password)
    
    if error:
        if "no account found" in error.lower():
            return APIResponse.unauthorized(error)
        if "incorrect password" in error.lower():
            return APIResponse.unauthorized(error)
        return APIResponse.error(error, "Validation Error", 400)
    
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    
    return APIResponse.success(
        data={"api_key": user.api_key, "user": user_data},
        message="Login successful"
    )


@auth_bp.route('/me', methods=['GET'])
@require_auth()
def get_current_user():
    """Get current authenticated user info"""
    user = request.current_user
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    return APIResponse.success(data=user_data)


@auth_bp.route('/refresh-key', methods=['POST'])
@require_auth()
def refresh_api_key():
    """Generate new API key for current user"""
    auth_service = AuthService()
    user = auth_service.refresh_api_key(request.current_user)
    
    return APIResponse.success(
        data={"api_key": user.api_key},
        message="API key refreshed successfully"
    )