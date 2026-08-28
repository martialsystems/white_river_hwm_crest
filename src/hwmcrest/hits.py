# Copyright (c) 2026 Martial Systems LLC
"""Point-in-cell on the crest wet mask."""

from __future__ import annotations

from typing import Any

import numpy as np

from hwmcrest.config import WET_DRY, WET_NODATA, WET_WET
from hwmcrest.errors import GateError


def score_points(
    points: list[dict[str, Any]],
    *,
    wet: np.ndarray,
    transform,
    crs,
) -> dict[str, Any]:
    from rasterio.transform import rowcol
    from rasterio.warp import transform as rio_transform

    if not points:
        raise GateError("no HWM points to score")
    nrows, ncols = wet.shape
    scored: list[dict[str, Any]] = []
    n_hit = n_miss = n_out = 0
    for rec in points:
        lon, lat = float(rec["lon"]), float(rec["lat"])
        xs, ys = rio_transform("EPSG:4326", crs, [lon], [lat])
        row_i, col_i = rowcol(transform, xs[0], ys[0], op=round)
        status = "out"
        if 0 <= int(row_i) < nrows and 0 <= int(col_i) < ncols:
            val = int(wet[int(row_i), int(col_i)])
            if val == WET_WET:
                status = "hit"
                n_hit += 1
            elif val == WET_DRY:
                status = "miss"
                n_miss += 1
        if status == "out":
            n_out += 1
        scored.append({**rec, "row": int(row_i), "col": int(col_i), "status": status})
    n = len(scored)
    return {
        "n": n,
        "n_hit": n_hit,
        "n_miss": n_miss,
        "n_out": n_out,
        "hit_rate_in_window": (n_hit / (n_hit + n_miss)) if (n_hit + n_miss) else None,
        "points": scored,
        "tests_fema": False,
        "tests_sir_2011": False,
    }
