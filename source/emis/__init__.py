from flask import Flask
from .configuration import configuration


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
