from database import db
from app.orders.domain import Order, OrderItem
from app.inventory.service import InventoryService
import random
import string


class OrderService:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.STAFF_DISCOUNT = 5.0
    
    def generate_order_number(self):
        prefix = 'ORD'
        timestamp = db.func.now()
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}-{random_part}"
    
    def calculate_totals(self, items):
        subtotal = sum(item['total_price'] for item in items)
        discount_amount = subtotal * (self.STAFF_DISCOUNT / 100)
        total = subtotal - discount_amount
        return subtotal, discount_amount, total
    
    def create_order(self, data, current_user):
        required = ['items', 'branch_id']
        missing = [field for field in required if not data.get(field)]
        if missing:
            return None, f"Missing required fields: {', '.join(missing)}"
        
        if not data['items'] or len(data['items']) == 0:
            return None, "Order must have at least one item"
        
        # Verify branch exists
        from app.branches.repo import BranchRepository
        branch_repo = BranchRepository()
        branch = branch_repo.get_by_id(data['branch_id'])
        if not branch:
            return None, f"Branch with ID '{data['branch_id']}' does not exist"
        
        order = Order(
            order_number=self.generate_order_number(),
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            branch_id=data['branch_id'],
            user_id=current_user.id,
            discount_percent=self.STAFF_DISCOUNT,
            payment_method=data.get('payment_method', 'cash'),
            notes=data.get('notes', ''),
            status='completed'
        )
        db.session.add(order)
        db.session.flush()
        
        subtotal = 0
        order_items = []
        
        for item_data in data['items']:
            if not item_data.get('product_id') or not item_data.get('quantity'):
                db.session.rollback()
                return None, f"Each item needs product_id and quantity"
            
            quantity = item_data['quantity']
            if quantity <= 0:
                db.session.rollback()
                return None, "Quantity must be greater than 0"
            
            from app.products.repo import ProductRepository
            product_repo = ProductRepository()
            product = product_repo.get_by_id(item_data['product_id'])
            
            if not product:
                db.session.rollback()
                return None, f"Product with ID '{item_data['product_id']}' not found"
            
            unit_price = product.selling_price if product.selling_price else product.buying_price
            total_price = unit_price * quantity
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            db.session.add(order_item)
            order_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            })
            
            stock_result, stock_error = self.inventory_service.stock_transaction({
                'product_id': product.id,
                'branch_id': data['branch_id'],
                'quantity': quantity,
                'type': 'out',
                'reason': f'Sale - Order {order.order_number}'
            }, current_user)
            
            if stock_error:
                db.session.rollback()
                return None, f"Failed to reduce stock for {product.name}: {stock_error}"
            
            subtotal += total_price
        
        order.subtotal = subtotal
        order.discount_amount = subtotal * (self.STAFF_DISCOUNT / 100)
        order.total = subtotal - order.discount_amount
        
        db.session.commit()
        
        return {
            'order_id': order.id,
            'order_number': order.order_number,
            'customer_name': order.customer_name,
            'branch': order.branch.name if order.branch else 'Unknown',
            'items': order_items,
            'subtotal': subtotal,
            'discount_percent': self.STAFF_DISCOUNT,
            'discount_amount': order.discount_amount,
            'total': order.total,
            'payment_method': order.payment_method,
            'processed_by': f"{current_user.first_name} {current_user.last_name}",
            'created_at': order.created_at.isoformat() if order.created_at else None
        }, None
    
    def get_order(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return None, f"Order with ID '{order_id}' not found"
        
        items = []
        for item in order.items:
            items.append({
                'product_id': item.product_id,
                'product_name': item.product.name if item.product else 'Unknown',
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.total_price
            })
        
        return {
            'order_id': order.id,
            'order_number': order.order_number,
            'customer_name': order.customer_name,
            'customer_phone': order.customer_phone,
            'branch': order.branch.name if order.branch else 'Unknown',
            'items': items,
            'subtotal': order.subtotal,
            'discount_percent': order.discount_percent,
            'discount_amount': order.discount_amount,
            'total': order.total,
            'status': order.status,
            'payment_method': order.payment_method,
            'processed_by': f"{order.user.first_name} {order.user.last_name}" if order.user else 'Unknown',
            'created_at': order.created_at.isoformat() if order.created_at else None
        }, None
    
    def get_orders_by_branch(self, branch_id=None, limit=50):
        query = Order.query
        
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        
        orders = query.order_by(Order.created_at.desc()).limit(limit).all()
        
        result = []
        for order in orders:
            result.append({
                'order_id': order.id,
                'order_number': order.order_number,
                'customer_name': order.customer_name,
                'total': order.total,
                'item_count': len(order.items),
                'branch': order.branch.name if order.branch else 'Unknown',
                'processed_by': f"{order.user.first_name} {order.user.last_name}" if order.user else 'Unknown',
                'created_at': order.created_at.isoformat() if order.created_at else None
            })
        
        return result, None
    
    def get_daily_sales_summary(self, branch_id=None):
        from datetime import datetime, timedelta
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        query = Order.query.filter(
            db.func.date(Order.created_at) >= today,
            db.func.date(Order.created_at) < tomorrow
        )
        
        if branch_id:
            query = query.filter_by(branch_id=branch_id)
        
        orders = query.all()
        
        total_sales = len(orders)
        total_revenue = sum(order.total for order in orders)
        total_discount = sum(order.discount_amount for order in orders)
        total_subtotal = sum(order.subtotal for order in orders)
        
        return {
            'date': today.isoformat(),
            'total_orders': total_sales,
            'total_revenue': total_revenue,
            'total_discount_given': total_discount,
            'subtotal_before_discount': total_subtotal,
            'average_order_value': total_revenue / total_sales if total_sales > 0 else 0
        }, None