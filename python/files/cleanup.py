#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pyrax

pyrax.set_environment("scale12x")
pyrax.keyring_auth()

cf = pyrax.cloudfiles
try:
    cf.delete_container("python-demo", del_objects=True)
    print "Container deleted."
except pyrax.exceptions.NoSuchContainer:
    print "Container does not exist."
