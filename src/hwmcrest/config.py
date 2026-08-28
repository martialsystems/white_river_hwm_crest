# Copyright (c) 2026 Martial Systems LLC
"""Locked Nora crest HWM compare. Do not reopen FEMA or SIR 2011."""

from __future__ import annotations

from pathlib import Path

HUC8 = "05120201"
GAGE_ID = "03351000"
GAGE_NWS_ID = "NORI3"
CREST_STAGE_FT = 21.18
CREST_DATE = "2026-08-15"
QUESTION = (
    "Do August 2026 high-water marks land on the Nora HAND wet mask at 21.18 ft?"
)
TEMPLATE_CRS = 5070
TEMPLATE_RES_M = 30.0
WET_NODATA = 255
WET_DRY = 0
WET_WET = 1
MAX_FIGURES = 2
NORA_DEFAULT = Path.home() / "white_river_stage_inundation"
NORA_CREST_WET = (
    NORA_DEFAULT / "logs" / "nora_live" / "rasters" / "wet_crest_2026-08-15.tif"
)
LOCKED_NORA_V1_PNG_SHA256 = (
    "cab5c15439bb322b5116ae158f58c7777acd5634db7e351bdd47dd6f68d720ab"
)
LOCKED_CREST_WET_SHA256 = (
    "f8f0a00f2470787c064c64e8d49f46cb5cbfb1a55badd21de7ea1ea1514eb09c"
)
LOCKED_WINDOW_SHA256 = (
    "be00bbfb15ea71a9865ed2f197f392484fdbd6fc371daac2976f49e5fa4459ec"
)
USER_AGENT = "MartialSystemsResearch/white_river_hwm_crest"
STN_IN_URL = (
    "https://stn.wim.usgs.gov/STNServices/HWMs/FilteredHWMs.json?States=IN"
)
STN_MARION_URL = (
    "https://stn.wim.usgs.gov/STNServices/HWMs/FilteredHWMs.json"
    "?States=IN&Counties=Marion"
)
SCIENCEBASE_URL = (
    "https://www.sciencebase.gov/catalog/items"
    "?q=high-water%20mark%20Indiana%202026&format=json&max=10"
)
FIXTURE_WEST = 830_790.0
FIXTURE_NORTH = 1_926_570.0
FIXTURE_ROWS = 16
FIXTURE_COLS = 16
