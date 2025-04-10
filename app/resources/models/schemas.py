from marshmallow import Schema, fields

from .basic import UserRoleEnum

class BaseSchema(Schema):
    """
        Basic schema that contains all the common fields.
    """
    id = fields.Integer(dump_only=True)

class UserSchema(BaseSchema):
    """
        Schema for the user model.
    """
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.Enum(UserRoleEnum, by_value=False)
