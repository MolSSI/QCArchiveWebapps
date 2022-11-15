import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    QCFRACTAL_URI = "https://api.qcarchive.molssi.org"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
