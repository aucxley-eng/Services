from flask import Blueprint, request
from services import InventoryService
from middleware import require_auth
from responses import APIResponse

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/transaction', methods=['POST'])
@require_auth()
def stock_transaction():
    """Record stock in or out"""
    data = request.get_json() or {}
    
    inventory_service = InventoryService()
    result, error = inventory_service.stock_transaction(data, request.current_user)
    
    if error:
        if "does not exist" in error.lower():
            return APIResponse.not_found(error)
        if "quantity" in error.lower() or "type" in error.lower():
            return APIResponse.error(error, "Invalid Input", 400)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=result, status_code=201)


@inventory_bp.route('/levels', methods=['GET'])
@require_auth()
def get_stock_levels():
    """Get stock levels by branch"""
    branch_id = request.args.get('branch_id', type=int)
    
    inventory_service = InventoryService()
    result, error = inventory_service.get_stock_levels(branch_id)
    
    if error:
        return APIResponse.not_found(error)
    
    return APIResponse.success(data=result)