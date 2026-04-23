from app.categories.repo import CategoryRepository


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()
    
    def get_all_categories(self):
        categories = self.category_repo.find_all()
        return categories, None
    
    def get_category(self, category_id):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            return None, f"Category with ID '{category_id}' not found"
        return category, None
    
    def create_category(self, data, user):
        if not data.get('name'):
            return None, "Category name is required"
        
        existing = self.category_repo.find_by_name(data['name'])
        if existing:
            return None, f"Category '{data['name']}' already exists"
        
        category = self.category_repo.create(
            name=data['name'],
            description=data.get('description', ''),
            is_active=True
        )
        return category, None
    
    def update_category(self, category_id, data, user):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            return None, f"Category with ID '{category_id}' not found"
        
        if data.get('name') and data['name'] != category.name:
            existing = self.category_repo.find_by_name(data['name'])
            if existing:
                return None, f"Category '{data['name']}' already exists"
        
        category = self.category_repo.update(category, **data)
        return category, None
    
    def delete_category(self, category_id, user):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            return None, f"Category with ID '{category_id}' not found"
        
        if category.products.count() > 0:
            return None, f"Cannot delete category with existing products. Remove products first."
        
        self.category_repo.delete(category)
        return category, None