from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from config import config
from .blocklist import BLOCKLIST


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                    "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    from .main import mainpage as main_blueprint
    api.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    api.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .audio import audio as audio_blueprint
    api.register_blueprint(audio_blueprint, url_prefix='/audio')

    # from .user import user as user_blueprint
    # app.register_blueprint(user_blueprint, url_prefix='/user')

    from .user_record import user_record as user_record_blueprint
    app.register_blueprint(user_record_blueprint, url_prefix='/userRecord')

    from .location import location as location_blueprint
    app.register_blueprint(location_blueprint, url_prefix='/location')

    return app
