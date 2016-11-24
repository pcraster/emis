import requests
from flask import current_app, jsonify, request
from . import api_blueprint


def aggregate_queries_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["AGGREGATE_QUERY_HOST"],
        current_app.config["AGGREGATE_QUERY_PORT"],
        route)


# - Post a query
# - Get collection of all queries
@api_blueprint.route(
    "/aggregate_queries",
    methods=["GET", "POST"])
def aggregate_queries_all():

    uri = aggregate_queries_uri("aggregate_queries")

    if request.method == "GET":
        # TODO This requires the admin API key!
        response = requests.get(uri)
    elif request.method == "POST":
        response = requests.post(uri, json=request.get_json())

    return response.text, response.status_code


# - Get query by user-id and query-id
@api_blueprint.route(
    "/aggregate_queries/<uuid:user_id>/<uuid:query_id>",
    methods=["GET"])
def aggregate_query(
        user_id,
        query_id):

    uri = aggregate_queries_uri("aggregate_queries/{}/{}".format(
        user_id, query_id))
    response = requests.get(uri)

    return response.text, response.status_code


# - Get queries by user-id
@api_blueprint.route(
    "/aggregate_queries/<uuid:user_id>",
    methods=["GET"])
def aggregate_queries(
        user_id):
    uri = aggregate_queries_uri("aggregate_queries/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
