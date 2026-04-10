from flask import Blueprint, request
from services import CategoryService
from middleware import require_auth
from responses import APIResponse

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/', methods=['GET'])
@require_auth()
def get_categories():
    """Get all categories"""
    category_service = CategoryService()
    categories, error = category_service.get_all_categories()
    
    return APIResponse.success(data=categories)


@categories_bp.route('/', methods=['POST'])
@require_auth()
def add_category():
    """Create a new category"""
    data = request.get_json() or {}
    
    category_service = CategoryService()
    category, error = category_service.create_category(data, request.current_user)
    
    if error:
        if "already exists" in error.lower():
            return APIResponse.conflict(error)
        if "required" in error.lower():
            return APIResponse.error(error, "Validation Error", 400)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=category, status_code=201)