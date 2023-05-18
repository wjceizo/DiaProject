from flask.views import MethodView
from flask_smorest import Blueprint, abort

auth = Blueprint("Auth", "auths", description="control auths")

from . import update, register, login, user