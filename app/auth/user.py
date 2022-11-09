from . import auth_api, Resource
from ..models import User, Userlog
from .. import db
from flask_restful import reqparse
from flask import current_app


class UserView(Resource):
    def get(self):
        pagination = User.query.order_by(User.username).paginate(page=3, per_page=10, error_out=False)
        users = pagination.items
        # https://blog.csdn.net/qq_43193386/article/details/120172469
        return {'hello': 'you'}


auth_api.add_resource(UserView, '/users')
