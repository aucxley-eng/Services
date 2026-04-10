from flask import Blueprint, request, jsonify
from app.models import db, Product, Category
from app.schemas import ProductSchema
from app.utils.decorators import require_auth, admin_required

products_bp = Blueprint('products', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@products_bp.route('/', methods=['GET'])
@require_auth()
def get_products():
    """Get list of products with Pagination and Filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    pagination = query.order_by(Product.id).paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    return jsonify({
        "products": products_schema.dump(products),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }), 200

@products_bp.route('/', methods=['POST'])
@admin_required()
def add_product():
    """Create a new product with validation"""
    data = request.get_json() or {}
    
    # Validation
    required = {'name': 'Name', 'buying_price': 'Buying Price'}
    missing = [label for field, label in required.items() if data.get(field) is None]
    if missing:
        return jsonify({"error": "Validation Error", "message": f"Missing fields: {', '.join(missing)}"}), 400

    if data.get('category_id') and not Category.query.get(data['category_id']):
        return jsonify({"error": "Not Found", "message": "The specified Category ID does not exist."}), 404

    try:
        new_product = Product(
            name=data['name'],
            buying_price=data['buying_price'],
            selling_price=data.get('selling_price'),
            product_id=data.get('product_id'),
            category_id=data.get('category_id'),
            unit=data.get('unit', 'pcs'),
            threshold=data.get('threshold', 10)
        )

        db.session.add(new_product)
        db.session.commit()
        return jsonify(product_schema.dump(new_product)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": "Could not save product."}), 500

@products_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_product(id):
    """Update a product with specific feedback"""
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Not Found", "message": "Product not found."}), 404
        
    data = request.get_json() or {}
    
    # Update fields if provided
    product.name = data.get('name', product.name)
    product.buying_price = data.get('buying_price', product.buying_price)
    product.selling_price = data.get('selling_price', product.selling_price)
    product.unit = data.get('unit', product.unit)
    product.threshold = data.get('threshold', product.threshold)
    
    if data.get('category_id'):
        if not Category.query.get(data['category_id']):
            return jsonify({"error": "Not Found", "message": "Category does not exist."}), 404
        product.category_id = data['category_id']

    try:
        db.session.commit()
        return jsonify(product_schema.dump(product)), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": "Could not update product."}), 500

@products_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_product(id):
    """Delete a product"""
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Not Found", "message": "Product not found."}), 404
        
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product '{product.name}' deleted successfully"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": "Could not delete product."}), 500
