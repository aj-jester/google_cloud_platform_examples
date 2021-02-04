#!/bin/bash

echo "$(context.properties["tier"])" > /tmp/tier.txt

# Pull hostname from metadata
#hostname=`/usr/bin/curl --silent "http://metadata.google.internal/computeMetadata/v1/instance/attributes/hostname" -H "Metadata-Flavor: Google"`

# Pull ip from ip
#ip=`ip a | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`

# Get data from hosts for GCE
#gce_hostname=`grep vm- /etc/hosts | awk '{print $2}'`

# Update the /etc/hosts with CCM & GCE Information
#/bin/sed -i "/$ip/c\\" /etc/hosts
#echo "$ip $hostname $gce_hostname" >> /etc/hosts
#echo "10.12.0.20 ppt-server-0.sandbox-dev.g-us-east-4.ccmteam.com" >> /etc/hosts

# set hostname
#/bin/hostname $hostname
#echo $hostname > /etc/hostname

# google_hostname.sh will unset this work, so let us delete it.
#/bin/rm /etc/dhcp/dhclient.d/google_hostname.sh

# clean up existing repos
#/bin/rm /etc/yum.repos.d/*
