from database import db


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    
    product = db.relationship('Product', back_populates='stock')
    branch = db.relationship('Branch', back_populates='stock')
    
    __table_args__ = (db.UniqueConstraint('product_id', 'branch_id', name='unique_branch_product'),)