from __future__ import print_function
import os
import sys
import json

SERVICE_TAG = 'datadog'


def main():
    appinfo = get_application_info()
    service = find_datadog_service()
    inject_datadog(service, appinfo)


def get_application_info():
    """ Collect the information about the application """

    appinfo = {}
    vcap_application = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
    appinfo['name'] = vcap_application.get('application_name')
    if not appinfo['name']:
        abort("VCAP_APPLICATION must specify application_name")
    return appinfo


def find_datadog_service():
    """ Find datadog service """
    vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    tagged_services = [s for s in vcap_services if SERVICE_TAG in s['tags']]
    if not tagged_services:
        abort("No service bind found with tag {}".format(SERVICE_TAG))
    datadog_service = tagged_services[0]
    if len(tagged_services) > 1:
        warn("Multiple tagged services found, using {}".format(datadog_service))
    return datadog_service


# TODO:
# - understand what to do with env variables already set
# - undertand what to do with non DD_ variables that we will need to set
def inject_datadog(service, appinfo):
    """ Injects DO env variables """
    print('injecting env variables')
    env_vars = service.get('credentials', {})
    for (key, value) in env_vars.items():
        print('injecting: {}={}'.format(key, value))
        os.environ[key] = value
    print('============= FILE LIST ========================')
    file_list = os.listdir('.')
    print(file_list)


def warn(msg):
    print(msg, file=sys.stderr)


def abort(msg, rc=1):
    print(msg, file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()
