# Copyright (c) 2026 Martial Systems LLC

from hwmcrest.claims import scan_text
from hwmcrest.config import QUESTION


def test_question_and_bans() -> None:
    assert scan_text(QUESTION) == []
    assert "flood_ai" in scan_text("we built flood AI")
    assert "hand_firm" in scan_text("HAND bathtub is a FIRM")
