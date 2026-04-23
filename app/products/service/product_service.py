from app.products.repo import ProductRepository
from app.categories.domain import CategoryRepository


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()
    
    def get_all_products(self, page=1, per_page=10, search=''):
        pagination = self.product_repo.get_all_paginated(page, per_page, search)
        return {
            'products': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }
    
    def get_product(self, product_id):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None, "Product not found"
        return product.to_dict(), None
    
    def create_product(self, data, current_user):
        required_fields = ['name', 'buying_price']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return None, f"Missing required fields: {', '.join(missing)}"
        
        # Validate category if provided
        if data.get('category_id'):
            category = self.category_repo.get_by_id(data['category_id'])
            if not category:
                return None, "The specified Category ID does not exist."
        
        # Check duplicate name
        if self.product_repo.find_by_name(data['name']):
            return None, f"A product with name '{data['name']}' already exists."
        
        try:
            product = self.product_repo.create(
                name=data['name'],
                buying_price=data['buying_price'],
                selling_price=data.get('selling_price'),
                product_id=data.get('product_id'),
                category_id=data.get('category_id'),
                unit=data.get('unit', 'pcs'),
                threshold=data.get('threshold', 10)
            )
            return product.to_dict(), None
        except Exception as e:
            return None, f"Could not save product: {str(e)}"
    
    def update_product(self, product_id, data, current_user):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None, "Product not found."
        
        # Validate category if provided
        if data.get('category_id'):
            category = self.category_repo.get_by_id(data['category_id'])
            if not category:
                return None, "Category does not exist."
        
        try:
            update_data = {
                'name': data.get('name', product.name),
                'buying_price': data.get('buying_price', product.buying_price),
                'selling_price': data.get('selling_price', product.selling_price),
                'unit': data.get('unit', product.unit),
                'threshold': data.get('threshold', product.threshold),
                'category_id': data.get('category_id', product.category_id)
            }
            product = self.product_repo.update(product, **update_data)
            return product.to_dict(), None
        except Exception as e:
            return None, f"Could not update product: {str(e)}"
    
    def delete_product(self, product_id, current_user):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return None, "Product not found."
        
        try:
            self.product_repo.delete(product)
            return {"message": "Product deleted successfully"}, None
        except Exception as e:
            return None, f"Could not delete product: {str(e)}"