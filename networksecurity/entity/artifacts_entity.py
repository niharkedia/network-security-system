"""
this file is used to tell what all output we want from the data ingestion
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    
    training_file_path:Path
    testing_file_path:Path