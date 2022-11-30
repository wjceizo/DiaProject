from marshmallow import Schema, fields


## 用户Schema

class AuthRegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    lang = fields.Str(required=True)

class AuthLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class AuthupdatePasswordSchema(Schema):
    token = fields.Str(required=True)
    password = fields.Str(required=True)
    newpassword = fields.Str(required=True)

class AuthupdateInformationSchema(Schema):
    token = fields.Str(required=True)    
    email = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    location = fields.Str(allow_none=True)
    lang = fields.Str(allow_none=True)

class AuthSchema(Schema):    
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    order = fields.Str(required=True)
    order_by = fields.Str(required=True)
