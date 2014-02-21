<?php

//
// 1. Create client
//

require 'vendor/autoload.php';

use OpenCloud\Rackspace;
use OpenCloud\Compute\Constants\Network;
use OpenCloud\Common\Constants\State;

$client = new Rackspace(Rackspace::US_IDENTITY_ENDPOINT, array(
    'username' => getenv('RAX_USERNAME'),
    'apiKey' => getenv('RAX_API_KEY')
));

$databaseService = $client->databaseService('cloudDatabases', 'DFW');

//
// 2. Create DB server instance.
//

$twoGbFlavor = $databaseService->flavor(4);

$dbInstance = $databaseService->instance();
$dbInstance->name = 'PHP demo database instance';
$dbInstance->volume = new stdClass();
$dbInstance->volume->size = 20; // GB
$dbInstance->flavor = $twoGbFlavor;
$dbInstance->create();

$dbInstance->waitFor(State::ACTIVE, null, function ($dbInstance) {

    printf("Database instance build status: %s\n", $dbInstance->status);

});

//
// 2. Create database.
//

$db = $dbInstance->database();
$db->name = 'demo_db';

printf("Creating database %s...\n", $db->name);
$db->create();

//
// 3. Create database user and give it access to database.
//

$user = $dbInstance->user();
$user->name = 'demo_user';
$user->databases = array('demo_db');
$user->password = 'h@X0r!';

printf("Creating database user %s...\n", $user->name);
$user->create();

//
// 4. Create a load balancer to allow access to the database
// from the Internet.
//

$loadBalancerService = $client->loadBalancerService('cloudLoadBalancers', 'DFW');

$loadBalancer = $loadBalancerService->loadBalancer();

$dbServerNode = $loadBalancer->node();
$dbServerNode->address = $dbInstance->hostname;
$dbServerNode->port = 3306;
$dbServerNode->condition = 'ENABLED';

$loadBalancer->addVirtualIp('PUBLIC');
$loadBalancer->create(array(
    'name'     => 'My proxy load balancer',
    'port'     => 3306,
    'protocol' => 'MYSQL',
    'nodes'    => array($dbServerNode)
));

$loadBalancer->waitFor(State::ACTIVE, null, function ($lb) {
});

foreach ($loadBalancer->virtualIps as $vip) {
    if ($vip->type == 'PUBLIC') {
        printf("Load balancer public IPv%d address: %s\n", $vip->ipVersion, $vip->address);
    }
}
