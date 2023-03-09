from ..schemas import AuthUploadRecordSchema
from ..models import Userwordrel, User
from . import user_record, basepath, MethodView, abort
from .. import db
from datetime import datetime
import time
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import base64, os
from werkzeug.utils import secure_filename
import hashlib

# md5校验
def checksum(data, true_md5):
    # 创建md5对象，传入数据，获取摘要
    m = hashlib.md5(data)
    digest = m.hexdigest()
    if digest == true_md5:
        return True
    else:
        raise ValueError("md5校验错误")


@user_record.route("/upload")
class Upload(MethodView):
    def get(self):
        return {"help": "Upload the record"}

    @user_record.arguments(AuthUploadRecordSchema)
    @jwt_required(fresh=True)
    def post(self, record_data):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        try:
            recordData = base64.b64decode(record_data["record_file"])
            userid = str(time.time()).split('.')[0]
            upload_path = os.path.join(
                basepath,
                "records",
                secure_filename(str(user.id) + "_" + str(record_data["word_id"]) + ".mp4"),
            )
            current_app.logger.info("ee")
            userwordrel = Userwordrel(
                user_id=user.id,
                word_id=record_data["word_id"],
                snd_path=upload_path,
                snd_abs=record_data["snd_abs"],
            )
            if checksum(recordData, record_data["md5"]):
                with open(upload_path, "wb") as out_record:
                    out_record.write(recordData)
        except Exception as e:
            current_app.logger.error(e)
            return {"status": 400, "message": "未成功上传录音文件"}, 400
        try:
            db.session.add(userwordrel)
            db.session.commit()  # SQLAlchemy用
        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            os.remove(upload_path)
            return {"status": 404, "message": "数据库查询异常"}, 404

        return {"status": 201, "message": "录入成功"}, 201


@user_record.route("/update")
class Update(MethodView):
    def get(self):
        return {"help": "Update the record"}

    @user_record.arguments(AuthUploadRecordSchema)
    @jwt_required(fresh=True)
    def post(self, record_data):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        userwordrel = Userwordrel.query.filter_by(
            user_id=user.id, word_id=record_data["word_id"]
        ).first()
        if userwordrel is not None:
            try:
                recordData = base64.b64decode(record_data["record_file"])
                update_path = os.path.join(
                    basepath,
                    "records",
                    secure_filename(
                        str(user.id) + "_" + str(record_data["word_id"]) + "new.mp4"
                    ),
                )
                if checksum(recordData, record_data["md5"]):
                    with open(update_path, "wb") as out_record:
                        out_record.write(recordData)
                userwordrel.update_at = datetime.now()
                userwordrel.snd_abs = record_data["snd_abs"]
                userwordrel.verified = True
            except Exception as e:
                current_app.logger.error(e)
                return {"status": 400, "message": "未上传录音文件"}, 400
            try:
                db.session.commit()  # SQLAlchemy用
            except Exception as e:
                # 数据库出错回滚
                db.session.rollback()
                current_app.logger.error(e)
                os.remove(update_path)
                return {"status": 404, "message": "数据库查询异常"}, 404

            return {"status": 200, "message": "更新成功"}, 200
