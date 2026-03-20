from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact

import yaml,os,sys,dill,pickle


import numpy as np
import pandas as pd 


from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score


def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        logging.info("Calculating classification metrics")
        accuracy=accuracy_score(y_true,y_pred)
        model_precision=precision_score(y_true,y_pred)
        model_recall=recall_score(y_true,y_pred)
        model_f1_score=f1_score(y_true,y_pred)
        logging.info("Classification metrics calculated successfully")
        return ClassificationMetricArtifact(
            accuracy=accuracy,
            precision=model_precision,
            recall=model_recall,
            f1_score=model_f1_score
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys)