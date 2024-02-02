import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
from datetime import datetime, date
import yaml
from sqlalchemy import create_engine, inspect

random.seed(100)

class AWSDBConnector:

    def __init__(self,creds_file):
        """
        Initialise the DataConnector instance with credentials from specified YAML file.

        Args:
            creds_file (str): YAML file containing database credentials.
        """
        self.creds_file = creds_file
        self.db_creds = self.read_db_creds()
        self.engine = self.create_db_connector()

    # read credentials from yaml file and return dictionary of credentials
    def read_db_creds(self):
         """
        Reads database credentials from a YAML file and returns them as a dictionary.

        Returns:
        dict: Database credentials.
        """
         with open(self.creds_file, 'r') as f:
            try:
                inputfile = yaml.safe_load(f)
                return inputfile  
            except yaml.YAMLError as exc:
                print(f"File configuration error: {exc}")
       
        
    def create_db_connector(self):
        # Read the credentials from the YAML file
        creds = self.db_creds
        # Extract the credentials
        HOST = creds['HOST']
        USER = creds['USER']
        PASSWORD = creds['PASSWORD']
        DATABASE = creds['DATABASE']
        PORT = creds['PORT']

       # Create and return the SQLAlchemy engine
        engine= sqlalchemy.create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4")
        return engine

new_connector = AWSDBConnector('db_creds.yaml')
db_creds = new_connector.read_db_creds()

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def load_data(record,topic):
    """
    Define method to send data to relevant kafka topics.
    Parameters
    - record: single entry of data
    - topic: kafka topic to send data to
    """    
    invoke_url = "https://t6blhfhug7.execute-api.us-east-1.amazonaws.com/test/topics/"+topic
    payload = json.dumps({"records": [{"value": record}]},default=json_serial)
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    response = requests.request("POST", invoke_url, headers=headers, data=payload)
    print(invoke_url)
    if response.status_code == 200:
        print(f"Data load to {topic} succesful")
    else:
        print(f"Data load failure for {topic}. Status code: {response.status_code}")

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)

            #Comment out print commands#
            #print(pin_result)
            #print(geo_result)
            #print(user_result)
            
            #Send data to kafka topics
            load_data(pin_result,"128a59195de3.pin")
            load_data(geo_result,"128a59195de3.geo")
            load_data(user_result,"128a59195de3.user")

if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    
