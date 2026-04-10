from database import db, generate_api_key
from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def find_by_api_key(self, api_key):
        return User.query.filter_by(api_key=api_key).first()
    
    def create_with_api_key(self, **kwargs):
        user = User(
            username=kwargs.get('username'),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            email=kwargs.get('email'),
            role=kwargs.get('role', 'staff'),
            api_key=generate_api_key()
        )
        user.set_password(kwargs.get('password'))
        db.session.add(user)
        db.session.commit()
        return user
    
    def generate_new_api_key(self, user):
        user.api_key = generate_api_key()
        db.session.commit()
        return user