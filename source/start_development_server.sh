#!/usr/bin/env bash
set -e


docker build -t test/emis .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis:/emis \
    test/emis
