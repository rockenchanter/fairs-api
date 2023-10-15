import os


class Config:
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in memory db will do for tests
    ADMIN_EMAIL = 'admin@example.com'
    ADMIN_PASSWORD = 'root'


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    def __init__(self, app):
        path = os.path.join(app.instance_path, "test.db")
        Config.SQLALCHEMY_DATABASE_URI = "sqlite:///" + path
        Config.ASSETS_DIR = os.path.join(app.instance_path, "assets/tests/")


class DevelopmentConfig(TestConfig):

    def __init__(self, app):
        super().__init__(app)
        path = os.path.join(app.instance_path, "development.db")
        Config.SQLALCHEMY_DATABASE_URI = "sqlite:///" + path
        Config.ASSETS_DIR = os.path.join(app.instance_path, "assets/")


class ProductionConfig(Config):
    pass
