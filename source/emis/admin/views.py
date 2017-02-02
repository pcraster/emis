import json
import sys
from flask import current_app, jsonify, request
import pika
from . import admin_blueprint


@admin_blueprint.route("/ping")
def ping():
    return jsonify(response="pong"), 200


@admin_blueprint.route(
    "/properties/scan",
    methods=["POST"])
def scan_properties():

    json_as_dict = request.get_json()
    message = json.dumps(json_as_dict)

    # Post message in rabbitmq and be done with it.
    credentials = pika.PlainCredentials(
        current_app.config["EMIS_RABBITMQ_DEFAULT_USER"],
        current_app.config["EMIS_RABBITMQ_DEFAULT_PASS"]
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="rabbitmq",
        virtual_host=current_app.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
        credentials=credentials,
        # Keep trying for 8 minutes.
        connection_attempts=100,
        retry_delay=5  # Seconds
    ))
    channel = connection.channel()
    channel.queue_declare(
        queue="scan")
    channel.basic_publish(
        exchange="",
        routing_key="scan",
        body=message
    )

    sys.stdout.write("sent {}\n".format(message))
    sys.stdout.flush()
    connection.close()


    return jsonify(response="request for scan posted"), 201


@admin_blueprint.route(
    "/resources/clear_expired",
    methods=["POST"])
def clear_expired_resources():

    json_as_dict = request.get_json(silent=True)

    if json_as_dict:
        expiration_period = float(json_as_dict["expiration_period"])
    else:
        expiration_period = current_app.config[
            "EMIS_RESOURCE_EXPIRATION_PERIOD"]


    payload = json.dumps({
        "expiration_period": expiration_period
    })

    # Post message in rabbitmq and be done with it.
    credentials = pika.PlainCredentials(
        current_app.config["EMIS_RABBITMQ_DEFAULT_USER"],
        current_app.config["EMIS_RABBITMQ_DEFAULT_PASS"]
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="rabbitmq",
        virtual_host=current_app.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
        credentials=credentials,
        # Keep trying for 8 minutes.
        connection_attempts=100,
        retry_delay=5  # Seconds
    ))
    channel = connection.channel()
    channel.queue_declare(
        queue="clear_expired_resource",
        durable=False)
    channel.basic_publish(
        exchange="",
        routing_key="clear_expired_resource",
        body=payload,
        properties=pika.BasicProperties(
            delivery_mode=1,  # Non-persistent messages.
        )
    )

    sys.stdout.write("sent {}\n".format(payload))
    sys.stdout.flush()
    connection.close()

    return jsonify(response="request to clear expired resources posted"), 201
