import sys
from networksecurity.components.data_ingestion import DataIngestion


from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig,Training_Pipeline_Config


if __name__=="__main__":
    try:
        logging.info("Starting data ingestion")
        training_pipeline_config=Training_Pipeline_Config()
        data_ingestion_config=DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )

        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("Data ingestion initiated")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data ingestion completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)