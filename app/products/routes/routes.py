from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.products.service import ProductService
from app.products.repo import ProductRepository
from app.api_response import APIResponse

products_bp = Blueprint('products', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@products_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    """Get list of products - any authenticated user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    product_service = ProductService()
    result = product_service.get_all_products(page, per_page, search)
    
    return APIResponse.success(data={
        "products": result['products'],
        "total": result['total'],
        "pages": result['pages'],
        "current_page": result['current_page']
    })


@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get a single product - any authenticated user"""
    product_service = ProductService()
    product, error = product_service.get_product(product_id)
    
    if error:
        return APIResponse.not_found(
            message=error,
            details="Product not found",
            solution="Check the product ID"
        )
    
    return APIResponse.success(data=product)


@products_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    """Create product - admin only"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can create products",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide product data: name (required), buying_price (required)"
        )
    
    product_service = ProductService()
    product, error = product_service.create_product(data, user)
    
    if error:
        if "required" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Provide name and buying_price")
        if "already exists" in error.lower():
            return APIResponse.conflict(message=error, details=f"Product '{data.get('name')}' already exists", solution="Use a different product name")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=product, message="Product created successfully", status_code=201)


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product - admin only"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can update products",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    product_service = ProductService()
    product, error = product_service.update_product(product_id, data, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Product ID {product_id} not found", solution="Check the product ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=product, message="Product updated successfully")


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete product - admin only (manager needs admin approval)"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Admin approval required",
            details=f"Managers need admin approval to delete products",
            solution="Contact the administrator to delete this product"
        )
    
    product_service = ProductService()
    product, error = product_service.delete_product(product_id, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Product ID {product_id} not found", solution="Check the product ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(message="Product deleted successfully")