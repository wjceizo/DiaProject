from flask import Blueprint
from flask_restful import Api, Resource

auth = Blueprint('auth', __name__)
auth_api = Api(auth)

from . import register, login, user,update
