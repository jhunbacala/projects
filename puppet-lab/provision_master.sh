#!/bin/bash
set -e

# Add Puppet 7 repo
# wget https://apt.puppet.com/puppet7-release-noble.deb
# dpkg -i puppet7-release-noble.deb
apt-get update
# apt-get upgrade -y 

# Install Puppet Server
apt-get install -y puppetserver

# Configure puppet.conf
# cat <<EOF >>/etc/puppetlabs/puppet/puppet.conf
cat <<EOF >>/etc/puppet/puppet.conf
[main]
certname = puppetmaster.local
server = puppetmaster.local
environment = production
EOF

# Set Java heap size to something lighter
sed -i 's/JAVA_ARGS.*/JAVA_ARGS="-Xms256m -Xmx512m"/' /etc/default/puppetserver

# Hosts file
echo "192.168.56.10 puppetmaster.local puppetmaster" >>/etc/hosts
echo "192.168.56.11 puppetagent.local puppetagent" >>/etc/hosts

# Start Puppet Server
systemctl enable puppetserver
systemctl start puppetserver
