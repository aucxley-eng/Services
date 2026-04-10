from repositories import CategoryRepository


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()
    
    def get_all_categories(self):
        categories = self.category_repo.get_all()
        return [{"id": c.id, "name": c.name} for c in categories], None
    
    def create_category(self, data, current_user):
        name = data.get('name')
        
        if not name:
            return None, "The category 'name' is required."
        
        if self.category_repo.find_by_name(name):
            return None, f"A category with the name '{name}' already exists."
        
        try:
            category = self.category_repo.create(name=name)
            return {"id": category.id, "name": category.name}, None
        except Exception:
            return None, "Could not create category."