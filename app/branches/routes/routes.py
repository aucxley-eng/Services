from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.branches.service import BranchService
from app.api_response import APIResponse

branches_bp = Blueprint('branches', __name__)


def get_current_user():
    user_id = int(get_jwt_identity())
    from app.auth.repo import UserRepository
    return UserRepository().find_by_id(user_id)


@branches_bp.route('/', methods=['GET'])
@jwt_required()
def get_branches():
    """Get all branches - any authenticated user"""
    branch_service = BranchService()
    branches, error = branch_service.get_all_branches()
    
    if error:
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data={"branches": branches})


@branches_bp.route('/<int:branch_id>', methods=['GET'])
@jwt_required()
def get_branch(branch_id):
    """Get a single branch - any authenticated user"""
    branch_service = BranchService()
    branch, error = branch_service.get_branch(branch_id)
    
    if error:
        return APIResponse.not_found(message=error, details="Branch not found", solution="Check the branch ID")
    
    return APIResponse.success(data=branch)


@branches_bp.route('/', methods=['POST'])
@jwt_required()
def add_branch():
    """Create branch - admin only"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins can create branches",
            solution="Contact the administrator to create a new branch"
        )
    
    data = request.get_json() or {}
    
    if not data:
        return APIResponse.error(
            message="No data provided",
            error_code="Validation Error",
            status_code=400,
            details="Request body is empty",
            solution="Provide branch data: name (required), location, phone, email"
        )
    
    branch_service = BranchService()
    branch, error = branch_service.create_branch(data, user)
    
    if error:
        if "required" in error.lower():
            return APIResponse.error(message=error, error_code="Validation Error", status_code=400, details=error, solution="Provide the branch name")
        if "already exists" in error.lower():
            return APIResponse.conflict(message=error, details=f"Branch '{data.get('name')}' already exists", solution="Use a different branch name")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=branch, message="Branch created successfully", status_code=201)


@branches_bp.route('/<int:branch_id>', methods=['PUT'])
@jwt_required()
def update_branch(branch_id):
    """Update branch - admin only"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Access denied",
            details="Only admins can update branch details",
            solution="Contact the administrator"
        )
    
    data = request.get_json() or {}
    branch_service = BranchService()
    branch, error = branch_service.update_branch(branch_id, data, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Branch ID {branch_id} not found", solution="Check the branch ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(data=branch, message="Branch updated successfully")


@branches_bp.route('/<int:branch_id>', methods=['DELETE'])
@jwt_required()
def delete_branch(branch_id):
    """Delete branch - admin only (never allow deletion of branches)"""
    user = get_current_user()
    
    if user.role != 'admin':
        return APIResponse.forbidden(
            message="Cannot delete branch",
            details="Only admins can delete branches",
            solution="Contact the administrator"
        )
    
    branch_service = BranchService()
    branch, error = branch_service.delete_branch(branch_id, user)
    
    if error:
        if "not found" in error.lower():
            return APIResponse.not_found(message=error, details=f"Branch ID {branch_id} not found", solution="Check the branch ID")
        return APIResponse.error(error, "Error", 400)
    
    return APIResponse.success(message="Branch deleted successfully")