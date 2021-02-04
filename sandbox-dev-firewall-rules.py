"""Sandbox-Dev Firewall rules"""

def GenerateConfig(context):
    """MongoDB Firewall Rules"""

    resources = []

    """SSH Firewall Rule"""
    resources.append({
        'name': 'ig-ssh',
        'type': 'firewall.py',
        'properties': {
            'network': 'sandbox-dev',
            'sourceRanges': [
                '10.6.6.108/32',
                '10.12.0.10/32',
            ],
            'direction': 'INGRESS',
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [22],
            }]
        },
    })

    """ICMP Firewall Rule"""
    resources.append({
        'name': 'ig-icmp',
        'type': 'firewall.py',
        'properties': {
            'network': 'sandbox-dev',
            'sourceRanges': ['10.0.0.0/8'],
            'direction': 'INGRESS',
            'allowed': [{
                'IPProtocol': 'ICMP',
            }]
        },
    })

    return { 'resources': resources }
