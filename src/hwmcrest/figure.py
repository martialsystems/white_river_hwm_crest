# Copyright (c) 2026 Martial Systems LLC
"""Two figures max: map of points on the crest wet mask, and a hit/miss bar."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from hwmcrest.claims import require_clean
from hwmcrest.config import GAGE_ID, MAX_FIGURES
from hwmcrest.errors import FigureCapError, GateError

FIG1_FIXTURE_TITLE = (
    "FIXTURE / not live / synthetic: four HWM points on a tiny crest mask"
)
FIG1_FIXTURE_SUB = "Not the August 2026 result."
FIG2_FIXTURE_TITLE = "Fixture path counts (synthetic n=4). Official layer empty."
FIG2_FIXTURE_FOOTER = "Not the August 2026 result."
FIG1_LIVE_TITLE = f"{GAGE_ID} crest 21.18 ft: HWM points on HAND wet mask"
FIG1_LIVE_SUB = (
    "Green: hit. Orange: miss (dry in window). Purple: outside the Nora window."
)
FIG2_LIVE_TITLE = "HWM points vs Nora HAND at 21.18 ft"


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def map_copy(*, fixture: bool) -> tuple[str, str]:
    if fixture:
        title, sub = FIG1_FIXTURE_TITLE, FIG1_FIXTURE_SUB
    else:
        title, sub = FIG1_LIVE_TITLE, FIG1_LIVE_SUB
    require_clean(title, source="fig1_title")
    require_clean(sub, source="fig1_sub")
    return title, sub


def counts_copy(*, fixture: bool) -> tuple[str, str]:
    if fixture:
        title, footer = FIG2_FIXTURE_TITLE, FIG2_FIXTURE_FOOTER
    else:
        title, footer = FIG2_LIVE_TITLE, ""
    require_clean(title, source="fig2_title")
    if footer:
        require_clean(footer, source="fig2_footer")
    return title, footer


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
    from matplotlib.patches import Patch

    legend_labels = ("hit", "miss (dry in window)", "out of window")
    for lab in legend_labels:
        require_clean(lab, source="fig1_legend")
    ax.legend(
        handles=[
            Patch(facecolor="#1b9e77", edgecolor="white", label=legend_labels[0]),
            Patch(facecolor="#d95f02", edgecolor="white", label=legend_labels[1]),
            Patch(facecolor="#7570b3", edgecolor="white", label=legend_labels[2]),
        ],
        loc="lower right",
        fontsize=7,
        framealpha=0.92,
    )
    fig.text(0.5, 0.03, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.12, top=0.90)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return dest


def write_counts(
    dest: Path, *, table: dict[str, Any], title: str, footer: str = ""
) -> Path:
    require_clean(title, source="fig2_title")
    if footer:
        require_clean(footer, source="fig2_footer")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = ["hit", "miss", "out of window"]
    vals = [int(table["n_hit"]), int(table["n_miss"]), int(table["n_out"])]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(labels, vals, color=["#1b9e77", "#d95f02", "#7570b3"])
    ax.set_ylabel("HWM points")
    ax.set_title(title, fontsize=10)
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=9)
    if footer:
        fig.text(0.5, 0.03, footer, ha="center", fontsize=8)
        fig.subplots_adjust(bottom=0.18, top=0.88)
    else:
        fig.tight_layout()
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return dest


def write_two(
    log_dir: Path, *, wet: np.ndarray, table: dict[str, Any], fixture: bool = False
) -> list[Path]:
    if wet.size == wet.shape[0] * wet.shape[1] and np.all(np.asarray(wet) != 255):
        # HUC-wide check: all cells comparable
        if int((np.asarray(wet) != 255).sum()) == wet.size:
            raise GateError("figure refuses a HUC-wide mask")
    t1, s1 = map_copy(fixture=fixture)
    t2, f2 = counts_copy(fixture=fixture)
    paths = [
        write_map(
            log_dir / "hwm_on_crest.png",
            wet=wet,
            scored=table["points"],
            title=t1,
            subtitle=s1,
        ),
        write_counts(
            log_dir / "hwm_counts.png",
            table=table,
            title=t2,
            footer=f2,
        ),
    ]
    _cap(len(paths))
    return paths
