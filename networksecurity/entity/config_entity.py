from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)
print(training_pipeline.FILE_NAME)


class Training_Pipeline_Config:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name =training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(os.getcwd(),self.artifact_name)
        self.file_name=training_pipeline.FILE_NAME
        self.timestamp=timestamp
        
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:Training_Pipeline_Config):
        self.data_ingestion_dir=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
            )
        self.feature_store_file_path=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
            )
        self.training_file_path=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
            )
        self.train_test_ratio=training_pipeline.TRAIN_TEST_RATION 
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,training_pipeline_config:Training_Pipeline_Config):
        self.data_validation_dir=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
            )
        self.data_validation_valid_dir=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
            )
        self.data_validation_invalid_dir=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
            )
        self.valid_train_file_path=os.path.join(
            self.data_validation_valid_dir,
            training_pipeline.TRAIN_FILE_NAME
            )
        self.valid_test_file_path=os.path.join(
            self.data_validation_valid_dir,
            training_pipeline.TEST_FILE_NAME
            )
        self.invalid_train_file_path=os.path.join(
            self.data_validation_invalid_dir,
            training_pipeline.TRAIN_FILE_NAME
            )
        self.invalid_test_file_path=os.path.join(
            self.data_validation_invalid_dir,
            training_pipeline.TEST_FILE_NAME
            )
        self.drift_report_file_path=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
            )


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:Training_Pipeline_Config):
        self.data_transformation_dir=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
            )
        self.transformed_train_file_path=os.path.join(
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy")
            )
        self.transformed_test_file_path=os.path.join(
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv","npy")
            )
        self.transformed_object_file_path=os.path.join(
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
            )

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:Training_Pipeline_Config):
        self.model_trainer_dir=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME
            )
        self.trained_model_file_path=os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_FILE_NAME
            )
        self.expected_score=float(training_pipeline.MODEL_TRAINER_EXPECTED_SCORE)
        self.over_fitting_under_fitting_threshold=float(training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD)
