from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
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