# Milestone 4 - Batch Processing: Connect a MSK cluster to a S3 bucket
This milestone demonstrates how to use MSK Connect to connect an MSK cluster to a S3 bucket. This ensures that any data going through the cluster is automatically saved and stored in the dedicated S3 bucket.

An S3 bucket, an IAM role that allows to write to this bucket and a VPC Endpoint to S3 have already been configured by Ai Core on my AWS account.

## Create a custom plugin with MSK Connect
A plugin will contain the code that defines the logic of our connector.
### Step 1 - Retrieve bucket name
1) This can be found with the assigned UserId in the S3 console - user-128a59195de3-bucket
### Step 2 - On EC2 client, download Confluent.io Amazon S3 Connector and copy it to the S3 bucket 
This connector is a sink connector that exports data from Kafka topics to S3 objects in either JSON, Avro or Bytes format
1) Connect to EC2 client machine
```
ssh -i "128a59195de3-key-pair.pem" ec2-user@ec2-54-208-238-180.compute-1.amazonaws.com
```
2)  To do download & copy this connector run the code below inside your client machine:
```
# assume admin user privileges
sudo -u ec2-user -i
# create directory where we will save our connector 
mkdir kafka-connect-s3 && cd kafka-connect-s3
# download connector from Confluent
wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-s3/versions/10.0.3/confluentinc-kafka-connect-s3-10.0.3.zip
# copy connector to our S3 bucket
aws s3 cp ./confluentinc-kafka-connect-s3-10.0.3.zip s3://user-128a59195de3-bucket/kafka-connect-s3/
```
If this has run successfully, the folder and file should be visible inside the S3 bucket.
### Step 3 - Create custom plugin in the MSK Connect console
1) Navigate to the MSK Connect console and select customised plugins on the left pane.
2) Click on "Create customised plugin".
3) Enter the S3 URI for the downloaded ZIP file. This can be found by selecting the file in the S3 bucket and looking under the Object Overview
s3://user-128a59195de3-bucket/kafka-connect-s3/confluentinc-kafka-connect-s3-10.0.3.zip
4) The plugin name should be - 128a59195de3-plugin

## Create a connector with MSK Connect
This step will enable data from the MSK Cluster to be sent to the S3 bucket. Any data that will pass through the MSK cluster will be automatically uploaded to the S3 bucket.
1) Navigate to the MSK console and select "Connectors" under MSK Connect. Choose "Create Connector".
2) Select the correct plugin - user-128a59195de3-bucket-plugin and click "Next".
3) The connector name should be set as 128a59195de3-connector and under MSK cluster the pinterest-msk-cluster should be selected.
4) The following configuration should be added to the "Connector configuration settings":
```
connector.class=io.confluent.connect.s3.S3SinkConnector
# same region as our bucket and cluster
s3.region=us-east-1
flush.size=1
schema.compatibility=NONE
tasks.max=3
# include nomeclature of topic name, given here as an example will read all data from topic names starting with msk.topic....
topics.regex=user-128a59195de3-bucket.*
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
value.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
storage.class=io.confluent.connect.s3.storage.S3Storage
key.converter=org.apache.kafka.connect.storage.StringConverter
s3.bucket.name=user-128a59195de3-bucket
```
5) Leave the rest of the configurations as default, except for:
- Connector type change to Provisioned
- MCU count per worker is set to 1
- Number of workers is set to 1
- Worker Configuration, select Use a custom configuration, then pick confluent-worker
- Access permissions, where you should select the IAM role you have created previously - 128a59195de3-ec2-access-role
6) Skip the rest of the pages until you get to Create connector button page. Once your connector is up and running you will be able to visualise it in the Connectors tab in the MSK console.