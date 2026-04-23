from datetime import datetime
from database import db


class StockTransaction(db.Model):
    __tablename__ = 'stock_transactions'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    stock = db.relationship('Stock', backref='transactions')
    user = db.relationship('User', backref='stock_transactions')
    
    __table_args__ = (
        db.CheckConstraint('type IN (\'in\', \'out\')', name='check_transaction_type'),
        db.CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )