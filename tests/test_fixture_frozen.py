# Copyright (c) 2026 Martial Systems LLC
"""Committed Stage 0 figures stay frozen until an official layer exists."""

import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "logs" / "stage0_fixture"

LOCKED_SHA256 = {
    "hwm_on_crest.png": "8038a06aaa98b318b353ee2386e7025dd833ab0e75cbce0872e9704efdd218df",
    "hwm_counts.png": "12a2d913b40d43bd341533b08ddb0df5f54f690e24b1503c0f5d8a0f2d5a1b8b",
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
