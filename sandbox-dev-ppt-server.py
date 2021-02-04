"""Sandbox-Dev PPT Server"""

def GenerateConfig(context):
    """Sandbox-Dev PPT Server"""

    IMAGE_FAMILY      = 'centos-cloud'
    IMAGE_VERSION     = 'centos-7-v20171129'
    BOOT_DISK_SIZE_GB = 15

    resources = []

    resources.append({
        'name': 'ppt-server',
        'type': 'basic-instances.py',
        'properties': {
            'instanceCount':            1,
            'region':                   'us-east4',
            'tier':                     'ppt',
            'role':                     'server',
            'zones':                    ['b'],
            'network':                  'sandbox-dev',
            'machineType':              'g1-small',
            'serialPort':               True,
            'manageHostname':           True,
            'startupScript':            'startup-script.sh',
            'staticPrimaryInternalIps': ['10.12.0.20'],
            'bootDiskSizeGb':           BOOT_DISK_SIZE_GB,
            'imageFamily':              IMAGE_FAMILY,
            'imageVersion':             IMAGE_VERSION,
        },
    })

    """Puppet Server Firewall rule"""
    resources.append({
        'name': 'ig-ppt-server',
        'type': 'firewall.py',
        'properties': {
            'network': 'sandbox-dev',
            'direction': 'INGRESS',
            'sourceTags': ['base'],
            'targetTags': ['ppt-server'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': ['8140'],
            }],
        },
    })

    return { 'resources': resources }
