from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,Training_Pipeline_Config
from networksecurity.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import os,sys


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=Training_Pipeline_Config()
        self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
        self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"Error in data ingestion: {e}")
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            data_validation=DataValidation(self.data_validation_config,data_ingestion_artifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            logging.error(f"Error in data validation: {e}")
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            data_transformation=DataTransformation(self.data_transformation_config,data_validation_artifact)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            logging.info("Starting model training")
            model_trainer=ModelTrainer(self.model_trainer_config,data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Model training completed")
            return model_trainer_artifact
        except Exception as e:
            logging.error(f"Error in model training: {e}")
            raise NetworkSecurityException(e,sys)
    
    def run_pipeline(self):
        try:
            logging.info("Starting training pipeline")
            
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)

            logging.info("Training pipeline completed")
            return model_trainer_artifact
        except Exception as e:
            logging.error(f"Error in training pipeline: {e}")
            raise NetworkSecurityException(e,sys)
