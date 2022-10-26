from flask_login import login_required, current_user
from . import main_api, Resource
from .. import db
from ..models import Role, User


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


main_api.add_resource(HelloWorld, '/')

