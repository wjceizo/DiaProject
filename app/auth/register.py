from . import auth_api, Resource
from ..models import User
from ..utils.user import encode_auth_token
from .. import db
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, location='json', help='用户名重复')
parser.add_argument('password_hash', required=True, type=str, location='json', help='密码不能为空')
parser.add_argument('email', type=str, required=True, location='json', help='电子邮箱重复')
parser.add_argument('name', required=True, type=str, location='json', help='姓名不能为空')
parser.add_argument('location', required=True, type=str, location='json', help='地址不能为空')
parser.add_argument('lang', required=True, type=str, location='json', help='语言不能为空')

class RegisterView(Resource):
    def get(self):
        return 'get register page'

    def post(self):
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'],
                    name=args['name'], location=args['location'], lang=args['lang']
                    )
        user.password = args['password_hash']
        user_id = user.id
        token = encode_auth_token(user_id)
        user.token = token
        try:
            db.session.add(user)
            # db.commit()
            db.session.commit()  # SQLAlchemy用

        except IntegrityError as e:
            # 数据库出错回滚
            db.session.rollback()
            # 手机号重复，记录错误日志
            current_app.logger.error(e)
            return {"status": 422, "message": "用户已注册"}

        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            return {"status": 404, "message": "数据库查询异常"}

        return {"status": 201, "message": "注册成功"}, 201


class Helloyou(Resource):
    def get(self):
        return {'status': 200}


auth_api.add_resource(Helloyou, '/')
auth_api.add_resource(RegisterView, '/register')
