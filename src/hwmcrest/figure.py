# Copyright (c) 2026 Martial Systems LLC
"""Two figures max: map of points on the crest wet mask, and a hit/miss bar."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from hwmcrest.claims import require_clean
from hwmcrest.config import GAGE_ID, MAX_FIGURES, WET_WET
from hwmcrest.errors import FigureCapError, GateError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_map(
    dest: Path,
    *,
    wet: np.ndarray,
    scored: list[dict[str, Any]],
    title: str,
    subtitle: str,
) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    show = np.asarray(wet, dtype=float)
    show[show == 255] = np.nan
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    ax.imshow(show, origin="upper", cmap="Blues", vmin=0, vmax=1)
    colors = {"hit": "#1b9e77", "miss": "#d95f02", "out": "#7570b3"}
    for rec in scored:
        ax.scatter(
            rec["col"],
            rec["row"],
            c=colors.get(rec["status"], "#333333"),
            s=36,
            edgecolors="white",
            linewidths=0.4,
            zorder=3,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=10)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.10, top=0.90)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return dest


def write_counts(dest: Path, *, table: dict[str, Any], title: str) -> Path:
    require_clean(title, source="fig2_title")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = ["hit", "miss", "out of window"]
    vals = [int(table["n_hit"]), int(table["n_miss"]), int(table["n_out"])]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.bar(labels, vals, color=["#1b9e77", "#d95f02", "#7570b3"])
    ax.set_ylabel("HWM points")
    ax.set_title(title, fontsize=10)
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, wet: np.ndarray, table: dict[str, Any]) -> list[Path]:
    if wet.size == wet.shape[0] * wet.shape[1] and np.all(np.asarray(wet) != 255):
        # HUC-wide check: all cells comparable
        if int((np.asarray(wet) != 255).sum()) == wet.size:
            raise GateError("figure refuses a HUC-wide mask")
    paths = [
        write_map(
            log_dir / "hwm_on_crest.png",
            wet=wet,
            scored=table["points"],
            title=f"{GAGE_ID} crest 21.18 ft: HWM points on HAND wet mask",
            subtitle="Green: hit. Orange: miss (dry in window). Purple: outside the Nora window.",
        ),
        write_counts(
            log_dir / "hwm_counts.png",
            table=table,
            title="August 2026 HWM points vs Nora HAND at 21.18 ft",
        ),
    ]
    _cap(len(paths))
    return paths
