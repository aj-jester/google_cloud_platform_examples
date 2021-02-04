"""Sandbox-Dev NAT HA Gateway"""

def GenerateConfig(context):
    """Sandbox-Dev NAT HA Gateway"""

    IMAGE_FAMILY      = 'centos-cloud'
    IMAGE_VERSION     = 'centos-7-v20171129'
    BOOT_DISK_SIZE_GB = 15

    resources = []

    """NAT Gateway Instances"""
    resources.append({
        'name': 'nat-gw',
        'type': 'basic-instances.py',
        'properties': {
            'instanceCount':              3,
            'region':                     'us-east4',
            'tier':                       'nat',
            'role':                       'gw',
            'zones':                      ['a', 'b', 'c'],
            'network':                    'sandbox-dev',
            'machineType':                'n1-standard-2',
            'ephemeralPrimaryExternalIp': True,
            'canIpForward'              : True,
            'startupScript':              'startup-script.sh',
            'bootDiskSizeGb':             BOOT_DISK_SIZE_GB,
            'imageFamily':                IMAGE_FAMILY,
            'imageVersion':               IMAGE_VERSION,
        },
    })

    """NAT Gateway Routes"""
    for instanceCtx in range(3):
        INSTANCE_NAME = 'nat-gw-{}'.format(instanceCtx)

        resources.append({
            'name': INSTANCE_NAME,
            'type': 'route.py',
            'properties': {
                'description':     'Route for ' + INSTANCE_NAME,
                'destRange':       '0.0.0.0/0',
                'priority':        800,
                'tags':            ['base'],
                'nextHopInstance': '$(ref.vm-' + INSTANCE_NAME + '.selfLink)',
                'network':         'sandbox-dev',
            },
        })

    """NAT Gateway Firewall rule"""
    resources.append({
        'name': 'ig-nat-gw',
        'type': 'firewall.py',
        'properties': {
            'network': 'sandbox-dev',
            'direction': 'INGRESS',
            'sourceTags': ['base'],
            'targetTags': ['nat-gw'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': ['0-65535'],
            },
            {
                'IPProtocol': 'UDP',
                'ports': ['0-65535'],
            }],
        },
    })

    return { 'resources': resources }
