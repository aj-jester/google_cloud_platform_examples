"""Sandbox-Dev Reserved Private IPs"""

def GenerateConfig(context):
    """Sandbox-Dev Reserved Private IPs"""

    resources = []

    """Jumpbox US-EAST4"""
    resources.append({
        'name': '10-12-0-10',
        'type': 'reserve-internal-ip.py',
        'properties': {
            'address': '10.12.0.10',
            'description': 'Jumpbox US-EAST4',
            'network': 'sandbox-dev',
            'region': 'us-east4',
        },
    })

    """Puppet Server US-EAST4"""
    resources.append({
        'name': '10-12-0-20',
        'type': 'reserve-internal-ip.py',
        'properties': {
            'address': '10.12.0.20',
            'description': 'Puppet Server US-EAST4',
            'network': 'sandbox-dev',
            'region': 'us-east4',
        },
    })

    """Temporary Elasticsearch US-EAST4"""
    resources.append({
        'name': '10-12-0-5',
        'type': 'reserve-internal-ip.py',
        'properties': {
            'address': '10.12.0.5',
            'description': 'Temporary Elasticsearch US-EAST4',
            'network': 'sandbox-dev',
            'region': 'us-east4',
        },
    })

    """Temporary Elasticsearch US-EAST4"""
    resources.append({
        'name': '10-12-0-6',
        'type': 'reserve-internal-ip.py',
        'properties': {
            'address': '10.12.0.6',
            'description': 'Temporary Elasticsearch US-EAST4',
            'network': 'sandbox-dev',
            'region': 'us-east4',
        },
    })

    """Temporary Elasticsearch US-EAST4"""
    resources.append({
        'name': '10-12-0-7',
        'type': 'reserve-internal-ip.py',
        'properties': {
            'address': '10.12.0.7',
            'description': 'Temporary Elasticsearch US-EAST4',
            'network': 'sandbox-dev',
            'region': 'us-east4',
        },
    })

    return { 'resources': resources }
