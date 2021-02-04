"""Firewall rules template"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Firewall rules template"""

    resources = {
        'name': 'firewall-' + context.env['name'],
        'type': 'compute.v1.firewall',
        'properties': {
            'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/global/networks/' + context.properties['network'],
            'direction': context.properties['direction'],
            'allowed': context.properties['allowed'],
            'priority': context.properties['priority'] if 'priority' in context.properties else 1000,
            'sourceTags': context.properties['sourceTags'] if 'sourceTags' in context.properties else [],
            'targetTags': context.properties['targetTags'] if 'targetTags' in context.properties else [],
            'sourceRanges': context.properties['sourceRanges'] if 'sourceRanges' in context.properties else [],
            'destinationRanges': context.properties['destinationRanges'] if 'destinationRanges' in context.properties else [],
        }
    }

    return { 'resources': [resources] }
