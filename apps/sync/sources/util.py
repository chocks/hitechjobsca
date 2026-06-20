"""Pure parsing helpers (no I/O) so they can be unit-tested directly."""

from __future__ import annotations

import re
from datetime import datetime

from .base import DEFAULT_SALARY

# Cities/regions considered in-scope for this Canadian jobs board.
# Preserved from the original 2020 script (including "remote").
CITIES = (
    "toronto",
    "vancouver",
    "ottawa",
    "montreal",
    "halifax",
    "ontario",
    "saskatoon",
    "remote",
    "canada",
)

# Captures a dollar amount, an optional range, and an optional frequency
# (e.g. "$50,000-$80,000/year", "$2000-$4000/month", "$100k/yr" via the title
# segment which is taken verbatim).
SALARY_RE = re.compile(
    r"\$[\d.,]+(?:\s*(?:[-\u2013\u2014]|to)\s*\$?[\d.,]+)?(?:\s*/\s*[A-Za-z]+)?"
)


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def is_canadian_city(city: str | None) -> bool:
    if not city:
        return False
    low = city.lower()
    return any(c in low for c in CITIES)


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def parse_salary_from_body(body: str | None) -> str:
    """Pull a salary out of a GitHub issue body's ``### Salary Expectation`` block."""
    if not body:
        return DEFAULT_SALARY
    m = re.search(r"###\s*Salary Expectation(.+?)(?:\n###|\Z)", body, re.S | re.I)
    section = m.group(1) if m else body
    match = SALARY_RE.search(section)
    return match.group(0).strip() if match else DEFAULT_SALARY


def split_issue_title(title: str | None) -> list[str]:
    """Split a ``Company - Title - Location - Salary`` issue title."""
    if not title:
        return []
    return [part.strip() for part in title.split(" - ")]
