#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Ed Leafe

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import json
import os
import time

import pyrax
import pyrax.utils as utils
import pyrax.exceptions as exc

pyrax.set_environment("scale12x")

# If you have keyring configured...
pyrax.keyring_auth()
# If you have a credential file...
#pyrax.set_credential_file("/path/to/file")
# Or just set directly
#pyrax.set_credentials(username, password)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
cnw = pyrax.cloud_networks


def add_to_cleanup(svc, reso):
    filename = "scaledemo.json"
    cleanup = {}
    try:
        with open(filename) as ff:
            cleanup = json.load(ff)
    except IOError:
        pass
    try:
        cleanup[svc].append(reso.id)
    except (KeyError, AttributeError):
        cleanup[svc] = [reso.id]
    with open(filename, "w") as ff:
        json.dump(cleanup, ff)


start = time.time()
print "*" * 66
print "Starting at", time.ctime() 
print "*" * 66


# ID of appserver image
# This is hardcoded for demo purposes.
IMAGE_ID = "b598f4ab-14d3-40f7-a23c-078983654fc6"

# Get the flavor. We'll use the 1GB Performance flavor,
# which has ram = 1024, and disk = 20.
flavors = cs.list_flavors()
flavor = [flav for flav in flavors
        if flav.ram == 1024
        and flav.disk == 20][0]

# Store the public key
keyfile = os.path.expanduser("~/.ssh/id_rsa.pub")
with open(keyfile, "r") as kf:
    pub = kf.read()
key = cs.keypairs.create("scale_key", pub)
add_to_cleanup("CSK", key)

# Create two servers with only ServiceNet
networks = [{"net-id": cnw.SERVICE_NET_ID}]
server1 = cs.servers.create("scale12x_Srv1",
        image=IMAGE_ID, flavor=flavor, key_name="scale_key",
        nics=networks)
server2 = cs.servers.create("scale12x_Srv2",
        image=IMAGE_ID, flavor=flavor, key_name="scale_key",
        nics=networks)
add_to_cleanup("CS", server1)
add_to_cleanup("CS", server2)
utils.wait_for_build(server1, verbose=True)
utils.wait_for_build(server2, verbose=True)
print "App servers created."
print "Server 1:", server1.name, server1.addresses
print "Server 2:", server2.name, server2.addresses

# Get the server IPs
print
print "Creating the nodes"
ip1 = server1.addresses["private"][0]["addr"]
ip2 = server2.addresses["private"][0]["addr"]
# Define the nodes
node1 = clb.Node(address=ip1, port=80,
        weight=1, condition="ENABLED")
node2 = clb.Node(address=ip2, port=80,
        weight=1, condition="ENABLED")
print "Node 1 created:", node1
print "Node 2 created:", node2

# Create the Virtual IP
print
print "Creating the Virtual IP"
vip = clb.VirtualIP(type="PUBLIC")
print "Virtual IP:", vip

# Create the Load Balancer
print
print "Creating the Load Balancer"
lb = clb.create("scale12x_LB", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=vip,
        algorithm="WEIGHTED_ROUND_ROBIN")
add_to_cleanup("CLB", lb)
utils.wait_for_build(lb, verbose=True)
lb_ip = lb.virtual_ips[0].address
print "Load Balancer created:", lb
print
print "=" * 66
print "Load Balancer IP:", lb_ip
print "=" * 66

end = time.time()
elapsed = end - start
print
print
print "*" * 66
print "It took %6.2f seconds to build the infrastructure." % elapsed
print "*" * 66
print
print "Server 1 IP address:", ip1
print "Server 2 IP address:", ip2
print "Load Balancer IP address:", lb_ip
print
print
# Wait until we're ready
server3 = None
answer = raw_input("Ready to add a third app server?")
if answer[0] in "YyTt":
    # Add another node
    print
    print "Creating a third app server..."
    server3 = cs.servers.create("scale12x_Srv3",
            image=IMAGE_ID, flavor=flavor, key_name="scale_key",
            nics=networks)
    add_to_cleanup("CS", server3)
    utils.wait_for_build(server3, verbose=True)
    print "Third app server created."
    print "Server 3:", server3.name, server3.addresses
    ip3 = server3.addresses["private"][0]["addr"]
    node3 = clb.Node(address=ip3, port=80,
            weight=3, condition="ENABLED")
    lb.add_nodes(node3)
    print 
    print "Third node added with a weight of 3"
print
print "*" * 66
print "Server 1 IP address:", ip1
print "Server 2 IP address:", ip2
if server3:
    print "Server 3 IP address:", ip3
print "Load Balancer IP address:", lb_ip
print "*" * 66
print
print
