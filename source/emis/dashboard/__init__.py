from flask import Blueprint
from starling.flask.template_filter import *


def format_property_name(
        string):
    return format_pathname(string, 50)


dashboard = Blueprint("dashboard", __name__,
    template_folder="templates",
    static_folder="static")
dashboard.add_app_template_filter(format_time_point)
dashboard.add_app_template_filter(format_pathname)
dashboard.add_app_template_filter(format_property_name)
dashboard.add_app_template_filter(format_uuid)


from . import views
