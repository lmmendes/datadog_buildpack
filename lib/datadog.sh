#!/bin/bash

echo "Starting Datadog meta buildpack"

#__BUILDPACK_INDEX__ gets replaced by bin/supply at cf push

python $DEPS_DIR/__BUILDPACK_INDEX__/datadog.py &