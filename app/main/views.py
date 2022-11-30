from . import mainpage,MethodView,abort
from .. import db
from ..models import User
from flask_restful import reqparse
from flask import current_app


@mainpage.route("/")
class Mainpage(MethodView):
    def get(self):
        try:
            return {"message":"Hello, world"}
        except KeyError:
            abort(404, message="Not found.")