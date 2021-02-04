def deterministicZones(vmCount=1, zones=['a', 'b', 'c']):
    """Deterministically select zones based on number of VMs"""

    return (zones * vmCount)[:vmCount]

def mangleRegion(gregion):
    """Mangle the default gcloud region to fit into the aws style format used by CCM"""
    import re
    return ('-'.join(re.findall(r"[^\W\d_]+|\d+", gregion)))
