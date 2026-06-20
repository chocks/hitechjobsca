import pytest

from sources.util import (
    is_canadian_city,
    parse_iso_datetime,
    parse_salary_from_body,
    split_issue_title,
    clean_text,
)


@pytest.mark.parametrize("city,expected", [
    ("Toronto, ON, Canada", True),
    ("Remote, Canada", True),
    ("Vancouver, BC", True),
    ("Montreal, QC", True),
    ("New York, NY", False),
    ("London, UK", False),
    ("", False),
    (None, False),
])
def test_is_canadian_city(city, expected):
    assert is_canadian_city(city) is expected


def test_parse_iso_datetime_z_suffix():
    d = parse_iso_datetime("2024-05-01T12:34:56Z")
    assert d is not None
    assert d.year == 2024 and d.month == 5 and d.day == 1


def test_parse_iso_datetime_offset():
    d = parse_iso_datetime("2024-05-01T12:34:56+00:00")
    assert d is not None


def test_parse_iso_datetime_invalid():
    assert parse_iso_datetime(None) is None
    assert parse_iso_datetime("") is None
    assert parse_iso_datetime("not a date") is None


def test_parse_salary_from_body_salary_block():
    body = (
        "## What You'll get\n\n### Salary Expectation\n\n"
        "- $50.000/year\n- Contract / Full Time\n\n### Benefits\n\n"
    )
    assert parse_salary_from_body(body) == "$50.000/year"


def test_parse_salary_from_body_range():
    body = "### Salary Expectation\n\n- $2000-$4000/month or negotiable\n"
    assert parse_salary_from_body(body) == "$2000-$4000/month"


def test_parse_salary_from_body_none():
    assert parse_salary_from_body(None) == "N/A"
    assert parse_salary_from_body("no salary here") == "N/A"


def test_split_issue_title():
    parts = split_issue_title("WebBoxes - Sr. AI Engineer - Remote/LatAm - $50,000 USD/Year")
    assert parts == ["WebBoxes", "Sr. AI Engineer", "Remote/LatAm", "$50,000 USD/Year"]


def test_split_issue_title_empty():
    assert split_issue_title(None) == []
    assert split_issue_title("") == []


def test_clean_text():
    assert clean_text("  hello  ") == "hello"
    assert clean_text("") is None
    assert clean_text(None) is None
