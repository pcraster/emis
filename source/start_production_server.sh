#!/usr/bin/env bash
set -e
docker build -t test/emis .
docker run -p5000:9090 test/emis
