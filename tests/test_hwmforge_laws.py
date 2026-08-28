# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hwmforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from hwmforge.gate import require_claims, require_fetch, require_figures, require_sibling, require_stage
from hwmforge.product_laws import laws


def test_stage_zero_and_skip() -> None:
    require_stage(current_stage="0", target_stage="0", sibling_sha_ok=True, thread_id="t0")
    with pytest.raises(LawBlockedError):
        require_stage(current_stage="0", target_stage="B", sibling_sha_ok=True, thread_id="tskip")


def test_fetch_and_figures() -> None:
    require_fetch(official_ok=True, thread_id="tf.ok")
    with pytest.raises(LawBlockedError):
        require_fetch(official_ok=False, thread_id="tf.bad")
    require_figures(n_figures=2, thread_id="tfig.ok")
    with pytest.raises(LawBlockedError):
        require_figures(n_figures=3, thread_id="tfig.bad")


def test_sibling_and_claims() -> None:
    require_sibling(sibling_sha_ok=True, thread_id="ts.ok")
    with pytest.raises(LawBlockedError):
        require_sibling(sibling_sha_ok=False, thread_id="ts.bad")
    require_claims(thread_id="tc.ok")
    with pytest.raises(LawBlockedError):
        require_claims(tests_fema=True, thread_id="tc.fema")


def test_registry() -> None:
    assert {row["id"] for row in laws()} == {
        "hwm.stage_gate",
        "hwm.sibling_sha",
        "hwm.fetch_stop",
        "hwm.figure_cap",
        "hwm.claim_bans",
    }
