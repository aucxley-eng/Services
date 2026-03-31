from flask import Blueprint, request, jsonify
from app.models import db, Supplier
from flask_jwt_extended import jwt_required

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/', methods=['GET'])
@jwt_required()
def get_suppliers():
    """Get all suppliers"""
    suppliers = Supplier.query.all()
    output = []
    for s in suppliers:
        output.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "phone": s.phone,
            "taking_returns": s.taking_returns
        })
    return jsonify(output), 200

@suppliers_bp.route('/', methods=['POST'])
@jwt_required()
def add_supplier():
    """Add a new supplier with validation"""
    data = request.get_json() or {}
    name = data.get('name')
    
    if not name:
        return jsonify({
            "error": "Validation Error",
            "message": "The supplier 'name' is required."
        }), 400

    if Supplier.query.filter_by(name=name).first():
        return jsonify({
            "error": "Conflict",
            "message": f"A supplier with the name '{name}' already exists."
        }), 409

    try:
        new_supplier = Supplier(
            name=name,
            email=data.get('email'),
            phone=data.get('phone'),
            taking_returns=data.get('taking_returns', True)
        )
        
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({"message": "Supplier added successfully", "id": new_supplier.id}), 201
    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "Could not save supplier information."
        }), 500
