from app.schemas import AuthLoginSchema
from . import auth, MethodView,abort
from ..models import User, Userlog
from .. import db
from flask_restful import reqparse
from flask import current_app



@auth.route("/login")
class LoginView(MethodView):
    def get(self):
        return {'help': 'LoginView'}

    @auth.arguments(AuthLoginSchema)
    def post(self,auth_data):
        user = User.query.filter_by(username=auth_data['username']).first()
        if user is not None and user.verify_password(auth_data['password']):
            userid = user.id
            token = User.encode_auth_token(userid)
            user_logs = Userlog(user_id=userid, location='China')
            try:
                db.session.add(user_logs)
                # db.commit()
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                abort(404, message='数据库查询异常')
            return {'status': 200, 'message': 'success', 'token': token}
        else:
            abort(403, message='wrong password')


