"""Central configuration loader.

Reads required settings from environment variables (populated from a
`.env` file in local development, or from real environment variables in
CI/containers). Fails loudly and early if something required is missing,
rather than letting later code hit a confusing runtime error.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE)

_REQUIRED_VARS = (
    "POSTGRES_WAREHOUSE_HOST",
    "POSTGRES_WAREHOUSE_PORT",
    "POSTGRES_WAREHOUSE_DB",
    "POSTGRES_WAREHOUSE_USER",
    "POSTGRES_WAREHOUSE_PASSWORD",
    "MINIO_ENDPOINT",
    "MINIO_ROOT_USER",
    "MINIO_ROOT_PASSWORD",
    "MINIO_RAW_BUCKET",
)


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable '{name}'. "
            "Copy .env.example to .env and fill in real values."
        )
    return value


@dataclass(frozen=True)
class Settings:
    postgres_warehouse_host: str
    postgres_warehouse_port: str
    postgres_warehouse_db: str
    postgres_warehouse_user: str
    postgres_warehouse_password: str
    minio_endpoint: str
    minio_root_user: str
    minio_root_password: str
    minio_raw_bucket: str

    @property
    def warehouse_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_warehouse_user}:{self.postgres_warehouse_password}"
            f"@{self.postgres_warehouse_host}:{self.postgres_warehouse_port}"
            f"/{self.postgres_warehouse_db}"
        )


def load_settings() -> Settings:
    """Load and validate settings from the environment.

    Raises RuntimeError if any required variable is missing.
    """
    for var in _REQUIRED_VARS:
        _require(var)

    return Settings(
        postgres_warehouse_host=os.environ["POSTGRES_WAREHOUSE_HOST"],
        postgres_warehouse_port=os.environ["POSTGRES_WAREHOUSE_PORT"],
        postgres_warehouse_db=os.environ["POSTGRES_WAREHOUSE_DB"],
        postgres_warehouse_user=os.environ["POSTGRES_WAREHOUSE_USER"],
        postgres_warehouse_password=os.environ["POSTGRES_WAREHOUSE_PASSWORD"],
        minio_endpoint=os.environ["MINIO_ENDPOINT"],
        minio_root_user=os.environ["MINIO_ROOT_USER"],
        minio_root_password=os.environ["MINIO_ROOT_PASSWORD"],
        minio_raw_bucket=os.environ["MINIO_RAW_BUCKET"],
    )
