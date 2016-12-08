from flask import Blueprint


api_blueprint = Blueprint("api", __name__)


from . import aggregate_method, aggregate_query, api, domain, ping
