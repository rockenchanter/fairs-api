class Config:
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in memory db will do for tests


class TestConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass
