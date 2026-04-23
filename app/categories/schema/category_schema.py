from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.categories.domain import Category


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=255))
    is_active = fields.Bool(load_default=True)
    created_at = fields.DateTime(dump_only=True)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)