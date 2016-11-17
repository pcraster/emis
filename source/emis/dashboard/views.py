from flask import jsonify, render_template
from . import dashboard


@dashboard.route("/")
def dashboard():
    return render_template("index.html")
