from marshmallow import Schema, fields, validate, ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=must_not_be_blank)
    first_name = fields.Str(required=True, validate=must_not_be_blank)
    last_name = fields.Str(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True)
    role = fields.Str(dump_only=True)
    api_key = fields.Str(dump_only=True)