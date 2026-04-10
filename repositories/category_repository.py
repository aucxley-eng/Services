from database import db
from models.category import Category
from repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Category)
    
    def find_by_name(self, name):
        return Category.query.filter_by(name=name).first()