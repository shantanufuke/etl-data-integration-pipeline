import psycopg2
import pandas as pd
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# AWS & Redshift Configuration
S3_BUCKET = "your-s3-bucket"
REDSHIFT_HOST = "your-redshift-cluster-endpoint"
REDSHIFT_DB = "analytics"
REDSHIFT_USER = "admin"
REDSHIFT_PASSWORD = "password"
REDSHIFT_IAM_ROLE = "arn:aws:iam::123456789012:role/RedshiftS3Access"

# Function to extract data from S3
def extract_data():
    s3 = boto3.client('s3')
    s3.download_file(S3_BUCKET, 'raw_data.csv', 'raw_data.csv')
    print("Data extracted from S3")

# Function to transform data using Pandas
def transform_data():
    df = pd.read_csv("raw_data.csv")
    df['amount'] = df['amount'] * 1.1  # Sample transformation
    df.to_csv("transformed_data.csv", index=False)
    print("Data transformation complete")

# Function to load data into AWS Redshift
def load_data():
    conn = psycopg2.connect(
        dbname=REDSHIFT_DB, user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD, host=REDSHIFT_HOST, port="5439"
    )
    cur = conn.cursor()

    query = f"""
    COPY sales_data FROM 's3://{S3_BUCKET}/transformed_data.csv'
    IAM_ROLE '{REDSHIFT_IAM_ROLE}'
    FORMAT AS CSV;
    """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded into Redshift")

# Airflow DAG definition
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

dag = DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
)

extract_task = PythonOperator(task_id="extract", python_callable=extract_data, dag=dag)
transform_task = PythonOperator(task_id="transform", python_callable=transform_data, dag=dag)
load_task = PythonOperator(task_id="load", python_callable=load_data, dag=dag)

extract_task >> transform_task >> load_task
