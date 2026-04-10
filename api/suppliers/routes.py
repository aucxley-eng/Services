from flask import Blueprint, request
from services import SupplierService
from middleware import require_auth
from responses import APIResponse

suppliers_bp = Blueprint('suppliers', __name__)


@suppliers_bp.route('/', methods=['GET'])
@require_auth()
def get_suppliers():
    """Get all suppliers"""
    supplier_service = SupplierService()
    suppliers, error = supplier_service.get_all_suppliers()
    
    return APIResponse.success(data=suppliers)


@suppliers_bp.route('/', methods=['POST'])
@require_auth()
def add_supplier():
    """Add a new supplier"""
    data = request.get_json() or {}
    
    supplier_service = SupplierService()
    supplier, error = supplier_service.create_supplier(data, request.current_user)
    
    if error:
        if "already exists" in error.lower():
            return APIResponse.conflict(error)
        if "required" in error.lower():
            return APIResponse.error(error, "Validation Error", 400)
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=supplier, status_code=201)