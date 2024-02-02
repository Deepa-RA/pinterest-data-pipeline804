# Milestone 8 - Batch Processing: AWS MWAA
This milestone demonstrates how to orchestrate Databricks Workloads on AWS MWAA
## Create & upload a DAG to MWAA
- DAGs (Directed Acyclic Graphs) are used to define a workflow (order and execution of jobs).
- The jobs are managed by the Databricks' Jobs API (a set of tools for developers) or the user interface (UI).
- AWS MWAA is used to oversee and schedule the jobs, providing a centralized way to monitor and manage the workflow.

The DAG is saved in the file 128a59195de3_dag.py.

The parameters are as follows:

notebook_path: path to the Databricks- file /Users/ramaiya89@hotmail.com/Batch Processing - Databricks
start_date: the date the DAG begins - datetime(2024, 1, 30)
schedule_interval: the DAG is ran daily - '@daily'
existing_cluster_id: cluster id of Databricks cluster - 1108-162752-8okw8dgg

The DAG file is then loaded to the mwaa-dags-bucket/dags/ in the S3 bucket under the name 128a59195de3_dag.

## Trigger the DAG
Once uploaded to the `dags` folder, you will be able to see the new DAG in the Airflow UI on your MWAA environment, under paused DAGs. In order to manually trigger the DAG, you will first have to unpause it.
