from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inventory.service import InventoryService
from app.api_response import APIResponse

inventory_bp = Blueprint('inventory', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@inventory_bp.route('/transaction', methods=['POST'])
@jwt_required()
def stock_transaction():
    """Record stock in/out - admin or manager"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can record stock transactions",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide: product_id, branch_id, quantity, type (in/out)"
        )
    
    inventory_service = InventoryService()
    result, error = inventory_service.stock_transaction(data, user)
    
    if error:
        if "does not exist" in error.lower():
            return APIResponse.not_found(error)
        if "quantity" in error.lower() or "type" in error.lower():
            return APIResponse.error(error, "Invalid Input", 400)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=result, message="Stock transaction recorded", status_code=201)


@inventory_bp.route('/levels', methods=['GET'])
@jwt_required()
def get_stock_levels():
    """Get stock levels - any authenticated user"""
    branch_id = request.args.get('branch_id', type=int)
    
    inventory_service = InventoryService()
    result, error = inventory_service.get_stock_levels(branch_id)
    
    if error:
        return APIResponse.not_found(message=error, details="Branch not found", solution="Check the branch ID")
    
    return APIResponse.success(data={"stock_levels": result})


@inventory_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get products below threshold - admin or manager"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can view low stock alerts",
            solution="Contact the administrator"
        )
    
    branch_id = request.args.get('branch_id', type=int)
    
    inventory_service = InventoryService()
    result, error = inventory_service.get_low_stock(branch_id)
    
    if error:
        return APIResponse.not_found(message=error, details="Branch not found", solution="Check the branch ID")
    
    return APIResponse.success(data={"low_stock_products": result})