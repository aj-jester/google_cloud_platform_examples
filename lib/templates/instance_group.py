"""Intance Group template"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Instance Group template"""

    instancegroup_name = context.properties['region'] + '-' + context.env['deployment']

    resources = {
        'name': instancegroup_name,
        'type': 'compute.v1.instanceGroups',
        'properties': {
            'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/global/networks/' + context.properties['network'],
            'zone': context.properties['zone']
        }
    }

    return { 'resources': [resources] }
