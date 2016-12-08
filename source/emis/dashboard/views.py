import requests
from flask import current_app, flash, jsonify, render_template, url_for
from . import dashboard


def aggregate_methods_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_METHOD_HOST"],
        current_app.config["EMIS_AGGREGATE_METHOD_PORT"],
        route)


def aggregate_queries_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_QUERY_HOST"],
        current_app.config["EMIS_AGGREGATE_QUERY_PORT"],
        route)


def domains_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_DOMAIN_HOST"],
        current_app.config["EMIS_DOMAIN_PORT"],
        route)


@dashboard.route("/")
def dashboard():

    domains = []
    methods = []
    queries = []

    try:
        uri = aggregate_methods_uri("aggregate_methods")
        response = requests.get(uri)
        methods = response.json()
    except Exception as exception:
        flash("error contacting aggregate methods service: {}".format(
            exception))

    try:
        uri = domains_uri("domains")
        domains = requests.get(uri)
        queries = domains.json()
    except Exception as exception:
        flash("error contacting domain service: {}".format(exception))

    try:
        uri = aggregate_queries_uri("aggregate_queries")
        response = requests.get(uri)
        queries = response.json()
    except Exception as exception:
        flash("error contacting aggregate queries service: {}".format(
            exception))

    return render_template("index.html",
        methods=methods,
        domains=domains,
        queries=queries)
