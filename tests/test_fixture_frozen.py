# Copyright (c) 2026 Martial Systems LLC
"""Committed Stage 0 figures stay frozen until an official layer exists."""

import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "logs" / "stage0_fixture"

LOCKED_SHA256 = {
    "hwm_on_crest.png": "bb06c6ad7d54f23147bb108be4d307622ef63a869de760a54f13eef0a1bab2b5",
    "hwm_counts.png": "323248260dbe5c9d32d822688b72d568f87843eb7d7ff1c56c8b66ac25318db8",
    "stage0_report.json": "909910ab7b4c8a657f25459f56c5d52ce9ba8367e9dce3d5c91a2441d2679900",
}


def test_committed_fixture_blobs_are_frozen() -> None:
    for name, expected in LOCKED_SHA256.items():
        blob = (FIXTURE / name).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == expected


def test_vbd_fixture_path_does_not_follow_test_edits() -> None:
    import json

    spec = json.loads((REPO / "vbd.runtime.json").read_text(encoding="utf-8"))
    fixture = next(row for row in spec["runtime_checks"] if row["id"] == "fixture-path")
    assert "tests/**" not in fixture["paths"]
    assert fixture["argv"][-1] == "logs/stage0_fixture"
