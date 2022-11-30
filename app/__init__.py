from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .audio import audio as audio_blueprint
    app.register_blueprint(audio_blueprint, url_prefix='/audio')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
