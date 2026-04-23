from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.suppliers.service import SupplierService
from app.api_response import APIResponse

suppliers_bp = Blueprint('suppliers', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@suppliers_bp.route('/', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all suppliers - any authenticated user"""
    supplier_service = SupplierService()
    suppliers, error = supplier_service.get_all_suppliers()
    
    if error:
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data={"suppliers": suppliers})


@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    """Get a single supplier - any authenticated user"""
    supplier_service = SupplierService()
    supplier, error = supplier_service.get_supplier(supplier_id)
    
    if error:
        return APIResponse.not_found(
            message=error,
            details="Supplier not found",
            solution="Check the supplier ID"
        )
    
    return APIResponse.success(data=supplier)


@suppliers_bp.route('/', methods=['POST'])
@jwt_required()
def add_supplier():
    """Create supplier - admin only"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can create suppliers",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide supplier data: name (required), contact_person, phone, email, address"
        )
    
    supplier_service = SupplierService()
    supplier, error = supplier_service.create_supplier(data, user)
    
    if error:
        if "required" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Provide supplier name")
        if "already exists" in error.lower():
            return APIResponse.conflict(message=error, details=f"Supplier '{data.get('name')}' already exists", solution="Use a different supplier name")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=supplier, message="Supplier created successfully", status_code=201)


@suppliers_bp.route('/<int:supplier_id>', methods=['PUT'])
@jwt_required()
def update_supplier(supplier_id):
    """Update supplier - admin only"""
    user = get_current_user()
    
    if user.role not in ['admin', 'manager']:
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins and managers can update suppliers",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    supplier_service = SupplierService()
    supplier, error = supplier_service.update_supplier(supplier_id, data, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Supplier ID {supplier_id} not found", solution="Check the supplier ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=supplier, message="Supplier updated successfully")


@suppliers_bp.route('/<int:supplier_id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(supplier_id):
    """Delete supplier - admin only (manager needs admin approval)"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Admin approval required",
            details=f"Managers need admin approval to delete suppliers",
            solution="Contact the administrator to delete this supplier"
        )
    
    supplier_service = SupplierService()
    supplier, error = supplier_service.delete_supplier(supplier_id, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Supplier ID {supplier_id} not found", solution="Check the supplier ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(message="Supplier deleted successfully")