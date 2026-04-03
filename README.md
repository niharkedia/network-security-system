# 🛡️ Network Security: Phishing Data Detection

This project is a production-grade end-to-end Machine Learning pipeline designed to classify network traffic as legitimate or malicious (phishing). It implements a full MLOps lifecycle, including automated data ingestion from MongoDB, schema-based validation, and experiment tracking with MLflow.

## 🚀 Key Features
* **ETL Pipeline:** Automated data migration from **MongoDB Atlas** to local environments.
* **Data Validation:** Ensures data integrity using schema-based checks before training.
* **Experiment Tracking:** Logs metrics, parameters, and models using **MLflow**.
* **Cloud Integration:** Ready for **AWS S3** artifact storage and deployment.
* **Containerization:** Fully Dockerized for consistent deployment across environments.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Database:** MongoDB (Data Lake)
* **ML Frameworks:** Scikit-learn, CatBoost, XGBoost
* **DevOps/MLOps:** Docker, MLflow, AWS S3, GitHub Actions

## 📂 Project Structure
```text
├── networksecurity          # Core logic (Ingestion, Validation, Transformation, Model)
├── data_schema              # JSON definitions for data validation
├── templates & static       # Flask Web UI for real-time predictions
├── app.py                   # Flask Application Entry
├── main.py                  # Training pipeline execution script
├── push_data.py             # Script to migrate local data to MongoDB
└── Dockerfile               # Containerization configuration
