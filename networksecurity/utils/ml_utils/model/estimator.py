from networksecurity.constant.training_pipeline import MODEL_FILE_NAME,SAVED_MODEL_DIR
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml,os,sys,dill,pickle


class NetworkModel:
    def __init__(self,model,preprocessor):
        try:
            self.model=model
            self.preprocessor=preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def predict(self,data):
        try:
            logging.info("Predicting the data")
            prediction=self.model.predict(self.preprocessor.transform(data))
            logging.info("Prediction completed successfully")
            return prediction
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def save(self,file_path):
        try:
            logging.info("Saving the model")
            with open(file_path,"wb") as f:
                dill.dump(self,f)
            logging.info("Model saved successfully")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def load(file_path):
        try:
            logging.info("Loading the model")
            with open(file_path,"rb") as f:
                model=dill.load(f)
            logging.info("Model loaded successfully")
            return model
        except Exception as e:
            raise NetworkSecurityException(e,sys)