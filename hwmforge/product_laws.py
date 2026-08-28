# Copyright (c) 2026 Martial Systems LLC
"""Five refuse laws. Verify-before-done is the finish gate."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from hwmforge.graphs.claim_bans import build_graph as claim_bans
    from hwmforge.graphs.fetch_stop import build_graph as fetch_stop
    from hwmforge.graphs.figure_cap import build_graph as figure_cap
    from hwmforge.graphs.sibling_sha import build_graph as sibling_sha
    from hwmforge.graphs.stage_gate import build_graph as stage_gate

    return [
        {
            "id": "hwm.stage_gate",
            "build": stage_gate,
            "state": {
                "current_stage": "0",
                "target_stage": "0",
                "sibling_sha_ok": True,
                "fetched_ok": False,
                "figures_ok": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "hwm.sibling_sha",
            "build": sibling_sha,
            "state": {"sibling_sha_ok": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "hwm.fetch_stop",
            "build": fetch_stop,
            "state": {"official_ok": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "hwm.figure_cap",
            "build": figure_cap,
            "state": {"n_figures": 2},
            "allow_decisions": ["allow"],
        },
        {
            "id": "hwm.claim_bans",
            "build": claim_bans,
            "state": {
                "p_as_forecast": False,
                "hand_as_firm": False,
                "tests_fema": False,
                "tests_sir_2011": False,
            },
            "allow_decisions": ["allow"],
        },
    ]
