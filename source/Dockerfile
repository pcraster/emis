FROM pcraster/emis_base:1.0.0

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY emis /emis
COPY test /test

CMD ["/cmd.sh"]
