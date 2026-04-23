from flask import Blueprint
from services import DashboardService
from middleware import require_auth
from responses import APIResponse

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@require_auth()
def get_stats():
    """Get dashboard statistics"""
    dashboard_service = DashboardService()
    stats, error = dashboard_service.get_stats()
    
    return APIResponse.success(data=stats)