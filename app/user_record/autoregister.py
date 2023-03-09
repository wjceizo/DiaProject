from . import user_record, basepath, MethodView, abort
from ..models import User,Userlog
from ..schemas import AuthRegisterSchema, AutoRegisterSchema
from ..utils.randomCreateUsers import getRandomUserName
from .. import db
from sqlalchemy.exc import IntegrityError
from flask import current_app
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,create_refresh_token,get_jwt_identity

@user_record.route("/autoregister")
class AutoregisterView(MethodView):
    def get(self):
        return {"help": "AutoregisterView"}

    @user_record.arguments(AutoRegisterSchema)
    @user_record.response(200, AuthRegisterSchema)
    def post(self, user_data):
        adv, name, extrastr, password = getRandomUserName()
        username = adv + name + extrastr
        user = User(
            username=username,
            email=username + "@dialect.com",
            name=name,
            location=user_data["location"],
            lang=user_data["language"],
        )
        user.password = password
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
        return(user)
        # userid = user.id
        # access_token = create_access_token(identity=user.id, fresh=True)
        # refresh_token = create_refresh_token(user.id)
        # user_logs = Userlog(user_id=userid, location=user_data["location"])
        # try:
        #     db.session.add(user_logs)
        #     db.session.commit()  # SQLAlchemy用
        # except Exception as e:
        #     # 数据库出错回滚
        #     db.session.rollback()
        #     current_app.logger.error(e)
        #     abort(404, message='数据库查询异常')
        # return {'message': 'success', 'access_token': access_token,'refresh_token':refresh_token},200

