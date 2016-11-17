import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("EMIS_SECRET_KEY") or "yabbadabbadoo!"
    JSON_AS_ASCII = False

    BOOTSTRAP_SERVE_LOCAL = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")

    @staticmethod
    def init_app(app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestingConfiguration(Configuration):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "data-test.sqlite")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
