#!/usr/bin/env bash
set -e
docker build -t test/emis .
docker run -p9090:9090 test/emis
