import requests
from flask import current_app
from . import api_blueprint


def properties_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_PROPERTY_HOST"],
        current_app.config["EMIS_PROPERTY_PORT"],
        route)


# - Get collection of all properties
@api_blueprint.route(
    "/properties",
    methods=["GET"])
def properties():

    uri = properties_uri("properties")
    response = requests.get(uri)

    return response.text, response.status_code


# - Get property by property-id
@api_blueprint.route(
    "/properties/<uuid:property_id>",
    methods=["GET"])
def property(
        property_id):

    uri = properties_uri("properties/{}".format(property_id))
    response = requests.get(uri)

    return response.text, response.status_code
