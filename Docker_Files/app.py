import pandas as pd
from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable
import json
import time



project_id = "your_project_id"
topic_id = "python_bigquery" # pubsub topic name

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []


def main():

    #read csv file
    df = pd.read_csv("data_file.csv") # csv file name
    df.rename(columns={'SMALL HYDRO':'SMALL_HYDRO','SOLAR PV':'SOLAR_PV','SOLAR THERMAL':'SOLAR_THERMAL','WIND TOTAL':'WIND_TOTAL'}, inplace=True)

    json_records = df.to_json(orient='records')
    messages = json.loads(json_records)


    for message in messages:
        message_json = json.dumps(message)
        message_bytes = message_json.encode('utf-8')
        publisher.publish(topic_path, data=message_bytes)
        time.sleep(10)
        print('published message')


    print(f"Published messages with error handler to {topic_path}.")
    
if __name__ == '__main__':
    main()