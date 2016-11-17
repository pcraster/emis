from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from .configuration import configuration


db = SQLAlchemy()


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    Bootstrap(app)


    db.init_app(app)


    # Attach routes and custom error pages.
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
