# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop. Two figures max."""

from __future__ import annotations

import json
from pathlib import Path

from hwmcrest.claims import require_clean, require_paths_clean
from hwmcrest.config import (
    CREST_DATE,
    CREST_STAGE_FT,
    GAGE_ID,
    NORA_CREST_WET,
    QUESTION,
)
from hwmcrest.fetch import fetch_official
from hwmcrest.figure import write_two
from hwmcrest.fixture import arrays, fixture_points_lonlat
from hwmcrest.hits import score_points
from hwmcrest.sibling import require_crest_wet

try:
    from hwmforge.gate import require_claims, require_fetch, require_figures, require_sibling, require_stage
except ImportError:  # pragma: no cover

    def require_claims(**kwargs):
        del kwargs

    def require_fetch(**kwargs):
        del kwargs

    def require_figures(**kwargs):
        del kwargs

    def require_sibling(**kwargs):
        del kwargs

    def require_stage(**kwargs):
        del kwargs


def stage0_fixture(log_dir: Path) -> dict:
    require_stage(current_stage="0", target_stage="0", sibling_sha_ok=True, thread_id="fix.s0")
    require_sibling(sibling_sha_ok=True, thread_id="fix.sha")
    require_claims(thread_id="fix.claims")
    blobs = arrays()
    pts = fixture_points_lonlat()
    table = score_points(pts, wet=blobs["wet"], transform=blobs["transform"], crs=blobs["crs"])
    require_clean(QUESTION, source="question")
    paths = write_two(log_dir, wet=blobs["wet"], table=table)
    require_figures(n_figures=len(paths), thread_id="fix.figs")
    log_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": "0",
        "fixture": True,
        "question": QUESTION,
        "gage_id": GAGE_ID,
        "crest_stage_ft": CREST_STAGE_FT,
        "crest_date": CREST_DATE,
        "tests_fema": False,
        "tests_sir_2011": False,
        "table": {k: table[k] for k in ("n", "n_hit", "n_miss", "n_out", "hit_rate_in_window")},
        "figures": [p.name for p in paths],
    }
    (log_dir / "stage0_report.json").write_text(json.dumps(report, indent=2) + "\n")
    require_paths_clean([log_dir / "stage0_report.json"])
    return report


def run_live(log_dir: Path) -> dict:
    sha = require_crest_wet()
    require_sibling(sibling_sha_ok=True, thread_id="live.sha")
    require_stage(
        current_stage="0",
        target_stage="A",
        sibling_sha_ok=True,
        thread_id="live.sA",
    )
    fetched = fetch_official()
    require_fetch(official_ok=True, thread_id="live.fetch")
    import rasterio

    with rasterio.open(NORA_CREST_WET) as src:
        wet = src.read(1)
        tf = src.transform
        crs = src.crs
    table = score_points(fetched["points"], wet=wet, transform=tf, crs=crs)
    require_stage(
        current_stage="A",
        target_stage="B",
        sibling_sha_ok=True,
        fetched_ok=True,
        thread_id="live.sB",
    )
    paths = write_two(log_dir, wet=wet, table=table)
    require_figures(n_figures=len(paths), thread_id="live.figs")
    require_stage(
        current_stage="B",
        target_stage="C",
        sibling_sha_ok=True,
        fetched_ok=True,
        figures_ok=True,
        thread_id="live.sC",
    )
    report = {
        "stage": "C",
        "fixture": False,
        "question": QUESTION,
        "gage_id": GAGE_ID,
        "crest_stage_ft": CREST_STAGE_FT,
        "crest_date": CREST_DATE,
        "tests_fema": False,
        "tests_sir_2011": False,
        "sibling_sha": sha,
        "probes": fetched["probes"],
        "table": {k: table[k] for k in ("n", "n_hit", "n_miss", "n_out", "hit_rate_in_window")},
        "points": table["points"],
        "figures": [p.name for p in paths],
    }
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / "stage_c_report.json").write_text(json.dumps(report, indent=2) + "\n")
    require_paths_clean(
        [log_dir / "stage_c_report.json", Path(__file__).resolve().parents[2] / "README.md"]
    )
    require_claims(thread_id="live.claims")
    return report
