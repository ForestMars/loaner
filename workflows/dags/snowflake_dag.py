import os
import sys
from datetime import datetime as dt
import logging

import airflow
from airflow import DAG
from airflow.contrip.hooks.snowflake_hook import SnowflakeHook
from airflow.contrip.operators.snowflake_operator import SnowflakeOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator


with add_path(os.environ['ETL_HOME']):
    etl = __import__('etl.etl') # NB. ETL transforms are not included in Bread Payments demo


SNOWFLAKE_CONNECT = os.environ['SNOWFLAKE_CONNECT']


args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt(2021, 2, 8),
    'email': ['forest@fractalgradient.com'],
    'email_on_failure': True,
    #'email_on_retry': True,
    'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    }

dag = DAG(
    dag_id='snowflake_dag',
    description='DAG to connect to Snowflake data warehouse',
    default_args=args,
    schedule_interval='0 0 3 * *',
    start_date=dt(2021, 2, 8),
    catchup=False
    )

snowflake_connect = SNOWFLAKE_CONNECT

# Using public schema for demo, but really should schematize this.
snowflake_query = [
    """ create table public.loans (loan_id number start_date date inital_amt decimal); """,
    """ create table public.loan_events (loan_id number event_type enum post_date date amt decimal); """,
    ]


def get_row_count(**context):
    hw_hook = SnowflakeHook(snowflake_connect_id=snowflake_connect)
    result = hw_hook_get_first("select count(*) from loans")

    return result


def create_snowflake_tables():
    with dag:
        create_insert = SnowflakeOperator(
            task_id="snowfalke_create",
            sql=snowflake_query ,
            snowflake_conn_id="snowflake_conn",
        )

        get_count = PythonOperator(task_id="get_row_count", python_callable=get_row_count)

    create_insert >> get_count


def sync_data():
    """ *Very* quick pseudo-code for synching small dataset from RDS for demo only.
    Does NOT include Postgres COPY to S3 or creating staging tables in Snowflake for large datasets. """
    _data = etl.etl.GetRDSData()
    process_rds_data = etl.etl.ProcessRDSData()

    home = os.environ['HOME']

    rds_data = process_rds_data.keep_cols(rds_data)
    process_rds_data.parse_rds_data(rds_data)  # (now called historic, not daily)
    os.system('echo ' + str(dt.now()) + ' >> ' + home + 'logs/rds_sync.log')

    fetch_data_operator = PythonOperator(task_id='sync_data_task', python_callable=sync_data, dag=dag)

    #return ctp_data
    return 'Snowflake synchronization successful.'


if __name__ == '__main__':
    create_snowflake_tables()
    sync_data()
