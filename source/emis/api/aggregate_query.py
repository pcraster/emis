import requests
from flask import current_app, request
import pika
from . import api_blueprint


def aggregate_queries_uri(
        route):
    route = route.lstrip("/")
    return "http://{}:{}/{}".format(
        current_app.config["EMIS_AGGREGATE_QUERY_HOST"],
        current_app.config["EMIS_AGGREGATE_QUERY_PORT"],
        route)


# - Post a query
# - Get collection of all queries
@api_blueprint.route(
    "/aggregate_queries",
    methods=["GET", "POST"])
def aggregate_queries_all():

    uri = aggregate_queries_uri("aggregate_queries")

    if request.method == "GET":
        # TODO This requires the admin API key!
        response = requests.get(uri)
    elif request.method == "POST":
        response = requests.post(uri, json=request.get_json())

        # If the query's 'edit_status' is 'final', a message must be posted
        # that the query should be executed.

        if response.status_code == 201:
            query_dict = response.json()["aggregate_query"]

            if query_dict["edit_status"] == "final":
                query_uri = aggregate_queries_uri(query_dict["_links"]["self"])

                # Mark query's execute_status as 'queued'.
                payload = {
                    "execute_status": "queued"
                }
                response = requests.patch(query_uri, json=payload)

                if response.status_code == 200:

                    # Post message in rabbitmq and be done with it.
                    credentials = pika.PlainCredentials(
                        current_app.config["EMIS_RABBITMQ_DEFAULT_USER"],
                        current_app.config["EMIS_RABBITMQ_DEFAULT_PASS"]
                    )

                    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host="rabbitmq",
                            virtual_host=current_app.config[
                                "EMIS_RABBITMQ_DEFAULT_VHOST"],
                            credentials=credentials,
                            # Keep trying for 8 minutes.
                            connection_attempts=100,
                            retry_delay=5  # Seconds
                    ))
                    channel = connection.channel()
                    channel.queue_declare(
                        queue="execute_query")
                    channel.basic_publish(
                        exchange="",
                        routing_key="execute_query",
                        body="{}".format(query_uri)
                    )
                    connection.close()


    return response.text, response.status_code


# - Get query by user-id and query-id
@api_blueprint.route(
    "/aggregate_queries/<uuid:user_id>/<uuid:query_id>",
    methods=["GET"])
def aggregate_query(
        user_id,
        query_id):

    uri = aggregate_queries_uri("aggregate_queries/{}/{}".format(
        user_id, query_id))
    response = requests.get(uri)

    return response.text, response.status_code


# - Get queries by user-id
@api_blueprint.route(
    "/aggregate_queries/<uuid:user_id>",
    methods=["GET"])
def aggregate_queries(
        user_id):
    uri = aggregate_queries_uri("aggregate_queries/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
