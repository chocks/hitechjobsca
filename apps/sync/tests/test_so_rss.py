from pathlib import Path

import httpx
import pytest
import respx

from config import Config
from sources.so_rss import StackOverflowRssSource, parse_so_rss, SO_JOBS_URL

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_so_rss():
    xml = (FIXTURES / "so_feed.xml").read_text()
    listings = parse_so_rss(xml)
    assert len(listings) == 2
    titles = {l.title for l in listings}
    assert titles == {"Senior Backend Engineer (Java)", "Frontend Developer"}
    rbc = next(l for l in listings if l.company_name == "RBC")
    assert rbc.apply_url == "https://stackoverflow.com/jobs/12345/senior-backend-engineer"
    assert rbc.location == "Toronto, ON, Canada"
    assert rbc.salary_range == "N/A"
    assert rbc.source == "so-rss"
    assert rbc.ext_id.startswith("so-rss:")


def test_parse_so_rss_empty():
    assert parse_so_rss("<rss><channel></channel></rss>") == []
    assert parse_so_rss("<rss></rss>") == []


@pytest.mark.asyncio
async def test_fetch_404_returns_empty():
    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})
    with respx.mock(base_url="https://stackoverflow.com") as mock:
        mock.get("/jobs/feed").respond(404)
        async with httpx.AsyncClient(base_url="https://stackoverflow.com") as client:
            src = StackOverflowRssSource(url=SO_JOBS_URL)
            listings = await src.fetch(client, cfg)
    assert listings == []


@pytest.mark.asyncio
async def test_fetch_403_returns_empty():
    # SO Jobs is dead; Cloudflare returns 403 to non-browser clients.
    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})
    with respx.mock(base_url="https://stackoverflow.com") as mock:
        mock.get("/jobs/feed").respond(403)
        async with httpx.AsyncClient(base_url="https://stackoverflow.com") as client:
            src = StackOverflowRssSource(url=SO_JOBS_URL)
            listings = await src.fetch(client, cfg)
    assert listings == []


@pytest.mark.asyncio
async def test_fetch_5xx_raises():
    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})
    with respx.mock(base_url="https://stackoverflow.com") as mock:
        mock.get("/jobs/feed").respond(500)
        async with httpx.AsyncClient(base_url="https://stackoverflow.com") as client:
            src = StackOverflowRssSource(url=SO_JOBS_URL)
            with pytest.raises(httpx.HTTPStatusError):
                await src.fetch(client, cfg)


@pytest.mark.asyncio
async def test_fetch_ok_parses():
    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})
    xml = (FIXTURES / "so_feed.xml").read_text()
    with respx.mock(base_url="https://stackoverflow.com") as mock:
        mock.get("/jobs/feed").respond(200, text=xml)
        async with httpx.AsyncClient(base_url="https://stackoverflow.com") as client:
            src = StackOverflowRssSource(url=SO_JOBS_URL)
            listings = await src.fetch(client, cfg)
    assert len(listings) == 2
