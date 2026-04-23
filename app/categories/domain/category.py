from database import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))


class CategoryRepository:
    def __init__(self):
        self.model = Category
    
    def get_by_id(self, id):
        return Category.query.get(id)
    
    def find_by_name(self, name):
        return Category.query.filter_by(name=name).first()
    
    def find_all(self):
        return Category.query.all()
    
    def create(self, **kwargs):
        category = Category(**kwargs)
        db.session.add(category)
        db.session.commit()
        return category