import requests
from flask import current_app, flash, jsonify, render_template, url_for
from . import dashboard


# def aggregate_methods_uri(
#         route):
#     route = route.lstrip("/")
#     return "http://{}:{}/{}".format(
#         current_app.config["EMIS_AGGREGATE_METHOD_HOST"],
#         current_app.config["EMIS_AGGREGATE_METHOD_PORT"],
#         route)


def aggregate_queries_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_QUERY_HOST"],
        current_app.config["EMIS_AGGREGATE_QUERY_PORT"],
        route)


def domains_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_DOMAIN_HOST"],
        current_app.config["EMIS_DOMAIN_PORT"],
        route)


def logs_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_LOG_HOST"],
        current_app.config["EMIS_LOG_PORT"],
        route)


def properties_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_PROPERTY_HOST"],
        current_app.config["EMIS_PROPERTY_PORT"],
        route)


@dashboard.route("/")
def dashboard():

    domains = []
    logs = []
    # methods = []
    properties = []
    queries = []
    results = []

    # try:
    #     uri = aggregate_methods_uri("aggregate_methods")
    #     response = requests.get(uri)
    #     methods = response.json()
    # except Exception as exception:
    #     flash("error contacting aggregate methods service: {}".format(
    #         exception))

    try:
        uri = domains_uri("domains")
        response = requests.get(uri)
        domains = response.json()
    except Exception as exception:
        flash("error contacting domain service: {}".format(exception))

    try:
        uri = aggregate_queries_uri("aggregate_queries")
        response = requests.get(uri)
        queries = response.json()

        uri = aggregate_queries_uri("aggregate_query_messages")
        response = requests.get(uri)
        messages = response.json()

        uri = aggregate_queries_uri("aggregate_query_results")
        response = requests.get(uri)
        results = response.json()
    except Exception as exception:
        flash("error contacting aggregate queries service: {}".format(
            exception))

    try:
        uri = properties_uri("properties")
        response = requests.get(uri)
        properties = response.json()
    except Exception as exception:
        flash("error contacting properties service: {}".format(exception))

    try:
        uri = logs_uri("logs")
        response = requests.get(uri)
        logs = response.json()
    except Exception as exception:
        flash("error contacting log service: {}".format(exception))


    return render_template("index.html",
        # methods=methods,
        domains=domains,
        properties=properties,
        queries=queries,
        messages=messages,
        results=results,
        logs=logs)
