#!/usr/bin/env bash
set -e


export EMIS_SSL_CERTIFICATE=$EMIS_SSL/development/localhost.crt
export EMIS_SSL_KEY=$EMIS_SSL/development/localhost.key

python -m unittest discover test *_test.py
