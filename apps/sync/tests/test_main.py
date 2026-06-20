from datetime import date

import httpx
import pytest
import respx

from config import Config
from main import run_once
from sources import GitHubIssuesSource, StackOverflowRssSource
from sources.base import JobListing


def _listing(**over):
    base = dict(
        title="T", company_name="C", apply_url="https://x/y",
        salary_range="N/A", location="Toronto, ON", from_date=date(2024, 1, 1),
        ext_id="github-tm:abc", source="github-tm",
    )
    base.update(over)
    return JobListing(**base)


@pytest.mark.asyncio
async def test_run_once_dry_run_skips_db(monkeypatch):
    called = {"upsert": False}

    def _fake_upsert(cfg, listings):
        called["upsert"] = True
        return (0, 0)

    monkeypatch.setattr("main.upsert_listings", _fake_upsert)

    cfg = Config.from_env({"SYNC_DRY_RUN": "1"})

    class _Src:
        name = "test-src"

        async def fetch(self, client, config):
            return [_listing()]

    summary = await run_once(cfg, sources=[_Src()])
    assert called["upsert"] is False
    assert summary["test-src"]["count"] == 1
    assert "_db" not in summary  # dry-run skips DB entirely
    assert summary["_meta"]["total_listings"] == 1


@pytest.mark.asyncio
async def test_run_once_source_error_is_captured(monkeypatch):
    monkeypatch.setattr("main.upsert_listings", lambda cfg, ls: (0, 0))
    cfg = Config.from_env({})

    class _Boom:
        name = "boom"

        async def fetch(self, client, config):
            raise RuntimeError("boom")

    summary = await run_once(cfg, sources=[_Boom()])
    assert summary["boom"]["count"] == 0
    assert summary["boom"]["error"] == "boom"
    assert summary["_meta"]["total_listings"] == 0


@pytest.mark.asyncio
async def test_run_once_db_error_captured(monkeypatch):
    def _bad_upsert(cfg, listings):
        raise RuntimeError("db down")

    monkeypatch.setattr("main.upsert_listings", _bad_upsert)
    cfg = Config.from_env({})

    class _Src:
        name = "ok"

        async def fetch(self, client, config):
            return [_listing()]

    summary = await run_once(cfg, sources=[_Src()])
    assert summary["_db"]["error"] == "upsert failed"
