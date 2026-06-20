"""Database access for the ingest — parameterized batch upsert into jobs.all_jobs.

Targets the schema in ``db/init/01_schema.sql``:
    title, company_name, apply_url, salary_range, from_date, end_date,
    location, search_vectors (trigger-maintained), pinned, status, rank, ext_id.

``ext_id`` has a unique index, so upserts are keyed on it — re-running ingest
is idempotent and refreshes title/company/url/salary/location/rank/status.
"""

from __future__ import annotations

import logging
from typing import Iterable

import psycopg2
import psycopg2.extras

from config import Config
from sources.base import JobListing

log = logging.getLogger(__name__)

UPSERT_SQL = """
INSERT INTO jobs.all_jobs
    (title, company_name, apply_url, salary_range, from_date, location,
     status, rank, ext_id)
VALUES %s
ON CONFLICT (ext_id) DO UPDATE SET
    title         = EXCLUDED.title,
    company_name  = EXCLUDED.company_name,
    apply_url     = EXCLUDED.apply_url,
    salary_range  = EXCLUDED.salary_range,
    location      = EXCLUDED.location,
    rank          = EXCLUDED.rank,
    status        = EXCLUDED.status
RETURNING (xmax = 0) AS inserted
"""


def connect(config: Config):
    log.info("connecting to Postgres at %s:%s/%s", config.db_host, config.db_port, config.db_name)
    conn = psycopg2.connect(config.dsn())
    conn.autocommit = False
    return conn


def upsert_listings(config: Config, listings: Iterable[JobListing]) -> tuple[int, int]:
    """Upsert all listings in a single transaction.

    Returns ``(inserted, updated)`` where ``inserted`` counts rows that did not
    already exist (approximated by evaluating the xmax sentinel Postgres sets
    on UPDATE).
    """
    rows = [listing_to_row(j) for j in listings]
    if not rows:
        log.info("no listings to upsert")
        return (0, 0)

    conn = connect(config)
    inserted = 0
    updated = 0
    try:
        with conn:
            with conn.cursor() as cur:
                psycopg2.extras.execute_values(
                    cur, UPSERT_SQL, rows, page_size=500,
                )
                for (was_inserted,) in cur.fetchall():
                    if was_inserted:
                        inserted += 1
                    else:
                        updated += 1
        log.info("upsert complete: %d inserted, %d updated", inserted, updated)
        return (inserted, updated)
    finally:
        conn.close()


# Column order must match UPSERT_SQL's column list.
def listing_to_row(j: JobListing) -> tuple:
    return (
        j.title,
        j.company_name,
        j.apply_url,
        j.salary_range,
        j.from_date,
        j.location,
        True,        # status
        j.rank,
        j.ext_id,
    )
