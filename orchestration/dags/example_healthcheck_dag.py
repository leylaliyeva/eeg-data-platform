"""Placeholder DAG proving the orchestration/dags folder is correctly
bind-mounted into Airflow and picked up by the scheduler.

No pipeline logic lives here yet -- ingestion and transformation DAGs
are built in later phases (see docs/PROJECT_PLAN.md).
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="phase0_infra_healthcheck",
    description="Confirms Airflow, its DAG folder mount, and the scheduler are wired correctly.",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["phase0", "infra"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end
