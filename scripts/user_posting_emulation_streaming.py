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
import uuid

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

class serialise_datetime(json.JSONEncoder):
    """
    JSON encoder for serialising datetime objects to ISO format.
    """
    def default(self, obj):
        """
        Override the default method to handle datetime objects during serialisation.

        Parameters:
        - obj (datetime): The object to be serialised.

        Returns:
        - str: The ISO format representation of the datetime object.

        Raises:
        - TypeError: If the input object is not a datetime object.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def send_to_kinesis(records, stream_name):
    """
    Sends data to corresponding stream in AWS Kinesis.
    
    Parameters:
    - records (dict): The data records to be written to the stream.
    - stream_name (str): The name of the corresponding stream.
    """
    # Construct the API endpoint URL for the Kinesis stream
    invoke_url = f'https://t6blhfhug7.execute-api.us-east-1.amazonaws.com/dev/streams/' + stream_name + '/record/'

    # Prepare the payload with data, stream name, and a unique partition key
    payload = json.dumps({
        "StreamName": stream_name,
        "Data": records,
        "PartitionKey": str(uuid.uuid4())
    }, cls=serialise_datetime)

    # Set request headers
    headers = {'Content-Type': 'application/json'}

    # PUT request to the Kinesis API endpoint
    response = requests.request("PUT", invoke_url, headers=headers, data=payload)
    
    # Check the HTTP response status code
    if response.status_code == 200:
        print(f"Data sent to Kinesis stream for {stream_name}")
    else:
        print(f"Failed to send data to Kinesis stream for {stream_name}. Status code: {response.status_code}")

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

            
            #Send data to Kinesis
            send_to_kinesis(pin_result,"streaming-128a59195de3-pin")
            send_to_kinesis(geo_result,"streaming-128a59195de3-geo")
            send_to_kinesis(user_result,"streaming-128a59195de3-user")

if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    
