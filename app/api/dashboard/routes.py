from flask import Blueprint, jsonify
from sqlalchemy import func
from app.models import db, Product, Stock
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Get Dashboard Statistics (Widgets)
    ---
    tags:
      - Dashboard
    security:
      - Bearer: []
    responses:
      200:
        description: Dashboard metrics
    """
    # 1. Total Products
    total_products = Product.query.count()
    
    # 2. Total Stock in Hand (Sum of all stock across all branches)
    total_stock = db.session.query(func.sum(Stock.quantity)).scalar() or 0
    
    # 3. Low Stock Items (Count items below threshold)
    # We use a join to compare stock.quantity with product.threshold
    low_stock_items = db.session.query(Stock).join(Product).filter(
        Stock.quantity <= Product.threshold
    ).count()

    # 4. Total Inventory Value (Sum of Buying Price * Quantity)
    # Note: This is a rough calculation. In production, you'd need Average Cost.
    total_value = db.session.query(
        func.sum(Product.buying_price * Stock.quantity)
    ).join(Stock).scalar() or 0

    return jsonify({
        "total_products": total_products,
        "total_stock_in_hand": total_stock,
        "low_stock_alerts": low_stock_items,
        "inventory_value": round(total_value, 2)
    }), 200