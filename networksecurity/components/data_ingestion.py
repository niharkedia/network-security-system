import sys
import os
import pandas as pd
import numpy as np
from typing import List

from networksecurity.exception.exception import NetworkSecurityException

## configuration of the data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import *

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import pymongo


load_dotenv()

MONGO_DB_URL=os.getenv("MONGODB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):

        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def export_collection_as_dataframe(self):
        try:
            logging.info("Exporting collection as dataframe")
            
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df= pd.DataFrame(list(collection.find()))
            logging.info("Exported collection as dataframe")


            if "_id" in df.columns.to_list():
                df=df.drop("_id",axis=1)
                logging.info("Dropped _id column")
            
            df.replace({"na":np.nan},inplace=True)
            logging.info("Replaced na with np.nan")
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")

            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            ##creating folder

            dir_path= os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("Exported data into feature store")
            
            return dataframe
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info("Splitting data as train test")

            train_set,test_set=train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_ratio,
                random_state=42
            )
            logging.info("Split data into train and test")

            logging.info(
                "Exited spilt_data_as_train_test method of DataIngestion class"

            )
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting data into train and test files")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
                )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
                )

            logging.info("Exported data into train and test files")

            logging.info(
                "Exited spilt_data_as_train_test method of DataIngestion class"

            )
           
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(
               
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)