from datetime import date

from db import listing_to_row, UPSERT_SQL
from sources.base import JobListing


def _listing(**over):
    base = dict(
        title="Senior Engineer", company_name="Shopify",
        apply_url="https://shopify.com/careers/1", salary_range="$130k-$175k",
        location="Toronto, ON", from_date=date(2024, 5, 1),
        ext_id="github-tm:abc123", source="github-tm",
    )
    base.update(over)
    return JobListing(**base)


def test_listing_to_row_column_order():
    row = listing_to_row(_listing())
    # Order must match UPSERT_SQL column list:
    # title, company_name, apply_url, salary_range, from_date, location,
    # status, rank, ext_id
    assert row == (
        "Senior Engineer",
        "Shopify",
        "https://shopify.com/careers/1",
        "$130k-$175k",
        date(2024, 5, 1),
        "Toronto, ON",
        True,
        10,  # default rank from JobListing
        "github-tm:abc123",
    )


def test_upsert_sql_uses_on_conflict_ext_id():
    assert "ON CONFLICT (ext_id) DO UPDATE" in UPSERT_SQL
    assert "VALUES %s" in UPSERT_SQL  # execute_values placeholder


def test_upsert_sql_targets_jobs_all_jobs():
    assert "jobs.all_jobs" in UPSERT_SQL
