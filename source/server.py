import os
from emis import create_app


app = create_app(os.getenv("EMIS_CONFIGURATION"))
