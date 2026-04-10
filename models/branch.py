from database import db


class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    stores = db.relationship('Stock', backref='branch', lazy=True)