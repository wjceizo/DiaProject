from flask import Blueprint
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os

user_record = Blueprint("Record", "records", description="user process records ")
basepath = os.path.abspath(os.getcwd())

from . import create, delete
