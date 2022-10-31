from . import main_api, Resource
from .. import db
from ..models import User
from flask_restful import reqparse
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, location='form', help='token不能为空')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        token = args['token']
        userid = User.decode_auth_token(token)
        current_app.logger.error(userid)
        return {'messgae': userid}


main_api.add_resource(HelloWorld, '/')
