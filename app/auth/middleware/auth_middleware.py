from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from services import AuthService
from responses import APIResponse


def require_auth(roles=None):
    """
    Decorator for JWT-based authentication with optional role check.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            
            if roles:
                claims = get_jwt()
                user_role = claims.get('role')
                if user_role not in roles:
                    return APIResponse.forbidden(f"Access denied. Required roles: {', '.join(roles)}")
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn=None):
    """Decorator for admin-only access."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != 'admin':
                return APIResponse.forbidden("Admin access required.")
            
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
            verify_jwt_in_request()
            
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in ['admin', 'manager']:
                return APIResponse.forbidden("Manager or Admin access required.")
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)