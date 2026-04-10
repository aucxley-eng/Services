from flask import Blueprint, request, jsonify
from app.models import db, Stock, Product, Branch
from app.utils.decorators import require_auth

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/transaction', methods=['POST'])
@require_auth()
def stock_transaction():
    """Record Stock In or Stock Out with detailed validation"""
    data = request.get_json() or {}
    
    # 1. Individual field validation
    required = {
        'product_id': 'Product ID',
        'branch_id': 'Branch ID',
        'quantity': 'Quantity',
        'type': 'Transaction Type (in/out)'
    }
    missing = [label for field, label in required.items() if data.get(field) is None]
    if missing:
        return jsonify({
            "error": "Validation Error",
            "message": f"Missing required data: {', '.join(missing)}"
        }), 400

    product_id = data['product_id']
    branch_id = data['branch_id']
    quantity = data['quantity']
    trans_type = data['type']

    # 2. Database Existence Checks
    product = Product.query.get(product_id)
    if not product:
        return jsonify({
            "error": "Not Found",
            "message": f"Product with ID '{product_id}' does not exist."
        }), 404

    branch = Branch.query.get(branch_id)
    if not branch:
        return jsonify({
            "error": "Not Found",
            "message": f"Branch with ID '{branch_id}' does not exist."
        }), 404

    if quantity <= 0:
        return jsonify({
            "error": "Invalid Input",
            "message": "Quantity must be a positive number."
        }), 400

    # 3. Process Transaction
    stock = Stock.query.filter_by(product_id=product_id, branch_id=branch_id).first()
    
    if not stock:
        # Create record if it doesn't exist
        stock = Stock(product_id=product_id, branch_id=branch_id, quantity=0)
        db.session.add(stock)
        db.session.flush()

    if trans_type == 'in':
        stock.quantity += quantity
    elif trans_type == 'out':
        if stock.quantity < quantity:
            return jsonify({
                "error": "Insufficient Stock",
                "message": f"Cannot remove {quantity} units. Only {stock.quantity} available at branch '{branch.name}'."
            }), 400
        stock.quantity -= quantity
    else:
        return jsonify({
            "error": "Invalid Input",
            "message": "Transaction type must be either 'in' or 'out'."
        }), 400

    # 4. Check Threshold Alerts
    alert_triggered = False
    if stock.quantity <= product.threshold:
        alert_triggered = True

    try:
        db.session.commit()
        return jsonify({
            "message": f"Stock {'added' if trans_type == 'in' else 'removed'} successfully",
            "details": {
                "product": product.name,
                "branch": branch.name,
                "current_quantity": stock.quantity,
                "low_stock_alert": alert_triggered
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "Failed to update stock levels. Please try again."
        }), 500

@inventory_bp.route('/levels', methods=['GET'])
@require_auth()
def get_stock_levels():
    """Get current stock levels with branch info"""
    branch_id = request.args.get('branch_id', type=int)
    
    query = Stock.query
    if branch_id:
        if not Branch.query.get(branch_id):
            return jsonify({"error": "Not Found", "message": "The specified branch ID does not exist."}), 404
        query = query.filter_by(branch_id=branch_id)
    
    stocks = query.all()
    
    output = []
    for s in stocks:
        output.append({
            "product_id": s.product_id,
            "product_name": s.product.name if s.product else "Unknown",
            "branch_name": s.branch.name if s.branch else "Unknown",
            "quantity": s.quantity
        })
        
    return jsonify(output), 200
