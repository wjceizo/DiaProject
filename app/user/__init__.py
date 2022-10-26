from flask import Blueprint
from flask_restful import Api, Resource

user = Blueprint('user', __name__)
user_api = Api(user)

from . import views, login
