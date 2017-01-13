import json
import requests
from werkzeug.exceptions import *
from flask import current_app, request
from flask_uploads import UploadNotAllowed
from . import api_blueprint
from .. import uploaded_domains


def domains_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_DOMAIN_HOST"],
        current_app.config["EMIS_DOMAIN_PORT"],
        route)


# - Post a domain
# - Get collection of all domains
@api_blueprint.route(
    "/domains",
    methods=["GET", "POST"])
def domains_all():
    uri = domains_uri("domains")

    if request.method == "GET":

        # TODO This requires the admin API key!
        response = requests.get(uri)

    elif request.method == "POST":
        # The data passed in should contain a file containing a domain
        # dataset and a JSON snippet with some additional information.
        # We must do the folowing:
        # - Grab the user's id
        # - Save the file
        # - Post some metadata to the domain service
        # - Return the result of posting the meta data to the client

        try:
            data = json.loads(request.form["data"])
            # request.files["domain"] -> FileStorage
            # request.files["domain"].name -> domain
            # request.files["domain"].filename -> domain.csv
            filename = uploaded_domains.save(
                request.files["domain"], folder=data["user"])
            pathname = uploaded_domains.path(filename)

            payload = {
                "user": data["user"],
                "name": request.files["domain"].filename,
                "pathname": pathname
            }

            response = requests.post(uri, json={"domain": payload})

        except UploadNotAllowed:
            raise BadRequest("uploading {} not allowed".format(
                request.files["domain"]))
        except Exception as exception:
            raise BadRequest(
                "invalid upload request, exception: {}, form: {}, "
                "files: {}".format(exception, request.form, request.files))

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
