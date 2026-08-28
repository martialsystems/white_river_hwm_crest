# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from hwmforge.graphs._common import binary_graph

_ORDER = ("0", "A", "B", "C")


def _rank(s: Any) -> int:
    try:
        return _ORDER.index(str(s or "0"))
    except ValueError:
        return -1


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    cr, tr = _rank(state.get("current_stage")), _rank(state.get("target_stage"))
    if cr < 0 or tr < 0:
        v.append("unknown_stage")
    if tr > cr + 1:
        v.append("stage_skip")
    if tr >= _rank("A") and not state.get("sibling_sha_ok"):
        v.append("advance_without_sibling_sha")
    if tr >= _rank("B") and not state.get("fetched_ok"):
        v.append("score_without_official_hwm")
    if tr >= _rank("C") and not state.get("figures_ok"):
        v.append("stop_without_figures")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="hwm.stage_gate",
        evaluate=_evaluate,
        extra=["current_stage", "target_stage", "sibling_sha_ok", "fetched_ok", "figures_ok"],
    )
