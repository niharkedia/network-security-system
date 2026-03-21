from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifacts_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import load_object,save_object,load_numpy_array_data,evaluate_model
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
import os
import sys
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import dagshub
from dotenv import load_dotenv




class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
            try:
                logging.info(f"{'='*30}Model Trainer Inititation{'='*30}")
                self.model_trainer_config=model_trainer_config
                self.data_transformation_artifact=data_transformation_artifact
                logging.info(f"{'='*30}Model Trainer Inititation Completed{'='*30}")
            except Exception as e:
                raise NetworkSecurityException(e,sys)
    
   
    def track_mlflow(self, best_model, classification_metric, model_name, x_train, dataset_type="Train"):
        """
        Track model metrics, parameters, and artifacts in MLflow.
        
        Args:
            best_model: The trained sklearn model
            classification_metric: ClassificationMetricArtifact with accuracy, f1, precision, recall
            model_name: Name of the model (e.g. "XGBClassifier")
            x_train: Training data (used to infer model signature)
            dataset_type: "Train" or "Test" to differentiate runs
        """
        try:
        
            with mlflow.start_run(run_name=f"{model_name}_{dataset_type}"):

                # Log model name and hyperparameters
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("dataset_type", dataset_type)

                # Log best hyperparameters
                best_params = best_model.get_params()
                for param_name, param_value in best_params.items():
                    try:
                        mlflow.log_param(param_name, param_value)
                    except Exception:
                        pass  # Skip params that can't be logged (e.g. complex objects)

                # Log metrics
                mlflow.log_metrics({
                    "accuracy": classification_metric.accuracy,
                    "f1_score": classification_metric.f1_score,
                    "precision": classification_metric.precision,
                    "recall": classification_metric.recall
                })

                # Infer model signature
                signature = infer_signature(x_train, best_model.predict(x_train))

                # Log model with signature
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    name="model",
                    signature=signature
                )

                logging.info(f"MLflow tracking successful for {model_name} ({dataset_type})")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            logging.info("Training the model")
            models={
                "KNeighborsClassifier":KNeighborsClassifier(n_jobs=-1),
                "RandomForestClassifier":RandomForestClassifier(n_jobs=-1),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "SVC":SVC(),
                "GaussianNB":GaussianNB(),  
                "LogisticRegression":LogisticRegression(max_iter=1000,n_jobs=-1),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "GradientBoostingClassifier":GradientBoostingClassifier(),
                "XGBClassifier":XGBClassifier(verbosity=0,n_jobs=-1),
                "LGBMClassifier":LGBMClassifier(verbose=-1,n_jobs=-1),
                "CatBoostClassifier":CatBoostClassifier(verbose=0)
            }   
            params={
                 "KNeighborsClassifier":{
                    "n_neighbors":[3,5,7,9,11]
                 },
                 "RandomForestClassifier":{
                    "n_estimators":[100,200,300,400,500],
                    "max_depth":[10,20,30,40,50],
                    "min_samples_split":[2,5,10,15,20],
                    "min_samples_leaf":[1,2,5,10,15],
                    "bootstrap":[True,False],
                    "criterion":['gini','entropy','log_loss']
                 },
                 "DecisionTreeClassifier":{
                    "max_depth":[10,20,30,40,50],
                    "min_samples_split":[2,5,10,15,20],
                    "min_samples_leaf":[1,2,5,10,15],
                    "criterion":['gini','entropy','log_loss'],
                    "max_features":['sqrt','log2']
                 },
                 "SVC":{
                    "C":[0.1,1,10,100],
                    "kernel":["linear","rbf","poly"],
                    "gamma":["scale","auto"]
                 },
                 "GaussianNB":{},
                 "LogisticRegression":{},

                 "AdaBoostClassifier":{
                    "n_estimators":[100,200,300,400,500],
                    "learning_rate":[0.01,0.1,1]
                 },
                 "GradientBoostingClassifier":{
                    "n_estimators":[100,200,300,400,500],
                    "learning_rate":[0.01,0.1,1],
                    "max_depth":[3,5,10,20],
                    "subsample":[0.6,0.8,1]
                 },
                 "XGBClassifier":{
                    "n_estimators":[100,200,300,400,500],
                    "learning_rate":[0.01,0.1,1],
                    "max_depth":[3,5,10,20],
                    "min_child_weight":[1,2,5,10],
                    "subsample":[0.6,0.8,1],
                    "colsample_bytree":[0.6,0.8,1]
                 },
                 "LGBMClassifier":{
                    "n_estimators":[100,200,300,400,500],
                    "learning_rate":[0.01,0.1,1],
                    "max_depth":[10,20,30,50],
                    "num_leaves":[31,50,100,200]
                 },
                 "CatBoostClassifier":{
                    "iterations":[100,200,300,500],
                    "learning_rate":[0.01,0.1,1],
                    "depth":[4,6,8,10]
                 }
            }
            model_report:dict=evaluate_model(
                models=models,
                params=params,
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test
            )
            best_model_name=max(model_report,key=model_report.get)
            best_model_score=model_report[best_model_name]

            logging.info(f"Best model name: {best_model_name}")
            logging.info(f"Best model score: {best_model_score}")

            best_model=models[best_model_name]

            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)

            classification_train_metric=get_classification_score(y_train,y_train_pred)
            ## Track train metrics in MLflow
            self.track_mlflow(best_model, classification_train_metric, best_model_name, x_train, "Train")

            classification_test_metric=get_classification_score(y_test,y_test_pred)
            ## Track test metrics in MLflow
            self.track_mlflow(best_model, classification_test_metric, best_model_name, x_train, "Test")
            
            logging.info(f"Train score: {classification_train_metric}")
            logging.info(f"Test score: {classification_test_metric}")

            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model=NetworkModel(model=best_model,preprocessor=preprocessor)
           
            save_object(self.model_trainer_config.trained_model_file_path,network_model)

            save_object("final_model/model.pkl",best_model)
            

            ## model trainer artifact
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info("Model trained successfully")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info(f"{'='*30}Model Trainer Initiation{'='*30}")

            ## Initialize DagsHub MLflow tracking (token from .env)
            
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
            load_dotenv(dotenv_path=env_path)
            dagshub_token = os.getenv("DAGSHUB_USER_TOKEN")
            if dagshub_token:
                os.environ["DAGSHUB_USER_TOKEN"] = dagshub_token
            dagshub.init(repo_owner='niharkedia', repo_name='network-security-system', mlflow=True)

            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            

            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            logging.info("Splitting data into training and testing sets")
            logging.info(f"Training data shape: {x_train.shape}")
            logging.info(f"Testing data shape: {x_test.shape}")

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)

            logging.info(f"{'='*30}Model Trainer Initiation Completed{'='*30}")
            
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)