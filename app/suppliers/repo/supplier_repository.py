from database import db
from models.supplier import Supplier
from repositories.base_repository import BaseRepository


class SupplierRepository(BaseRepository):
    def __init__(self):
        super().__init__(Supplier)
    
    def find_by_name(self, name):
        return Supplier.query.filter_by(name=name).first()