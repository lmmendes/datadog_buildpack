#!/usr/bin/env bash

echo "Starting Datadog decorator (dh-io-datadog)"

SCRIPTS_DIR=/home/vcap/app/dh-io-datadog
python $SCRIPTS_DIR/datadog.py
