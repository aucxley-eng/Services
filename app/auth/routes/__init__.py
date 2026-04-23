from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from app.auth.service import AuthService
from app.auth.schema import UserSchema
from app.api_response import APIResponse

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty or not valid JSON",
            solution="Send a valid JSON object with required fields: username, first_name, last_name, email, password"
        )
    
    auth_service = AuthService()
    user, access_token, error = auth_service.register(data)
    
    if error:
        if "required" in error.lower():
            return APIResponse.error(
                message=error,
                error_code="Validation Error",
                status_code=400,
                details=error,
                solution="Provide all required fields: username, first_name, last_name, email, password"
            )
        if "already taken" in error.lower() or "already registered" in error.lower():
            return APIResponse.conflict(
                message=error,
                details=f"Value '{data.get('username' if 'username' in error.lower() else 'email')}' already exists",
                solution="Use a different username or email address"
            )
        if "invalid" in error.lower():
            return APIResponse.error(
                message=error,
                error_code="Validation Error",
                status_code=400,
                details=error,
                solution="Fix the validation error and try again"
            )
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
    
    if not email or not password:
        missing = []
        if not email:
            missing.append("email")
        if not password:
            missing.append("password")
        return APIResponse.error(
            message="Missing credentials",
            error_code="Validation Error",
            status_code=400,
            details=f"Missing required fields: {', '.join(missing)}",
            solution="Provide both email and password in the request body"
        )
    
    auth_service = AuthService()
    user, access_token, error = auth_service.login(email, password)
    
    if error:
        if "no account found" in error.lower():
            return APIResponse.unauthorized(
                message=error,
                details="No user account exists with this email address",
                solution="Check the email address or register a new account"
            )
        if "incorrect password" in error.lower():
            return APIResponse.unauthorized(
                message=error,
                details="The password does not match our records",
                solution="Check your password or use 'forgot password' to reset"
            )
        return APIResponse.error(error, "Validation Error", 400)
    
    user_data = user_schema.dump(user)
    
    return APIResponse.success(
        data={"access_token": access_token, "user": user_data},
        message="Login successful"
    )


@auth_bp.errorhandler(NoAuthorizationError)
def handle_no_auth(e):
    return APIResponse.unauthorized(
        message="Authorization required",
        details="No JWT token was provided",
        solution="Include a valid JWT token in the Authorization header"
    )


@auth_bp.errorhandler(InvalidHeaderError)
def handle_invalid_header(e):
    return APIResponse.unauthorized(
        message="Invalid authorization header",
        details="The authorization header is malformed",
        solution="Use format: 'Authorization: Bearer <token>'"
    )


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info"""
    user_id = int(get_jwt_identity())
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.not_found(
            message="User not found",
            details="User account no longer exists",
            solution="This account may have been deleted"
        )
    
    user_data = user_schema.dump(user)
    return APIResponse.success(data=user_data)


@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required()
def refresh_token():
    """Generate new JWT token for current user"""
    user_id = int(get_jwt_identity())
    auth_service = AuthService()
    user = auth_service.get_user_by_id(user_id)
    
    if not user:
        return APIResponse.not_found(
            message="User not found",
            details="Cannot refresh token - user no longer exists",
            solution="Log in again with credentials"
        )
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    
    return APIResponse.success(
        data={"access_token": access_token},
        message="Token refreshed successfully"
    )