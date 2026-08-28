# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from hwmforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [] if state.get("sibling_sha_ok") else ["sibling_sha_mismatch"]
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="hwm.sibling_sha", evaluate=_evaluate, extra=["sibling_sha_ok"])
