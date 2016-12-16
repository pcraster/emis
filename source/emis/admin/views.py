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

    dict_ = request.get_json()

    try:
        pathname = dict_["pathname"]
    except Exception as exception:
        raise BadRequest(exception)


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
        body="{}".format(pathname)
    )
    print("sent {}".format(pathname))
    connection.close()


    return jsonify(response="request for scan posted"), 201
