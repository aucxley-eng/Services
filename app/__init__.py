from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from app.models import db

# Initialize extensions
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Enable CORS
    CORS(app)

    # Swagger Configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, config=swagger_config)

    # Import Blueprints from the new 'api' directory
    from app.api.auth.routes import auth_bp
    from app.api.products.routes import products_bp
    from app.api.inventory.routes import inventory_bp
    from app.api.categories.routes import categories_bp
    from app.api.suppliers.routes import suppliers_bp
    from app.api.dashboard.routes import dashboard_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # Global Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad Request", message=str(e.description)), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Not Found", message="The requested resource was not found on this server."), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error="Method Not Allowed", message="This method is not allowed for the requested URL."), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error="Internal Server Error", message="An unexpected error occurred on the server."), 500

    return app
