import os.path
import requests
from flask import current_app, request, send_from_directory
import pika
from . import api_blueprint


def aggregate_queries_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_QUERY_HOST"],
        current_app.config["EMIS_AGGREGATE_QUERY_PORT"],
        route)


# - Get collection of all query results
@api_blueprint.route(
    "/aggregate_query_results",
    methods=["GET"])
def aggregate_query_results():

    uri = aggregate_queries_uri("aggregate_query_results")

    # TODO This requires the admin API key!
    response = requests.get(uri)


    return response.text, response.status_code


# - Get result by query-id
@api_blueprint.route(
    "/aggregate_query_results/<uuid:query_id>",
    methods=["GET"])
def aggregate_query_result(
        query_id):
    uri = aggregate_queries_uri("aggregate_query_results/{}".format(query_id))
    response = requests.get(uri)

    return response.text, response.status_code


# - Get the result dataset by user-id and query-id
@api_blueprint.route(
    "/aggregate_query_results/<uuid:user_id>/<uuid:query_id>/<path:filename>",
    methods=["GET"])
def download(
        user_id,
        query_id,
        filename):
    results_pathname = os.path.join(current_app.config["EMIS_RESULT_DATA"],
        str(user_id), str(query_id))

    return send_from_directory(directory=results_pathname, filename=filename)
