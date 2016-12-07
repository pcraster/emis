import requests
from flask import current_app, flash, jsonify, render_template, url_for
from . import dashboard


def aggregate_queries_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["AGGREGATE_QUERY_HOST"],
        current_app.config["AGGREGATE_QUERY_PORT"],
        route)


@dashboard.route("/")
def dashboard():

    methods = []
    queries = []

    try:
        uri = aggregate_queries_uri("aggregate_methods")
        response = requests.get(uri)
        methods = response.json()
    except Exception as exception:
        flash("error contacting aggregate_methods: {}".format(exception))

    try:
        uri = aggregate_queries_uri("aggregate_queries")
        response = requests.get(uri)
        queries = response.json()
    except Exception as exception:
        flash("error contacting aggregate_queries: {}".format(exception))

    return render_template("index.html", methods=methods, queries=queries)
