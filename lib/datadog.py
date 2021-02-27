from __future__ import print_function
import os
import sys
import json
import re

SERVICE_TAG = 'datadog'
KEY_TAGS = 'DD_TAGS'

AGENT_REGEXP = re.compile('dd-java-agent-[0-9.]*.jar')
APP_NAME_REGEXP = re.compile("-v\d+-")
DEBUG = os.environ.get('DEBUG_DH_IO_DATADOG', False)

def main():
    appinfo = get_application_info()
    service = find_datadog_service()
    defaults, default_tags = get_defaults(appinfo, service)
    agents = find_agents()
    env_vars = make_env(service, appinfo, defaults, default_tags, agents)
    change_env_vars(add=env_vars, remove=['DD_API_KEY'], override=['JAVA_OPTS'])


def get_defaults(appinfo, service):
    app = get_application_name(appinfo)
    space = appinfo.get('space_name', '')
    org = appinfo.get('organization_name', '')
    detected_version = find_version()
    version = os.environ.get('DD_VERSION', detected_version if detected_version is not None else 1)
    logs_port = os.environ.get('STD_LOG_COLLECTION_PORT', '10514')
    defaults= {
            'DD_ENV': space,
            'DD_VERSION': version,
            'DD_SERVICE': app,
            'DD_SITE': 'datadoghq.eu',
            'RUN_AGENT': 'true',
            'DD_APM_ENABLED': 'true',
            'DD_LOGS_ENABLED': 'true',
            'DD_LOGS_INJECTION': 'true',
            'DD_TRACE_ANALYTICS_ENABLED': 'true',
            'DD_ENABLE_CHECKS': 'false',
            'DD_PROPAGATION_STYLE_INJECT': 'Datadog,B3',
            'STD_LOG_COLLECTION_PORT': logs_port,
            'LOGS_CONFIG': json.dumps([{"type": "tcp", "port": logs_port, "source": "pcf", "service": app}]),
            }
    default_tags = {
            'service': app,
            'tenant': org,
            'version': version,
            }
    return (defaults, default_tags)


def find_agents():
    result = []
    for root, dirs, files in os.walk('.'):
        for name in files:
            if AGENT_REGEXP.match(name):
                result.append(os.path.join(root, name))
    return result


def find_version():
    try:
        with open('META-INF/MANIFEST.MF') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            keyvalues = dict(tuple(line.split(': ', 1)) for line in lines)
            return keyvalues.get('Implementation-Version', None)
    except:
        return None


def get_application_info():
    """ Collect the information about the application """

    appinfo = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
    if 'name' not in appinfo:
        abort("VCAP_APPLICATION must specify application_name")
    return appinfo

def get_application_name(app_info):
    """ Get the application name from APPLICATION_NAME env var or from VCAP_APPLICATION values """
    if os.environ.get('APPLICATION_NAME'):
        return os.environ.get('APPLICATION_NAME')
    app_name = APP_NAME_REGEXP.split(app_info.get('application_name', ''))[0]
    org_name = app_info.get('organization_name', '')
    return "{}-{}".format(org_name, app_name)


def find_datadog_service():
    """ Find datadog service """

    vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    tagged_services = [s for _, service_list in vcap_services.items() for s in service_list if SERVICE_TAG in s['tags']]
    if not tagged_services:
        abort("No service bind found with tag {}".format(SERVICE_TAG))
    datadog_service = tagged_services[0]
    if len(tagged_services) > 1:
        log("Multiple tagged services found, using {}".format(datadog_service))
    return datadog_service


def make_env(service, appinfo, defaults, default_tags, agents):
    service_vars = service.get('credentials', {})
    combined = merge_dicts(service_vars, defaults)

    if KEY_TAGS in service_vars:
        service_tags = dict(tuple(kv.strip().split(':')) for kv in service_vars[KEY_TAGS].split(','))
        tags = merge_dicts(service_tags, default_tags)
    else:
        tags = default_tags
    combined[KEY_TAGS] = ','.join('{}:{}'.format(k, v) for k, v in tags.items())

    java_opts = os.environ.get('JAVA_OPTS', '')
    opts = java_opts.split(' ')
    agent_opts = [o for o in opts if o.startswith('-javaagent:') and AGENT_REGEXP.search(o)]
    if agent_opts:
        log('Skipping agent configuration, already defined')
    elif agents:
        agent = agents[0]
        log('Found agents: {}'.format(' '.join(agents)))
        log('Adding agent configuration: {}'.format(agent))
        opts.append('-javaagent:{}'.format(agent))
        combined['JAVA_OPTS'] = ' '.join(opts)
    else:
        log('No agent configured and none found')

    return combined


def change_env_vars(add, remove, override):
    """ Sets and unsets env variables """

    for key in remove:
        if key in os.environ:
            log('removing: {}'.format(key))
            print('unset {}'.format(key))

    for (key, value) in add.items():
        if key in os.environ and not key in override:
            log('skipping: {}, overriden with value {}'.format(key, os.environ[key]))
        else:
            log('injecting: {}={}'.format(key, value))
            print("export {}='{}'".format(key, str(value)))


def merge_dicts(*dicts):
    """ merges a set of dicts, highest to lowest prority on conflicts """
    res = {}
    for d in dicts[::-1]:
        res.update(d)
    return res

def log(msg):
    if DEBUG: print('[dh-io-datadog]', msg, file=sys.stdout)


def abort(msg, rc=1):
    print('[dh-io-datadog]', msg, file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()
