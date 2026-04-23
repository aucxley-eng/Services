from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from config import Config
from database import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    JWTManager(app)
    
    CORS(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, config=swagger_config)

    from app.auth.routes import auth_bp
    # from app.products.routes import products_bp
    # from app.inventory.routes import inventory_bp
    # from app.categories.routes import categories_bp
    # from app.suppliers.routes import suppliers_bp
    # from app.dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(products_bp, url_prefix='/api/products')
    # app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    # app.register_blueprint(categories_bp, url_prefix='/api/categories')
    # app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
    # app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "error": "Bad Request",
            "message": str(e.description),
            "details": "The request was malformed or invalid",
            "solution": "Check your request body and headers"
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": str(e.description) if e.description else "The requested endpoint does not exist",
            "details": f"Route {request.method} {request.path} not found",
            "solution": "Check the API endpoint URL"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "error": "Method Not Allowed",
            "message": str(e.description) if e.description else "This method is not allowed",
            "details": f"Method {request.method} not supported for this endpoint",
            "solution": "Use the correct HTTP method (GET, POST, PUT, DELETE)"
        }), 405

    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth(e):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authorization required",
            "details": "No JWT token was provided",
            "solution": "Include 'Authorization: Bearer <token>' header"
        }), 401

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header(e):
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid authorization header",
            "details": str(e),
            "solution": "Use format: 'Authorization: Bearer <token>'"
        }), 401

    @app.errorhandler(500)
    def internal_error(e):
        error_msg = str(e.original) if hasattr(e, 'original') else str(e)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "details": error_msg,
            "solution": "Contact support or check server logs"
        }), 500

    return app