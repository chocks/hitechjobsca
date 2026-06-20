"""Core types shared by all ingest sources."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from typing import Protocol, List

import httpx

DEFAULT_SALARY = "N/A"
DEFAULT_LOCATION = "Canada"
INGEST_DEFAULT_RANK = 10


@dataclass(frozen=True)
class JobListing:
    """A normalized job listing ready to upsert into ``jobs.all_jobs``."""

    title: str
    company_name: str
    apply_url: str
    salary_range: str
    location: str
    from_date: date
    ext_id: str
    source: str
    rank: int = INGEST_DEFAULT_RANK


class Source(Protocol):
    """A fetcher that produces normalized listings from a single feed."""

    name: str

    async def fetch(self, client: httpx.AsyncClient, config) -> List[JobListing]:
        ...


def ext_id_for(source: str, key: str) -> str:
    """Build a stable, source-namespaced external id (fits ``varchar(255)``)."""
    digest = hashlib.sha256(f"{source}:{key}".encode("utf-8")).hexdigest()
    return f"{source}:{digest[:24]}"
