from flask import Blueprint, request, jsonify
from app.models import db, Category
from app.utils.decorators import require_auth

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
@require_auth()
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    output = [{"id": c.id, "name": c.name} for c in categories]
    return jsonify(output), 200

@categories_bp.route('/', methods=['POST'])
@require_auth()
def add_category():
    """Create a new category with specific feedback"""
    data = request.get_json() or {}
    name = data.get('name')
    
    if not name:
        return jsonify({
            "error": "Validation Error",
            "message": "The category 'name' is required."
        }), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({
            "error": "Conflict",
            "message": f"A category with the name '{name}' already exists."
        }), 409

    try:
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"id": new_category.id, "name": new_category.name}), 201
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "Could not create category."
        }), 500
