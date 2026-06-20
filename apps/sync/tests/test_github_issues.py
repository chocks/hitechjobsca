import json
from pathlib import Path

import httpx
import pytest
import respx

from config import Config
from sources.github_issues import GitHubIssuesSource, parse_github_issue, GITHUB_ISSUES_URL

FIXTURES = Path(__file__).parent / "fixtures"


def _load_issue():
    return json.loads((FIXTURES / "github_issue.json").read_text())


def test_parse_github_issue_canadian():
    listing = parse_github_issue(_load_issue())
    assert listing is not None
    assert listing.company_name == "WebBoxes"
    assert listing.title == "Sr. AI Engineer"
    assert listing.location == "Remote/LatAm"  # "remote" matches the city allowlist
    assert listing.apply_url == "https://github.com/TechnologyMasters/jobs/issues/721"
    # title-segment salary is preferred over the body salary block
    assert listing.salary_range == "$50,000 USD/Year"
    assert listing.source == "github-tm"
    assert listing.ext_id.startswith("github-tm:")


def test_parse_github_issue_non_canadian_skipped():
    issue = _load_issue()
    issue["title"] = "WebBoxes - Sr. AI Engineer - Bangalore, India - $50k"
    assert parse_github_issue(issue) is None


def test_parse_github_issue_missing_fields_skipped():
    issue = _load_issue()
    issue["title"] = "Just one part"
    assert parse_github_issue(issue) is None


def test_parse_github_issue_title_salary_preferred():
    issue = _load_issue()
    issue["title"] = "WebBoxes - Sr. AI Engineer - Toronto - $50,000 USD/Year"
    listing = parse_github_issue(issue)
    assert listing is not None
    assert listing.salary_range == "$50,000 USD/Year"


@pytest.mark.asyncio
async def test_fetch_uses_respx_mock():
    issue = _load_issue()
    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})
    with respx.mock(base_url="https://api.github.com") as mock:
        mock.get("/repos/TechnologyMasters/jobs/issues").respond(
            200, json=[issue]
        )
        async with httpx.AsyncClient(base_url="https://api.github.com") as client:
            src = GitHubIssuesSource(
                url="https://api.github.com/repos/TechnologyMasters/jobs/issues"
            )
            listings = await src.fetch(client, cfg)
    assert len(listings) == 1
    assert listings[0].company_name == "WebBoxes"


@pytest.mark.asyncio
async def test_fetch_sends_auth_header_when_token_present():
    issue = _load_issue()
    cfg = Config.from_env({"SYNC_GITHUB_TOKEN": "ghp_test", "SYNC_DRY_RUN": "1"})
    captured = {}

    def _intercept(request):
        captured["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json=[issue])

    with respx.mock(base_url="https://api.github.com") as mock:
        route = mock.get("/repos/TechnologyMasters/jobs/issues")
        route.mock(side_effect=_intercept)
        async with httpx.AsyncClient(base_url="https://api.github.com") as client:
            src = GitHubIssuesSource(
                url="https://api.github.com/repos/TechnologyMasters/jobs/issues"
            )
            await src.fetch(client, cfg)
    assert captured["auth"] == "Bearer ghp_test"
