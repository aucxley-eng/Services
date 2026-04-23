from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.orders.service import OrderService
from app.api_response import APIResponse

orders_bp = Blueprint('orders', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order/sale - staff and above"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager', 'staff']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only staff, managers and admins can process sales",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide: items (array), branch_id"
        )
    
    order_service = OrderService()
    order, error = order_service.create_order(data, user)
    
    if error:
        if "missing" in error.lower() or "item" in error.lower() or "product" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Check your order items")
        if "branch" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Staff must be assigned to a branch")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=order, message="Sale completed successfully!", status_code=201)


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    """Get orders - any authenticated user"""
    branch_id = request.args.get('branch_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    order_service = OrderService()
    orders, error = order_service.get_orders_by_branch(branch_id, limit)
    
    if error:
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data={"orders": orders})


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get single order - any authenticated user"""
    order_service = OrderService()
    order, error = order_service.get_order(order_id)
    
    if error:
        return APIResponse.not_found(message=error, details="Order not found", solution="Check the order ID")
    
    return APIResponse.success(data=order)


@orders_bp.route('/summary/today', methods=['GET'])
@jwt_required()
def get_daily_summary():
    """Get today's sales summary - manager and above"""
    user = get_current_user()
    
    if user.role == 'staff':
        return APIResponse.forbidden(
            message="Access denied",
            details="Only managers and admins can view sales summaries",
            solution="Contact the manager"
        )
    
    branch_id = request.args.get('branch_id', type=int)
    
    order_service = OrderService()
    summary, error = order_service.get_daily_sales_summary(branch_id)
    
    if error:
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=summary)