# Copyright (c) 2026 Martial Systems LLC
"""Call sites for refuse laws."""

from __future__ import annotations

from typing import Any

from hwmforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from hwmforge.graphs.claim_bans import build_graph as build_claim_bans
from hwmforge.graphs.fetch_stop import build_graph as build_fetch
from hwmforge.graphs.figure_cap import build_graph as build_figs
from hwmforge.graphs.sibling_sha import build_graph as build_sibling
from hwmforge.graphs.stage_gate import build_graph as build_stage


def require_stage(**state: Any) -> None:
    thread_id = str(state.pop("thread_id", "hwm_stage"))
    base = {
        "current_stage": "0",
        "target_stage": "0",
        "sibling_sha_ok": False,
        "fetched_ok": False,
        "figures_ok": False,
    }
    base.update(state)
    require_law(
        build_stage(),
        base,
        allow_decisions=["allow"],
        law_id="hwm.stage_gate",
        thread_id=thread_id,
        raise_error=True,
    )


def require_sibling(*, sibling_sha_ok: bool, thread_id: str = "hwm_sha") -> None:
    require_law(
        build_sibling(),
        {"sibling_sha_ok": sibling_sha_ok},
        allow_decisions=["allow"],
        law_id="hwm.sibling_sha",
        thread_id=thread_id,
        raise_error=True,
    )


def require_fetch(*, official_ok: bool, thread_id: str = "hwm_fetch") -> None:
    require_law(
        build_fetch(),
        {"official_ok": official_ok},
        allow_decisions=["allow"],
        law_id="hwm.fetch_stop",
        thread_id=thread_id,
        raise_error=True,
    )


def require_figures(*, n_figures: int, thread_id: str = "hwm_figs") -> None:
    require_law(
        build_figs(),
        {"n_figures": n_figures},
        allow_decisions=["allow"],
        law_id="hwm.figure_cap",
        thread_id=thread_id,
        raise_error=True,
    )


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "hwm_claims"))
    state = {
        "p_as_forecast": False,
        "hand_as_firm": False,
        "tests_fema": False,
        "tests_sir_2011": False,
    }
    state.update(flags)
    require_law(
        build_claim_bans(),
        state,
        allow_decisions=["allow"],
        law_id="hwm.claim_bans",
        thread_id=thread_id,
        raise_error=True,
    )
