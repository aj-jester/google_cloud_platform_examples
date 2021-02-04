#!/bin/bash

gcloud compute instance-groups unmanaged add-instances us-east4-sandbox-dev-infra-muppet-instance-group --instances vm-infra-muppet-0 --zone us-east4-c

# Pull hostname from metadata
hostname=`/usr/bin/curl --silent "http://metadata.google.internal/computeMetadata/v1/instance/attributes/hostname" -H "Metadata-Flavor: Google"`

# Pull ip from ip
ip=`ip a | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`

# Set a DNS record
infra_env=`echo "infra-muppet-0.sandbox-dev.g-us-east-4.ccmteam.com" | cut -d \. -f2`
location=`echo "infra-muppet-0.sandbox-dev.g-us-east-4.ccmteam.com" | cut -d \. -f3`
zone=`echo -n $infra_env;echo -n "-";echo -n $location; `

# Not enabled as default account lacks permission
#gcloud dns record-sets transaction start --zone $zone
#gcloud dns record-sets transaction add --zone $zone --name $hostname --ttl 600 --type A $ip
#gcloud dns record-sets transaction execute --zone $zone

# Get data from hosts for GCE
gce_hostname=`grep vm- /etc/hosts | awk '{print $2}'`

# Update the /etc/hosts with CCM & GCE Information
/bin/sed -i "/$ip/c\\" /etc/hosts
echo "$ip $hostname $gce_hostname" >> /etc/hosts
echo "10.12.0.20 ppt-server-0.sandbox-dev.g-us-east-4.ccmteam.com" >> /etc/hosts

# set hostname
/bin/hostname $hostname
echo $hostname > /etc/hostname

# google_hostname.sh will unset this work, so let us delete it.
/bin/rm /etc/dhcp/dhclient.d/google_hostname.sh

# clean up existing repos
/bin/rm /etc/yum.repos.d/*

# set inital ccm repos

# add puppet repository
cat <<EOF >> /etc/yum.repos.d/collectivei-puppet5.repo
[collectivei-puppet5]
name=collectivei-puppet5 repository
baseurl=http://yum.puppetlabs.com/puppet/el/7/x86_64/
enabled=1
gpgcheck=0
EOF

# add centos repository
cat <<EOF >> /etc/yum.repos.d/collectivei-centos-os.repo
[collectivei-centos-os]
name=CentOS os 7.4.1708 x86_64
baseurl=http://mirror.centos.org/centos/\$releasever/os/\$basearch/
enabled=1
gpgcheck=1
EOF

# add centos sclo repository
cat <<EOF >> /etc/yum.repos.d/collectivei-centos-sclo.repo
[collectivei-centos-sclo]
name=Collective[i]'s Sclo Mirror
baseurl=http://mirror.centos.org/centos/7/sclo/x86_64/sclo/
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
EOF

# add centos sclo/rh repository
cat <<EOF >> /etc/yum.repos.d/collectivei-centos-sclo-rh.repo
[collectivei-centos-sclo-rh]
name=Collective[i]'s Sclo RH Mirror
baseurl=http://mirror.centos.org/centos/7/sclo/x86_64/rh/
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
EOF

# add centos updates repository
cat <<EOF >> /etc/yum.repos.d/collectivei-centos-updates.repo
[collectivei-centos-updates]
name=CentOS updates 7.4.1708 x86_64
baseurl=http://mirror.centos.org/centos/\$releasever/updates/\$basearch/
enabled=1
gpgcheck=1
EOF

# add centos epel repository
cat <<EOF >> /etc/yum.repos.d/collectivei-epel.repo
[collectivei-epel]
name=EPEL 7 x86_64
baseurl=http://download.fedoraproject.org/pub/epel/7/\$basearch
enabled=1
gpgcheck=1
gpgkey=https://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7
EOF

# install puppet
/usr/bin/yum install -y puppet-agent


# Initial puppet run
/opt/puppetlabs/bin/puppet agent -tv --server ppt-server-0.sandbox-dev.g-us-east-4.ccmteam.com --environment cloud 


# Add DNS Record 
#gcloud dns record-sets transaction start --zone ops-sandbox-gce-useast4"
#gcloud dns record-sets transaction add --zone ops-sandbox-gce-useast4  --name " + args.n + ".ops-sandbox.gce-useast4.ccmteam.com --ttl 600 --type A " + description["networkInterfaces"][0]["networkIP"])
#gcloud dns record-sets transaction execute --zone ops-sandbox-gce-useast4
