# from airflow.decorators import dag, task
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig, LoadMode
# from cosmos.profiles import PostgresUserPasswordProfileMapping
# from pendulum import datetime
# import os

# YOUR_NAME = "<your_name>"
# CONNECTION_ID = "db_conn"
# DB_NAME = "<your_db_name>"
# SCHEMA_NAME = "<your_schema_name>"
# MODEL_TO_QUERY = "model2"
# DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/my_simple_dbt_project"
# DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

# profile_config = ProfileConfig(
#     profile_name="default",
#     target_name="dev",
#     profile_mapping=PostgresUserPasswordProfileMapping(
#         conn_id=CONNECTION_ID,
#         profile_args={"schema": SCHEMA_NAME},
#     ),
# )

# execution_config = ExecutionConfig(
#     dbt_executable_path=DBT_EXECUTABLE_PATH,
# )


# @dag(
#     start_date=datetime(2023, 8, 1),
#     schedule=None,
#     catchup=False,
#     params={"my_name": YOUR_NAME},
# )
# def my_simple_dbt_dag():
#     @task
#     def fetch_tag_list():
#         # Maybe you read this from a config file or external system
#         return ["number1", "number2", "number3"]

#     @dag
#     def dynamic_dbt_dag(tag_list):
#         def make_dbt_task_group(selected_tag):
#             return DbtTaskGroup(
#                 group_id=f"transform_data_{selected_tag}",
#                 project_config=ProjectConfig(DBT_PROJECT_PATH),
#                 profile_config=profile_config,
#                 execution_config=execution_config,
#                 render_config=RenderConfig(
#                     select=[f"tag:{selected_tag}"],
#                     load_method=LoadMode.DBT_LS
#                 )
#             )
        
#         transform_data_groups = make_dbt_task_group.expand(selected_tag=tag_list)

#     dynamic_dbt_dag()

# my_simple_dbt_dag()
