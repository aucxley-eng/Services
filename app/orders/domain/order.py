from datetime import datetime
from database import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subtotal = db.Column(db.Float, default=0)
    discount_percent = db.Column(db.Float, default=5)
    discount_amount = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='completed')
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    branch = db.relationship('Branch', backref='orders')
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    def generate_order_number(self):
        import random
        import string
        prefix = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"ORD-{prefix}-{random_part}"


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', backref='order_items')