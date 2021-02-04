"""Sandbox-Dev Routes"""

def GenerateConfig(context):
    """Sandbox-Dev Routes"""

    resources = []

    """Default Internet Gateway"""
    resources.append({
        'name': 'public-interwebz',
        'type': 'route.py',
        'properties': {
            'description':    'Default Internet Gateway US-EAST4',
            'destRange':      '0.0.0.0/0',
            'nextHopGateway': True,
            'network':        'sandbox-dev',
        },
    })

    return { 'resources': resources }
