import os


class Config:
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in memory db will do for tests


class TestConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):

    def __init__(self, app):
        path = os.path.join(app.instance_path, "development.db")
        Config.SQLALCHEMY_DATABASE_URI = "sqlite:///" + path


class ProductionConfig(Config):
    pass
