# Milestone 3 - Batch Processsing: Configure the EC2 Kafka Client
This milestone demonstrates the steps required to configure an EC2 instance to use an Apache client machine.

## Create a .pem key file locally
This is required to connect to the EC2 instance
### Step 1 - Retrieve key pair
1) Navigate to the Parameter Store in you AWS account
2) Using your SSH Keypair ID find and select the key pair associated with your EC2 instance 
3) The key pair can be retrieved by showing the Value field. Copy its entire value (including the BEGIN and END header) and paste it in the .pem file.
### Step 2 - Create .pem file
1) Using the EC2 console identify your instance and retrieve the key pair name. Save the .pem file as key pair name.pem.

## Connect to the EC2 instance using SSH client
The private key file(.pem) created in the previous step is required to connect to the EC2 instance.
1) Set permissions for the private key file to ensure it is accessible by the owner only.
``` 
chmod 400 128a59195de3-key-pair.pem
```
2) Connect to the EC2 instance using:
ssh - the ssh client
-i key pair name.pem - the private key file for the EC2 instance
ec2-user@ec2-54-208-238-180.compute-1.amazonaws.com - the username and public DNS

```
ssh -i "128a59195de3-key-pair.pem" ec2-user@ec2-54-208-238-180.compute-1.amazonaws.com
```
## Set up Kafka on the EC2 instance
### Step 1 - Install Kafka on EC2 instance
1) Ensure you are connected to your EC2 instance
2) Install Java on the client instance by running the following command
```
sudo yum install java-1.8.0
```
3) Then download Apache Kafka 2.12-2.8.1 using the following code:
```
wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
```
4) Run the following command in the directory where you downloaded the TAR file in the previous step.
```
tar -xzf kafka_2.12-2.2.1.tgz
```
### Step 2 - Install IAM authentication package on EC2 machine
Ai Core has created an IAM authenticated MSK cluster for use for this project.
In order to connect to the IAM authenticated cluster, you will need to install the appropriate packages on your EC2 client machine.
1) Navigate to your Kafka installation folder and then in the libs folder. Inside here download the IAM MSK authentication package from Github, using the following command:
```
cd kafka_2.12-2.8.1/libs/
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar
```
2) Create CLASSPATH environment variable. This will store the location of the aws-msk-iam-auth-1.1.5-all.jar file and give the Kafka client access to the Amazon MSK IAM libraries regardless of the location commands are run from.
```
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```
### Step 3 - Prerequisite for configuring EC2 client to use AWS IAM for cluster authentication
1) Navigate to the IAM console on your AWS account.
2) On the left hand side select the Roles section.
3) Select the role with the following format: <your_UserId>-ec2-access-role (128a59195de3-ec2-access-role).
4) Retrieve this role ARN as it will be required for cluster authentication.
5) Go to the Trust relationships tab and select Edit trust policy
6) Click on the Add a principal button and select IAM roles as the Principal type
7) Replace ARN with the <your_UserId>-ec2-access-role ARN you have just copied
8) By following the steps above you will be able to now assume the <your_UserId>-ec2-access-role, which contains the necessary permissions to authenticate to the MSK cluster.
### Step 4 - Configure Kafka client to use AWS IAM authentication to the cluster by creating the client.properties file
1) Navigate to the bin folder in the Kafka directory
```
cd kafka_2.12-2.8.1/bin/
```
2) Create/edit client.properties file
```
nano client.properties
```
3) In the client.properties file, copy and paste the following code:
```
# Sets up TLS for encryption and SASL for authN.
security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required awsRoleArn="arn:aws:iam::584739742957:role/128a59195de3-ec2-access-role";

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
## Create Kafka topics
### Step 1 - Retrieve information about MSK cluster
1) Navigate to the msk management console. Select the pinterest-msk-cluster and select "View client information"
2) Retrieve the following information
BootstrapServerString: b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098
Plaintext Apache Zookeeper connection string: z-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181,z-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:2181
### Step 2 - Create Kafka topics
1) Navigate to the bin folder in the Kafka directory.
```
cd kafka_2.12-2.8.1/bin/
```
2) The generic command to create a topic is written below. If the command run succesfully you will see the following message: Created topic <topic_name>.
```
./kafka-topics.sh --bootstrap-server BootstrapServerString --command-config client.properties --create --topic <topic_name>
```
3) Create a topic for the Pinterest posts data.
```
./kafka-topics.sh --bootstrap-server b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 128a59195de3.pin
```
4) Create a topic for the post geolocation data.
```
./kafka-topics.sh --bootstrap-server b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 128a59195de3.geo
```
5) Create a topic for the post user data.
```
./kafka-topics.sh --bootstrap-server b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 128a59195de3.user


