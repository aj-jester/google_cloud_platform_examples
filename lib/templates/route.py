"""Route template"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Route template"""

    resources = {
        'name': 'rte-' + context.env['name'],
        'type': 'compute.v1.route',
        'properties': {
            'description': context.properties['description'],
            'destRange': context.properties['destRange'],
            'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/global/networks/' + context.properties['network'],
            'tags': context.properties['tags'] if 'tags' in context.properties else [],
            'priority': context.properties['priority'] if 'priority' in context.properties else 1000,
        }
    }

    if 'nextHopInstance' in context.properties:
        resources['properties'].update({
            'nextHopInstance': context.properties['nextHopInstance'],
        })

    elif 'nextHopIp' in context.properties:
        resources['properties'].update({
            'nextHopIp': context.properties['nextHopIp'],
        })

    elif 'nextHopNetwork' in context.properties:
        resources['properties'].update({
            'nextHopNetwork': context.properties['nextHopNetwork'],
        })

    elif 'nextHopVpnTunnel' in context.properties:
        resources['properties'].update({
            'nextHopVpnTunnel': context.properties['nextHopNetwork'],
        })

    elif context.properties.get('nextHopGateway') == True:
        resources['properties'].update({
            'nextHopGateway': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/global/gateways/default-internet-gateway',
        })


    return { 'resources': [resources] }
