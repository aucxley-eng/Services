from app import db
from marshmallow import Schema, fields, validate, ValidationError

# --- Validation Helpers ---
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

# --- Schemas ---

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=must_not_be_blank)
    first_name = fields.Str(required=True, validate=must_not_be_blank)
    last_name = fields.Str(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True)
    role = fields.Str(dump_only=True) # Only readable, not settable via public API

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    product_id = fields.Str() # SKU/Barcode
    buying_price = fields.Float(required=True)
    selling_price = fields.Float()
    unit = fields.Str()
    category_id = fields.Int()
    expiry_date = fields.Date()
    threshold = fields.Int()
    image_url = fields.Str()

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

# Generic Response Schema (for messages like "Success")
class MessageSchema(Schema):
    message = fields.Str()
    status = fields.Str()