from database import db
from app.branches.domain import Branch


class BranchRepository:
    def __init__(self):
        self.model = Branch
    
    def get_by_id(self, id):
        return Branch.query.get(id)
    
    def find_by_name(self, name):
        return Branch.query.filter_by(name=name).first()
    
    def find_all(self):
        return Branch.query.all()
    
    def create(self, **kwargs):
        branch = Branch(**kwargs)
        db.session.add(branch)
        db.session.commit()
        return branch
    
    def update(self, branch, **kwargs):
        for key, value in kwargs.items():
            if hasattr(branch, key):
                setattr(branch, key, value)
        db.session.commit()
        return branch
    
    def delete(self, branch):
        db.session.delete(branch)
        db.session.commit()