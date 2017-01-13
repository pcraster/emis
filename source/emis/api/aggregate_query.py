import datetime
import json
import sys
import traceback
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


def log(
        message,
        priority="low",
        severity="non_critical"):

    try:

        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "priority": priority,
            "severity": severity,
            "message": message
        }

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
                credentials=credentials)
        )
        channel = connection.channel()

        properties = pika.BasicProperties()
        properties.content_type = "application/json"
        properties.durable = False

        channel.basic_publish(
            exchange="alerts",
            properties=properties,
            routing_key="{}.{}".format(priority, severity),
            body=json.dumps(payload)
        )
        connection.close()

    except Exception as exception:

        sys.stderr.write("Error while sending log message to broker\n")
        sys.stderr.write("Log message: {}\n".format(message))
        sys.stderr.write("Error message: {}\n".format(str(exception)))
        sys.stderr.write("{}\n".format(traceback.format_exc()))
        sys.stderr.flush()


# - Post a query
# - Get collection of all queries
@api_blueprint.route(
    "/aggregate_queries",
    methods=["GET", "POST"])
def aggregate_queries_all():

    uri = aggregate_queries_uri("aggregate_queries")

    if request.method == "GET":
        log("get aggregate queries")
        # TODO This requires the admin API key!
        response = requests.get(uri)
    elif request.method == "POST":
        log("post aggregate query")
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

    log("get aggregate query {} for user {}".format(query_id, user_id))

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

    log("get aggregate queries user {}".format(user_id))

    uri = aggregate_queries_uri("aggregate_queries/{}".format(user_id))
    response = requests.get(uri)

    return response.text, response.status_code
