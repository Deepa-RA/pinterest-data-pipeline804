# Milestone 9 - Stream Processing: AWS Kinesis
Real-time streaming data from Pinterest is processed in this milestone.

Kinesis Data Streams is a highly customizable AWS streaming solution.

## Create Data Streams
Using Kinesis Data Streams three data streams, one for each Pinterest table, are created.
The provided AWS account has only been granted permissions to create and describe the following streams:
streaming-<your_UserId>-pin
streaming-<your_UserId>-geo
streaming-<your_UserId>-user
1) Navigate to the Kinesis console, and select the Data Streams section. Choose the `Create stream` button.
2) Choose the desired name for your stream and input this in the Data stream name field. Select the `On-demand` capacity mode.
3) Click on `Create data stream. When your stream is finished creating the Status will change from `Creating` to `Active`.

## Configure an API with Kineses proxy integration
Configure your previously created REST API to allow it to invoke Kinesis actions.

To complete this step instructions from [https://colab.research.google.com/github/AI-Core/Content-Public/blob/main/Content/units/Cloud-and-DevOps/4.%20AWS%20Serverless%20API%20Stack/3.%20Integrating%20API%20Gateway%20with%20Kinesis/Notebook.ipynb] are followed.

## Send data to the Kinesis streams
The script `user_posting_emulation_streaming.py` sends requests to the API, which adds one record at a time to the streams that have been created. Data from the three Pinterest tables is sent to their corresponding Kinesis stream.

The function `send_to_kinesis(records, stream_name)` has been added to the file to accept data from the piterest data and send the data to its corresponding stream name.

The function `run_infinite_post_data_loop` runs continuosly until cancelled to send data to the Kinesis stream.

## Read data to Kinesis stream in Databricks, Clean data and write data to Delta tables
This part is completed within Databricks. The directory Streaming_Data within the Databricks_notebooks directory includes steps from the `Stream Processing` Databricks notebook.
