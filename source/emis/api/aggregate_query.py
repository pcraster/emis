import requests
from flask import jsonify, request
from . import api_blueprint


# - Post a query
# - Get collection of all queries
@api_blueprint.route(
    "/aggregate_queries",
    methods=["GET", "POST"])
def aggregate_queries_all():
    uri = "http://aggregate_query:5000/aggregate_queries"

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
    uri = "http://aggregate_query:5000/aggregate_queries/{}/{}".format(
        user_id, query_id)
    response = requests.get(uri)

    return response.text, response.status_code


# - Get queries by user-id
@api_blueprint.route(
    "/aggregate_queries/<uuid:user_id>",
    methods=["GET"])
def aggregate_queries(
        user_id):
    uri = "http://aggregate_query:5000/aggregate_queries/{}".format(user_id)
    response = requests.get(uri)

    return response.text, response.status_code
