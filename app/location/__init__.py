from flask import Blueprint
from flask.views import MethodView
from flask_smorest import Blueprint, abort

location = Blueprint("Location", "locations", description="get dialect locations")

from . import userLocation