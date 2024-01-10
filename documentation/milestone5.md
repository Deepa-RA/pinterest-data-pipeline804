# Milestone 5 - Batch Processing: Configuring an API in API Gateway
Build own API to replicate Pinterest's experimental data pipeline. The API will send data to the MSK cluster, which in turn will be stored in an S3 bucket via the connect built in milestone 4.

## Build a Kafka REST proxy integration method for the API
An API with the same name as given user id has been provided by Ai Core.
### Step 1 - Create resourse to build a PROXY integration for the API
1) Navigte to API Gateway on the AWS console
2) Select API with given user id `128a59195de3`
3) Select `Create Resource`. Turn on the `Proxy resource` toggle, add `Resource name` as `{proxy+}` and `Enable Cors`.
### Step 2 - Create HTTP ANY method
1) Once done select the created `{proxy+}` resource and select the `ANY` method type.
2) Select `Edit integration`. For integration type select `HTTP` and toggle the `HTTP proxy integration` on. Select the`HTTP method` as `ANY`.
3) Set the `Endpoint URL` as http://ec2-54-208-238-180.compute-1.amazonaws.com:8082/{proxy}. This uses the Public DNS for the EC2 instance. Save the changes
### Step 3 - Deploy API
1) `Deploy API` and create new stage called `test`.

## Set up Kafka REST proxy on the EC2 client
To consume data using MSK from the API additional packages need to be downloaded on the client EC2 machine - these are used to communicate with the MSK cluster.
### Step 1 - Install Confluent package
1) Connect to the EC2 client machine
```
ssh -i "128a59195de3-key-pair.pem" ec2-user@ec2-54-208-238-180.compute-1.amazonaws.com
```
2) Install the REST proxy package
```
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
tar -xvzf confluent-7.2.0.tar.gz 
```
A `confluent-7.2.0` directory will have been created on the EC2 instance.
### Step 2 - Modify the kafka-rest.properties file.
Allow the REST proxy to perform IAM authentication to the MSK cluster by modifying the kafka-rest.properties file.
1) To configure the REST proxy to communicate with the desired MSK cluster, and to perform IAM authentication you first need to navigate to confluent-7.2.0/etc/kafka-rest and modify the kafka-rest.properties file.
```
cd confluent-7.2.0/etc/kafka-rest
nano kafka-rest.properties
```
2) Modify the bootstrap.servers and the zookeeper.connect variables in this file, with the corresponding Boostrap server string and Plaintext Apache Zookeeper connection string respectively. Guidance on how to find these can be found in Milestone 3.
3) To surpass the IAM authentication of the MSK cluster, we will make use of the IAM MSK authentication package again (can be found here: https://github.com/aws/aws-msk-iam-auth). Add the following to your kafka-rest.properties file.
```
# Sets up TLS for encryption and SASL for authN.
client.security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
client.sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="Your Access Role";

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
To allow communication between the REST proxy and the cluster brokers, all configurations should be prefixed with client.
### Step 3 - Start the REST proxy
Before sending messages to the API, in order to make sure they are consumed in MSK, we need to start our REST proxy.
1) Navigate to the `confluent-7.2.0/bin folder`.
cd confluent-7.2.0/bin
2) Run tne following command.
```
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```
If successful and your proxy is ready to receive requests from the API, you should see `INFO Server started, listening for requests...` in your EC2 console.