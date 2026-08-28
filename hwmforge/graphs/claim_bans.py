# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from hwmforge.graphs._common import binary_graph

_FLAGS = ("p_as_forecast", "hand_as_firm", "tests_fema", "tests_sir_2011")


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [k for k in _FLAGS if state.get(k)]
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="hwm.claim_bans", evaluate=_evaluate, extra=list(_FLAGS))
