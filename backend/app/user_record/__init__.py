from flask import Blueprint
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os

user_record = Blueprint("Record", "records", description="user process records ")
basepath = os.path.abspath(os.getcwd())

record_path = os.path.join(basepath, "records")
if not os.path.exists(record_path):
    os.mkdir(record_path)

from . import autoregister, create, delete
