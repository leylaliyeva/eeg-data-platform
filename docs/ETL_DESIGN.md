# ETL Design: Airflow as Pure Orchestration

Status: design convention for Phase 1+ pipeline code. No pipeline logic exists yet (Phase 0 is infrastructure only) — this document fixes the pattern before that code is written, so ingestion, transformation, and orchestration stay decoupled from the start rather than needing a later refactor.

## Principle

A DAG file's only job is scheduling, retries, and dependency ordering. It never contains extract/transform/load logic itself. If a piece of logic can't be unit-tested without spinning up Airflow, it's in the wrong place.

This is why the repository already separates `ingestion/`, `transformation/`, and `orchestration/dags/` into distinct top-level directories (see [README.md](../README.md#project-structure)) rather than putting everything inside DAG files.

## Where each piece lives

| Layer | Directory | Contains | Imports Airflow? |
|---|---|---|---|
| Extract | `ingestion/` | Functions that pull data from OpenNeuro/PhysioNet and write raw files to MinIO | No |
| Transform | `transformation/` | Functions that parse EEG files, standardize metadata, compute derived stats, write to Postgres staging | No |
| Load / model | `dbt/` | SQL models, staging → curated. Invoked as a subprocess from Airflow, never reimplemented in Python | No |
| Orchestrate | `orchestration/dags/` | Wires the above into tasks; declares schedule, retries, and dependencies | Yes — the only place it should appear |
| Shared | `config/` | `Settings`, imported identically by DAG tasks and the plain functions they call, so there is one source of truth either way | No |

## Shape of a thin DAG

Using Airflow's TaskFlow API, an ingestion DAG contains no HTTP calls, no parsing, and no SQL — only wiring:

```python
from airflow.decorators import dag, task
from datetime import datetime

from config.settings import load_settings
from ingestion.openneuro_client import fetch_and_store  # the real logic

STUDY_IDS = ["ds002778"]

@dag(schedule=None, start_date=datetime(2026, 1, 1), catchup=False, tags=["ingestion"])
def openneuro_ingest_dag():
    @task(retries=2)
    def ingest_study(study_id: str):
        settings = load_settings()
        return fetch_and_store(study_id, settings)  # e.g. {"keys_written": 264}

    ingest_study.expand(study_id=STUDY_IDS)

openneuro_ingest_dag()
```

`fetch_and_store` lives in `ingestion/openneuro_client.py` as plain Python, with no `from airflow import ...` anywhere in it. That function is what Phase 1's unit tests call directly, with `requests` mocked out — no DAG involved (see the Phase 1 Definition of Done in [PROJECT_PLAN.md §8](PROJECT_PLAN.md#8-phase-roadmap): "unit tests with mocked HTTP responses").

## Two Airflow-specific rules

1. **XComs carry references, not payloads.** Airflow persists XCom values in its own metadata database, so a task must never return raw EEG bytes. Tasks pass around small things — an S3 key, a row count, a status — while the actual data flows ingestion → MinIO → transformation directly.
2. **Idempotency is the function's job; retries are the DAG's job.** The deterministic-MinIO-key and upsert logic from [PROJECT_PLAN.md §6](PROJECT_PLAN.md#6-pipeline-design) belongs inside the `ingestion`/`transformation` functions. `retries=` and backoff belong on the `@task` decorator. Keeping that split clean is what makes "safe to retry" actually true rather than assumed.

## Shape of the full pipeline

`openneuro_ingest_dag` and `physionet_ingest_dag` each populate MinIO independently. A downstream `transform_dag` reads from MinIO, populates staging, then runs `dbt run` and `dbt test` (via a `BashOperator` or dbt's Airflow provider — still orchestration only; dbt owns the SQL). The ingest → transform handoff can be a manual `TriggerDagRunOperator` chain, or Airflow's Datasets feature (data-aware scheduling) can trigger `transform_dag` automatically once an ingestion task reports it wrote new data — a decision to make when Phase 1 DAGs are actually implemented, not before.
