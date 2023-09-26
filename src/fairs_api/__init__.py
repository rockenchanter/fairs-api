from flask import Flask
import os

from .models import db
from . import config


def create_app(mode='development'):
    app = Flask(__name__, instance_relative_config=True)

    if mode == 'development':
        app.config.from_object(config.DevelopmentConfig(app))
    elif mode == 'test':
        app.config.from_object(config.TestConfig())
    else:
        app.config.from_object(config.ProductionConfig())

    # create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print("Could not create instance path")

    # initialize Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
