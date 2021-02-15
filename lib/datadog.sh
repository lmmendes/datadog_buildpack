#!/bin/bash

echo "Starting Datadog decorator (dh-io-datadoh)"

#__BUILDPACK_INDEX__ gets replaced by bin/supply at cf push

python -u $DEPS_DIR/__BUILDPACK_INDEX__/datadog.py &

