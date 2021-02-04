"""Sandbox-Dev Jumpbox Adm"""

def GenerateConfig(context):
    """Sandbox-Dev Jumpbox Adm"""

    IMAGE_FAMILY      = 'centos-cloud'
    IMAGE_VERSION     = 'centos-7-v20171129'
    BOOT_DISK_SIZE_GB = 15

    resources = []

    resources.append({
        'name': 'jumpbox-adm',
        'type': 'basic-instances.py',
        'properties': {
            'instanceCount':            1,
            'region':                   'us-east4',
            'tier':                     'jumpbox',
            'role':                     'adm',
            'zones':                    ['b'],
            'network':                  'sandbox-dev',
            'machineType':              'g1-small',
            'staticPrimaryInternalIps': ['10.12.0.10'],
            'bootDiskSizeGb':           BOOT_DISK_SIZE_GB,
            'imageFamily':              IMAGE_FAMILY,
            'imageVersion':             IMAGE_VERSION,
        },
    })

    return { 'resources': resources }
