"""Generates Multiple Instances."""

import lib.helpers as helper
import re

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Generates Multiple Instances."""

    resources = []
    DETERMINISTIC_ZONES = helper.compute.deterministicZones(context.properties['instanceCount'], context.properties['zones'])

    # convert region from google style to ccm style. e.g. us-east4 to us-east-4
    compute_region = helper.compute.mangleRegion(context.properties['region'])

    for instanceCtx in range(context.properties['instanceCount']):

        INSTANCE_NAME      = '{}-{}-{}'.format(context.properties['tier'], context.properties['role'], instanceCtx)
        DATA_DISK_NAME     = INSTANCE_NAME + '-data'
        DETERMINISTIC_ZONE = '{}-{}'.format(context.properties['region'], DETERMINISTIC_ZONES[instanceCtx])

        resources.append({
            'name': 'vm-' + INSTANCE_NAME,
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
                }],
                'tags': {
                    'items': [
                        'base' if context.properties['tier'] != 'nat' else 'nat-base',
                        '{}'.format(context.properties['tier']),
                        '{}'.format(context.properties['role']),
                        '{}-{}'.format(context.properties['tier'], context.properties['role']),
                    ],
                },
                'metadata': {
                    'items': [{
                        'key': 'hostname',
                        'value': INSTANCE_NAME + "." + context.properties['network'] + "." + "g-" + compute_region + '.ccmteam.com',
                    }],
                },
                'serviceAccounts': [{
                    'email': 'default',
                    'scopes': [
                        'https://www.googleapis.com/auth/compute',
                    ],
                }],
                'canIpForward': True if context.properties.get('canIpForward') == True else False,
            },
        })


        if 'tags' in context.properties:
            resources[-1]['properties']['tags']['items'] += context.properties['tags']

        if context.properties.get('serialPort') == True:

            resources[-1]['properties']['metadata']['items'].append({
                'key': 'serial-port-enable',
                'value': '1',
            })

        if 'startupScript' in context.properties:

            resources[-1]['properties']['metadata']['items'].append({
                'key': 'startup-script',
                'value': context.imports[context.properties['startupScript']],
            })

        if 'staticPrimaryInternalIps' in context.properties:

            resources[-1]['properties']['networkInterfaces'][0].update({
                'networkIP': context.properties['staticPrimaryInternalIps'][instanceCtx],
            })

        if context.properties.get('ephemeralPrimaryExternalIp') == True:

            resources[-1]['properties']['networkInterfaces'][0].update({
                'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT',
                }],
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
