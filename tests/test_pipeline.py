# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from hwmcrest.config import QUESTION
from hwmcrest.figure import (
    FIG2_FIXTURE_TITLE,
    counts_copy,
    map_copy,
)
from hwmcrest.pipeline import stage0_fixture


def test_fixture_titles_say_synthetic_not_live() -> None:
    t1, s1 = map_copy(fixture=True)
    t2, f2 = counts_copy(fixture=True)
    assert "FIXTURE" in t1
    assert "not live" in t1
    assert "synthetic" in t1
    assert s1 == "Not the August 2026 result."
    assert t2 == FIG2_FIXTURE_TITLE
    assert "Official layer empty" in t2
    assert t2 != "August 2026 HWM points vs Nora HAND at 21.18 ft"
    assert f2 == "Not the August 2026 result."
    live_t2, _ = counts_copy(fixture=False)
    assert live_t2 != "August 2026 HWM points vs Nora HAND at 21.18 ft"


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["tests_fema"] is False
    assert report["fixture"] is True
    assert report["table"]["n_hit"] == 2
    assert report["table"]["n_miss"] == 1
    assert report["table"]["n_out"] == 1
    assert (tmp_path / "hwm_on_crest.png").is_file()
    assert (tmp_path / "hwm_counts.png").is_file()
    assert report["figures"] == ["hwm_on_crest.png", "hwm_counts.png"]
