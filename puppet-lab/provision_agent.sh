#!/bin/bash
set -e

# Add Puppet 7 repo
# wget https://apt.puppet.com/puppet7-release-noble.deb
# dpkg -i puppet7-release-noble.deb
apt-get update
# apt-get upgrade -y

# Install Puppet Agent
apt-get install -y puppet-agent

# Configure puppet.conf
# cat <<EOF >>/etc/puppetlabs/puppet/puppet.conf
cat <<EOF >>/etc/puppet/puppet.conf
[main]
certname = puppetagent.local
server = puppetmaster.local
EOF

# Hosts file
echo "192.168.56.10 puppetmaster.local puppetmaster" >>/etc/hosts
echo "192.168.56.11 puppetagent.local puppetagent" >>/etc/hosts

# Enable and start puppet agent
/usr/bin/puppet resource service puppet ensure=running enable=true

# Trigger first certificate request
/usr/bin/puppet agent --test || true
