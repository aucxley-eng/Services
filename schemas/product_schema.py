from marshmallow import Schema, fields, validate, ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    product_id = fields.Str()
    buying_price = fields.Float(required=True)
    selling_price = fields.Float()
    unit = fields.Str()
    category_id = fields.Int()
    expiry_date = fields.Date()
    threshold = fields.Int()
    image_url = fields.Str()


class ProductSchemaMany(ProductSchema):
    pass