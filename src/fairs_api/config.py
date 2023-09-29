import os


class Config:
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in memory db will do for tests


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    def __init__(self, app):
        app.static_folder = os.path.join(app.instance_path, "static/")


class DevelopmentConfig(TestConfig):

    def __init__(self, app):
        super().__init__(app)
        path = os.path.join(app.instance_path, "development.db")
        Config.SQLALCHEMY_DATABASE_URI = "sqlite:///" + path
        TestConfig.TESTING = False


class ProductionConfig(Config):
    pass
