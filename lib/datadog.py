from __future__ import print_function
import os
import sys
import json

SERVICE_TAG = 'datadog'


def main():
    appinfo = get_application_info()
    service = find_datadog_service()
    defaults, default_tags = get_defaults(appinfo, service)
    env_vars = make_env(service, appinfo, defaults, default_tags)
    change_env_vars(add=env_vars, remove=['DD_API_KEY'])


def get_defaults(appinfo, service):
    app = appinfo.get('application_name', '')
    space = appinfo.get('space_name', '')
    org = appinfo.get('organization_name', '')
    defaults= {
            'DD_ENV': space,
            #'DD_VERSION': TODO,
            'DD_SERVICE': app,
            'DD_SITE': 'datadoghq.eu',
            'RUN_AGENT': 'true',
            'DD_APM_ENABLED': 'true',
            'DD_LOGS_ENABLED': 'true',
            'DD_LOGS_INJECTION': 'true',
            'DD_TRACE_ANALYTICS_ENABLED': 'true',
            'DD_ENABLE_CHECKS': 'false',
            'STD_LOG_COLLECTION_PORT': 10514,
            'LOGS_CONFIG': json.dumps([{"type": "tcp", "port": "10514", "source": "pcf-mendelui", "service": app}]),
            }
    default_tags = {
            'service': app,
            'tenant': org,
            #'version': TODO,
            }
    return (defaults, default_tags)


def get_application_info():
    """ Collect the information about the application """

    appinfo = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
    if 'name' not in appinfo:
        abort("VCAP_APPLICATION must specify application_name")
    return appinfo


def find_datadog_service():
    """ Find datadog service """

    vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    tagged_services = [s for _, service_list in vcap_services.items() for s in service_list if SERVICE_TAG in s['tags']]
    if not tagged_services:
        abort("No service bind found with tag {}".format(SERVICE_TAG))
    datadog_service = tagged_services[0]
    if len(tagged_services) > 1:
        warn("Multiple tagged services found, using {}".format(datadog_service))
    return datadog_service


def make_env(service, appinfo, defaults, default_tags):
    env_vars = service.get('credentials', {})
    keys = set(env_vars.keys()) | set(defaults.keys())
    combined = dict((k, env_vars[k] if k in env_vars else defaults[k]) for k in keys)

    # TODO tags

    return combined


def change_env_vars(add, remove):
    """ Sets and unsets env variables """

    print('removing env variables')
    for key in remove:
        if key in os.environ:
            print('removing: {}'.format(key))
            del os.environ[key]

    print('injecting env variables')
    for (key, value) in add.items():
        if key in os.environ:
            print('skipping: {}, overriden with value {}'.format(key, os.environ[key]))
        else:
            print('injecting: {}={}'.format(key, value))
            os.environ[key] = str(value)


def warn(msg):
    print(msg, file=sys.stderr)


def abort(msg, rc=1):
    print(msg, file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()
