#!/usr/bin/env python3
"""
Equilibrium shoreline built from three arcs:
  - left lateral arc (shoreline -> inner toe T1 -> bay point S0)
  - central arc (T2 -> apex S -> T3)
  - right lateral arc (T4 -> bay point S1 -> shoreline)

Inputs are read from examples/configs/hsu_tombolo.yaml.
Computation uses helper utilities in pyCoastal.tools.morphodynamics.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Prefer local checkout
THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from pyCoastal.io import read_data
from pyCoastal.tools import (
    build_tombolo_arcs,
    accretion_metrics,
    two_point_arc,
    circle_through_points,
)


def main():
    cfg = read_data(os.path.join(THIS_DIR, "configs", "equilibrium_shoreline.yaml"))

    Lshore = cfg["geometry"]["Lshore"]
    Gb = cfg["geometry"]["Gb"]
    Lb1 = cfg["geometry"]["Lb1"]
    Lb2 = cfg["geometry"]["Lb2"]
    yb = cfg["geometry"]["Yi"]
    n_pts = cfg["numerics"]["n_points"]
    sag_side_factor = cfg["numerics"]["sag_side_factor"]


    if Gb > 0 and yb / Gb > 1.4:
        msg = "Breakwater is too far from shore; no equilibrium profile will be reached. set a lower Yi or increase Gb."
        print(msg)
        return

    x_eq, y_eq, geom = build_tombolo_arcs(
        Lshore=Lshore,
        Gb=Gb,
        Lb1=Lb1,
        Lb2=Lb2,
        yb=yb,
        n_pts=n_pts,
        sag_side_factor=sag_side_factor,
    )

    # Rebuild individual arcs for overlap highlighting
    sag_side = sag_side_factor * geom["Ye"]
    xL, yL = two_point_arc(geom["S0"], geom["T1"], sag_side, n=n_pts)
    xCen, yCen = circle_through_points(geom["T2"], geom["S"], geom["T3"], n=n_pts)
    xR, yR = two_point_arc(geom["T4"], geom["S1"], sag_side, n=n_pts)

    retreat_val, acc_pct = accretion_metrics(x_eq, y_eq, geom)

    fig, ax = plt.subplots(figsize=(12, 4.5), dpi=200)

    y_min = min(0.0, y_eq.min()) - 0.1 * abs(y_eq.min() - y_eq.max())
    y_max = max(y_eq.max(), geom["Yi"] + 0.5 * max(Lb1, Lb2))
    ax.set_ylim(y_min, y_max)
    ax.fill_between(x_eq, y_min, y_eq, color="#eed9b7", alpha=0.6, zorder=0.4)  # sand
    ax.fill_between(x_eq, y_eq, y_max, color="#c2e0ff", alpha=1, zorder=0.5)  # water
    ax.fill_between([geom["S0"][0], geom["S1"][0]], y_min, 0.0, color="#d6c09c", alpha=0.5, zorder=1.8)

    # Overlap fill on top
    def overlap_fill(ax, x1, y1, x2, y2, color="#c2e0ff", alpha=1, zorder=6):
        idx1 = np.argsort(x1); idx2 = np.argsort(x2)
        x1s, y1s = np.array(x1)[idx1], np.array(y1)[idx1]
        x2s, y2s = np.array(x2)[idx2], np.array(y2)[idx2]
        xmin, xmax = max(x1s.min(), x2s.min()), min(x1s.max(), x2s.max())
        if xmax <= xmin:
            return
        xs = np.linspace(xmin, xmax, 300)
        y1i = np.interp(xs, x1s, y1s)
        y2i = np.interp(xs, x2s, y2s)
        ax.fill_between(xs, np.minimum(y1i, y2i), np.maximum(y1i, y2i),
                        color=color, alpha=alpha, zorder=zorder)


    overlap_fill(ax, xL, yL, xCen, yCen)
    overlap_fill(ax, xCen, yCen, xR, yR)

    # Initial shoreline y=0
    ax.hlines(0.0, geom["S0"][0], geom["S1"][0], linestyles="--", linewidth=0.5, colors="C0",
              label="Original Shoreline", zorder=2)

    # Equilibrium shoreline (arc)
    ax.plot(x_eq, y_eq, "r--", linewidth=0.2, label="Equilibrium shoreline", zorder=3)

    # Breakwaters on top
    for x_b, Lb in [(geom["x_b1"], Lb1), (geom["x_b2"], Lb2)]:
        x0 = x_b - 0.5 * Lb
        y0_rect = geom["Yi"] - 2.0
        rect = plt.Rectangle((x0, y0_rect), Lb, 4.0,
                             facecolor="tan", edgecolor="k", zorder=5)
        ax.add_patch(rect)

    ax.set_xlim(geom["S0"][0], geom["S1"][0])
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Equilibrium shoreline")
    ax.legend(loc="upper right")

    # Dimensional annotations
    span = y_max - y_min
    y_annot = geom["Yi"] + 0.08 * span

    # Breakwater lengths
    bw1_x0, bw1_x1 = geom["x_b1"] - 0.5 * Lb1, geom["x_b1"] + 0.5 * Lb1
    bw2_x0, bw2_x1 = geom["x_b2"] - 0.5 * Lb2, geom["x_b2"] + 0.5 * Lb2
    ax.annotate("", xy=(bw1_x1, y_annot), xytext=(bw1_x0, y_annot),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=0.8))
    ax.text(0.5 * (bw1_x0 + bw1_x1), y_annot + 0.01 * span, f"Lb1 = {Lb1:.1f} m",
            ha="center", va="bottom", fontsize=8, color="k")
    ax.annotate("", xy=(bw2_x1, y_annot), xytext=(bw2_x0, y_annot),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=0.8))
    ax.text(0.5 * (bw2_x0 + bw2_x1), y_annot + 0.01 * span, f"Lb2 = {Lb2:.1f} m",
            ha="center", va="bottom", fontsize=8, color="k")

    # Gap between inner toes
    y_gap = y_annot + 0.06 * span
    gb_start = geom["x_b1"] + 0.5 * Lb1
    gb_end = geom["x_b2"] - 0.5 * Lb2
    ax.annotate("", xy=(gb_end, y_gap), xytext=(gb_start, y_gap),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=0.8))
    ax.text(0.5 * (gb_start + gb_end), y_gap + 0.01 * span,
            f"Gb = {Gb:.1f} m", ha="center", va="bottom", fontsize=8, color="k")

    # Yi at left breakwater center
    ax.annotate("", xy=(geom["x_b1"], geom["Yi"]), xytext=(geom["x_b1"], 0.0),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=0.8))
    ax.text(geom["x_b1"], 0.5 * geom["Yi"], f"Yi = {geom['Yi']:.1f} m",
            ha="right", va="center", fontsize=8, color="k")

    # Ye at apex
    ax.annotate("", xy=(geom["S"][0], geom["Yi"]), xytext=(geom["S"][0], geom["S"][1]),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=0.8))
    ax.text(geom["S"][0], geom["S"][1] + 0.5 * (geom["Yi"] - geom["S"][1]),
            f"Ye = {geom['Ye']:.1f} m", ha="left", va="center", fontsize=8, color="k")

    ax.text(
        0.02, 0.97,
        f"Central retreat = {retreat_val:.2f} m\nAccretion = {acc_pct:.1f}%",
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8)
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
