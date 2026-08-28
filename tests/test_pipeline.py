# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from hwmcrest.config import QUESTION
from hwmcrest.pipeline import stage0_fixture


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["tests_fema"] is False
    assert (tmp_path / "hwm_on_crest.png").is_file()
    assert (tmp_path / "hwm_counts.png").is_file()
    assert report["figures"] == ["hwm_on_crest.png", "hwm_counts.png"]
