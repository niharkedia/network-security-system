from networksecurity.Pipeline.training_pipeline import TrainingPipeline
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object,save_object
import sys,os,certifi
from dotenv import load_dotenv
import pymongo
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse
import io
import pandas as pd

ca = certifi.where()

load_dotenv()

mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)

client =pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app =FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training pipeline completed and sucessfully ")
    except Exception as e:
        logging.error(f"Error in training pipeline: {e}")
        raise NetworkSecurityException(e, sys)



@app.post("/predict")
async def predict(request:Request,file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV file
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Perform prediction using the trained model
        # Replace this with your actual prediction logic
        preprocessor=load_object(file_path="final_model/preprocessor.pkl")
        model=load_object(file_path="final_model/model.pkl")

        network_model = NetworkModel(model=model,preprocessor=preprocessor)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        df['prediction']=y_pred
        print(df['prediction'])

        os.makedirs("prediction_o",exist_ok=True)
        df.to_csv("prediction_o/output.csv",index=False)
        table_html=df.to_html(classes="table table-striped")

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        raise NetworkSecurityException(e, sys)

def perform_prediction(df):
    # Replace this with your actual prediction logic
    # For now, return a dummy prediction
    return {"status": "success", "prediction": "normal"}

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)