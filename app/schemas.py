from marshmallow import Schema, fields


# 用户Schema

class AuthRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    lang = fields.Str(required=True)


class AuthLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class AuthupdatePasswordSchema(Schema):
    password = fields.Str(required=True)
    newpassword = fields.Str(required=True)


class AuthupdateInformationSchema(Schema):
    email = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    lang = fields.Str(allow_none=True)


class AuthSchema(Schema):
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    order = fields.Str(required=True)
    order_by = fields.Str(required=True)


class AudioWordsSchema(Schema):
    stem = fields.Str(required=True)
    meaning = fields.Str(required=True)
    comm = fields.Str()

