from server import app


app.run(host="0.0.0.0", ssl_context=app.config["EMIS_SSL_CONTEXT"])
