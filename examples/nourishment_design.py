"""
Beach nourishment design study.

Evolves a beach fill with the one-line model, compares it against the
Pelnard-Considere analytical solution, and reports design life and a
renourishment schedule over a 30-year planning horizon.

Run from the repository root:

    python examples/nourishment_design.py
"""

import matplotlib
import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.nourishment import (
    SECONDS_PER_YEAR,
    NourishmentDesign,
    WaveClimate,
    longshore_diffusivity,
    pelnard_considere,
    renourishment_schedule,
    simulate_nourishment,
)

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial"]

# --- design case -----------------------------------------------------------
design = NourishmentDesign(
    length=3000.0,      # m of full-width fill
    berm_width=30.0,    # m of shoreline advance
    taper=200.0,        # m of linear taper at each end
    D=8.0,              # m depth of closure
    B=2.0,              # m berm height
    porosity=0.4,
)
climate = WaveClimate(Hb=1.0, T=8.0, alpha0=0.0)

eps = longshore_diffusivity(climate, design)
print(f"Placed volume        : {design.placed_volume:,.0f} m3")
print(f"Active profile height: {design.active_height:.1f} m")
print(f"Diffusivity          : {eps:.4f} m2/s  ({eps * SECONDS_PER_YEAR:,.0f} m2/yr)")

# --- evolve ----------------------------------------------------------------
result = simulate_nourishment(
    design, climate, duration=20.0 * SECONDS_PER_YEAR, dx=20.0, n_outputs=41
)

print(f"\n{'year':>6}{'retained %':>12}{'berm width (m)':>16}")
for yr, frac, width in list(
    zip(result.times_years, result.retained_fraction, result.berm_width)
)[::8]:
    print(f"{yr:>6.1f}{100 * frac:>12.1f}{width:>16.1f}")

life = result.design_life(threshold=0.5)
print(f"\nDesign life (50% retained): {life / SECONDS_PER_YEAR:.1f} yr")

plan = renourishment_schedule(
    design, climate, horizon=30.0 * SECONDS_PER_YEAR, threshold=0.5,
    dx=20.0, n_outputs=61,
)
print(f"Renourishment interval    : {plan['interval'] / SECONDS_PER_YEAR:.1f} yr")
print(f"Renourishments in 30 yr   : {plan['n_renourishments']}")
print(f"Total sand over 30 yr     : {plan['total_volume']:,.0f} m3")

# --- figure ----------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

for i in (0, 4, 10, 20, 40):
    yr = result.times_years[i]
    ax1.plot(result.x / 1000.0, result.planforms[i], lw=1.6, label=f"{yr:.0f} yr")

# The analytical solution is for a bare rectangle of length `design.length`,
# so it carries slightly less sand than the simulated fill, which also has a
# taper at each end. The small offset between the two curves is that volume
# difference, not solver error. test_applications_nourishment.py compares the
# two with the taper removed.
analytic = pelnard_considere(result.x, result.times[-1], result.design, climate)
ax1.plot(
    result.x / 1000.0, analytic, "k--", lw=1.2,
    label=f"Pelnard-Considere, {result.times_years[-1]:.0f} yr",
)
ax1.set_xlabel("Alongshore distance (km)")
ax1.set_ylabel("Shoreline offset (m)")
ax1.legend(frameon=False, fontsize=9)
ax1.grid(True, which="both", alpha=0.3)
ax1.minorticks_on()

ax2.plot(result.times_years, 100 * result.retained_fraction, lw=1.8)
ax2.axhline(50, color="0.4", ls=":", lw=1.2)
if np.isfinite(life):
    ax2.axvline(life / SECONDS_PER_YEAR, color="0.4", ls=":", lw=1.2)
    ax2.annotate(
        f"design life {life / SECONDS_PER_YEAR:.1f} yr",
        xy=(life / SECONDS_PER_YEAR, 50),
        xytext=(life / SECONDS_PER_YEAR + 1.0, 70),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.4"),
    )
ax2.set_xlabel("Time (yr)")
ax2.set_ylabel("Volume retained in project area (%)")
ax2.set_ylim(0, 105)
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()

panel_labels([ax1, ax2])
fig.tight_layout()
fig.savefig("media/nourishment_design.png", dpi=600)
print("\nWrote media/nourishment_design.png")
