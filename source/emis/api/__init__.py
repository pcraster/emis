from flask import Blueprint


api_blueprint = Blueprint("api", __name__)


from . import aggregate_method, aggregate_query, aggregate_query_result, \
api, domain, ping, property
