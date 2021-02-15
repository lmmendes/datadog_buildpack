import os
import sys
import json

def main():
    appinfo = get_application_info()
    service = find_datadog_service()
    if service != None:
        inject_datadog(service, appinfo)

def detect():
    appinfo = get_application_info()
    service = find_datadog_service()
    if service == None:
        print >> sys.stderr, "Can't find dh-io-datadog service"
        sys.exit(1)

# Get Application Info
#
# Collect the information about the application
#
def get_application_info():
    appinfo = {}
    vcap_application = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
    appinfo['name'] = vcap_application.get('application_name')
    if appinfo['name'] == None:
        print >> sys.stderr, "VCAP_APPLICATION must specify application_name"
        sys.exit(1)
    return appinfo

# Find datadog service
#
def find_datadog_service():
    vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    for service in vcap_services:
        service_instances = vcap_services[service]
        for instance in service_instances:
            if instance['name'] == 'dh-io-datadog':
                return instance
    return None

# Injects DO env variables
# TODO:
# - understand what to do with env variables already set
# - undertand what to do with non DD_ variables that we will need to set
def inject_datadog(service, appinfo):
    print('injecting env variables')
    env_vars = service.get('credentials', {})
    for (key, value) in env_vars.items():
        print('injecting: {}={}'.format(key, value))
        os.environ[key]=value
    print('============= FILE LIST ========================')
    file_list = os.listdir('.')
    print(file_list)


if __name__ == "__main__":
    main()