import requests
from flask import current_app, request
from . import api_blueprint


def aggregate_methods_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["AGGREGATE_METHOD_HOST"],
        current_app.config["AGGREGATE_METHOD_PORT"],
        route)


# - Get collection of all queries
@api_blueprint.route(
    "/aggregate_methods",
    methods=["GET"])
def aggregate_methods():

    uri = aggregate_methods_uri("aggregate_methods")

    assert request.method == "GET"

    response = requests.get(uri)

    return response.text, response.status_code
