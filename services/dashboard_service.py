from database import db
from sqlalchemy import func
from models import Product, Stock


class DashboardService:
    def get_stats(self):
        total_products = Product.query.count()
        
        total_stock = db.session.query(func.sum(Stock.quantity)).scalar() or 0
        
        low_stock_items = db.session.query(Stock).join(Product).filter(
            Stock.quantity <= Product.threshold
        ).count()
        
        total_value = db.session.query(
            func.sum(Product.buying_price * Stock.quantity)
        ).join(Stock).scalar() or 0
        
        return {
            "total_products": total_products,
            "total_stock_in_hand": total_stock,
            "low_stock_alerts": low_stock_items,
            "inventory_value": round(total_value, 2)
        }, None