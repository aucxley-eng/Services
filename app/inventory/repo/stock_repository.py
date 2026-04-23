from database import db
from app.inventory.domain import Stock
from app.auth.repo.base_repository import BaseRepository


class StockRepository(BaseRepository):
    def __init__(self):
        super().__init__(Stock)
    
    def find_by_product_and_branch(self, product_id, branch_id):
        return Stock.query.filter_by(product_id=product_id, branch_id=branch_id).first()
    
    def get_by_branch(self, branch_id):
        return Stock.query.filter_by(branch_id=branch_id).all()
    
    def get_all_with_product_info(self):
        return Stock.query.all()