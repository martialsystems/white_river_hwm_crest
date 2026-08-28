# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from hwmforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    n = int(state.get("n_figures") or 0)
    v = [] if 1 <= n <= 2 else ["figure_cap"]
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="hwm.figure_cap", evaluate=_evaluate, extra=["n_figures"])
