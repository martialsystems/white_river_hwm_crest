# Copyright (c) 2026 Martial Systems LLC
"""Fail closed: this tree tests water, not FEMA and not SIR 2011."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from hwmcrest.errors import ClaimBanError

_BANS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("casualty", re.compile(r"\b(deaths?|fatalit(?:y|ies)|casualt(?:y|ies)|killed)\b", re.I)),
    ("climate", re.compile(r"\b(cmip\d*|downscal(?:e|ed|ing)|gcm)\b", re.I)),
    ("par", re.compile(r"\b(lives|people|population)\s+at\s+risk\b", re.I)),
    ("p100", re.compile(r"\b100-year\s+exceedance\b", re.I)),
    ("forecast", re.compile(r"\bP\(sfha\s*\|\s*hydro\)\s+is\s+(?:a\s+)?(?:flood\s+)?forecast\b", re.I)),
    ("hand_firm", re.compile(r"\bHAND (?:mask|wet(?: area)?|bathtub) is (?:a |the )?FIRM\b", re.I)),
    ("fema_test", re.compile(r"\btests FEMA\b|\bFEMA is the test\b|\bagainst FEMA SFHA as truth\b", re.I)),
    ("sir_test", re.compile(r"\bSIR 2011(?:–|-)?5138\b.{0,40}\btest\b|\btests SIR 2011\b", re.I)),
    ("site", re.compile(r"\bsite-level flood risk\b", re.I)),
    ("flood_ai", re.compile(r"\bflood AI\b", re.I)),
)


def scan_text(text: str) -> list[str]:
    return [name for name, pat in _BANS if pat.search(text or "")]


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")
    if "—" in (text or ""):
        raise ClaimBanError(f"{source}: em dash")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
