from . import user_api, Resource
from ..models import Userwordrel
from .. import db
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, location='json', help='token不能为空')
parser.add_argument('time', required=True, type=str, location='json', help='更新时间不能为空')


class RecordView(Resource):
    def get(self, word_id):
        return {'hello': 'you'}

    def post(self, word_id):
        args = parser.parse_args()


user_api.add_resource(RecordView, '/<word_id>/record')
