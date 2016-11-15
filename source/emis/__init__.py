from flask import Flask, jsonify, request
from flask.json import dumps


app = Flask(__name__)
app.config.from_object("emis.default_settings")


@app.route("/ping")
def ping():
    return jsonify(response="pong"), 200
