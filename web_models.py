
from marshmallow import Schema, fields

class UserWebSchema(Schema):
    username = fields.Str()
    id = fields.Str()

class MessageWebSchema(Schema):
    content = fields.Str()
    sender = fields.Str()
    recipients = fields.List(fields.Str())
    timestamp = fields.Str()
    id = fields.Str()
