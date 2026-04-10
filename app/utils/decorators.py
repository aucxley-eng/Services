from functools import wraps
from flask import request, jsonify
from app.models import User


def require_auth(roles=None):
    """
    Decorator for API key-based authentication with optional role check.
    
    Usage:
        @require_auth()                    - Any authenticated user
        @require_auth(roles=['admin'])     - Only admin
        @require_auth(roles=['admin', 'manager']) - Admin or manager
    
    Header required: X-API-Key: <api_key>
    
    Returns:
        401 if no API key or invalid key
        403 if role doesn't match
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "API key required. Include 'X-API-Key' header."
                }), 401
            
            user = User.query.filter_by(api_key=api_key).first()
            
            if not user:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid API key. Please check your credentials."
                }), 401
            
            if roles and user.role not in roles:
                return jsonify({
                    "error": "Forbidden",
                    "message": f"Access denied. Required roles: {', '.join(roles)}"
                }), 403
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn=None):
    """
    Shorthand decorator for admin-only access.
    Usage: @admin_required (without parentheses)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "API key required. Include 'X-API-Key' header."
                }), 401
            
            user = User.query.filter_by(api_key=api_key).first()
            
            if not user:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid API key."
                }), 401
            
            if user.role != 'admin':
                return jsonify({
                    "error": "Forbidden",
                    "message": "Admin access required."
                }), 403
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)


def manager_required(fn=None):
    """
    Shorthand decorator for manager or admin access.
    Usage: @manager_required (without parentheses)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "API key required. Include 'X-API-Key' header."
                }), 401
            
            user = User.query.filter_by(api_key=api_key).first()
            
            if not user:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid API key."
                }), 401
            
            if user.role not in ['admin', 'manager']:
                return jsonify({
                    "error": "Forbidden",
                    "message": "Manager or Admin access required."
                }), 403
            
            request.current_user = user
            
            return fn(*args, **kwargs)
        return wrapper
    
    if fn is None:
        return decorator
    return decorator(fn)