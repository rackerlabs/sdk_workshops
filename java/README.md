# Scale 12x Examples
This example code based on the jclouds Rackspace examples.

   mvn dependency:copy-dependencies "-DoutputDirectory=./lib"
   javac -classpath "lib/*;src/main/java/;src/main/resources/" src/main/java/org/jclouds/examples/rackspace/*.java
   java -classpath "lib/*;src/main/java/;src/main/resources/" org.jclouds.examples.rackspace.SmokeTest scale_workshops 9b0702a0f3b143c4b15ff62b2589e768
   
To run a single example:

   java -classpath "lib/*;src/main/java/;src/main/resources/" org.jclouds.examples.rackspace.cloudfiles.GenerateTempURL scale_workshops 9b0702a0f3b143c4b15ff62b2589e768