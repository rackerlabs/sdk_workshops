# Working with Cloud Databases


To do this, we're going to use *pyrax*, the Python SDK for OpenStack clouds. If you're not familiar with pyrax, you can read the docs at https://github.com/rackspace/pyrax/tree/master/docs

I have an environment configuration for this named 'scale12x'; this sets up my keyring username for authentication, and also sets my desired region to 'DFW'. I also included a small method for adding the IDs of the resources the script creates to a dictionary that I write to disk in JSON format. This allows me to run a cleanup.py script to delete these resources when the demo is over.

Cloud Databases are specialized Cloud Server instances which are only accessible from other cloud resources, such as Cloud Servers or Cloud Load Balancers that are located within the same region. So we'll create a Cloud Database instance, along with a Cloud Load Balancer, and then verify that it is accessible from the outside via the load balancer. It is also important to remember that the Cloud Database API only gives you the ability to create and manage databases; it doesn't represent a full client for creating tables and inserting/querying data. For those you use any regular MySQL client.

Please note the confusing terminology: you don't create a database; you create an *instance*, and then create one or more databases on that instance. Think of an instance as a Cloud Server that comes pre-configured with a private network, and MySQL already installed. These instances can be different sizes of RAM and disk space, depending on your data needs.

For this, we'll use the smallest flavor, with 512MB of RAM. To get this, we list all the flavors, and then select the one whose 'ram' attribute is 512MB. We then create the instance, passing in this flavor, and also specifying that we want a 2GB volume. This will take a little while to build, so we call the utility method `wait_for_build()`, which will block until the instance build is complete.

Once the instance is built, you can create databases on it. To do this, call the `create_database()` method on the instance, passing in the name of the database, which in this case is 'demodb'. You will also need to create a user and give them access to one or more of the databases you create.

Next we define a Node to represent the database instance, along with a Virtual IP object with type "PUBLIC", since we want the load balancer accesible from the public internet. The node requires the address of the instance, which we can get from the `hostname` attribute of the instance. It will be some really long ugly name like 'b5c33e8ef2ffa520520a120b9062cd9557a82301.rackspaceclouddb.com'. The Node and VirtualIP are then used to create the Cloud Load Balancer. Again, it takes a little while for the load balancer to build, so we call `wait_for_build()` on it, and when it completes, we grab its public IP address. We'll need to use this address when working with our MySQL clients.

Using the standard MySQL client, you can connect to the database by using the Load Balancer's IP address as the host:

    mysql -h <ip_address> -u demouser -p

When prompted for the password, enter the one we used when we created the user: 'topsecret'. This will connect us to our Cloud Database instance, where we can now use it like any other MySQL database:

    MySQL [(none)]> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | demodb             |
    +--------------------+
    2 rows in set (0.00 sec)

You can see that the database we created in the script, 'demodb', shows up in the database listing. We could now create a table, add rows of data to that table, and everything else we would normally do with a database.

There is also a script called 'cleanup.py' included; it simply deletes the database instance. There is no need to delete anything inside the instance; it will all get wiped out when you delete the instance.