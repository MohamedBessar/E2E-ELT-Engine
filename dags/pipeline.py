from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator
from scripts.Processing import *
from scripts.utils.snowflake_utilz import *
from dotenv import load_dotenv
import os
import boto3
import logging


load_dotenv("secrets.env")
profiles_path = '/opt/airflow/datalake/dbt'
project_path = '/opt/airflow/datalake/dbt/ecommerce'

default_args = {
    'owner': 'Mahmoud',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

dag = DAG(
    'ecommerce_pipeline',
    default_args=default_args,
    description='E2E ELT engine',
    schedule_interval='*/15 * * * *',
    start_date=days_ago(1),
    catchup=False
)

def snowflake_credentials():
    return {
        'user': os.getenv("SNOWFLAKE_USER"),
        'password': os.getenv("SNOWFLAKE_PASSWORD"),
        'account': os.getenv("SNOWFLAKE_ACCOUNT"),
        'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
        'database': os.getenv("SNOWFLAKE_DATABASE"),
        'schema': os.getenv("SNOWFLAKE_SCHEMA"),
    }

def Folder_credentials():
    return {
        'raw_folder': os.getenv("raw_path"),
        'archive_folder': os.getenv("archive_folder")
    }

def test_snowflake_connection():
    snowflake_cred = snowflake_credentials()
    create_connection(**snowflake_cred)

def process_raw_data_task():
    snowflake_cred = snowflake_credentials()
    connection, engine = create_connection(**snowflake_cred)
    folder_cred = Folder_credentials()


    list_file = process_raw_data(
        conn=connection,
        engine=engine,
        row_folder=folder_cred['raw_folder']
    )
    close_connection(connection=connection,engine=engine)
    return list_file
    

def move_files():
    folder_cred = Folder_credentials()
    move_files_to_archive(**folder_cred)


with dag:
    test_connection_task = PythonOperator(
        task_id='test_snowflake_connection',
        python_callable=test_snowflake_connection
    )

    process_data_task = PythonOperator(
        task_id='process_raw_data',
        python_callable=process_raw_data_task
    )

    move_files_task = PythonOperator(
        task_id='move_files',
        python_callable=move_files
    )

    dbt_test_connection = BashOperator(
        task_id='dbt_test_connection',
        bash_command=f"dbt debug --profiles-dir {profiles_path} --project-dir {project_path}"
    )

    test_connection_task >> process_data_task >> move_files_task >> dbt_test_connection
