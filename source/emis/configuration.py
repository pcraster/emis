import os
import ssl
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("EMIS_SECRET_KEY") or "yabbadabbadoo!"
    JSON_AS_ASCII = False

    BOOTSTRAP_SERVE_LOCAL = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AGGREGATE_METHOD_HOST = "aggregate_method"
    AGGREGATE_QUERY_HOST = "aggregate_query"

    SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23)


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis-dev.sqlite")

    AGGREGATE_METHOD_PORT = 5000
    AGGREGATE_QUERY_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)

        DevelopmentConfiguration.SSL_CONTEXT.load_cert_chain(
            os.environ.get("EMIS_SSL_CERTIFICATE")
                or "/ssl/localhost.crt",
            os.environ.get("EMIS_SSL_KEY")
                or "/ssl/localhost.key")


class TestingConfiguration(Configuration):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis-test.sqlite")

    AGGREGATE_METHOD_PORT = 5000
    AGGREGATE_QUERY_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        TestingConfiguration.SSL_CONTEXT.load_cert_chain(
            os.environ.get("EMIS_SSL_CERTIFICATE")
                or "/ssl/localhost.crt",
            os.environ.get("EMIS_SSL_KEY")
                or "/ssl/localhost.key")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis.sqlite")

    AGGREGATE_METHOD_PORT = 3031
    AGGREGATE_QUERY_PORT = 3031


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        ProductionConfiguration.SSL_CONTEXT.load_cert_chain(
            os.environ.get("EMIS_SSL_CERTIFICATE")
                or "/ssl/emisdev_geo_uu_nl.crt",
            os.environ.get("EMIS_SSL_KEY")
                or "/ssl/emisdev_geo_uu_nl.key")


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
