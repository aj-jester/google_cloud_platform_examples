"""Sandbox-Dev Fe MongoDB Shards / Replica Sets"""

def GenerateConfig(context):
    """Fe MongoDB Shards / Replica Sets"""

    IMAGE_FAMILY      = 'centos-cloud'
    IMAGE_VERSION     = 'centos-7-v20171129'
    BOOT_DISK_SIZE_GB = 15

    resources = []

    """Shard fe-c6pt42"""
    resources.append({
        'name': 'fe-c6pt42',
        'type': 'mongodb-shard.py',
        'properties': {
            'shardSize':      3,
            'region':         'us-east4',
            'zones':          ['a', 'b', 'c'],
            'network':        'sandbox-dev',
            'machineType':    'f1-micro',
            'dataDiskSizeGb': 100,
            'bootDiskSizeGb': BOOT_DISK_SIZE_GB,
            'imageFamily':    IMAGE_FAMILY,
            'imageVersion':   IMAGE_VERSION,
        },
    })

    return { 'resources': resources }
