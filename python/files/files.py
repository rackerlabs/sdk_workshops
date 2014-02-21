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


import datetime
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

cf = pyrax.cloudfiles


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


print "Creating the container..."
cont = cf.create_container("python-demo")
pic = "python-logo.png"
print "Uploading the file..."
obj = cf.upload_file(cont, pic)

# Create the temp URL key
cf.set_temp_url_key()
key = cf.get_temp_url_key()

temp_url = cf.get_temp_url(cont, pic, seconds=120, method="GET")
expire_time = datetime.datetime.now() + datetime.timedelta(seconds=120)

# Print out the temp URL, and pause while it is downloaded.
print
print "Temp URL:"
print temp_url
print "Expires at:", expire_time.strftime("%H:%M:%S") 

answer = raw_input("Press any key to continue...")

print "Publishing container to the CDN..."
cont.make_private()

answer = raw_input("Press any key to continue...")




