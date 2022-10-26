from . import user_api, Resource
from ..models import User
from .. import db
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, location='json', help='用户名重复')
parser.add_argument('password', required=True, type=str, location='json', help='密码不能为空')


class LoginView(Resource):
    def get(self):
        return {'hello': 'you'}

    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user is not None and user.verify_password(args['password']):
            return {'status': 200, 'message': 'success'}
        else:
            return {'status': 403, 'message': 'failed'}, 403


user_api.add_resource(LoginView, '/login')
