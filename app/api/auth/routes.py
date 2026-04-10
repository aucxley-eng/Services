import re
from flask import Blueprint, request, jsonify
from app.models import db, User, generate_api_key
from app.schemas import UserSchema
from app.utils.decorators import require_auth

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


def validate_email(email):
    """Simple regex for email validation"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with strict validation and API key generation"""
    data = request.get_json() or {}
    
    required_fields = {
        'username': 'Username',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email Address',
        'password': 'Password'
    }
    
    missing = [label for field, label in required_fields.items() if not data.get(field)]
    if missing:
        return jsonify({
            "error": "Validation Error",
            "message": f"The following fields are required: {', '.join(missing)}"
        }), 400

    if not validate_email(data['email']):
        return jsonify({
            "error": "Invalid Input",
            "message": "The email format is invalid. Please include an '@' and a domain (e.g., user@example.com)."
        }), 400

    if len(data['password']) < 6:
        return jsonify({
            "error": "Invalid Input",
            "message": "Password is too weak. It must be at least 6 characters long."
        }), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            "error": "Conflict",
            "message": f"The username '{data['username']}' is already taken. Please choose another."
        }), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            "error": "Conflict",
            "message": f"The email '{data['email']}' is already registered. Try logging in instead."
        }), 409

    try:
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role=data.get('role', 'staff'),
            api_key=generate_api_key()
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        user_data = user_schema.dump(new_user)
        user_data['api_key'] = new_user.api_key
        
        return jsonify({
            "message": "User registered successfully",
            "user": user_data
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "An error occurred while saving the user. Please try again later."
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return API key"""
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "error": "Missing Credentials",
            "message": "Both email and password are required to login."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Unauthorized",
            "message": "No account found with this email address."
        }), 401

    if not user.check_password(password):
        return jsonify({
            "error": "Unauthorized",
            "message": "Incorrect password. Please try again."
        }), 401

    if not user.api_key:
        user.api_key = generate_api_key()
        db.session.commit()

    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    
    return jsonify({
        "message": "Login successful",
        "api_key": user.api_key,
        "user": user_data
    }), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth()
def get_current_user():
    """Get current authenticated user info"""
    user = request.current_user
    user_data = user_schema.dump(user)
    user_data['api_key'] = user.api_key
    return jsonify(user_data), 200


@auth_bp.route('/refresh-key', methods=['POST'])
@require_auth()
def refresh_api_key():
    """Generate a new API key for the current user"""
    user = request.current_user
    user.api_key = generate_api_key()
    db.session.commit()
    
    return jsonify({
        "message": "API key refreshed successfully",
        "api_key": user.api_key
    }), 200