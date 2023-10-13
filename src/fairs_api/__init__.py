from flask import Flask, session
import os

from .models import db
from .validations import get_from_locale
from . import config


def handle_400(exc):
    return {"errors": {
        "generic": get_from_locale("bad_request", session["locale"])
    }}, 400


def handle_401(exc):
    return {"errors": {
        "generic": get_from_locale("invalid_credentials", session["locale"])
    }}, 401


def handle_404(exc):
    return {"errors": {
        "generic": get_from_locale("not_found", session["locale"])
    }}, 404


def create_app(mode="development"):
    app = Flask(__name__, instance_relative_config=True)

    if mode == "development":
        app.config.from_object(config.DevelopmentConfig(app))
        from flask import send_from_directory

        @app.route("/assets/<path:filename>")
        def serve_static(filename):
            return send_from_directory(
                app.config["ASSETS_DIR"], os.path.basename(filename)
            )
    elif mode == "test":
        app.config.from_object(config.TestConfig(app))
    else:
        app.config.from_object(config.ProductionConfig())

    # create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config["ASSETS_DIR"])
    except OSError:
        pass

    # configure session
    @app.before_request
    def set_session_defaults():
        if "locale" not in session:
            session["locale"] = "en"

    # initialize Flask-SQLAlchemy
    db.init_app(app)
    if app.config["TESTING"]:
        with app.app_context():
            db.create_all()

    # register error handlers
    app.register_error_handler(400, handle_400)
    app.register_error_handler(401, handle_401)
    app.register_error_handler(404, handle_404)

    # register blueprints
    from .auth_bp import bp as auth
    from .hall_bp import bp as hall
    from .image_bp import bp as image
    from .stall_bp import bp as stall
    app.register_blueprint(auth)
    app.register_blueprint(hall)
    app.register_blueprint(stall)
    return app
