""" marshmallow schema with functions:
1.Validate input data.
2.Deserialize input data to app-level objects.
3.Serialize app-level objects to primitive Python types.
The serialized objects can then be rendered to standard
formats such as JSON for use in an HTTP API. """
from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):

    user_id = fields.Integer(dump_only=True)
    fullnames = fields.String(validate=[validate.Length(min=3),
                              validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                              error="Invalid characters")],
                              required=True,
                              error_messages={"required": "Enter full names"})
    email = fields.Email(validate=[validate.Length(max=50)],
                         required=True,
                         error_messages={"required": "Enter email"})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={"required": "Enter password"})


class UserLoginSchema(Schema):

    list_id = fields.Integer(dump_only=True)
    email = fields.Email(validate=[validate.Length(max=50)],
                         required=True,
                         error_messages={"required": "Enter email"})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={"required": "Enter password"})


class BucketListSchema(Schema):
    list_id = fields.Integer(dump_only=True)
    name = fields.String(validate=[validate.Length(min=3),
                         validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                         error="Invalid characters")],
                         required=True,
                         error_messages={"required": "Enter bucketlist name"})
    items = fields.Nested('ItemsSchema', dump_only=True, many=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Integer()


class ItemsSchema(Schema):
    item_id = fields.Integer(dump_only=True)
    name = fields.String(validate=[validate.Length(min=3),
                         validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                         error="Invalid characters")],
                         required=True,
                         error_messages={"required": "Enter bucketlist name"})
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Boolean()
