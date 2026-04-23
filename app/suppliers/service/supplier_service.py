from app.suppliers.repo import SupplierRepository


class SupplierService:
    def __init__(self):
        self.supplier_repo = SupplierRepository()
    
    def get_all_suppliers(self):
        suppliers = self.supplier_repo.find_all()
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
    
    def get_supplier(self, supplier_id):
        supplier = self.supplier_repo.get_by_id(supplier_id)
        if not supplier:
            return None, "Supplier not found"
        return {
            "id": supplier.id,
            "name": supplier.name,
            "email": supplier.email,
            "phone": supplier.phone,
            "taking_returns": supplier.taking_returns
        }, None
    
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
        except Exception as e:
            return None, f"Could not save supplier information: {str(e)}"
    
    def update_supplier(self, supplier_id, data, current_user):
        supplier = self.supplier_repo.get_by_id(supplier_id)
        if not supplier:
            return None, "Supplier not found."
        
        try:
            if data.get('name'):
                supplier.name = data['name']
            if 'email' in data:
                supplier.email = data['email']
            if 'phone' in data:
                supplier.phone = data['phone']
            if 'taking_returns' in data:
                supplier.taking_returns = data['taking_returns']
            
            from database import db
            db.session.commit()
            
            return {
                "id": supplier.id,
                "name": supplier.name,
                "email": supplier.email,
                "phone": supplier.phone,
                "taking_returns": supplier.taking_returns
            }, None
        except Exception as e:
            return None, f"Could not update supplier: {str(e)}"
    
    def delete_supplier(self, supplier_id, current_user):
        supplier = self.supplier_repo.get_by_id(supplier_id)
        if not supplier:
            return None, "Supplier not found."
        
        try:
            from database import db
            db.session.delete(supplier)
            db.session.commit()
            return {"message": "Supplier deleted successfully"}, None
        except Exception as e:
            return None, f"Could not delete supplier: {str(e)}"