"""Load Balancer template"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def GenerateConfig(context):
    """Load Balancer rules template"""

    prefix = context.properties['region'] + '-' + context.env['deployment']
    healthcheck_name = prefix + '-hc'
    firewallrule_name = prefix + '-fw-lb-hc'
    loadbalancer_name = prefix + '-lb'
    loadbalancer_fwdrule = prefix + '-fwd-rule'
    instancegroup_name = prefix + '-instance-group'

    resources = [{
        'name': healthcheck_name + '-' + str(context.properties['port']),
        'type': 'compute.v1.healthCheck',
        'properties': {
            'type': 'TCP',
            'tcpHealthCheck': {
                'port': context.properties['port'],
             },
        },
    },{
        'name': firewallrule_name,
        'type': 'firewall.py',
        'properties': {
            'network': context.properties['network'],
            'sourceRanges': [
                '130.211.0.0/22',
                '35.191.0.0/16',
            ],
            'targetTags': context.properties['targetTags'],
            'direction': 'INGRESS',
            'allowed': [{
                'IPProtocol': context.properties['protocol'],
                'ports': [context.properties['port']],
            }]
        },
#    },{
#        'name': instancegroup_name,
#        'type': 'compute.v1.instanceGroups',
#        'properties': {
#            'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
#                + '/global/networks/' + context.properties['network'],
#            'zone': context.properties['region'] + '-' + context.properties['zone']
#        }
    },{
        'name': loadbalancer_name,
        'type': 'compute.v1.regionBackendService',
        'properties': {
            'region': context.properties['region'],
            'network': COMPUTE_URL_BASE + 'projects/' + context.env['project']
                + '/global/networks/' + context.properties['network'],
            'healthChecks': ['$(ref.' + healthcheck_name + '-' + str(context.properties['port']) + '.selfLink)'],
            #'healthChecks': healthchecks,
            'backends': [{
                'group':  'projects/' + context.env['project'] + '/zones/' + context.properties['region'] 
                    + "-" + context.properties['zone'] + '/instanceGroups/' + instancegroup_name

                # Possible things to explore in the near future.
                #"balancingMode": enum,
                #"maxUtilization": number,
                #"maxRate": number,
                #"maxRatePerInstance": number,
                #"maxConnections": number,
                #"maxConnectionsPerInstance": number,
                #"capacityScaler": number
            }],
            'protocol': context.properties['protocol'],
            'loadBalancingScheme': context.properties['loadBalancingScheme'],
        }
    },{
        'name': loadbalancer_fwdrule,
        'type': 'compute.v1.forwardingRule',
        'properties': {
            'region':              context.properties['region'],
            'ports':               [context.properties['port']],
            'backendService':      '$(ref.' + loadbalancer_name + '.selfLink)',
            'loadBalancingScheme': 'INTERNAL',
            'IPAddress':           context.properties['IPaddress'],
            'network':             'projects/' + context.env['project'] + '/global/networks/' 
                                   + context.properties['network'],
            'subnetwork':          'projects/' + context.env['project'] + '/regions/' + context.properties['region'] 
                                   + '/subnetworks/' + context.properties['network'],
            'tags': {
                'items': [
                    'us-east4-lb'
                ],
            },
        },
    }]

    return { 'resources': resources }
