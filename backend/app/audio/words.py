from ..schemas import AudioWordsSchema, AudioImageSchema
from . import audio, MethodView, abort, basepath
from ..models import Word, User
from .. import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app
import base64, os
from werkzeug.utils import secure_filename


def convert_base64(num):

    # 选择要转换的图片
    selected_image = "record_imgs/" + str(num) + ".png"

    # 打开文件并将其转换为Base64编码
    with open(selected_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    # 将Base64编码添加到data URI字符串中
    data_uri = f"data:image/png;base64,{encoded_string}"

    # 打印Base64编码的data URI字符串
    return data_uri


@audio.route("/word")
class Words(MethodView):
    @audio.arguments(AudioWordsSchema)
    @jwt_required(fresh=True)
    def post(self, word_data):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role_id != 1:
            return {"status": 403, "message": "权限不足"}, 403
        current_app.logger.info(word_data)
        
        word = Word(
            stem=word_data["stem"], meaning=word_data["meaning"]
        )

        if "lang" in word_data:
            word.lang = word_data["lang"]
        if "translation" in word_data:
            word.translation = word_data["translation"]
        if "prompt" in word_data:
            word.prompt = word_data["prompt"]


        try:
            db.session.add(word)
            db.session.commit()  

        except IntegrityError as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            abort(422, message="已存在该词汇")

        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            abort(404, message="数据库查询异常")

        return {"status": 201, "message": "录入成功"}, 201


@audio.route("/word/<word_id>/image")
class UploadImage(MethodView):
    @audio.arguments(AudioImageSchema)
    @jwt_required(fresh=True)
    def post(self, image_data, word_id):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role_id != 1:
            return {"status": 403, "message": "权限不足"}, 403
        try:
            word = Word.query.filter_by(id=word_id).first()
        except Exception as e:
            return {"status": 404, "message": "未找到该词汇"}, 404
        try:
            imageData = base64.b64decode(image_data["image_file"])
            upload_path = os.path.join(
                basepath,
                "record_imgs",
                secure_filename(str(word.id) + ".png"),
            )
            with open(upload_path, "wb") as out_image:
                out_image.write(imageData)
            word.image_path = upload_path
        except Exception as e:
            current_app.logger.error(e)
            return {"status": 400, "message": "未成功上传图片文件"}, 400
        try:
            db.session.add(word)
            db.session.commit()  # SQLAlchemy用
        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            os.remove(upload_path)
            return {"status": 404, "message": "数据库查询异常"}, 404
        
        return {"message": "ok"}


@audio.route("/word/<word_id>")
class WordById(MethodView):
    def get(self, word_id):
        word = Word.query.filter_by(id=word_id).first()
        return {
            "id": word.id,
            "stem": word.stem,
            "stemtranslation": word.translation,
            # "img": convert_base64(word.id),
            "desc": word.meaning,
            "prompt": word.prompt,
        }
