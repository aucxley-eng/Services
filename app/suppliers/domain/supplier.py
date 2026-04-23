from database import db


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    taking_returns = db.Column(db.Boolean, default=True)
    
    products = db.relationship('Product', back_populates='supplier', lazy='dynamic')