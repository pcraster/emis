import requests
from flask import current_app
from . import api_blueprint


def aggregate_queries_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_QUERY_HOST"],
        current_app.config["EMIS_AGGREGATE_QUERY_PORT"],
        route)


# - Get collection of all query messages
@api_blueprint.route(
    "/aggregate_query_messages",
    methods=["GET"])
def aggregate_query_messages():

    uri = aggregate_queries_uri("aggregate_query_messages")

    # TODO This requires the admin API key!
    response = requests.get(uri)


    return response.text, response.status_code


# - Get message by query-id
@api_blueprint.route(
    "/aggregate_query_messages/<uuid:query_id>",
    methods=["GET"])
def aggregate_query_message(
        query_id):
    uri = aggregate_queries_uri("aggregate_query_messages/{}".format(query_id))
    response = requests.get(uri)

    return response.text, response.status_code
