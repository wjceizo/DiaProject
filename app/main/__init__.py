from flask import Blueprint
from flask_restful import Api, Resource


main = Blueprint('main', __name__)
main_api = Api(main)


from . import views, errors
# from ..models import Permission
#
#
# @main.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)
