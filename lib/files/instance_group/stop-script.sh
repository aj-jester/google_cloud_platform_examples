#!/bin/bash

gcloud compute instance-groups unmanaged remove-instances us-east4-sandbox-dev-infra-muppet-instance-group --instances vm-infra-muppet-0

# Pull ip from ip
ip=`ip a | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`

fqdn=`hostname -f`
infra_env=`echo "infra-muppet-0.sandbox-dev.g-us-east-4.ccmteam.com" | cut -d \. -f2` 
location=`echo "infra-muppet-0.sandbox-dev.g-us-east-4.ccmteam.com" | cut -d \. -f3` 
zone=`echo -n $infra_env;echo -n "-";echo -n $location; `

# Not enabled as default account lacks permission
#gcloud dns record-sets transaction start --zone $zone
#gcloud dns record-sets transaction remove --zone $zone --name $fqdn --ttl 600 --type A $ip
#gcloud dns record-sets transaction execute --zone $zone
