from app.blocklist import BLOCKLIST
from app.schemas import AuthLoginSchema
from . import auth, MethodView, abort
from ..models import User, Userlog
from .. import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,create_refresh_token,get_jwt_identity
from flask import current_app


@auth.route("/login")
class LoginView(MethodView):
    def get(self):
        return {'help': 'LoginView'}

    @auth.arguments(AuthLoginSchema)
    def post(self, auth_data):
        user = User.query.filter_by(username=auth_data['username']).first()
        if user is not None and user.verify_password(auth_data['password']):
            userid = user.id
            token = User.encode_auth_token(userid)
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            user_logs = Userlog(user_id=userid, location='China')
            try:
                db.session.add(user_logs)
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                abort(404, message='数据库查询异常')
            return {'message': 'success', 'access_token': access_token,'refresh_token':refresh_token},200
        else:
            abort(403, message='wrong password')


@auth.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        # jti = get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@auth.route("/logout")
class LogoutView(MethodView):
    
    def get(self):
        return {'help': 'LogoutView'}


    @jwt_required(verify_type=False)
    def post(self):
        jti = get_jwt()["jti"]
        ttype = get_jwt()["type"]
        BLOCKLIST.add(jti)
        return {"message": ttype.capitalize() + " token successfully logged out"}, 200
    ## 记得注销时前端发两个请求同时将access_token和refresh_token都放入blocklist

