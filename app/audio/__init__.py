from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort


audio = Blueprint("Audio", "audio", description="audio processing")

from . import words