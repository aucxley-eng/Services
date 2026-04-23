from database import db
from app.products.domain import Product
from app.branches.domain import Branch
from app.inventory.domain import Stock
from app.inventory.repo import StockRepository
from app.branches.repo import BranchRepository
from app.products.repo import ProductRepository


class InventoryService:
    def __init__(self):
        self.stock_repo = StockRepository()
        self.branch_repo = BranchRepository()
        self.product_repo = ProductRepository()
    
    def stock_transaction(self, data, current_user):
        required = ['product_id', 'branch_id', 'quantity', 'type']
        missing = [field for field in required if not data.get(field)]
        if missing:
            return None, f"Missing required data: {', '.join(missing)}"
        
        product = self.product_repo.get_by_id(data['product_id'])
        if not product:
            return None, f"Product with ID '{data['product_id']}' does not exist."
        
        branch = self.branch_repo.get_by_id(data['branch_id'])
        if not branch:
            return None, f"Branch with ID '{data['branch_id']}' does not exist."
        
        quantity = data['quantity']
        if quantity <= 0:
            return None, "Quantity must be a positive number."
        
        trans_type = data['type']
        if trans_type not in ['in', 'out']:
            return None, "Transaction type must be either 'in' or 'out'."
        
        stock = self.stock_repo.find_by_product_and_branch(data['product_id'], data['branch_id'])
        
        if not stock:
            stock = self.stock_repo.create(
                product_id=data['product_id'],
                branch_id=data['branch_id'],
                quantity=0
            )
        
        if trans_type == 'in':
            stock.quantity += quantity
        elif trans_type == 'out':
            if stock.quantity < quantity:
                return None, f"Cannot remove {quantity} units. Only {stock.quantity} available."
            stock.quantity -= quantity
        
        db.session.commit()
        
        alert_triggered = stock.quantity <= product.threshold
        
        return {
            'message': f"Stock {'added' if trans_type == 'in' else 'removed'} successfully",
            'details': {
                'product': product.name,
                'branch': branch.name,
                'current_quantity': stock.quantity,
                'low_stock_alert': alert_triggered
            }
        }, None
    
    def get_stock_levels(self, branch_id=None):
        if branch_id:
            branch = self.branch_repo.get_by_id(branch_id)
            if not branch:
                return None, "The specified branch ID does not exist."
            stocks = self.stock_repo.get_by_branch(branch_id)
        else:
            stocks = self.stock_repo.get_all()
        
        output = []
        for s in stocks:
            output.append({
                'product_id': s.product_id,
                'product_name': s.product.name if s.product else "Unknown",
                'branch_name': s.branch.name if s.branch else "Unknown",
                'quantity': s.quantity
            })
        
        return output, None
    
    def get_low_stock(self, branch_id=None):
        if branch_id:
            branch = self.branch_repo.get_by_id(branch_id)
            if not branch:
                return None, "The specified branch ID does not exist."
            stocks = self.stock_repo.get_by_branch(branch_id)
        else:
            stocks = self.stock_repo.get_all()
        
        low_stock = []
        for s in stocks:
            if s.product and s.quantity <= s.product.threshold:
                low_stock.append({
                    'product_id': s.product_id,
                    'product_name': s.product.name,
                    'branch_id': s.branch_id,
                    'branch_name': s.branch.name if s.branch else "Unknown",
                    'current_quantity': s.quantity,
                    'threshold': s.product.threshold,
                    'severity': 'critical' if s.quantity == 0 else 'warning'
                })
        
        return low_stock, None