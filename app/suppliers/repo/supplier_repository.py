from database import db
from app.suppliers.domain import Supplier
from app.auth.repo.base_repository import BaseRepository


class SupplierRepository(BaseRepository):
    def __init__(self):
        super().__init__(Supplier)
    
    def find_by_name(self, name):
        return Supplier.query.filter_by(name=name).first()
    
    def find_all(self):
        return Supplier.query.all()