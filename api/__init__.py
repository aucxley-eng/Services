from api.auth import auth_bp
from api.products import products_bp
from api.inventory import inventory_bp
from api.categories import categories_bp
from api.suppliers import suppliers_bp
from api.dashboard import dashboard_bp

__all__ = [
    'auth_bp',
    'products_bp',
    'inventory_bp',
    'categories_bp',
    'suppliers_bp',
    'dashboard_bp'
]