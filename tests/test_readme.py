# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from hwmcrest.claims import scan_text
from hwmcrest.config import QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    first = text.strip().splitlines()[2] if text.startswith("#") else text.strip().splitlines()[0]
    # Title line, then blank or question. Require question is first sentence of body.
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert "21.18" in text
    assert "white_river_stage_inundation" in text
    assert scan_text(text) == []
    assert "—" not in text
    assert "What it is not" not in text
