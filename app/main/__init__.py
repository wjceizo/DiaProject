from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort


mainpage = Blueprint("Main", "main", description="main page")

from . import views

