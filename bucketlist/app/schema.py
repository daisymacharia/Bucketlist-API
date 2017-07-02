from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):

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

    email = fields.Email(validate=[validate.Length(max=50)],
                         required=True,
                         error_messages={"required": "Enter email"})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={"required": "Enter password"})
