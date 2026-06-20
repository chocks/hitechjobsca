"""Ingest sources package."""

from .base import JobListing, Source, ext_id_for
from .github_issues import GitHubIssuesSource
from .so_rss import StackOverflowRssSource

__all__ = [
    "JobListing",
    "Source",
    "ext_id_for",
    "GitHubIssuesSource",
    "StackOverflowRssSource",
]
