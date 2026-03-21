
from networksecurity.entity.artifacts_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.utils.main_utils.utils import save_object,save_numpy_array_data
from networksecurity.logging.logger import logging
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from pathlib import Path
import pandas as pd 
import numpy as np

import os,sys


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            logging.info("Data Transformation initialized")
        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info(f"Reading data from {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error in reading data: {e}")
            raise NetworkSecurityException(e,sys)


    def gat_data_transformer_object(cls)->Pipeline:
        """
         it initialises a KNNImputer object with the paramters specified in the training.pipeline.py file
         and returns a Pipeline object with the knn imputer object as the first step.

         Args:
            cls: DataTransformation

         Returns:
            Pipeline: Pipeline object with the knn imputer object as the first step
        """
        logging.info("Getting data transformer object")
        try:
            knn_imputer_param=DATA_TRANSFORMATION_IMPUTER_PARAMS
            knn_imputer=KNNImputer(**knn_imputer_param)
            logging.info(f"KNNImputer object created successfully with parameters: {knn_imputer_param}")

            preprocessor=Pipeline([
                ("knn_imputer",knn_imputer)
            ])
            logging.info("Data transformer object created successfully")
            return preprocessor
        except Exception as e:
            logging.error(f"Error in getting data transformer object: {e}")
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_df=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=self.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            ## testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            ## getting the preprocessor object
            preprocessor=self.gat_data_transformer_object()

            ## transforming the data
            input_feature_train_arr=preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor.transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

           

            ## saving the transformed data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
             ## saving the preprocessor object
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)


            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            train_file_path=self.data_transformation_config.transformed_train_file_path
            test_file_path=self.data_transformation_config.transformed_test_file_path
            logging.info("Data transformation initiated")

            save_object("final_model/preprocessor.pkl",preprocessor)

            return DataTransformationArtifact(
                transformed_train_file_path=train_file_path,
                transformed_test_file_path=test_file_path,
                transformed_object_file_path=transformed_object_file_path
                )
        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise NetworkSecurityException(e,sys)
