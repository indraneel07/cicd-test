from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum


def get_task_id():
    return "print_array_task"  # <- is that code going to be executed?


def get_array():
    return [1, 2, 3]  # <- is that code going to be executed?


with DAG(
    dag_id="top_level_code4",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    operator = PythonOperator(
        task_id=get_task_id(),
        python_callable=get_array,
        dag=dag,
    )
