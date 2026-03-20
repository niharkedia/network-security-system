from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.logging.logger import logging
from sklearn.model_selection import RandomizedSearchCV
import yaml,os,sys,dill,pickle

import numpy as np
import pandas as pd


def read_yaml_file(file_path:str)->dict:
    """
    Read a YAML file and return its content as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



def save_numpy_array_data(file_path:str,array:np.ndarray)->None:
    """
    Save a numpy array to a file.
    file_path location of the file to save
    array numpy array to save
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path ,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)



def save_object(file_path:str,obj:object)->None:
    """
    Save an object to a file.
    file_path location of the file to save
    obj object to save
    """
    try:
        logging.info(f"Saving object to {file_path}")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj,file)
        logging.info(f"Object saved to {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_object(file_path:str)->object:
    """
    Load an object from a file.
    file_path location of the file to load
    obj object to load
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")
        logging.info(f"Loading object from {file_path}")
        with open(file_path,"rb") as file:
            obj=pickle.load(file)
            return obj
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.ndarray:
    """
    Load a numpy array from a file.
    file_path location of the file to load
    array numpy array to load
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")
        logging.info(f"Loading numpy array from {file_path}")
        with open(file_path,"rb") as file:
            array=np.load(file)
            return array
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e



def evaluate_model(models,params,x_train,y_train,x_test,y_test):
    try:
        logging.info("Evaluating the model")
        model_report:dict={}
        for model_name,model in models.items():

            logging.info(f"Training {model_name}")
            para = params[model_name]

            if para:
                rs = RandomizedSearchCV(model,para,n_iter=5,cv=2,scoring="accuracy",random_state=42,n_jobs=-1)
                rs.fit(x_train,y_train)
                model.set_params(**rs.best_params_)
            
            model.fit(x_train,y_train)
            
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            train_score=get_classification_score(y_train,y_train_pred)
            test_score=get_classification_score(y_test,y_test_pred)
            
            model_report[model_name]=test_score.accuracy
            logging.info(f"{model_name} - Test Accuracy: {test_score.accuracy}")
        
        logging.info("Model evaluation completed successfully")
        return model_report
    except Exception as e:
        raise NetworkSecurityException(e,sys)