import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:

    # Flask
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True


class TestingConfiguration(Configuration):

    TESTING = True


class ProductionConfiguration(Configuration):

    pass


configuration = {
    "development": DevelopmentConfiguration,
    "testing": TestingConfiguration,
    "production": ProductionConfiguration
}
