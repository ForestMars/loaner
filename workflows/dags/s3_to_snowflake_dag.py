import os
import sys

from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.providers.snowflake.transfers.snowflake_to_slack import SnowflakeToSlackOperator
from airflow.utils.dates import days_ago


SNOWFLAKE_CONN_ID = os.environ['my_snowflake_conn']
SLACK_CONN_ID = os.environ['slack_conn']
SNOWFLAKE_SCHEMA = os.environ['snowflake_schema']
SNOWFLAKE_STAGE = os.environ['snowflake_stage']
SNOWFLAKE_WAREHOUSE = os.environ['snowflake_warehouse']
SNOWFLAKE_DATABASE = os.environ['snowflake_database']
SNOWFLAKE_ROLE = os.environ['snowflake_iam_role']
SNOWFLAKE_TABLE = os.environ['snowflake_table']
S3_FILE_PATH = os.environ['/path/to/file.csv']


CREATE_TABLE_SQL_STRING = (
    f"CREATE OR REPLACE TRANSIENT TABLE {SNOWFLAKE_TABLE} (name VARCHAR(250), id INT);"
)
SQL_INSERT_STATEMENT = f"INSERT INTO {SNOWFLAKE_TABLE} VALUES ('name', %(id)s)"
SQL_LIST = [SQL_INSERT_STATEMENT % {"id": n} for n in range(0, 10)]
SNOWFLAKE_SLACK_SQL = f"SELECT name, id FROM {SNOWFLAKE_TABLE} LIMIT 10;"
SNOWFLAKE_SLACK_MESSAGE = (
    "Results in an ASCII table:\n```{{ results_df | tabulate(tablefmt='pretty', headers='keys') }}```"
)

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'example_snowflake',
    default_args=default_args,
    start_date=days_ago(2),
    tags=['example'],
)


snowflake_op_sql_str = SnowflakeOperator(
    task_id='snowflake_op_sql_str',
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=CREATE_TABLE_SQL_STRING,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

snowflake_op_with_params = SnowflakeOperator(
    task_id='snowflake_op_with_params',
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=SQL_INSERT_STATEMENT,
    parameters={"id": 56},
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

snowflake_op_sql_list = SnowflakeOperator(
    task_id='snowflake_op_sql_list', dag=dag, snowflake_conn_id=SNOWFLAKE_CONN_ID, sql=SQL_LIST
)

snowflake_op_template_file = SnowflakeOperator(
    task_id='snowflake_op_template_file',
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql='/path/to/sql/<filename>.sql',
)


copy_into_table = S3ToSnowflakeOperator(
    task_id='copy_into_table',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    s3_keys=[S3_FILE_PATH],
    table=SNOWFLAKE_TABLE,
    schema=SNOWFLAKE_SCHEMA,
    stage=SNOWFLAKE_STAGE,
    file_format="(type = 'CSV',field_delimiter = ';')",
    dag=dag,
)

slack_report = SnowflakeToSlackOperator(
    task_id="slack_report",
    sql=SNOWFLAKE_SLACK_SQL,
    slack_message=SNOWFLAKE_SLACK_MESSAGE,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    slack_conn_id=SLACK_CONN_ID,
    dag=dag,
)


snowflake_op_sql_str >> [
    snowflake_op_with_params,
    snowflake_op_sql_list,
    snowflake_op_template_file,
    copy_into_table,
] >> slack_report
