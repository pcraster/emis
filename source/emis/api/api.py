from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/api")
def api():
    return jsonify({
            "resources": {
                # "aggregate_methods": {
                #     "route": "/aggregate_methods"
                # },
                "aggregate_queries": {
                    "route": "/aggregate_queries"
                },
                "aggregate_query_messages": {
                    "route": "/aggregate_query_messages"
                },
                "aggregate_query_results": {
                    "route": "/aggregate_query_results"
                },
                "domains": {
                    "route": "/domains"
                },
                "properties": {
                    "route": "/properties"
                },
            }
        }), 200
