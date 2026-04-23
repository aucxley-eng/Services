from app.branches.repo import BranchRepository


class BranchService:
    def __init__(self):
        self.branch_repo = BranchRepository()
    
    def get_all_branches(self):
        branches = self.branch_repo.find_all()
        return [b.to_dict() for b in branches], None
    
    def get_branch(self, branch_id):
        branch = self.branch_repo.get_by_id(branch_id)
        if not branch:
            return None, "Branch not found"
        return branch.to_dict(), None
    
    def create_branch(self, data, current_user):
        name = data.get('name')
        
        if not name:
            return None, "Branch name is required"
        
        if self.branch_repo.find_by_name(name):
            return None, f"Branch '{name}' already exists"
        
        try:
            branch = self.branch_repo.create(
                name=name,
                location=data.get('location'),
                phone=data.get('phone'),
                email=data.get('email'),
                is_active=data.get('is_active', True)
            )
            return branch.to_dict(), None
        except Exception as e:
            return None, f"Could not create branch: {str(e)}"
    
    def update_branch(self, branch_id, data, current_user):
        branch = self.branch_repo.get_by_id(branch_id)
        if not branch:
            return None, "Branch not found"
        
        try:
            if data.get('name'):
                branch.name = data['name']
            if 'location' in data:
                branch.location = data['location']
            if 'phone' in data:
                branch.phone = data['phone']
            if 'email' in data:
                branch.email = data['email']
            if 'is_active' in data:
                branch.is_active = data['is_active']
            
            from database import db
            db.session.commit()
            
            return branch.to_dict(), None
        except Exception as e:
            return None, f"Could not update branch: {str(e)}"
    
    def delete_branch(self, branch_id, current_user):
        branch = self.branch_repo.get_by_id(branch_id)
        if not branch:
            return None, "Branch not found"
        
        try:
            self.branch_repo.delete(branch)
            return {"message": "Branch deleted successfully"}, None
        except Exception as e:
            return None, f"Could not delete branch: {str(e)}"