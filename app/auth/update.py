from . import auth, MethodView,abort
from ..models import User
from ..schemas import AuthupdateInformationSchema,AuthupdatePasswordSchema
from .. import db
from flask_restful import reqparse
from flask import current_app


@auth.route("update/password")
class UpdatePasswordView(MethodView):
    def get(self):
        return {'help': 'UpdatePasswordView'}, 200

    @auth.arguments(AuthupdatePasswordSchema)
    def put(self,pass_data):
        user = User.query.filter_by(id=User.decode_auth_token(pass_data['token'])).first()
        if user is not None:
            if user.verify_password(pass_data['password']):
                user.verified = True
                user.password = pass_data['newpassword']
                try:
                    db.session.commit()  # SQLAlchemy用
                except Exception as e:
                    # 数据库出错回滚
                    db.session.rollback()
                    current_app.logger.error(e)
                    abort(404, message='数据库查询异常')
            else:
                abort(403, message='密码错误')
        else:
            abort(403, message='不存在该用户')
        return {'status': 200, 'message': '密码更新成功'}, 200

@auth.route("update/info")
class UpdateInformationView(MethodView):
    @auth.arguments(AuthupdateInformationSchema)
    def get(self,info_data):
        user = User.query.filter_by(id=User.decode_auth_token(info_data['token'])).first()
        return {'id': user.id, 'email': user.email, 'username': user.username,
                'name': user.name, 'location': user.location, 'lang': user.lang}, 200

    @auth.arguments(AuthupdateInformationSchema)
    def put(self,info_data):
        user = User.query.filter_by(id=User.decode_auth_token(info_data['token'])).first()
        if user is not None:
            user.verified = True
            current_app.logger.info(user.email)
            user.email = info_data['email'] or user.email
            user.name = info_data['name'] or user.name
            user.location = info_data['location'] or user.location
            user.lang = info_data['lang'] or user.lang
            try:
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                abort(404, message='数据库查询异常')
        else:
            abort(403, message='不存在该用户')

        return {'status': 200, 'message': '用户信息更新成功'}, 200



