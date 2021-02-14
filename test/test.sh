#!/usr/bin/env bash

export VCAP_SERVICES='{
  "user-provided": [
    {
      "label": "user-provided",
      "name": "circuit-breaker",
      "tags": [],
      "instance_name": "circuit-breaker",
      "binding_name": null,
      "credentials": {
        "amqp": {
          "dashboard_url": "https://rabbit.escola.internal",
          "hostname": "127.0.0.1",
          "hostnames": [
            "127.0.0.1"
          ],
          "http_api_uri": "https://username:password@rabbit.escola.internal/api/",
          "http_api_uris": [
            "https://username:password@rabbit.escola.internal/api/"
          ],
          "password": "password",
          "protocols": {
            "amqp": {
              "host": "127.0.0.1",
              "hosts": [
                "127.0.0.1"
              ],
              "password": "password",
              "port": 5672,
              "ssl": false,
              "uri": "amqp://username:password@127.0.0.1:5672/vhostname",
              "uris": [
                "amqp://username:password@127.0.0.1:5672/vhostname"
              ],
              "username": "username",
              "vhost": "vhostname"
            },
            "management": {
              "host": "127.0.0.1",
              "hosts": [
                "127.0.0.1"
              ],
              "password": "password",
              "path": "/api/",
              "port": 15672,
              "ssl": false,
              "uri": "http://username:password@127.0.0.1:15672/api/",
              "uris": [
                "http://username:password@127.0.0.1:15672/api/"
              ],
              "username": "username"
            }
          },
          "ssl": false,
          "uri": "amqp://username:password@127.0.0.1/vhostname",
          "uris": [
            "amqp://username:password@127.0.0.1/vhostname"
          ],
          "username": "username",
          "vhost": "vhostname"
        },
        "dashboard": "https://hystrix.apps.escola.internal",
        "stream": "https://turbine.apps.escola.internal"
      },
      "syslog_drain_url": "",
      "volume_mounts": []
    },
    {
      "label": "user-provided",
      "name": "service-registry",
      "tags": [
        "eureka"
      ],
      "instance_name": "service-registry",
      "binding_name": null,
      "credentials": {
        "access_token_uri": "https://escola.internal/oauth/token",
        "client_id": "service-registry",
        "client_secret": "secret",
        "uri": "https://eureka-instance.apps.escola.internal"
      },
      "syslog_drain_url": "",
      "volume_mounts": []
    },
    {
      "label": "user-provided",
      "name": "dh-io-datadog",
      "tags": [],
      "instance_name": "dh-io-datadog",
      "binding_name": null,
      "credentials": {
        "DD_API_KEY": "THIS_IS_API_KEY"
      },
      "syslog_drain_url": "",
      "volume_mounts": []
    }
  ],
  "p.config-server": [
    {
      "label": "p.config-server",
      "provider": null,
      "plan": "standard",
      "name": "scs-config-server",
      "tags": [
        "configuration",
        "spring-cloud",
        "9f0d43e2c8d06628208ef6958d921758"
      ],
      "instance_name": "scs-config-server",
      "binding_name": null,
      "credentials": {
        "credhub-ref": "/redentials-json"
      },
      "syslog_drain_url": null,
      "volume_mounts": []
    }
  ]
}'

export VCAP_APPLICATION='{
  "cf_api": "https://api.escola.internal",
  "limits": {
    "fds": 16384,
    "mem": 1024,
    "disk": 1024
  },
  "application_name": "nebula-sandbox-app",
  "application_uris": [
    "nebula-v1-alpha.escola.internal"
  ],
  "name": "nebula-sandbox-app",
  "space_name": "alpha",
  "space_id": "ea984bf2",
  "organization_id": "cbf1d0f0",
  "organization_name": "mbiocsa",
  "uris": [
    "nebula-v1-alpha.escola.internal"
  ],
  "process_id": "db9f2e28",
  "process_type": "web",
  "application_id": "db9f2e28",
  "version": "69839494",
  "application_version": "69839494"
}'

python ../lib/datadog.py