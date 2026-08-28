# Copyright (c) 2026 Martial Systems LLC
"""Tiny window and four points so CI scores without a live HWM layer."""

from __future__ import annotations

from typing import Any

import numpy as np

from hwmcrest.config import (
    FIXTURE_COLS,
    FIXTURE_NORTH,
    FIXTURE_ROWS,
    FIXTURE_WEST,
    TEMPLATE_CRS,
    TEMPLATE_RES_M,
    WET_DRY,
    WET_NODATA,
    WET_WET,
)


def affine():
    from rasterio.transform import from_origin

    return from_origin(FIXTURE_WEST, FIXTURE_NORTH, TEMPLATE_RES_M, TEMPLATE_RES_M)


def arrays() -> dict[str, Any]:
    wet = np.full((FIXTURE_ROWS, FIXTURE_COLS), WET_NODATA, dtype=np.uint8)
    wet[2:14, 2:10] = WET_DRY
    wet[4:12, 4:7] = WET_WET
    tf = affine()
    # Two hits on wet, one miss on dry-in-window, one out of window.
    pts = []
    cells = [(6, 5, "hit"), (8, 5, "hit"), (6, 8, "miss"), (0, 0, "out")]
    for row, col, _status in cells:
        x, y = tf * (col + 0.5, row + 0.5)
        # identity: fixture is already 5070; store as lon/lat via a dummy
        pts.append({"x": x, "y": y, "row": row, "col": col})
    return {"wet": wet, "transform": tf, "crs": f"EPSG:{TEMPLATE_CRS}", "cells": cells, "xy": pts}


def fixture_points_lonlat() -> list[dict[str, Any]]:
    """Project fixture cell centers to lon/lat so score_points uses the live path."""
    from rasterio.warp import transform as rio_transform

    blobs = arrays()
    out: list[dict[str, Any]] = []
    for i, rec in enumerate(blobs["xy"]):
        lon, lat = rio_transform(blobs["crs"], "EPSG:4326", [rec["x"]], [rec["y"]])
        out.append(
            {
                "id": f"fix{i}",
                "lat": float(lat[0]),
                "lon": float(lon[0]),
                "elev_ft": None,
                "source": "fixture",
                "event": "fixture",
                "waterbody": "White River",
            }
        )
    return out
