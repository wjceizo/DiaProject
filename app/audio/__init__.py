from flask import Blueprint
from flask_restful import Api, Resource

audio = Blueprint('audio', __name__)
audio_api = Api(audio)

from . import words