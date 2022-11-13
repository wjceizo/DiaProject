import os
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
        if userwordrel:
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
            return {'status': 200, 'message': "delete successfully"}, 200
        else:
            return {'status': 403, 'message': 'Do not upload this audio!'}, 403


class DeleteAllView(Resource):
    def get(self):
        return {'word_id': 'sad'}

    def post(self):
        args = parser.parse_args()
        userid = User.decode_auth_token(args['token'])
        userwordrel = Userwordrel.query.filter_by(user_id=userid).all()
        current_app.logger.info(userwordrel)
        if userwordrel:
            try:
                for item in userwordrel:
                    db.session.delete(item)
                    db.session.commit()
                    os.remove(item.snd_path)
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                return {"status": 404, "message": "数据库查询异常"}, 404
            return {"status": 200, "message": 'delete successfully'}, 200
        else:
            return {'status': 403, 'message': 'Do not upload audio yet!'}, 403


user_api.add_resource(DeleteOneView, '/<word_id>/delete')
user_api.add_resource(DeleteAllView, '/all/delete')
