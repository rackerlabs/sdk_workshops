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
$twoGbFlavor = $computeService->flavor(4);

$server1 = $computeService->server();
$server1->create(array(
    'name'     => 'SK web server 1',
    'image'    => $webServerImage,
    'flavor'   => $twoGbFlavor,
    'networks' => array(
        $computeService->network(Network::RAX_PRIVATE)
    )
));

$server1->waitFor(State::ACTIVE, null, function ($server) {

    printf("Server 1 build progress: %d%%\n", $server->progress);

});

$server2 = $computeService->server();
$server2->create(array(
    'name'     => 'SK Web server 2',
    'image'    => $webServerImage,
    'flavor'   => $twoGbFlavor,
    'networks' => array(
        $computeService->network(Network::RAX_PRIVATE)
    )
));

$server2->waitFor(State::ACTIVE, null, function ($server) {

    printf("Server 2 build progress: %d%%\n", $server->progress);

});

//
// 3. Create load balancer
//

$loadBalancerService = $client->loadBalancerService('cloudLoadBalancers', 'DFW');

$loadBalancer = $loadBalancerService->loadBalancer();

//
// 4. Create nodes using server IPs
//

$server1Node = $loadBalancer->node();
$server1Node->address = $server1->addresses->private[0]->addr;
$server1Node->port = 80;
$server1Node->condition = 'ENABLED';

$server2Node = $loadBalancer->node();
$server2Node->address = $server2->addresses->private[0]->addr;
$server2Node->port = 80;
$server2Node->condition = 'ENABLED';

//
// 5. Create load balancer with those two nodes on HTTP/80
//

$loadBalancer->addVirtualIp('PUBLIC');
$loadBalancer->create(array(
    'name'     => 'SK load balancer - web',
    'port'     => 80,
    'protocol' => 'HTTP',
    'nodes'    => array($server1Node, $server2Node)
));

//
// 6. Get public IP address of load balancer
//

$loadBalancer->waitFor(State::ACTIVE, null, function ($lb) {
});

foreach ($loadBalancer->virtualIps as $vip) {
    if ($vip->type == 'PUBLIC') {
        printf("Load balancer public IPv%d address: %s\n", $vip->ipVersion, $vip->address);
    }
}
