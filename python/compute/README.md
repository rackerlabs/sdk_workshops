# Create Two Cloud Servers Behind a Cloud Load Balancer

To do this, we're going to use *pyrax*, the Python SDK for OpenStack clouds. If you're not familiar with pyrax, you can read the docs at https://github.com/rackspace/pyrax/tree/master/docs

I have an environment configuration for this named 'scale12x'; this sets up my keyring username for authentication, and also sets my desired region to 'DFW'. I also included a small method for adding the IDs of the resources the script creates to a dictionary that I write to disk in JSON format. This allows me to run a cleanup.py script to delete these resources when the demo is over.

When creating a Cloud Server, you need to specify the image to use for the server, along with the desired amount of resources for the server. Images can be one of the stock images for the various operating systems, or it can be a saved image of a Cloud Server, allowing you to essentially clone a server in a given state.

Ahead of time I created a Cloud Server with a basic web application on it. When you browse the index of that server, it returns a page with the IP address of the server, along with the current UTC date/time. Nothing fancy, but it gives us the information we need for this demonstration, and shows that we're not faking it. I then created a snapshot of that server, from which I can create multiple copies in that exact state. The demo program hard-codes that image ID; in real life you'd have to supply your own value.

Next I get a reference to the flavor I want to use for the servers. A 'flavor' refers to a particular combination of disk, RAM, network capactity, and virtual CPUs for the server. For the demo I'm selecting the Performance 1GB flavor, by finding the flavor with 1024MB RAM and disk size of 20GB.
