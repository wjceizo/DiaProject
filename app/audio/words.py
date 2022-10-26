from . import audio_api, Resource
from ..models import Word
from .. import db
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError
from flask import current_app

parser = reqparse.RequestParser()
parser.add_argument('stem', type=str, required=True, location='json', help='stem不能为空')
parser.add_argument('meaning', required=True, type=str, location='json', help='meaning不能为空')
parser.add_argument('comm', type=str, location='json')


class Words(Resource):
    def get(self):
        return 'get Create page'

    def post(self):
        args = parser.parse_args()
        word = Word(stem=args['stem'], meaning=args['meaning'], comm=args['comm']
                    )
        try:
            db.session.add(word)
            # db.commit()
            db.session.commit()  # SQLAlchemy用

        except IntegrityError as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            return {"status": 422, "message": "已存在该词汇"}

        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            return {"status": 404, "message": "数据库查询异常"}

        return {"status": 201, "message": "录入成功"}, 201


audio_api.add_resource(Words, '/words')
