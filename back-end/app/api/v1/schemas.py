from marshmallow import Schema, fields


class DataResponseSchema(Schema):
    version = fields.Str()
    data = fields.List(fields.Int())
