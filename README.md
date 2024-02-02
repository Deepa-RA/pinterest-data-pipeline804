# Pintrest Data Pipeline

## Contents
1) Introduction
2) Instructions

## Introduction
Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project, the AWS cloud is utilised to mimic this system.

This project demonstrates the following skills:
Milestone 1 & 2:
1) Connecting and navigating to AWS
BATCH PROCESSING
Milestone 3
1) Configuring an Amazon EC2 instance to use as an Apache Kafka client machine
2) Configuring EC2 Kafka Client
Milestone 4
1) Use MSK connect to connect MSK cluster to S3 bucket.
Milestone 5
4) Configuring an API in API Gateway. API will send data to the MSK Cluster, through the connector, storing data in the S3 bucket.
Milestone 6 
1) Read data from AWS into Databricks
Milestone 7
1) Cleaning the dataframes on Databricks
2) Querying the data on Databricks
Milestone 8
Orchestrate Databricks workload on AWS MWAA
1) Create and upload a DAG to MWAA environment
2) Trigger DAG to run Databricks notebook

The key tools utilised in this project include:

AWS EC2: create an EC2 instance to manage batch processing of data
AWS IAM: IAM User authentication on the MSK Cluster for batch data processing and for Kinesis access for streaming data.
AWS MSK: manage cluster, create custom plugins and connectors for batch data processing.
AWS MWAA: use of DAG to monitor workflow of batch processed data.
Apache Kafka: to query and analyse Pinterest data pipeline.
Databricks: manage and query batch and streaming data.
Airflow UI: interface to monitor the workflow of the DAG for batch data.
AWS Kinesis: to store and process streaming data.

## Instructions

### Setup
1) To utilise this project clone the repository from GitHub onto local machine
```
git clone https://github.com/Deepa-RA/pinterest-data-pipeline804.git
```
2) Ensure the project is run within the repository
```
cd pinterest-data-pipeline804/
```
### Running the project
1) The directory /documentation contains guidance for completing each milestone
2) The directory /Databricks_notebooks contains two further directories for the Batch processing and Stream processing parts of this project. The notebooks within here are run in Databricks.
3) The directory /scripts contain the python scripts `user_posting_emulation.py` and `user_posting_emulation_streaming.py` to send data to the Kafka topics and Kinesis streams respectively.