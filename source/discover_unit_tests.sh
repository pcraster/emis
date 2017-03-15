#!/usr/bin/env bash
set -e


export EMIS_SSL_CERTIFICATE=$EMIS_SSL/development/emis.crt
export EMIS_SSL_KEY=$EMIS_SSL/development/emis.key

python -m unittest discover test *_test.py
