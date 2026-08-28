# Copyright (c) 2026 Martial Systems LLC
"""Pin Nora crest wet mask. Do not rewrite Nora v1 PNG."""

from __future__ import annotations

import hashlib
from pathlib import Path

from hwmcrest.config import (
    LOCKED_CREST_WET_SHA256,
    LOCKED_NORA_V1_PNG_SHA256,
    LOCKED_WINDOW_SHA256,
    NORA_CREST_WET,
    NORA_DEFAULT,
    TEMPLATE_CRS,
)
from hwmcrest.errors import SiblingShaError


def band_sha256(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        return hashlib.sha256(src.read(1).tobytes()).hexdigest()


def window_sha256(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        t = src.transform
        payload = (
            f"{int(src.crs.to_epsg() or 0)}|{src.width}|{src.height}|"
            f"{t.a},{t.b},{t.c},{t.d},{t.e},{t.f}"
        )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_crest_wet(path: Path = NORA_CREST_WET) -> dict[str, str]:
    if not path.is_file():
        raise SiblingShaError(f"Nora crest wet mask missing: {path}")
    band = band_sha256(path)
    if band != LOCKED_CREST_WET_SHA256:
        raise SiblingShaError(f"crest wet band {band} != locked {LOCKED_CREST_WET_SHA256}")
    win = window_sha256(path)
    if win != LOCKED_WINDOW_SHA256:
        raise SiblingShaError(f"window {win} != locked {LOCKED_WINDOW_SHA256}")
    import rasterio

    with rasterio.open(path) as src:
        if int(src.crs.to_epsg() or 0) != TEMPLATE_CRS:
            raise SiblingShaError(f"CRS {src.crs} is not EPSG:{TEMPLATE_CRS}")
    v1 = NORA_DEFAULT / "logs" / "nora_live" / "three_wet.png"
    if v1.is_file():
        got = file_sha256(v1)
        if got != LOCKED_NORA_V1_PNG_SHA256:
            raise SiblingShaError(f"Nora v1 PNG drifted {got}")
    return {"crest_wet": band, "window": win}
