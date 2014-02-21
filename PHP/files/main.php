<?php

//
// 1. Create client
//

require 'vendor/autoload.php';

use OpenCloud\Rackspace;

$client = new Rackspace(Rackspace::US_IDENTITY_ENDPOINT, array(
    'username' => getenv('RAX_USERNAME'),
    'apiKey' => getenv('RAX_API_KEY')
));

$service = $client->objectStoreService('cloudFiles', 'DFW');

//
// 2. Create container
//

$containerName = 'PHP-images-for-demo';
echo "Creating container " . $containerName . "...\n";
$container = $service->createContainer($containerName);

//
// 3. Upload file (photo)
//

$filePath = __DIR__ . DIRECTORY_SEPARATOR . 'php-elephant.jpg';
$fileHandle = fopen($filePath, 'r');

$destinationFilename = 'elePHPant.jpg';

echo "Uploading file " . $destinationFilename . "...\n";
$object = $container->uploadObject($destinationFilename, $fileHandle);

//
// 4. Create temporary URL with TTL = 90 seconds.
//

$account = $service->getAccount();
$account->setTempUrlSecret('we are in LA!'); // string is optional; default: randomly-generated

const TEMP_URL_TTL = 90; // seconds
const TEMP_URL_ALLOWED_METHOD = 'GET';

$tempUrl = $object->getTemporaryUrl(TEMP_URL_TTL, TEMP_URL_ALLOWED_METHOD);

printf("Temporary download URL = %s\n", $tempUrl);

//
// 5. View photo in browser.
//
