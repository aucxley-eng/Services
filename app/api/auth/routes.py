import re
from flask import Blueprint, request, jsonify
from app.models import db, User
from app.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

def validate_email(email):
    """Simple regex for email validation"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with strict validation"""
    data = request.get_json() or {}
    
    # 1. Check for missing fields individually
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

    # 2. Validate Email Format
    if not validate_email(data['email']):
        return jsonify({
            "error": "Invalid Input",
            "message": "The email format is invalid. Please include an '@' and a domain (e.g., user@example.com)."
        }), 400

    # 3. Check Password Strength (Example: Min 6 chars)
    if len(data['password']) < 6:
        return jsonify({
            "error": "Invalid Input",
            "message": "Password is too weak. It must be at least 6 characters long."
        }), 400

    # 4. Specific Uniqueness Checks
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

    # 5. Create User
    try:
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role='staff'
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(new_user)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "An error occurred while saving the user. Please try again later."
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user with clear feedback"""
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

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user_schema.dump(user)
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user info"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user: 
        return jsonify({"error": "Not Found", "message": "User session is invalid."}), 404
    return jsonify(user_schema.dump(user)), 200
