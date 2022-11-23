from . import auth_api, Resource
from ..models import User
from .. import db
from flask_restful import reqparse
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, location='json', help='token不能为空')
parser.add_argument('password', type=str, location='json', help='密码不能为空')
parser.add_argument('newpassword', type=str, location='json', help='密码不能为空')
parser.add_argument('email', type=str, location='json', help='电子邮箱重复')
parser.add_argument('name', type=str, location='json', help='姓名不能为空')
parser.add_argument('location', type=str, location='json', help='地址不能为空')
parser.add_argument('lang', type=str, location='json', help='语言不能为空')


class UpdatePasswordView(Resource):
    def get(self):
        return {'help': 'UpdatePasswordView'}, 200

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(id=User.decode_auth_token(args['token'])).first()
        if user is not None:
            if user.verify_password(args['password']):
                user.verified = True
                user.password = args['newpassword']
                try:
                    db.session.commit()  # SQLAlchemy用
                except Exception as e:
                    # 数据库出错回滚
                    db.session.rollback()
                    current_app.logger.error(e)
                    return {"status": 404, "message": "数据库查询异常"}, 404
            else:
                return {'status': 403, 'message': '密码错误'}, 403
        else:
            return {'status': 403, 'message': '不存在该用户'}, 403

        return {'status': 200, 'message': '密码更新成功'}, 200


class UpdateInformationView(Resource):

    def get(self):
        args = parser.parse_args()
        user = User.query.filter_by(id=User.decode_auth_token(args['token'])).first()
        return {'id': user.id, 'email': user.email, 'username': user.username,
                'name': user.name, 'location': user.location, 'lang': user.lang}, 200


    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(id=User.decode_auth_token(args['token'])).first()
        if user is not None:
            user.verified = True
            user.email = args['email']
            user.name = args['name']
            user.location = args['location']
            user.lang = args['lang']
            try:
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                return {"status": 404, "message": "数据库查询异常"}, 404
        else:
            return {'status': 403, 'message': '不存在该用户'}, 403

        return {'status': 200, 'message': '用户信息更新成功'}, 200


auth_api.add_resource(UpdatePasswordView, '/update/password')
auth_api.add_resource(UpdateInformationView, '/update/information')
