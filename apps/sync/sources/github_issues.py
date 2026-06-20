"""GitHub issues source — ``TechnologyMasters/jobs`` issues feed.

This is the only live source: Stack Overflow Jobs (and its RSS feed) was
discontinued in 2023. Issue titles follow the repo convention
``Company - Job Title - Location - Salary``.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List

import httpx

from config import Config
from .base import (
    DEFAULT_LOCATION,
    DEFAULT_SALARY,
    JobListing,
    ext_id_for,
)
from .util import (
    clean_text,
    is_canadian_city,
    parse_iso_datetime,
    parse_salary_from_body,
    split_issue_title,
)

log = logging.getLogger(__name__)

GITHUB_ISSUES_URL = "https://api.github.com/repos/TechnologyMasters/jobs/issues"
SOURCE_NAME = "github-tm"


class GitHubIssuesSource:
    name = SOURCE_NAME

    def __init__(self, url: str = GITHUB_ISSUES_URL, per_page: int = 100):
        self.url = url
        self.per_page = per_page

    async def fetch(self, client: httpx.AsyncClient, config: Config) -> List[JobListing]:
        headers = {"Accept": "application/vnd.github+json"}
        if config.github_token:
            headers["Authorization"] = f"Bearer {config.github_token}"

        params = {"state": "open", "per_page": self.per_page}
        log.info("fetching GitHub issues from %s", self.url)
        resp = await client.get(self.url, headers=headers, params=params)
        resp.raise_for_status()
        items = resp.json()
        log.info("received %d GitHub issues", len(items))
        return [listing for item in items if (listing := parse_github_issue(item))]

    # kept for symmetry with the other sources / tests
    @staticmethod
    def _parse(item: dict) -> JobListing | None:
        return parse_github_issue(item)


def parse_github_issue(item: dict) -> JobListing | None:
    """Parse a single GitHub issue into a listing, or None if out of scope."""
    parts = split_issue_title(item.get("title"))
    company_name = clean_text(parts[0]) if parts else None
    title = clean_text(parts[1]) if len(parts) > 1 else None
    location = clean_text(parts[2]) if len(parts) > 2 else None

    apply_url = clean_text(item.get("html_url"))
    body = item.get("body") or ""
    salary_range = parse_salary_from_body(body)
    # Prefer a salary found in the title segment, if present.
    if len(parts) > 3 and parts[3]:
        salary_range = parts[3]

    created = parse_iso_datetime(item.get("created_at"))
    from_date = created.date() if created else datetime.utcnow().date()

    if not (title and company_name and apply_url):
        return None
    if not is_canadian_city(location):
        return None

    return JobListing(
        title=title[:128],
        company_name=company_name[:128],
        apply_url=apply_url[:256],
        salary_range=(salary_range or DEFAULT_SALARY)[:64],
        location=(location or DEFAULT_LOCATION)[:64],
        from_date=from_date,
        ext_id=ext_id_for(SOURCE_NAME, str(item.get("id") or apply_url)),
        source=SOURCE_NAME,
    )
