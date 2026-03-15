import os
import sys
import numpy as np
import pandas as pd

"""
definig common constants variable for training pipeline 
"""

TARGET_COLUMN='Result'
PIPELINE_NAME='network_traffic'
ARTIFACT_DIR='Artifacts'
FILE_NAME='phisingData.csv'

DATA_INGESTION_COLLECTION_NAME="network_traffic"
DATA_INGESTION_DATABASE_NAME="NIHAR"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested_data"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRAIN_TEST_RATION = 0.2

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

"""
Data Validation related constants start with DATA_VALIDATION VAR name
"""
DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="Report.yaml"