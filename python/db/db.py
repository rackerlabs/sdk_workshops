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

# Configure the settings
pyrax.set_environment("scale12x")

# If you have keyring configured...
pyrax.keyring_auth()
# If you have a credential file...
#pyrax.set_credential_file("/path/to/file")
# Or just set directly
#pyrax.set_credentials(username, password)

cs = pyrax.cloudservers
cf = pyrax.cloudfiles
clb = pyrax.cloud_loadbalancers
cdb = pyrax.cloud_databases
cnw = pyrax.cloud_networks
dns = pyrax.cloud_dns

start = time.time()
print "*" * 66
print "Starting at", time.ctime() 
print "*" * 66


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

# Get the available flavors
flavors = cdb.list_flavors()
# Select the 512MB flavor
flavor = [flav for flav in flavors
        if flav.ram == 512][0]

# Create the database instance
print
print "Creating the database instance..."
db_instance = cdb.create("scale12x_DB", flavor=flavor, volume=2)
utils.wait_for_build(db_instance, verbose=True)

# Create a database on this instance
db = db_instance.create_database("demodb")
add_to_cleanup("CDB", db_instance)

# Create a user, giving them access to the database.
db_user = db_instance.create_user("demouser", "topsecret", db)
db_host = db_instance.hostname
print "Database instance created; hostname:", db_host

# Define a Node for this database
print
print "Creating the node"
node = clb.Node(address=db_host, port=3306, condition="ENABLED")
print "Node created:", node

# Create the Virtual IP
print
print "Creating the Virtual IP"
vip = clb.VirtualIP(type="PUBLIC")
print "Virtual IP:", vip

# Create a Load Balancer for accessing the database from the public internet
print
print "Creating the Load Balancer"
lb = clb.create("scale12x_data_LB", port=3306, protocol="MYSQL",
        nodes=[node], virtual_ips=vip, algorithm="RANDOM")
add_to_cleanup("CLB", lb)
utils.wait_for_build(lb, verbose=True)
lb_ip = lb.virtual_ips[0].address
print "Load Balancer created:", lb
print
print "=" * 66
print "Load Balancer IP:", lb_ip
print "=" * 66

