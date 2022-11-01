import os
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from . import user_api, Resource
from ..models import Userwordrel, User
from .. import db
from flask_restful import reqparse
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, location='json', help='token不能为空')


class DeleteOneView(Resource):
    def get(self, word_id):
        return {'word_id': word_id}

    def post(self, word_id):
        args = parser.parse_args()
        userid = User.decode_auth_token(args['token'])
        userwordrel = Userwordrel.query.filter_by(user_id=userid, word_id=word_id).first()
        if userwordrel is not None:
            try:
                path = userwordrel.snd_path
                db.session.delete(userwordrel)
                db.session.commit()
                os.remove(path)
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                return {"status": 404, "message": "数据库查询异常"}, 404
            return {"status": 200, "message": "delete successful"}, 200
        else:
            return {'status': 403, 'message': 'no this audio'}, 403


user_api.add_resource(DeleteOneView, '/<word_id>/delete')
