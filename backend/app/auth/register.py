from . import auth, MethodView, abort
from ..models import User
from ..schemas import AuthRegisterSchema
from .. import db
from sqlalchemy.exc import IntegrityError
from flask import current_app


@auth.route("/")
class Helloyou(MethodView):
    def get(self):
        return {"status": 200}


@auth.route("/register")
class RegisterView(MethodView):
    def get(self):
        return {"help": "RegisterView"}

    @auth.arguments(AuthRegisterSchema)
    @auth.response(200, AuthRegisterSchema)
    def post(self, auth_data):
        user = User(
            username=auth_data["username"],
            email=auth_data["email"],
            name=auth_data["name"],
            location=auth_data["location"],
            lang=auth_data["lang"],
            sex=auth_data["sex"],
            work=auth_data["work"],
            role_id = 2
        )
        user.password = auth_data["password"]
        try:
            db.session.add(user)
            # db.commit()
            db.session.commit()  # SQLAlchemy用

        except IntegrityError as e:
            # 数据库出错回滚
            db.session.rollback()
            # 用户名重复，记录错误日志
            current_app.logger.error(e)
            abort(422, message="用户已注册")

        except Exception as e:
            # 数据库出错回滚
            db.session.rollback()
            current_app.logger.error(e)
            abort(404, message="数据库查询异常")
        user = User.query.filter_by(username=user.username).first()
        return user,201
