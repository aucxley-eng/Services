from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff') # 'admin', 'manager', 'staff'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200)) # e.g., "Singanallur, Coimbatore"
    phone = db.Column(db.String(20))
    stores = db.relationship('Stock', backref='branch', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True) # Barcode or SKU
    name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float) # Added for profit calculation
    unit = db.Column(db.String(20)) # "kg", "pcs"
    expiry_date = db.Column(db.Date)
    threshold = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    image_url = db.Column(db.String(255))
    
    # Relationship to Stock
    stocks = db.relationship('Stock', backref='product', lazy=True)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    taking_returns = db.Column(db.Boolean, default=True)

# Critical: Multi-branch stock tracking
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    
    __table_args__ = (db.UniqueConstraint('product_id', 'branch_id', name='unique_branch_product'),)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending') # Confirmed, Delayed, Returned
    order_date = db.Column(db.DateTime, default=datetime.utcnow)