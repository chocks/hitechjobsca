"""apps/sync entrypoint.

Fetches Canadian tech job listings from configured sources and upserts them
into ``jobs.all_jobs`` (Postgres). Runs once by default; set
``SYNC_INTERVAL_SECONDS`` to run on a loop (sidecar). ``SYNC_DRY_RUN=1`` fetches
and parses but skips the DB write.

    uv run python -m sync            # via uv project
    python main.py                   # plain interpreter / Docker
"""

from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime

import httpx

from config import Config
from db import upsert_listings
from sources import GitHubIssuesSource, StackOverflowRssSource, Source

log = logging.getLogger("sync")

DEFAULT_SOURCES: list[Source] = [
    StackOverflowRssSource(),
    GitHubIssuesSource(),
]


async def run_once(config: Config, sources: list[Source] | None = None) -> dict:
    """One ingest cycle. Returns a per-source result summary."""
    sources = sources if sources is not None else DEFAULT_SOURCES
    started = datetime.now()
    summary: dict[str, dict] = {}

    async with httpx.AsyncClient(
        timeout=config.request_timeout,
        headers={"User-Agent": "hitechjobsca-sync/2.0"},
        follow_redirects=True,
    ) as client:
        all_listings = []
        for source in sources:
            s_name = getattr(source, "name", source.__class__.__name__)
            try:
                listings = await source.fetch(client, config)
                summary[s_name] = {"count": len(listings), "error": None}
                log.info("%s: %d listings", s_name, len(listings))
                all_listings.extend(listings)
            except Exception as exc:
                summary[s_name] = {"count": 0, "error": str(exc)}
                log.exception("%s failed", s_name)

    if config.dry_run:
        log.info("dry-run: skipping DB write for %d listings", len(all_listings))
    else:
        try:
            upsert_listings(config, all_listings)
        except Exception:
            log.exception("DB upsert failed")
            summary["_db"] = {"error": "upsert failed"}
        else:
            summary["_db"] = {"upserted": len(all_listings)}

    summary["_meta"] = {
        "started_at": started.isoformat(),
        "duration_seconds": (datetime.now() - started).total_seconds(),
        "total_listings": len(all_listings),
    }
    return summary


async def run_loop(config: Config, sources: list[Source] | None = None) -> None:
    interval = config.interval_seconds or 0
    if interval <= 0:
        await run_once(config, sources)
        return
    log.info("running on loop every %d seconds", interval)
    while True:
        await run_once(config, sources)
        log.info("sleeping %d seconds until next cycle", interval)
        await asyncio.sleep(interval)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config = Config.from_env()
    try:
        asyncio.run(run_loop(config))
    except KeyboardInterrupt:
        log.info("interrupted; exiting")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
