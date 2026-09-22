"""
Rubble-mound breakwater design check.

Sizes armour with Van der Meer, sets the crest from an EurOtop overtopping
limit, and plots the two design curves an engineer actually reads: stone size
against slope, and overtopping against crest freeboard.

Run from the repository root:

    python examples/breakwater_design.py
"""

import matplotlib
import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.structures import (
    ROUGHNESS_FACTORS,
    TOLERABLE_DISCHARGE,
    DesignConditions,
    assess_overtopping,
    design_rubble_mound,
    overtopping_sloped,
    rock_armour_hudson,
    rock_armour_vandermeer,
)

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial"]

# --- design condition ------------------------------------------------------
conditions = DesignConditions.from_peak_period(
    Hm0=4.0,                   # 1 in 100 year significant wave height at the toe
    Tp=11.0,
    depth=12.0,
    storm_duration=6 * 3600.0,
)

design = design_rubble_mound(
    conditions,
    cot_alpha=2.0,
    armour="rock_two_layer_permeable",
    damage=2.0,                # start of damage
    permeability=0.4,          # permeable core
    tolerable_use="trained_staff",
)
print(design.summary())

print("\nTolerability of the mean discharge:")
for name, info in assess_overtopping(design.q_mean).items():
    mark = "ok " if info["acceptable"] else "NO "
    print(f"  {mark} {info['limit']:>6.2f} l/s/m  {name}")

# --- curve 1: stone size against slope -------------------------------------
cots = np.linspace(1.5, 4.0, 40)
vdm, hud, regimes = [], [], []
for cot in cots:
    v = rock_armour_vandermeer(conditions, cot)
    vdm.append(v["Dn50"])
    regimes.append(v["regime"])
    hud.append(rock_armour_hudson(conditions, cot)["Dn50"])

# --- curve 2: overtopping against freeboard --------------------------------
freeboards = np.linspace(1.5, 9.0, 60)
gamma_f = ROUGHNESS_FACTORS["rock_two_layer_permeable"]
q = [overtopping_sloped(conditions, Rc, 2.0, gamma_f=gamma_f)["q"] for Rc in freeboards]

# --- figure ----------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

plunging = [c for c, r in zip(cots, regimes) if r == "plunging"]
ax1.plot(cots, vdm, lw=2.0, label="Van der Meer (1988)")
ax1.plot(cots, hud, lw=1.6, ls="--", label="Hudson (SPM 1984), $K_D$ = 4")
if plunging and len(plunging) < len(cots):
    ax1.axvline(max(plunging), color="0.5", ls=":", lw=1.2)
    ax1.annotate(
        "plunging / surging",
        xy=(max(plunging), max(vdm)),
        xytext=(4, -6), textcoords="offset points", fontsize=8, color="0.35",
        rotation=90, va="top",
    )
ax1.plot(design.cot_alpha, design.Dn50, "o", ms=8, mfc="w", mec="k", mew=1.5, zorder=5)
ax1.annotate(
    f"design\n{design.Dn50:.2f} m, {design.M50 / 1000:.1f} t",
    xy=(design.cot_alpha, design.Dn50), xytext=(12, 10),
    textcoords="offset points", fontsize=9,
    arrowprops=dict(arrowstyle="->", color="0.3"),
)
ax1.set_xlabel(r"Slope, cot $\alpha$")
ax1.set_ylabel("Nominal stone diameter $D_{n50}$ (m)")
ax1.legend(frameon=False, fontsize=9)
ax1.grid(True, which="both", alpha=0.3)
ax1.minorticks_on()

ax2.semilogy(freeboards, q, lw=2.0, color="#1b6fa0")
for name in ("pedestrians_unaware", "trained_staff", "vehicles_low_speed"):
    limit, _ = TOLERABLE_DISCHARGE[name]
    ax2.axhline(limit, color="0.55", ls=":", lw=1.1)
    ax2.annotate(
        f"{name.replace('_', ' ')}  {limit:g}",
        xy=(freeboards[-1], limit), xytext=(-4, 3),
        textcoords="offset points", ha="right", fontsize=7.5, color="0.35",
    )
ax2.plot(design.crest_freeboard, design.q_mean, "o", ms=8, mfc="w", mec="k", mew=1.5, zorder=5)
ax2.annotate(
    f"design crest\n$R_c$ = {design.crest_freeboard:.2f} m",
    xy=(design.crest_freeboard, design.q_mean), xytext=(14, 14),
    textcoords="offset points", fontsize=9,
    arrowprops=dict(arrowstyle="->", color="0.3"),
)
ax2.set_xlabel("Crest freeboard $R_c$ (m)")
ax2.set_ylabel("Mean overtopping discharge $q$ (l/s per m)")
ax2.set_ylim(1e-4, 1e3)
ax2.grid(True, which="both", alpha=0.3)

panel_labels([ax1, ax2])
fig.tight_layout()
fig.savefig("media/breakwater_design.png", dpi=600)
print("\nWrote media/breakwater_design.png")

# --- the same design, issued as a drawing ---------------------------------
# The section is generated from the design object, so the armour drawn on the
# paper is the armour the stability calculation sized.
from pyCoastal.applications.sections import rubble_mound_section, rubble_mound_sheet
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

SWL = 1.10          # m CD, design still water level
SEABED = -10.9      # m CD, giving the 12.0 m depth the design was run at

section = rubble_mound_section(design, still_water_level=SWL,
                               seabed_level=SEABED)
section.save("media/breakwater_section.png")

sheet = rubble_mound_sheet(
    design,
    still_water_level=SWL,
    seabed_level=SEABED,
    project="Harbour protection works",
    title="Breakwater typical sections",
    client="Example Port Authority",
    size="A3",
    file="examples/breakwater_design.py",
)
sheet.save("media/breakwater_sheet.png")
sheet.to_dxf("media/breakwater_section.dxf")
print("Wrote media/breakwater_section.png, media/breakwater_sheet.png "
      "and media/breakwater_section.dxf")
