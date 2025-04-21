from datetime import datetime, timedelta
from pendulum import parse as parse_datetime
from tabulate import tabulate

from airflow.decorators import dag, task
from airflow.utils.session import provide_session
from airflow.models import TaskInstance
from airflow.utils.state import State

from sqlalchemy import func

@task
@provide_session
def get_avg_durations_from_tasks(start_date: str, end_date: str, session=None) -> list:
    """
    Calculate average running and queued durations per DAG from TaskInstance-level data.
    """
    start = parse_datetime(start_date).in_timezone("UTC")
    end = parse_datetime(end_date).in_timezone("UTC")

    results = session.query(
        TaskInstance.dag_id,
        func.avg(func.extract('epoch', TaskInstance.end_date - TaskInstance.start_date)).label("avg_running_duration"),
        func.avg(func.extract('epoch', TaskInstance.start_date - TaskInstance.queued_dttm)).label("avg_queued_duration"),
        func.count(TaskInstance.task_id).label("task_count")
    ).filter(
        TaskInstance.execution_date >= start,
        TaskInstance.execution_date <= end,
        TaskInstance.state.in_(State.finished),
        TaskInstance.start_date.isnot(None),
        TaskInstance.end_date.isnot(None),
        TaskInstance.queued_dttm.isnot(None),
        TaskInstance.start_date >= TaskInstance.queued_dttm
    ).group_by(TaskInstance.dag_id).all()

    return [
        {
            "dag_id": row.dag_id,
            "avg_running_duration": row.avg_running_duration,
            "avg_queued_duration": row.avg_queued_duration,
            "task_count": row.task_count
        }
        for row in results
    ]

@task
def display_table(dag_durations: list, start_date: str, end_date: str):
    """
    Display a table of average durations per DAG.
    """
    print(f"\n Average DAG durations from {start_date} to {end_date}:\n")
    table_data = [["DAG ID", "Avg Running Duration (s)", "Avg Queued Duration (s)"]]
    for entry in dag_durations:
        table_data.append([
            entry["dag_id"],
            f"{entry['avg_running_duration']:.2f}" if entry["avg_running_duration"] is not None else "N/A",
            f"{entry['avg_queued_duration']:.2f}" if entry["avg_queued_duration"] is not None else "N/A",
        ])
    table = tabulate(table_data, headers="firstrow", tablefmt="grid")
    print("\n" + table + "\n")

@dag(
    dag_id="example_dag_average_durations_per_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "airflow", "retries": 1},
    params={
        "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    },
    tags=["Example DAG"]
)
def average_durations_per_dags():
    """
    DAG to find average queued and run duration of a DAG based on task details 
    """
    start = "{{ params.start_date }}"
    end = "{{ params.end_date }}"
    durations = get_avg_durations_from_tasks(start, end)
    display_table(durations, start, end)

average_durations_per_dags()
