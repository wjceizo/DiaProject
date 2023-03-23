from ..schemas import AudioWordsSchema
from . import audio, MethodView, abort
from ..models import Word
from .. import db
from sqlalchemy.exc import IntegrityError
from flask import current_app
import base64, os

def convert_base64(num):

    # 选择要转换的图片
    selected_image = 'record_imgs/'+str(num)+'.png'

    # 打开文件并将其转换为Base64编码
    with open(selected_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    # 将Base64编码添加到data URI字符串中
    data_uri = f"data:image/png;base64,{encoded_string}"

    # 打印Base64编码的data URI字符串
    return data_uri


@audio.route("/word")
class Words(MethodView):
    # def get(self):
    #     return 'word'

    @audio.arguments(AudioWordsSchema)
    def post(self, word_data):
        current_app.logger.info(word_data)
        word = Word(stem=word_data['stem'], meaning=word_data['meaning'], comm=word_data['comm']
                    )
        try:
            db.session.add(word)
            # db.commit()
            db.session.commit()  # SQLAlchemy用

        except IntegrityError as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            abort(422, message='已存在该词汇')

        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            abort(404, message='数据库查询异常')

        return {"status": 201, "message": "录入成功"}, 201

@audio.route("/word/<word_id>")
class WordById(MethodView):
    def get(self, word_id):
        word = Word.query.filter_by(id=word_id).first()
        return {"id" : word.id, "stem":word.stem, "stemtranslation":word.comm, "img": convert_base64(word.id), "desc": word.meaning}