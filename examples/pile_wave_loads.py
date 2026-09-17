"""
Wave loads on a monopile: where the load is, and when it peaks.

Computes the Morison load distribution on an offshore wind monopile,
sweeps the wave phase for the worst base shear and the worst overturning
moment, and shows why they do not happen at the same instant.

The headline result is a trap worth knowing about. A large monopile is
inertia dominated, so the load follows the fluid acceleration, which peaks a
quarter cycle before the crest arrives. Evaluating the load under the crest
because that is where the water is highest understates the overturning
moment substantially.

Run from the repository root:

    python examples/pile_wave_loads.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from pyCoastal.applications.piles import (
    design_monopile,
    drag_inertia_coefficients,
    keulegan_carpenter,
    morison_pile_load,
    scour_depth_pile,
)
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

# --- the structure and the design wave ------------------------------------
DIAMETER = 8.0          # monopile outer diameter
DEPTH = 30.0            # water depth
H = 12.0                # design wave height
T = 13.0                # period

result = design_monopile(DIAMETER, H, T, DEPTH, rough=True)
worst, crest, sweep, scour = (result["load"], result["crest_load"],
                              result["sweep"], result["scour"])

print(worst.summary())
print(f"\nAt the crest phase        {crest.force / 1e3:,.0f} kN, "
      f"{crest.moment / 1e6:,.1f} MNm")
print(f"At the worst phase        {worst.force / 1e3:,.0f} kN, "
      f"{worst.moment / 1e6:,.1f} MNm")
print(f"Designing on the crest would miss "
      f"{100 * result['crest_underestimate']:.0f}% of the moment")
print(f"\nMax base shear at         "
      f"{math.degrees(sweep['phase_of_max_force']):.0f} degrees")
print(f"Max mudline moment at     "
      f"{math.degrees(sweep['phase_of_max_moment']):.0f} degrees")

print(f"\nScour                     {scour['depth']:.2f} m "
      f"({scour['ratio']:.2f} D) at KC = {scour['KC']:.1f}")
current = scour_depth_pile(DIAMETER, scour["KC"], current_only=True)
print(f"   under a steady current: {current['depth']:.2f} m "
      f"(1.3 D, standard deviation {current['standard_deviation']:.2f} m)")
print("   waves alone barely scour a pile this large, because KC is small; "
      "current is what governs.")

# --- how the load splits with pile size -----------------------------------
print("\nHow the load splits with pile diameter")
print("   D (m)    KC    regime              inertia share   moment (MNm)")
for diameter in (1.0, 2.0, 4.0, 8.0, 12.0):
    KC = keulegan_carpenter(H, T, DEPTH, diameter)
    coefficients = drag_inertia_coefficients(KC)
    case = design_monopile(diameter, H, T, DEPTH)["load"]
    flag = "  diffracts" if case.diffraction_ratio > 0.2 else ""
    print(f"   {diameter:5.1f}  {KC:5.1f}   {coefficients['regime']:<18}"
          f"{100 * case.inertia_fraction:6.0f}%      "
          f"{case.moment / 1e6:8.1f}{flag}")

# --- figure ----------------------------------------------------------------
fig = plt.figure(figsize=(14.0, 8.0))
gs = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.0, 1.35],
                      hspace=0.34, wspace=0.30)

# Load profile at the worst phase, drag and inertia separated. Only the wet
# part is drawn: the profile is zero above the instantaneous surface, and a
# line running back to zero there reads as a spike rather than as nothing.
wet = worst.z <= worst.eta
ax = fig.add_subplot(gs[:, 0])
ax.fill_betweenx(worst.z[wet], 0, worst.inertia[wet] / 1e3, color="#9fc4d6",
                 alpha=0.75, label="inertia")
ax.fill_betweenx(worst.z[wet], 0, worst.drag[wet] / 1e3, color="#c47f1a",
                 alpha=0.6, label="drag")
ax.plot(worst.total[wet] / 1e3, worst.z[wet], color="#0b3554", lw=1.9,
        label="total")
ax.axhline(0.0, color="#4d7f97", lw=1.0)
ax.axhline(worst.eta, color="#8a2f24", lw=1.2, ls="--",
           label=f"surface {worst.eta:+.2f} m")
ax.axhline(-DEPTH, color="#6d6243", lw=1.6)
ax.set_xlabel("load (kN/m)")
ax.set_ylabel("elevation (m)")
ax.set_title(f"Load profile at {math.degrees(worst.phase):.0f} degrees")
ax.annotate(f"{worst.moment / 1e6:.0f} MNm", xy=(0.95, 0.06),
            xycoords="axes fraction", ha="right", fontsize=9,
            fontweight="bold")
ax.legend(loc="lower right", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

# The same at the crest. Both x axes are shared, because two panels drawn to
# their own scales would make a load four times smaller look comparable.
wet_crest = crest.z <= crest.eta
ax = fig.add_subplot(gs[:, 1], sharey=ax, sharex=ax)
ax.fill_betweenx(crest.z[wet_crest], 0, crest.inertia[wet_crest] / 1e3,
                 color="#9fc4d6", alpha=0.75)
ax.fill_betweenx(crest.z[wet_crest], 0, crest.drag[wet_crest] / 1e3,
                 color="#c47f1a", alpha=0.6)
ax.plot(crest.total[wet_crest] / 1e3, crest.z[wet_crest], color="#0b3554",
        lw=1.9)
ax.axhline(0.0, color="#4d7f97", lw=1.0)
ax.axhline(crest.eta, color="#8a2f24", lw=1.2, ls="--",
           label=f"crest {crest.eta:+.2f} m")
ax.axhline(-DEPTH, color="#6d6243", lw=1.6)
ax.set_xlabel("load (kN/m)")
ax.set_title("Load profile under the crest")
ax.annotate(f"{crest.moment / 1e6:.0f} MNm", xy=(0.95, 0.06),
            xycoords="axes fraction", ha="right", fontsize=9,
            fontweight="bold")
ax.legend(loc="lower right", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

# Phase sweep.
ax = fig.add_subplot(gs[0, 2])
degrees = np.degrees(sweep["phase"])
ax.plot(degrees, sweep["force"] / 1e3, color="#0b3554", lw=1.8,
        label="base shear")
ax.axvline(math.degrees(sweep["phase_of_max_force"]), color="#0b3554",
           lw=1.0, ls=":")
ax.set_ylabel("base shear (kN)")
ax.set_title("Load through the wave cycle")
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()
ax.legend(loc="upper right", fontsize=8)

ax2 = fig.add_subplot(gs[1, 2], sharex=ax)
ax2.plot(degrees, sweep["moment"] / 1e6, color="#8a2f24", lw=1.8,
         label="mudline moment")
ax2.axvline(math.degrees(sweep["phase_of_max_moment"]), color="#8a2f24",
            lw=1.0, ls=":")
ax2.plot([0.0], [crest.moment / 1e6], "o", ms=7, markerfacecolor="white",
         markeredgecolor="#8a2f24", markeredgewidth=1.3,
         label="crest phase")
ax2.plot([math.degrees(sweep["phase_of_max_moment"])],
         [worst.moment / 1e6], "*", ms=15, color="#c47f1a",
         markeredgecolor="#5a3a05", markeredgewidth=0.6, label="worst phase")
ax2.annotate(
    f"{100 * result['crest_underestimate']:.0f}% larger\nthan at the crest",
    xy=(math.degrees(sweep["phase_of_max_moment"]), worst.moment / 1e6),
    xytext=(30, -40), textcoords="offset points", fontsize=8.5,
    arrowprops=dict(arrowstyle="->", color="#1a1a1a", lw=0.8),
)
ax2.set_xlabel("wave phase (degrees, crest at 0)")
ax2.set_ylabel("mudline moment (MNm)")
ax2.set_xlim(0, 360)
ax2.set_xticks(range(0, 361, 90))
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()
ax2.legend(loc="upper right", fontsize=8)

fig.suptitle(
    f"Monopile {DIAMETER:.0f} m in {DEPTH:.0f} m: H = {H:.0f} m, T = {T:.0f} s. "
    f"{worst.force / 1e3:,.0f} kN and {worst.moment / 1e6:,.0f} MNm, "
    f"{100 * worst.inertia_fraction:.0f}% inertia",
    y=0.975, fontsize=12, fontweight="bold",
)
fig.savefig("media/pile_wave_loads.png", dpi=600, bbox_inches="tight")
print("\nWrote media/pile_wave_loads.png")
