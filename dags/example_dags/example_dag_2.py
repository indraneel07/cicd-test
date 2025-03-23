# Import all packages needed at the top level of the DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime


def my_task_1_func():
    import time  # import packages only needed in the task function

    time.sleep(5)
    print(1)


# Instantiate the DAG
with DAG(
    dag_id="example_dag_2",
    start_date=datetime(2025, 2, 1),
    schedule="@daily",
    catchup=True,
):
    # Instantiate tasks within the DAG context
    my_task_1 = PythonOperator(
        task_id="my_task_1",
        python_callable=my_task_1_func,
        queue="high-mem"
    )

    my_task_2 = PythonOperator(
        task_id="my_task_2",
        python_callable=lambda: print(2),
    )

    # Define dependencies
    my_task_1 >> my_task_2
