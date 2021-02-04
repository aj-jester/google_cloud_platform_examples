"""Reserve Internal IP address."""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Reserve Internal IP address."""

    resources = []

    resources.append({
        'name': 'ip-' + context.env['name'],
        'type': 'compute.v1.address',
        'properties': {
            'address': context.properties['address'],
            'description': context.properties['description'],
            'region': context.properties['region'],
            'addressType': 'INTERNAL',
            'subnetwork': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/regions/' + context.properties['region'] + '/subnetworks/' + context.properties['network'],
        },
    })

    return {'resources': resources}
