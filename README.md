# ETL Pipeline for Data Integration

## Overview
This project implements an ETL pipeline using Apache Airflow, AWS Redshift, and Python to automate data extraction, transformation, and loading (ETL) for large-scale analytics.

## Features
- **Automated Data Extraction** → Pulls raw data from AWS S3.
- **Data Transformation with Pandas** → Cleans and preprocesses data.
- **Data Loading into AWS Redshift** → Uses the Redshift COPY command for efficient ingestion.
- **Airflow Workflow Automation** → Manages ETL execution with task dependencies.

## Installation
### 1️⃣ Install Dependencies
```sh
pip install apache-airflow pandas psycopg2-binary boto3
```

### 2️⃣ Start Airflow Scheduler & Webserver
```sh
airflow scheduler & airflow webserver
```

### 3️⃣ Run ETL Pipeline
```sh
airflow dags trigger etl_pipeline
```

## Technologies Used
- **Apache Airflow** → Workflow orchestration.
- **AWS S3 & Redshift** → Cloud storage & data warehousing.
- **Python & Pandas** → Data transformation.

## Author
Shantanu Fuke
