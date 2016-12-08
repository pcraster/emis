import requests
from flask import current_app, request
from . import api_blueprint


def domains_uri(
        route):
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_DOMAIN_HOST"],
        current_app.config["EMIS_DOMAIN_PORT"],
        route)


# - Get collection of all domains
@api_blueprint.route(
    "/domains",
    methods=["GET"])
def domains_all():

    uri = domains_uri("domains")

    # TODO This requires the admin API key!
    response = requests.get(uri)

    return response.text, response.status_code


# - Get domain by user-id and domain-id
@api_blueprint.route(
    "/domains/<uuid:user_id>/<uuid:domain_id>",
    methods=["GET"])
def domain(
        user_id,
        domain_id):

    uri = domains_uri("domains/{}/{}".format(
        user_id, domain_id))
    response = requests.get(uri)

    return response.text, response.status_code


# - Get domains by user-id
@api_blueprint.route(
    "/domains/<uuid:user_id>",
    methods=["GET"])
def domains(
        user_id):
    uri = domains_uri("domains/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
