/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.jclouds.examples.rackspace;

import java.io.IOException;

import org.jclouds.examples.rackspace.clouddatabases.CreateDatabase;
import org.jclouds.examples.rackspace.clouddatabases.CreateInstance;
import org.jclouds.examples.rackspace.clouddatabases.CreateUser;
import org.jclouds.examples.rackspace.clouddatabases.DeleteDatabase;
import org.jclouds.examples.rackspace.clouddatabases.DeleteInstance;
import org.jclouds.examples.rackspace.clouddatabases.DeleteUser;
import org.jclouds.examples.rackspace.clouddatabases.TestDatabase;
import org.jclouds.examples.rackspace.cloudfiles.DeleteObjectsAndContainer;
import org.jclouds.examples.rackspace.cloudfiles.CloudFilesPublish;
import org.jclouds.examples.rackspace.cloudloadbalancers.CreateLoadBalancerWithNewServers;
import org.jclouds.examples.rackspace.cloudloadbalancers.DeleteLoadBalancers;
import org.jclouds.examples.rackspace.cloudservers.DeleteServer;

/**
 * This example smoke tests all of the other examples in these packages.
 *
 * @author Everett Toews
 */
public class SmokeTest {

   /**
    * To get a username and API key see
    * http://www.jclouds.org/documentation/quickstart/rackspace/
    *
    * The first argument (args[0]) must be your username
    * The second argument (args[1]) must be your API key
    */
   public static void main(String[] args) throws IOException {
      SmokeTest smokeTest = new SmokeTest();
      smokeTest.smokeTest(args);
   }

   private void smokeTest(String[] args) throws IOException {
      Authentication.main(args);
      Logging.main(args);

      CloudFilesPublish.main(args);
      DeleteObjectsAndContainer.main(args);

      CreateLoadBalancerWithNewServers.main(args);
      DeleteServer.main(args);
      DeleteLoadBalancers.main(args);

      CreateInstance.main(args);
      CreateDatabase.main(args);
      CreateUser.main(args);
      TestDatabase.main(args);
      DeleteDatabase.main(args);
      DeleteUser.main(args);
      DeleteInstance.main(args);
   }
}
