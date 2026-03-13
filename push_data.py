import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL=os.getenv("MONGODB_URL")
print(MONGO_DB_URL)

import certifi 
## root to certify some thing and to make a http connection secure
## ca - certificate authority

ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json_conventor(self,file_path):
        try:

            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            json_data=list(json.loads(data.T.to_json()).values())

            logging.info("csv to json conventor")

            return json_data
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def insert_data_mongodb(self,json_data,database,collection):
        try:
            client=pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
            database=client[database]
            collection=database[collection]

            collection.insert_many(json_data)
        
            logging.info("data inserted into mongodb")

            return len(json_data)
        except Exception as e:
            raise NetworkSecurityException(e,sys)



if __name__ == "__main__":
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE='NIHAR'
    COLLECTION='network_traffic'
    obj=NetworkDataExtraction()
    json_data=obj.csv_to_json_conventor(FILE_PATH)
    print(json_data)
    records=obj.insert_data_mongodb(json_data,DATABASE,COLLECTION)
    print(records)
