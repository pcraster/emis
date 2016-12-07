#!/usr/bin/env bash
set -e


docker build -t test/emis .
docker run -p3031:3031 -v$EMIS_SSL/acceptance:/ssl:ro test/emis
