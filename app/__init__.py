from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from database import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    CORS(app)

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

    from api import auth_bp, products_bp, inventory_bp, categories_bp, suppliers_bp, dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

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