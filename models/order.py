from datetime import datetime
from database import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)