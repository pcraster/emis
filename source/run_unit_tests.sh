#!/usr/bin/env bash
set -e


docker build -t test/emis .
# docker run --env ENV=TEST -p5000:5000 test/emis
docker run --env ENV=TEST -p5000:5000 -v$EMIS_SSL/development:/ssl:ro -v$(pwd)/emis:/emis test/emis
