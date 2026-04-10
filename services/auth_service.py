import re
from database import db
from models import User
from repositories import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)
    
    def validate_registration_data(self, data):
        errors = []
        
        required_fields = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'password': 'Password'
        }
        
        for field, label in required_fields.items():
            if not data.get(field):
                errors.append(label)
        
        if errors:
            return False, f"The following fields are required: {', '.join(errors)}"
        
        if not self.validate_email(data.get('email', '')):
            return False, "The email format is invalid."
        
        if len(data.get('password', '')) < 6:
            return False, "Password must be at least 6 characters long."
        
        return True, None
    
    def register(self, data):
        is_valid, error = self.validate_registration_data(data)
        if not is_valid:
            return None, error
        
        if self.user_repo.find_by_username(data['username']):
            return None, f"The username '{data['username']}' is already taken."
        
        if self.user_repo.find_by_email(data['email']):
            return None, f"The email '{data['email']}' is already registered."
        
        try:
            user = self.user_repo.create_with_api_key(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'staff')
            )
            return user, None
        except Exception as e:
            return None, "An error occurred while saving the user."
    
    def login(self, email, password):
        if not email or not password:
            return None, "Both email and password are required."
        
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return None, "No account found with this email address."
        
        if not user.check_password(password):
            return None, "Incorrect password."
        
        if not user.api_key:
            user = self.user_repo.generate_new_api_key(user)
        
        return user, None
    
    def get_user_by_api_key(self, api_key):
        return self.user_repo.find_by_api_key(api_key)
    
    def refresh_api_key(self, user):
        return self.user_repo.generate_new_api_key(user)