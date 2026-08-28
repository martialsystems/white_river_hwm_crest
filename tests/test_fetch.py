# Copyright (c) 2026 Martial Systems LLC

import pytest

from hwmcrest.errors import FetchError
from hwmcrest.fetch import fetch_official, parse_stn


def test_empty_stn_is_no_points() -> None:
    assert parse_stn(b"[]") == []
    assert parse_stn(b"") == []


def test_stn_parse_one_point() -> None:
    blob = (
        b'[{"latitude_dd": 39.91, "longitude_dd": -86.10, "hwm_id": 1,'
        b' "elev_ft": 731.0, "eventName": "fixture", "waterbody": "White River"}]'
    )
    pts = parse_stn(blob)
    assert len(pts) == 1
    assert pts[0]["lat"] == 39.91
    assert pts[0]["source"] == "USGS STN"


def test_live_official_layer_stops() -> None:
    with pytest.raises(FetchError, match="empty or 404"):
        fetch_official()
