# Copyright (c) 2026 Martial Systems LLC
"""Official HWM fetch. Empty or 404 stops live paint."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from hwmcrest.config import SCIENCEBASE_URL, STN_IN_URL, STN_MARION_URL, USER_AGENT
from hwmcrest.errors import FetchError


def _get(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read() if exc.fp else b""
    except Exception as exc:  # noqa: BLE001
        raise FetchError(f"official HWM fetch failed: {url}: {exc}") from exc


def parse_stn(blob: bytes) -> list[dict[str, Any]]:
    if not blob or blob.strip() in {b"[]", b"{}"}:
        return []
    data = json.loads(blob.decode("utf-8"))
    if not isinstance(data, list):
        return []
    out: list[dict[str, Any]] = []
    for rec in data:
        lat = rec.get("latitude_dd") or rec.get("latitude") or rec.get("site_latitude")
        lon = rec.get("longitude_dd") or rec.get("longitude") or rec.get("site_longitude")
        if lat is None or lon is None:
            continue
        out.append(
            {
                "id": str(rec.get("hwm_id") or rec.get("site_no") or ""),
                "lat": float(lat),
                "lon": float(lon),
                "elev_ft": rec.get("elev_ft"),
                "event": str(rec.get("eventName") or rec.get("event_name") or ""),
                "waterbody": str(rec.get("waterbody") or ""),
                "source": "USGS STN",
                "flag_date": str(rec.get("flag_date") or rec.get("survey_date") or ""),
            }
        )
    return out


def fetch_official() -> dict[str, Any]:
    """Return points from USGS STN / ScienceBase. Empty list is a stop, not a zero-hit map."""
    probes: list[dict[str, Any]] = []
    points: list[dict[str, Any]] = []
    for name, url in (
        ("stn_in", STN_IN_URL),
        ("stn_marion", STN_MARION_URL),
        ("sciencebase", SCIENCEBASE_URL),
    ):
        code, body = _get(url)
        probes.append({"name": name, "url": url, "http": code, "bytes": len(body)})
        if name.startswith("stn") and code == 200:
            points.extend(parse_stn(body))
        if name == "sciencebase" and code == 200:
            try:
                total = int(json.loads(body.decode("utf-8")).get("total") or 0)
            except Exception:
                total = 0
            probes[-1]["total"] = total
            if total == 0:
                probes[-1]["empty"] = True
        if code == 404:
            probes[-1]["empty"] = True
    # Dedup by lat/lon rounded.
    seen: set[tuple[float, float]] = set()
    uniq: list[dict[str, Any]] = []
    for rec in points:
        key = (round(rec["lat"], 5), round(rec["lon"], 5))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(rec)
    if not uniq:
        raise FetchError(
            "official HWM layer empty or 404 (USGS STN Indiana/Marion, ScienceBase "
            "Indiana 2026). Live paint stops. Fixture path stays green."
        )
    return {"points": uniq, "probes": probes}
