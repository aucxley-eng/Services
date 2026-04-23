from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff')
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ROLES = ['admin', 'manager', 'staff']
    
    @staticmethod
    def get_roles():
        return User.ROLES
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_staff(self):
        return self.role == 'staff'
    
    def can_delete_employees(self):
        return self.role == 'admin'
    
    def can_manage_branch(self, branch_id):
        if self.role == 'admin':
            return True
        if self.role == 'manager':
            return self.branch_id == branch_id
        return False
    
    def can_delete_branch(self):
        return self.role == 'admin'
    
    def can_delete_any_record(self):
        return self.role == 'admin'
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def get_jwt_identity(self):
        return self.id