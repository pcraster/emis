FROM python:3.5

MAINTAINER Kor de Jong <k.dejong1@uu.nl>
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY emis /emis
COPY uwsgi.ini /
COPY cmd.sh /
COPY run_server.py /
COPY test.py /


USER uwsgi
CMD ["/cmd.sh"]
