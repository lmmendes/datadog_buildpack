#!/usr/bin/env bash

export DH_IO_DATADOG=1

echo "Starting Datadog decorator (dh-io-datadog)"

SCRIPTS_DIR=/home/vcap/app/dh-io-datadog
python $SCRIPTS_DIR/datadog.py
