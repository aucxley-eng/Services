from flask import Blueprint, request
from services import ProductService
from schemas import ProductSchema
from middleware import require_auth, admin_required
from responses import APIResponse

products_bp = Blueprint('products', __name__)
product_schema = ProductSchema()


@products_bp.route('/', methods=['GET'])
@require_auth()
def get_products():
    """Get list of products with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    product_service = ProductService()
    result = product_service.get_all_products(page, per_page, search)
    
    return APIResponse.success(data={
        "products": product_schema.dump(result['products'], many=True),
        "total": result['total'],
        "pages": result['pages'],
        "current_page": result['current_page']
    })


@products_bp.route('/', methods=['POST'])
@admin_required()
def add_product():
    """Create a new product"""
    data = request.get_json() or {}
    
    product_service = ProductService()
    product, error = product_service.create_product(data, request.current_user)
    
    if error:
        return APIResponse.error(error, "Validation Error", 400)
    
    return APIResponse.success(
        data=product_schema.dump(product),
        message="Product created successfully",
        status_code=201
    )


@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required()
def update_product(product_id):
    """Update a product"""
    data = request.get_json() or {}
    
    product_service = ProductService()
    product, error = product_service.update_product(product_id, data, request.current_user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(error)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(
        data=product_schema.dump(product),
        message="Product updated successfully"
    )


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required()
def delete_product(product_id):
    """Delete a product"""
    product_service = ProductService()
    product, error = product_service.delete_product(product_id, request.current_user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(error)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(
        message=f"Product '{product.name}' deleted successfully"
    )