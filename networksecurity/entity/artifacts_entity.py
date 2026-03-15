"""
this file is used to tell what all output we want from the data ingestion
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    
    training_file_path:Path
    testing_file_path:Path

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:Path
    valid_test_file_path:Path
    invalid_train_file_path:Path
    invalid_test_file_path:Path
    drift_report_file_path:Path