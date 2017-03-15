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

    UPLOADS_DEFAULT_DEST = \
        os.environ.get("EMIS_UPLOADS_DEFAULT_DEST") or \
        tempfile.gettempdir()

    EMIS_RESULT_DATA = \
        os.environ.get("EMIS_RESULT_DATA") or \
        tempfile.gettempdir()

    EMIS_AGGREGATE_METHOD_HOST = "emis_aggregate_method"
    EMIS_AGGREGATE_QUERY_HOST = "emis_aggregate_query"
    EMIS_DOMAIN_HOST = "emis_domain"
    EMIS_LOG_HOST = "emis_log"
    EMIS_PROPERTY_HOST = "emis_property"
    EMIS_SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")

    # Default period after which an unused allocated resource will
    # be cleared, in hours.
    EMIS_RESOURCE_EXPIRATION_PERIOD = 2.0


    @staticmethod
    def init_app(
            app):

        Configuration.EMIS_SSL_CONTEXT.load_cert_chain(
            os.environ.get("EMIS_SSL_CERTIFICATE") or "/ssl/emis.crt",
            os.environ.get("EMIS_SSL_KEY") or "/ssl/emis.key")


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis-dev.sqlite")

    EMIS_AGGREGATE_METHOD_PORT = 5000
    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_LOG_PORT = 5000
    EMIS_PROPERTY_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)

        # DevelopmentConfiguration.EMIS_SSL_CONTEXT.load_cert_chain(
        #     os.environ.get("EMIS_SSL_CERTIFICATE"), or "/ssl/emis.crt",
        #     os.environ.get("EMIS_SSL_KEY") or "/ssl/emis.key")


class TestConfiguration(Configuration):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis-test.sqlite")

    EMIS_AGGREGATE_METHOD_PORT = 5000
    EMIS_AGGREGATE_QUERY_PORT = 5000
    EMIS_DOMAIN_PORT = 5000
    EMIS_LOG_PORT = 5000
    EMIS_PROPERTY_PORT = 5000


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        # TestConfiguration.EMIS_SSL_CONTEXT.load_cert_chain(
        #     os.environ.get("EMIS_SSL_CERTIFICATE"),
        #         # or "/ssl/localhost.crt",
        #     os.environ.get("EMIS_SSL_KEY"))
        #         # or "/ssl/localhost.key")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = os.environ.get("EMIS_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(), "emis.sqlite")

    EMIS_AGGREGATE_METHOD_PORT = 3031
    EMIS_AGGREGATE_QUERY_PORT = 3031
    EMIS_DOMAIN_PORT = 3031
    EMIS_LOG_PORT = 3031
    EMIS_PROPERTY_PORT = 3031


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        # ProductionConfiguration.EMIS_SSL_CONTEXT.load_cert_chain(
        #     os.environ.get("EMIS_SSL_CERTIFICATE")
        #         or "/ssl/emisdev_geo_uu_nl.crt",
        #     os.environ.get("EMIS_SSL_KEY")
        #         or "/ssl/emisdev_geo_uu_nl.key")


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
