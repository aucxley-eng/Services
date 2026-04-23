from marshmallow import fields, validate, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.products.domain import Product


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
    
    id = fields.Int(dump_only=True)
    product_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    buying_price = fields.Float(required=True, validate=validate.Range(min=0))
    selling_price = fields.Float(validate=validate.Range(min=0))
    unit = fields.Str(validate=validate.Length(max=20))
    threshold = fields.Int(load_default=10, validate=validate.Range(min=0))
    category_id = fields.Int(allow_none=True)
    image_url = fields.Str(allow_none=True)


class ProductCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        exclude = ('id', 'product_id', 'created_at')
    
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    buying_price = fields.Float(required=True, validate=validate.Range(min=0))
    selling_price = fields.Float(validate=validate.Range(min=0))
    unit = fields.Str(validate=validate.Length(max=20))
    threshold = fields.Int(load_default=10, validate=validate.Range(min=0))
    category_id = fields.Int(allow_none=True)
    image_url = fields.Str(allow_none=True)


class ProductUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        exclude = ('id', 'product_id', 'created_at')
        partial = True
    
    name = fields.Str(validate=validate.Length(min=1, max=100))
    buying_price = fields.Float(validate=validate.Range(min=0))
    selling_price = fields.Float(validate=validate.Range(min=0))
    unit = fields.Str(validate=validate.Length(max=20))
    threshold = fields.Int(validate=validate.Range(min=0))
    category_id = fields.Int(allow_none=True)
    image_url = fields.Str(allow_none=True)


product_schema = ProductSchema()
product_create_schema = ProductCreateSchema()
product_update_schema = ProductUpdateSchema()
products_schema = ProductSchema(many=True)