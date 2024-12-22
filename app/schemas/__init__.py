from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    email = fields.Email(required=True)

class PackageSchema(Schema):
    description = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    location = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['in_warehouse', 'in_transit', 'delivered']))

class VatCalculationSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    calculation_date = fields.DateTime(required=False)

class RouteOptimizationSchema(Schema):
    origin = fields.Str(required=True)
    destinations = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
