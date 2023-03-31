from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os

audio = Blueprint("Audio", "audio", description="audio processing")
basepath = os.path.abspath(os.getcwd())

from . import words