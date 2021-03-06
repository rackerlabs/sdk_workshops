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

$computeService = $client->computeService('cloudServersOpenStack', 'DFW');

//
// 2. Create two servers
//

$webServerImage = $computeService->image(getenv('RAX_IMAGE_ID'));
$twoGbFlavor = $computeService->flavor(2);

$server1 = $computeService->server();

printf("Creating server 1 instance...\n");
$server1->create(array(
    'name'     => 'PHP web server 1',
    'image'    => $webServerImage,
    'flavor'   => $twoGbFlavor,
    'networks' => array(
        $computeService->network(Network::RAX_PRIVATE)
    )
));

$server2 = $computeService->server();

printf("Creating server 2 instance...\n");
$server2->create(array(
    'name'     => 'PHP Web server 2',
    'image'    => $webServerImage,
    'flavor'   => $twoGbFlavor,
    'networks' => array(
        $computeService->network(Network::RAX_PRIVATE)
    )
));

$server1->waitFor(State::ACTIVE, null, function ($server) {

    printf("Server 1 build progress: %d%%\n", $server->progress);

});

$server2->waitFor(State::ACTIVE, null, function ($server) {

    printf("Server 2 build progress: %d%%\n", $server->progress);

});

//
// 3. Create load balancer
//

$loadBalancerService = $client->loadBalancerService('cloudLoadBalancers', 'DFW');

//
// 5. Create load balancer with those two nodes on HTTP/80
//

$loadBalancer = $loadBalancerService->loadBalancer();

$loadBalancer->name = 'PHP load balancer - web';
$loadBalancer->addNode($server1->addresses->private[0]->addr, 80);
$loadBalancer->addNode($server2->addresses->private[0]->addr, 80);
$loadBalancer->port = 80;
$loadBalancer->protocol = 'HTTP';
$loadBalancer->addVirtualIp('PUBLIC');

printf("Creating load balancer %s...\n", $loadBalancer->name);
$loadBalancer->create();

//
// 6. Get public IP address of load balancer
//

$loadBalancer->waitFor(State::ACTIVE, null, function ($lb) {
    printf("Load balancer build status: %s\n", $lb->status);
});

echo str_repeat('=', 80);
printf("Server 1 private IP address: %s\n", $server1->addresses->private[0]->addr);
printf("Server 2 private IP address: %s\n", $server2->addresses->private[0]->addr);
echo str_repeat('-', 80);
foreach ($loadBalancer->virtualIps as $vip) {
    if ($vip->type == 'PUBLIC') {
        printf("Load balancer public %s address: %s\n", $vip->ipVersion, $vip->address);
    }
}
echo str_repeat('=', 80);
