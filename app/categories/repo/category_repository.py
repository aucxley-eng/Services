from database import db
from app.categories.domain import Category


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
    
    def update(self, category, **kwargs):
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        db.session.commit()
        return category
    
    def delete(self, category):
        db.session.delete(category)
        db.session.commit()