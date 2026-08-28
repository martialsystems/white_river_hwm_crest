# Copyright (c) 2026 Martial Systems LLC

from hwmcrest.fixture import arrays, fixture_points_lonlat
from hwmcrest.hits import score_points


def test_fixture_two_hit_one_miss_one_out() -> None:
    blobs = arrays()
    table = score_points(
        fixture_points_lonlat(),
        wet=blobs["wet"],
        transform=blobs["transform"],
        crs=blobs["crs"],
    )
    assert table["n"] == 4
    assert table["n_hit"] == 2
    assert table["n_miss"] == 1
    assert table["n_out"] == 1
    assert table["tests_fema"] is False
    assert table["tests_sir_2011"] is False
    statuses = [p["status"] for p in table["points"]]
    assert statuses.count("hit") == 2
