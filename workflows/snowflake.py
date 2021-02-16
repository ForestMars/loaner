

import os
import logging

from airflow import settings
from airflow.models import Connection
from airflow.secrets import BaseSecretsBackend


CONNECT_ID=os.environ[’SNOWFLAKE_ID']
CONNECT_TYPE=os.environ[’SNOWFLAKE_TYPE']
HOST=os.environ[’SNOWFLAKE_HOST']
USER=os.environ[’SNOWFLAKE_USER']
SECRET=os.environ[’SNOWFLAKE_PW']


snowflake_connect = Connection(
    host=HOST,
    conn_id=CONNECT_ID, # NB. conn_id does not have unique constraint, make sure no namespace collisions.
    conn_type=CONNECT_TYPE,
    login=USER,
    password=password,
    port=port
)
session = settings.Session()
sessionsession.add(snowflake_connect)
session.commit()

postgres_query = PostgresOperator(
            task_id="sync_query",
            postgres_conn_id=POSTGRES_CONNECT
            sql=sql_query_str,
            autocommit=True,
        )
