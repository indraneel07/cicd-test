# It's ok to import modules that are not expensive to load at top-level of a DAG file
import random
import pendulum
from airflow import DAG
from airflow.decorators import task

# Expensive imports should be avoided as top level imports, because DAG files are parsed frequently, resulting in top-level code being executed.
#
# import pandas
# import torch
# import tensorflow
#

with DAG(
    dag_id="top_level_code3",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    @task()
    def do_stuff_with_pandas_and_torch():
        import pandas
        import torch

        # do some operations using pandas and torch
        pass

    @task()
    def do_stuff_with_tensorflow():
        import tensorflow

        # do some operations using tensorflow
        pass

    do_stuff_with_pandas_and_torch() >> do_stuff_with_tensorflow()
