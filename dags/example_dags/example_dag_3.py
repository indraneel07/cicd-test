import json
from pendulum import datetime
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


def get_a_cat_fact(ti):
    """
    Gets a cat fact from the CatFacts API
    """
    url = "http://catfact.ninja/fact"
    res = requests.get(url)
    print(res.text)
    ti.xcom_push(key="cat_fact", value=json.loads(res.text)["fact"])


def analyze_cat_facts(ti):
    """
    Prints the cat fact
    """
    cat_fact = ti.xcom_pull(key="cat_fact", task_ids="get_a_cat_fact")
    print("Cat fact for today:", cat_fact)
    # run some analysis here


with DAG(
    "example_dag_3",
    start_date=datetime(2025, 1, 1),
    max_active_runs=2,
    schedule="@daily",
    default_args={"retries": 5},
    catchup=False,
) as dag:
    get_cat_data = PythonOperator(
        task_id="get_a_cat_fact", python_callable=get_a_cat_fact
    )

    analyze_cat_data = PythonOperator(
        task_id="analyze_data", python_callable=analyze_cat_facts
    )

    get_cat_data >> analyze_cat_data
