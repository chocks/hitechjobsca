"""Stack Overflow jobs RSS source.

Stack Overflow Jobs (and its RSS feed at ``stackoverflow.com/jobs/feed``) was
**discontinued in 2023** and now returns 404. This source is preserved so the
ingest path remains source-pluggable: it treats the dead feed as "no data"
rather than a fatal error, and logs a clear notice. If an RSS feed reappears
(e.g. a mirror), parsing still works against the original Atom/RSS shape.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List
from xml.etree import ElementTree

import httpx

from config import Config
from .base import (
    DEFAULT_LOCATION,
    DEFAULT_SALARY,
    JobListing,
    ext_id_for,
)
from .util import clean_text, is_canadian_city, parse_iso_datetime

log = logging.getLogger(__name__)

TOTAL_RESULTS_TAG = "{http://a9.com/-/spec/opensearch/1.1/}totalResults"
AUTHOR_NAME_TAG = "{http://www.w3.org/2005/Atom}author"
COMPANY_NAME_TAG = "{http://www.w3.org/2005/Atom}name"
UPDATED_DATE_TAG = "{http://www.w3.org/2005/Atom}updated"
LOCATION_TAG = "{http://stackoverflow.com/jobs/}location"

SO_JOBS_URL = "https://stackoverflow.com/jobs/feed?l=Canada"
SOURCE_NAME = "so-rss"


class StackOverflowRssSource:
    name = SOURCE_NAME

    def __init__(self, url: str = SO_JOBS_URL):
        self.url = url

    async def fetch(self, client: httpx.AsyncClient, config: Config) -> List[JobListing]:
        log.info("fetching Stack Overflow jobs RSS from %s", self.url)
        resp = await client.get(self.url)
        # Stack Overflow Jobs was discontinued in 2023. The feed is gone for
        # good: it returns 404 (not found) or 403 (Cloudflare blocks non-browser
        # clients). Either way the feed is dead — skip gracefully rather than
        # failing the whole ingest.
        if resp.status_code in (403, 404):
            log.warning(
                "Stack Overflow jobs RSS feed is gone (HTTP %d) — discontinued "
                "in 2023. Skipping this source; ingest continues with others.",
                resp.status_code,
            )
            return []
        resp.raise_for_status()
        return parse_so_rss(resp.text)


def parse_so_rss(xml_text: str) -> List[JobListing]:
    """Parse an SO jobs RSS/Atom document into listings."""
    root = ElementTree.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []
    all_jobs = channel.findall("item")
    total_results_el = channel.find(TOTAL_RESULTS_TAG)
    if total_results_el is not None:
        try:
            if int(total_results_el.text) != len(all_jobs):
                log.warning(
                    "SO RSS totalResults (%s) != item count (%d); proceeding",
                    total_results_el.text, len(all_jobs),
                )
        except (TypeError, ValueError):
            pass

    out: List[JobListing] = []
    for job in all_jobs:
        listing = _parse_item(job)
        if listing:
            out.append(listing)
    return out


def _parse_item(job) -> JobListing | None:
    location_el = job.find(LOCATION_TAG)
    location = clean_text(location_el.text) if location_el is not None else None

    link_el = job.find("link")
    apply_url = clean_text(link_el.text) if link_el is not None else None

    author_el = job.find(AUTHOR_NAME_TAG)
    company_name = None
    if author_el is not None:
        name_el = author_el.find(COMPANY_NAME_TAG)
        company_name = clean_text(name_el.text) if name_el is not None else None

    title_el = job.find("title")
    title = clean_text(title_el.text)[:128] if title_el is not None else None

    updated_el = job.find(UPDATED_DATE_TAG)
    created = parse_iso_datetime(updated_el.text if updated_el is not None else None)
    from_date = created.date() if created else datetime.utcnow().date()

    if not (title and company_name and apply_url):
        return None
    if not is_canadian_city(location):
        return None

    return JobListing(
        title=title[:128],
        company_name=company_name[:128],
        apply_url=apply_url[:256],
        salary_range=DEFAULT_SALARY,
        location=(location or DEFAULT_LOCATION)[:64],
        from_date=from_date,
        ext_id=ext_id_for(SOURCE_NAME, apply_url),
        source=SOURCE_NAME,
    )
