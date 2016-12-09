from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, patch_request_class, UploadSet
from .configuration import configuration


def app_errorhandler(
        exception):
    response = jsonify({
            "status_code": exception.code,
            "message": exception.description,
        })
    return response, exception.code


uploaded_domains = UploadSet(
    name="domain",
    extensions=("csv"))
db = SQLAlchemy()


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)


    @app.errorhandler(400)
    def bad_request(exception):
        return app_errorhandler(exception)


    @app.errorhandler(404)
    def not_found(exception):
        return app_errorhandler(exception)


    @app.errorhandler(405)
    def method_not_allowed(exception):
        return app_errorhandler(exception)


    @app.errorhandler(422)
    def unprocessable_entity(exception):
        return app_errorhandler(exception)


    @app.errorhandler(500)
    def internal_server_error(exception):
        return app_errorhandler(exception)


    Bootstrap(app)

    configure_uploads(app, (uploaded_domains,))
    # Limit uploads to 32 Mb.
    patch_request_class(app, 32 * 1024 * 1024)

    db.init_app(app)


    # Attach routes and custom error pages.
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    with app.app_context():
        # http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block.
        db.create_all()


    return app
