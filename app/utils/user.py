from flask import current_app
from ..models import User

# def check_iterate(value):
#     current_app.logger.info(value)
#     if value == 'email':
#         email = User.query.filter_by(email=value)
#         if email:
#             raise ValueError("邮箱已注册")
#         else:
#             return value
#
#     elif value == 'username':
#         username = User.query.filter_by(username=value)
#         if username:
#             raise ValueError("用户名已注册")
#         else:
#             return value
#
#     else:
#         current_app.logger.info('不太对劲')

# def check_username_iterate(value):
#     username = User.query.filter_by(username=value)
#     if username:
#         raise ValueError("用户已被注册")
#     else:
#         return Str
#
#
# def check_email_iterate(value):
#     email = User.query.filter_by(email=value)
#     if email:
#         raise ValueError("邮箱已被注册")
#     else:
#         return value
