import os
os.environ["EMIS_CONFIGURATION"] = "development"
from server import app


app.run(host="0.0.0.0", ssl_context=app.config["SSL_CONTEXT"])
