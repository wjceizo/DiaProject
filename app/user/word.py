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
parser.add_argument('token', type=str, required=True, location='form', help='token不能为空')
parser.add_argument('record', required=True, type=FileStorage, location='files', help='音频文件不能为空')
parser.add_argument('snd_abs', type=str, location='form')


class RecordView(Resource):
    def get(self, word_id):
        return {'hello': word_id}

    def post(self, word_id):

        args = parser.parse_args()
        basepath = os.path.abspath(os.getcwd())
        userid = User.decode_auth_token(args['token'])

        try:
            stream = args.get
            upload_path = os.path.join(basepath, "records", secure_filename(stream.filename))
            stream.save(upload_path)
            userwordrel = Userwordrel(user_id=userid, word_id=word_id, snd_path=upload_path, snd_abs=args['snd_abs'])
        except FileNotFoundError as e:
            current_app.logger.error(e)
            return {"status": 400, "message": "未上传录音文件"}, 400

        try:
            db.session.add(userwordrel)
            db.session.commit()  # SQLAlchemy用
        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            os.remove(upload_path)
            return {"status": 404, "message": "数据库查询异常"}, 404

        return {"status": 200, "message": "upload success"}, 200


class UpdateRecordView(Resource):
    def get(self, word_id):
        return {'word_id': word_id}

    def post(self, word_id):
        args = parser.parse_args()
        basepath = os.path.abspath(os.getcwd())
        userid = User.decode_auth_token(args['token'])
        userwordrel = Userwordrel.query.filter_by(user_id=userid, word_id=word_id).first()
        if userwordrel is not None:
            try:
                stream = args.get
                upload_path = os.path.join(basepath, "records", secure_filename(stream.filename))
                stream.save(upload_path)
                userwordrel.update_at = datetime.now()
                userwordrel.snd_abs = args['snd_abs']
                userwordrel.verified = True
            except FileNotFoundError as e:
                current_app.logger.error(e)
                return {"status": 400, "message": "未上传录音文件"}, 400
            try:
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                os.remove(upload_path)
                return {"status": 404, "message": "数据库查询异常"}, 404

            return {"status": 200, "message": "upload success"}, 200
        else:
            return {'status': 403, 'message': 'no this audio'}, 403


user_api.add_resource(RecordView, '/<word_id>/record')
user_api.add_resource(UpdateRecordView, '/<word_id>/update')

