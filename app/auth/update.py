from . import auth, MethodView, abort
from ..models import User
from ..schemas import AuthRegisterSchema, AuthupdateInformationSchema, AuthupdatePasswordSchema
from .. import db
from flask import current_app
from flask_jwt_extended import jwt_required,get_jwt_identity


@auth.route("/info")
class InformationView(MethodView):

    @auth.response(200,AuthRegisterSchema)
    @jwt_required()
    def get(self):
        user = User.query.filter_by(
            id = get_jwt_identity()).first()
        return user

@auth.route("/update/password")
class UpdatePasswordView(MethodView):
    def get(self):
        return {'help': 'Use put method to update password!'}, 200

    @auth.arguments(AuthupdatePasswordSchema)
    @jwt_required(fresh=True)
    def put(self, pass_data):
        user = User.query.filter_by(
            id = get_jwt_identity()).first()
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


@auth.route("/update/info")
class UpdateInformationView(MethodView):

    def get(self):
        return {'help': "Use put method to update auth's information!"}, 200

    @auth.arguments(AuthupdateInformationSchema)
    @auth.response(200,AuthRegisterSchema)
    @jwt_required()
    def put(self, info_data):
        user = User.query.filter_by(
            id = get_jwt_identity()).first()
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
        return user
