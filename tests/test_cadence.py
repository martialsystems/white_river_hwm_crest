# Copyright (c) 2026 Martial Systems LLC
"""Calendar for parked HWM fetch. Not a new model."""

from datetime import date, timedelta
from pathlib import Path

from hwmcrest.claims import scan_text

REPO = Path(__file__).resolve().parents[1]
CADENCE = (REPO / "CADENCE.md").read_text(encoding="utf-8")

LAST_EMPTY = date(2026, 9, 5)
SILENCE_END = date(2026, 9, 16)
FIRST_RUN = date(2026, 9, 17)
WEEKLY_END = date(2026, 10, 31)
CLOCK_STOP = date(2027, 2, 7)

WEEKLY_THURSDAYS = (
    date(2026, 9, 17),
    date(2026, 9, 24),
    date(2026, 10, 1),
    date(2026, 10, 8),
    date(2026, 10, 15),
    date(2026, 10, 22),
    date(2026, 10, 29),
)
FIRST_SUNDAYS = (
    date(2026, 11, 1),
    date(2026, 12, 6),
    date(2027, 1, 3),
    date(2027, 2, 7),
)


def _first_sunday(year: int, month: int) -> date:
    start = date(year, month, 1)
    return start + timedelta(days=(6 - start.weekday()) % 7)


def calendar_due(day: date) -> bool:
    if day <= SILENCE_END:
        return False
    if day == FIRST_RUN:
        return True
    if FIRST_RUN < day <= WEEKLY_END:
        return (day - FIRST_RUN).days % 7 == 0
    if date(2026, 11, 1) <= day <= CLOCK_STOP:
        return day == _first_sunday(day.year, day.month)
    return False


def test_silence_then_weekly_then_monthly_then_stop() -> None:
    assert LAST_EMPTY < SILENCE_END
    assert not calendar_due(date(2026, 9, 6))
    assert not calendar_due(date(2026, 9, 10))
    assert not calendar_due(SILENCE_END)
    assert calendar_due(FIRST_RUN)
    for day in WEEKLY_THURSDAYS:
        assert calendar_due(day)
    assert not calendar_due(date(2026, 10, 30))
    assert not calendar_due(date(2026, 10, 31))
    for day in FIRST_SUNDAYS:
        assert calendar_due(day)
        assert day == _first_sunday(day.year, day.month)
    assert not calendar_due(date(2027, 2, 8))
    assert not calendar_due(date(2027, 3, 7))


def test_cadence_doc_locks_the_calendar_and_the_run() -> None:
    text = CADENCE
    assert "2026-09-05" in text
    assert "`99c76a2`" in text
    assert "Not daily" in text
    assert "17 Sep 2026" in text
    assert "24 Sep" in text
    assert "29 Oct" in text
    assert "1 Nov 2026" in text
    assert "6 Dec 2026" in text
    assert "3 Jan 2027" in text
    assert "7 Feb 2027" in text
    assert "stop the clock" in text
    assert "run_live.py" in text
    assert "logs/stage0_fixture" in text
    assert "README probe date only" in text
    assert "No scoring on empty" in text
    assert "99c76a2" in text
    assert "Flood Event Viewer" in text
    assert "ScienceBase search total leaves 0" in text
    assert "no longer 2 bytes" in text
    assert "—" not in text
    assert "What it is not" not in text
    assert scan_text(text) == []
    for path in ("AGENTS.md", "CHECKLIST.md", "METHODOLOGY.md"):
        body = (REPO / path).read_text(encoding="utf-8")
        assert "CADENCE.md" in body
        assert "—" not in body
        assert "What it is not" not in body


def test_cadence_doc_lists_every_calendar_fire() -> None:
    text = CADENCE
    assert "17 Sep, 24 Sep, 1 Oct, 8 Oct, 15 Oct, 22 Oct, 29 Oct" in text
    assert "1 Nov 2026, 6 Dec 2026, 3 Jan 2027, 7 Feb 2027" in text


def test_readme_probe_date_stays_on_last_empty_fetch() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "Official probe (2026-09-05)" in readme
    assert "Official probe (2026-09-06)" not in readme
