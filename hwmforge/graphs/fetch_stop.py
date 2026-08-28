# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from hwmforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [] if state.get("official_ok") else ["official_hwm_empty_or_404"]
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="hwm.fetch_stop", evaluate=_evaluate, extra=["official_ok"])
