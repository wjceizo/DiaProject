from ..schemas import AudioWordsSchema
from . import audio, MethodView, abort
from ..models import Word
from .. import db
from sqlalchemy.exc import IntegrityError
from flask import current_app


@audio.route("/words")
class Words(MethodView):
    def get(self):
        return 'get Create page'

    @audio.arguments(AudioWordsSchema)
    def post(self, word_data):
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
