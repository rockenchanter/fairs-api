import os


class Config:
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in memory db will do for tests

    def __init__(self, app):
        Config.ASSETS_DIR = os.path.join(app.instance_path, "assets/")


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    def __init__(self, app):
        super().__init__(app)


class DevelopmentConfig(TestConfig):

    def __init__(self, app):
        super().__init__(app)
        path = os.path.join(app.instance_path, "development.db")
        Config.SQLALCHEMY_DATABASE_URI = "sqlite:///" + path


class ProductionConfig(Config):
    pass
