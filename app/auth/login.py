from . import auth_api, Resource
from ..models import User, Userlog
from .. import db
from flask_restful import reqparse
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, location='json', help='用户名重复')
parser.add_argument('password', required=True, type=str, location='json', help='密码不能为空')


# parser.add_argument('location', required=True, type=str, location='json', help='地点不能为空')
# !!测试用
class LoginView(Resource):
    def get(self):
        return {'help': 'LoginView'}

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user is not None and user.verify_password(args['password']):
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
                return {'status': 404, 'message': '数据库查询异常'}, 404
            return {'status': 200, 'message': 'success', 'token': token}
        else:
            return {'status': 403, 'message': 'failed'}, 403


auth_api.add_resource(LoginView, '/login')
