from .extensions import ma
from marshmallow import fields, validate

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(["admin", "owner", "client"]))
    is_active = fields.Bool()
    created_at = fields.DateTime(format='iso')

class SpaceSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image_url = fields.Str()
    price_per_hour = fields.Float(required=True)
    status = fields.Str()
    owner_id = fields.Int()
    created_at = fields.DateTime(format='iso')

class BookingSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    space_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True, format='iso')
    end_time = fields.DateTime(required=True, format='iso')
    amount = fields.Float()
    status = fields.Str()
    created_at = fields.DateTime(format='iso')
