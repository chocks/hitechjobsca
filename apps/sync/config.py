"""Configuration for the jobs ingest (apps/sync).

All settings come from environment variables (with sensible dev defaults) so
the same image runs in Docker, cron, or a sidecar. The DB credential env var
names (``DB_HOST``, ``DB_NAME``, ``DB_USER``, ``DB_PASSWORD``, ``DATA_FOLDER``)
are unchanged from the original 2020 script for docker-compose compatibility.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 5432
DEFAULT_DB_NAME = "jodb"
DEFAULT_DB_USER = "developer"
DEFAULT_DB_PASSWORD = "developer"
DEFAULT_DATA_FOLDER = "./data/"
DEFAULT_REQUEST_TIMEOUT = 30.0

_TRUE = {"1", "true", "yes", "y", "on"}


def _env_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in _TRUE


def _env_int(value: str | None, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _env_float(value: str | None, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@dataclass
class Config:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    data_folder: str
    github_token: str | None
    dry_run: bool
    interval_seconds: int | None
    request_timeout: float

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "Config":
        e = os.environ if env is None else env
        interval = (e.get("SYNC_INTERVAL_SECONDS") or "").strip()
        return cls(
            db_host=e.get("DB_HOST", DEFAULT_DB_HOST),
            db_port=_env_int(e.get("DB_PORT"), DEFAULT_DB_PORT),
            db_name=e.get("DB_NAME", DEFAULT_DB_NAME),
            db_user=e.get("DB_USER", DEFAULT_DB_USER),
            db_password=e.get("DB_PASSWORD", DEFAULT_DB_PASSWORD),
            data_folder=e.get("DATA_FOLDER", DEFAULT_DATA_FOLDER),
            github_token=e.get("SYNC_GITHUB_TOKEN") or None,
            dry_run=_env_bool(e.get("SYNC_DRY_RUN"), False),
            interval_seconds=int(interval) if interval else None,
            request_timeout=_env_float(e.get("SYNC_REQUEST_TIMEOUT"), DEFAULT_REQUEST_TIMEOUT),
        )

    def dsn(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
