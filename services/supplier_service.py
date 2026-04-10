from repositories import SupplierRepository


class SupplierService:
    def __init__(self):
        self.supplier_repo = SupplierRepository()
    
    def get_all_suppliers(self):
        suppliers = self.supplier_repo.get_all()
        output = []
        for s in suppliers:
            output.append({
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "phone": s.phone,
                "taking_returns": s.taking_returns
            })
        return output, None
    
    def create_supplier(self, data, current_user):
        name = data.get('name')
        
        if not name:
            return None, "The supplier 'name' is required."
        
        if self.supplier_repo.find_by_name(name):
            return None, f"A supplier with the name '{name}' already exists."
        
        try:
            supplier = self.supplier_repo.create(
                name=name,
                email=data.get('email'),
                phone=data.get('phone'),
                taking_returns=data.get('taking_returns', True)
            )
            return {"message": "Supplier added successfully", "id": supplier.id}, None
        except Exception:
            return None, "Could not save supplier information."