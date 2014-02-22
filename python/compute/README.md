# Create Two Cloud Servers Behind a Cloud Load Balancer

To do this, we're going to use *pyrax*, the Python SDK for OpenStack clouds. If you're not familiar with pyrax, you can read the docs at https://github.com/rackspace/pyrax/tree/master/docs

I have an environment configuration for this named 'scale12x'; this sets up my keyring username for authentication, and also sets my desired region to 'DFW'. I also included a small method for adding the IDs of the resources the script creates to a dictionary that I write to disk in JSON format. This allows me to run a cleanup.py script to delete these resources when the demo is over.

When creating a Cloud Server, you need to specify the image to use for the server, along with the desired amount of resources for the server. Images can be one of the stock images for the various operating systems, or it can be a saved image of a Cloud Server, allowing you to essentially clone a server in a given state.

Ahead of time I created a Cloud Server with a basic web application on it. When you browse the index of that server, it returns a page with the IP address of the server, along with the current UTC date/time. Nothing fancy, but it gives us the information we need for this demonstration, and shows that we're not faking it. I then created a snapshot of that server, from which I can create multiple copies in that exact state. The demo program hard-codes that image ID; in real life you'd have to supply your own value.

Next I get a reference to the flavor I want to use for the servers. A 'flavor' refers to a particular combination of disk, RAM, network capactity, and virtual CPUs for the server. For the demo I'm selecting the Performance 1GB flavor, by finding the flavor with 1024MB RAM and disk size of 20GB.

When you create a Cloud Server you have the option of specifying an SSH keypair that will be added to the root user's ~/.ssh/authorized_keys file. To do this, you create a keypair via the API, and then specify the name of that keypair when you create the server.

Now that we have all of that information, we can create the servers. Since they will be behind the load balancer, they do not need (nor should they have) public IP addresses. So we specify the internal network, called ServiceNet, as the only network created for the server, when we create the server. The calls to create the two servers are identical, with the sole exception of the name. They will both use the saved image as their basis, and will be created with the same flavor and keypair.

Servers take a few minutes to build and get configured, so we need to wait until they are built so that we can determine their internal IP addresses for the load balancer. Pyrax comes with a handy utility method called `wait_for_build()`, which takes an object and waits until it either builds successfully, or errors out. When they are built, we get their private IP addresses, and print them out so that we can verify that the app server we are hitting from the browser is one of these two servers.

Once the servers are built, we define Nodes for them, and also define a VirtualIP object with type "PUBLIC", since we want the load balancer accesible from the public internet. We then create the Cloud Load Balancer with these nodes and VirtualIP. Again, it takes a little while for the load balancer to build, so we call `wait_for_build()` on it, and when it completes, we grab its public IP address. We can now open that address in a web browser, and the page that is displayed should show the IP address of the server that is actually handling the request.

There is an option for building a third server and adding it to the load balancer; I included it so that you can see how to dynamically add servers as needed.

I've also included a cleanup script named `cleanup.py`. When resources are created, I add their type and ID to a dictionary, and then persist it to disk in JSON format. The cleanup script reads in these IDs, and deletes each resource.

