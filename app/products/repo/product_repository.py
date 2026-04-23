from database import db
from app.products.domain import Product
from app.auth.repo.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)
    
    def search_by_name(self, name):
        return Product.query.filter(Product.name.ilike(f'%{name}%')).all()
    
    def find_by_product_id(self, product_id):
        return Product.query.filter_by(product_id=product_id).first()
    
    def find_by_name(self, name):
        return Product.query.filter_by(name=name).first()
    
    def paginate(self, query, page, per_page):
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_all_paginated(self, page=1, per_page=10, search=''):
        query = Product.query
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        query = query.order_by(Product.id)
        return query.paginate(page=page, per_page=per_page, error_out=False)