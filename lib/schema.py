from marshmallow import Schema, fields


class PayloadSchema(Schema):
    data = fields.Int()


class PayloadSchemaBad(Schema):
    data1 = fields.Int()
