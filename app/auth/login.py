from . import auth_api, Resource
from ..models import User, Userlog
from .. import db
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, location='json', help='用户名重复')
parser.add_argument('password', required=True, type=str, location='json', help='密码不能为空')


# parser.add_argument('location', required=True, type=str, location='json', help='地点不能为空')

class LoginView(Resource):
    def get(self):
        return {'hello': 'you'}

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user is not None and user.verify_password(args['password']):
            userid = user.id
            user_logs = Userlog(user_id=userid, location='China')
            message = 'success'
            try:
                db.session.add(user_logs)
                # db.commit()
                db.session.commit()  # SQLAlchemy用

            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                message = '数据库查询异常'
            return {'status': 200, 'message': message}
        else:
            return {'status': 403, 'message': 'failed'}, 403


auth_api.add_resource(LoginView, '/login')
