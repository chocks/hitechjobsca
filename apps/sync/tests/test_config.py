import os
from datetime import date

from config import Config


def test_from_env_reads_all_db_vars(monkeypatch):
    env = {
        "DB_HOST": "db", "DB_PORT": "6543", "DB_NAME": "jodb",
        "DB_USER": "developer", "DB_PASSWORD": "s3cret",
        "DATA_FOLDER": "/data/", "SYNC_DRY_RUN": "1",
        "SYNC_INTERVAL_SECONDS": "3600", "SYNC_REQUEST_TIMEOUT": "10",
        "SYNC_GITHUB_TOKEN": "ghp_token",
    }
    cfg = Config.from_env(env)
    assert cfg.db_host == "db"
    assert cfg.db_port == 6543
    assert cfg.db_name == "jodb"
    assert cfg.db_user == "developer"
    assert cfg.db_password == "s3cret"
    assert cfg.data_folder == "/data/"
    assert cfg.dry_run is True
    assert cfg.interval_seconds == 3600
    assert cfg.request_timeout == 10.0
    assert cfg.github_token == "ghp_token"
    assert cfg.dsn() == "postgresql://developer:s3cret@db:6543/jodb"


def test_from_env_defaults(monkeypatch):
    for k in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD",
              "DATA_FOLDER", "SYNC_DRY_RUN", "SYNC_INTERVAL_SECONDS",
              "SYNC_REQUEST_TIMEOUT", "SYNC_GITHUB_TOKEN"):
        monkeypatch.delenv(k, raising=False)
    cfg = Config.from_env()
    assert cfg.db_host == "localhost"
    assert cfg.db_port == 5432
    assert cfg.dry_run is False
    assert cfg.interval_seconds is None
    assert cfg.github_token is None


def test_bool_and_int_coercion(monkeypatch):
    cfg = Config.from_env({"SYNC_DRY_RUN": "yes", "SYNC_INTERVAL_SECONDS": "0",
                           "DB_PORT": "not-an-int", "SYNC_REQUEST_TIMEOUT": "bad"})
    assert cfg.dry_run is True
    assert cfg.interval_seconds == 0
    assert cfg.db_port == 5432
    assert cfg.request_timeout == 30.0
