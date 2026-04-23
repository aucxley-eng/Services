from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.categories.service import CategoryService
from app.categories.schema import category_schema, categories_schema
from app.api_response import APIResponse

categories_bp = Blueprint('categories', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@categories_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories - any authenticated user"""
    category_service = CategoryService()
    categories, error = category_service.get_all_categories()
    
    if error:
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data={"categories": categories_schema.dump(categories)})


@categories_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    """Get a single category - any authenticated user"""
    category_service = CategoryService()
    category, error = category_service.get_category(category_id)
    
    if error:
        return APIResponse.not_found(message=error, details="Category not found", solution="Check the category ID")
    
    return APIResponse.success(data=category_schema.dump(category))


@categories_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    """Create category - admin only"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins can create categories",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide category data: name (required), description"
        )
    
    category_service = CategoryService()
    category, error = category_service.create_category(data, user)
    
    if error:
        if "required" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Provide the category name")
        if "already exists" in error.lower():
            return APIResponse.conflict(message=error, details=f"Category '{data.get('name')}' already exists", solution="Use a different category name")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=category_schema.dump(category), message="Category created successfully", status_code=201)


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update category - admin only"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins can update categories",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    category_service = CategoryService()
    category, error = category_service.update_category(category_id, data, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Category ID {category_id} not found", solution="Check the category ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=category_schema.dump(category), message="Category updated successfully")


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete category - admin only"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Cannot delete category",
            details="Only admins can delete categories",
            solution="Contact the administrator"
        )
    
    category_service = CategoryService()
    category, error = category_service.delete_category(category_id, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Category ID {category_id} not found", solution="Check the category ID")
        if "products" in error.lower():
            return APIResponse.error(message=error, error_code="Cannot Delete", status_code=400, details=error, solution="Remove products from this category first")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(message="Category deleted successfully")