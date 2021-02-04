"""Generates MongoDB Shards."""

import lib.helpers as helper

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Generates MongoDB Shards."""

    resources = []
    DETERMINISTIC_ZONES = helper.compute.deterministicZones(context.properties['shardSize'], context.properties['zones'])

    for shardIdx in range(context.properties['shardSize']):

        INSTANCE_NAME      = 'mongodb-{}-{}'.format(context.env['name'], shardIdx)
        DATA_DISK_NAME     = INSTANCE_NAME + '-data'
        DETERMINISTIC_ZONE = '{}-{}'.format(context.properties['region'], DETERMINISTIC_ZONES[shardIdx])

        resources.append({
            'name': 'instance-' + INSTANCE_NAME,
            'type': 'compute.v1.instance',
            'properties': {
                'zone': DETERMINISTIC_ZONE,
                'machineType': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                    + '/zones/' + DETERMINISTIC_ZONE + '/machineTypes/' + context.properties['machineType'],
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'diskName': 'disk-' + INSTANCE_NAME + '-os',
                        'diskSizeGb': context.properties['bootDiskSizeGb'],
                        'sourceImage': COMPUTE_URL_BASE + 'projects/' + context.properties['imageFamily'] + '/global/images/' + context.properties['imageVersion'],
                    },
                }],
                'networkInterfaces': [{
                    'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                        + '/global/networks/' + context.properties['network'],
                    'subnetwork': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                        + '/regions/' + context.properties['region'] + '/subnetworks/' + context.properties['network'],
                    'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT',
                    }],
                }],
                'metadata': {
                    'items': [{
                        'key': 'startup-script',
                        'value': """
                                cd /root
                                echo "test" > fe-mongo.txt
                            """,
                    }]
                }
            }
        })

        if 'dataDiskSizeGb' in context.properties:

            resources[-1]['properties']['disks'].append({
                'deviceName': DATA_DISK_NAME,
                'type': 'PERSISTENT',
                'autoDelete': False,
                'source': '$(ref.disk-' + DATA_DISK_NAME + '.selfLink)',
            })

            resources.append({
                'name': 'disk-' + DATA_DISK_NAME,
                'type': 'compute.v1.disk',
                'properties': {
                    'zone': DETERMINISTIC_ZONE,
                    'sizeGb': context.properties['dataDiskSizeGb'],
                    'type': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                        + '/zones/' + DETERMINISTIC_ZONE + '/diskTypes/pd-ssd',
                }
            })

    return {'resources': resources}
