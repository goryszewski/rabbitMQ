from marshmallow import Schema,fields

class PayloadSchema(Schema):
    data = fields.Int()