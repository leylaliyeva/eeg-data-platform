import pytest

from config.settings import load_settings

REQUIRED_ENV = {
    "POSTGRES_WAREHOUSE_HOST": "localhost",
    "POSTGRES_WAREHOUSE_PORT": "5432",
    "POSTGRES_WAREHOUSE_DB": "eeg_warehouse",
    "POSTGRES_WAREHOUSE_USER": "test_user",
    "POSTGRES_WAREHOUSE_PASSWORD": "test_pass",
    "MINIO_ENDPOINT": "http://localhost:9000",
    "MINIO_ROOT_USER": "test_minio",
    "MINIO_ROOT_PASSWORD": "test_minio_pass",
    "MINIO_RAW_BUCKET": "eeg-raw-test",
}


def _set_required_env(monkeypatch):
    for key, value in REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)


def test_load_settings_reads_required_vars(monkeypatch):
    _set_required_env(monkeypatch)

    settings = load_settings()

    assert settings.postgres_warehouse_db == "eeg_warehouse"
    assert settings.minio_raw_bucket == "eeg-raw-test"
    assert settings.warehouse_dsn == (
        "postgresql://test_user:test_pass@localhost:5432/eeg_warehouse"
    )


def test_load_settings_raises_when_var_missing(monkeypatch):
    _set_required_env(monkeypatch)
    monkeypatch.delenv("MINIO_RAW_BUCKET", raising=False)

    with pytest.raises(RuntimeError):
        load_settings()
