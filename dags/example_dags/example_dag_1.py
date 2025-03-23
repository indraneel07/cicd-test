# Import all packages needed at the top level of the DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime
import os
from airflow.utils.email import send_email


def my_task_1_func(**context):
    dag_run = context.get("dag_run")
    from airflow.models import Variable
    variable = Variable.get("secret_key")
    print(variable)
    msg = f"DAG ran successfully {variable}"
    subject = f"DAG {dag_run} has completed"
    send_email(to=["test@gmail.com"], subject=subject, html_content=msg)



# Instantiate the DAG
with DAG(
    dag_id="example_dag_1",
    start_date=datetime(2025, 2, 1),
    schedule="@daily",
    catchup=False,
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
