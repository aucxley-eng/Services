from functools import wraps
from flask import request
from services import AuthService
from responses import APIResponse


def require_auth(roles=None):
    """
    Decorator for API key-based authentication with optional role check.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return APIResponse.unauthorized("API key required. Include 'X-API-Key' header.")
            
            auth_service = AuthService()
            user = auth_service.get_user_by_api_key(api_key)
            
            if not user:
                return APIResponse.unauthorized("Invalid API key. Please check your credentials.")
            
            if roles and user.role not in roles:
                return APIResponse.forbidden(f"Access denied. Required roles: {', '.join(roles)}")
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn=None):
    """Decorator for admin-only access."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return APIResponse.unauthorized("API key required.")
            
            auth_service = AuthService()
            user = auth_service.get_user_by_api_key(api_key)
            
            if not user:
                return APIResponse.unauthorized("Invalid API key.")
            
            if user.role != 'admin':
                return APIResponse.forbidden("Admin access required.")
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)


def manager_required(fn=None):
    """Decorator for manager or admin access."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return APIResponse.unauthorized("API key required.")
            
            auth_service = AuthService()
            user = auth_service.get_user_by_api_key(api_key)
            
            if not user:
                return APIResponse.unauthorized("Invalid API key.")
            
            if user.role not in ['admin', 'manager']:
                return APIResponse.forbidden("Manager or Admin access required.")
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)