from database import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float)
    unit = db.Column(db.String(20))
    expiry_date = db.Column(db.Date)
    threshold = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    image_url = db.Column(db.String(255))
    
    stock = db.relationship('Stock', back_populates='product', lazy='dynamic')
    category = db.relationship('Category', back_populates='products')
    supplier = db.relationship('Supplier', back_populates='products')
    
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "name": self.name,
            "buying_price": self.buying_price,
            "selling_price": self.selling_price,
            "unit": self.unit,
            "threshold": self.threshold,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id,
            "image_url": self.image_url
        }