# Working With Cloud Files


To do this, we're going to use *pyrax*, the Python SDK for OpenStack clouds. If you're not familiar with pyrax, you can read the docs at https://github.com/rackspace/pyrax/tree/master/docs

I have an environment configuration for this named 'scale12x'; this sets up my keyring username for authentication, and also sets my desired region to 'DFW'. I also included a small method for adding the IDs of the resources the script creates to a dictionary that I write to disk in JSON format. This allows me to run a cleanup.py script to delete these resources when the demo is over.

We start by creating a container. I've named it 'python-demo'; you should name it something unique that identifies the contents. Note that the `create_container()` method will create the named container if it doesn't exist yet, but will not throw an error if a container of that name already exists. In either case, it returns a Container object.

I've included a small PNG file of the logo for Python, which we'll upload to the container next. This is done by calling the `upload_file()` method, passing in the container (either its name, or the corresponding Container object) and the path to the file. You may optionally specify a name for the object when it is stored; if you don't, the original name of the object is used.

One of the handy things you can do with objects in Cloud Files is to generate a temporary URL for accessing it. Normally you would need the account credentials to access anything stored in Cloud Files, but for those times that you want to provide a way for someone to download the file, you can generate a Temporary URL.

To do this, you first need to set the Temp URL Key, which is used to generate and validate URLs. You can provide your own, or you can let pyrax do it for you by not passing any value to the `set_temp_url_key()` call. If needed, you can then retrieve the current key by calling `get_temp_url_key()`. Normally, though, you don't need to use it directly. However, if you create a temp URL and then later wish to revoke it before it expires, you can change the key on the server, and any URLs generated with the prior key will no longer work.

Next, the `get_temp_url()` method is called, passing in the container and object name, along with an expiration time in seconds, and an optional HTTP method. The default method is **GET**, but you can also generate URLs for **PUT** that allow users to upload objects.

The script then generates a temp URL for the picture that was uploaded earlier, prints it out, and then pauses. Since the object was created with an expiration time of 2 minutes, we can now download it and verify that yes, we did indeed retrieve the object. If we wait until after the expiration of the URL and try to download it again, we should receive a *401 Unauthorized* error.

The other option for making objects accessible to others is to publish the container to the Akamai CDN network, which is integrated with Cloud Files. To do this, just call the Container's `make_public()` method, optionally specifying a TTL for objects. The default is 72 hours, with a minimum of 15 minutes and a maximum of one year. Once a container is made public, you can access any object within it by via its `cdn_uri` property. Note that if you later remove it from the CDN by calling the container's `make_private()` method, the objects may still be available for the duration of the container's TTL.


