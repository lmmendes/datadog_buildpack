#!/usr/bin/env bash

echo "Starting Datadog decorator (dh-io-datadog)"

#__BUILDPACK_INDEX__ gets replaced by bin/supply at cf push

# this should be the right command since I believe that $DEPS_DIR gets injected when this file is called
# but didnt prove that

python $DEPS_DIR/__BUILDPACK_INDEX__/datadog.py &
