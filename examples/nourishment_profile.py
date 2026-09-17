"""
Beach nourishment: what the borrow source is worth.

The planform model in `examples/nourishment_design.py` answers how long a
fill lasts. This answers the question asked before it: how much dry beach
does a given volume buy, and how much does that depend on where the sand
comes from.

A great deal, is the answer. A beach takes the profile its own grain size
can hold. Fill coarser than the native sand stands steeper and buys more
beach per cubic metre; fill finer lies flatter, and below a critical volume
it buys none at all, because the whole placement goes into flattening the
underwater profile.

Run from the repository root:

    python examples/nourishment_profile.py
"""

import matplotlib.pyplot as plt
import numpy as np

from pyCoastal.applications.nourishment import (
    critical_volume,
    dean_scale,
    grain_compatibility,
    profile_overfill_factor,
    shoreline_advance,
)
from pyCoastal.applications.nourishment import (
    SECONDS_PER_YEAR,
    NourishmentDesign,
    WaveClimate,
)
from pyCoastal.applications.sections import (
    nourishment_plan_section,
    nourishment_section,
    nourishment_sheet,
    spreading_half_life,
)
from pyCoastal.applications.sediment import sediment
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

NATIVE = "medium_sand"
BERM = 2.0            # m above mean sea level
CLOSURE = 6.0         # m, depth of closure
VOLUME = 250.0        # m3 per metre of beach
SOURCES = ["very_fine_sand", "fine_sand", "medium_sand", "coarse_sand",
           "fine_gravel"]

A_native = dean_scale(NATIVE)
print(f"Native beach: {sediment(NATIVE).name}, "
      f"d50 = {sediment(NATIVE).d50 * 1000:.2f} mm, A = {A_native:.3f}")
print(f"Berm {BERM:.1f} m, closure {CLOSURE:.1f} m, "
      f"fill {VOLUME:.0f} m3 per metre\n")

print("borrow            A      delta   profile            dry beach   critical")
results = {}
for key in SOURCES:
    A = dean_scale(key)
    got = shoreline_advance(A_native, A, VOLUME, BERM, CLOSURE)
    match = grain_compatibility(NATIVE, key)
    results[key] = (A, got, match)
    print(f"  {sediment(key).name:<15} {A:.3f}  {match['delta']:+5.2f}  "
          f"{got['kind']:<17} {got['advance']:6.1f} m  "
          f"{got['critical_volume']:6.0f} m3/m")

print("\nWhat that costs, per metre of beach, for 40 m of dry sand")
for key in SOURCES:
    factor = profile_overfill_factor(NATIVE, key, BERM, CLOSURE,
                                     advance=40.0)
    print(f"  {sediment(key).name:<15} {factor['borrow_volume']:6.0f} m3/m  "
          f"({factor['factor']:.2f} times the native requirement)")

print("\nCompatibility")
for key in SOURCES:
    print(f"  {sediment(key).name:<15} {results[key][2]['verdict']}")

# --- the design section ----------------------------------------------------
CHOSEN = "coarse_sand"
chosen = results[CHOSEN][1]
section = nourishment_section(chosen, NATIVE, CHOSEN, BERM, CLOSURE)
section.save("media/nourishment_profile.png")

# --- the same design seen from above ---------------------------------------
# The profile says how much dry beach the sand buys. It says nothing about
# how long it stays there, and for a fill that is the second half of the
# question: a 1.5 km placement in this climate is half gone inside a year.
LENGTH = 1500.0
climate = WaveClimate(Hb=1.2, T=8.0, alpha0=0.0)
design = NourishmentDesign(length=LENGTH, berm_width=chosen["advance"],
                           taper=0.1 * LENGTH, D=CLOSURE, B=BERM)

half_life = spreading_half_life(design, climate) / SECONDS_PER_YEAR
print(f"\nPlanform, {LENGTH:.0f} m of fill in Hb = {climate.Hb:.1f} m:")
print(f"  spreading half-life  {half_life:.2f} yr")
print(f"  placed volume        "
      f"{design.placed_volume / 1e3:.0f} thousand m3 in place")

plan = nourishment_plan_section(design, climate)
plan.save("media/nourishment_plan.png")

sheet = nourishment_sheet(
    chosen, NATIVE, CHOSEN, BERM, CLOSURE,
    project="Bayfront beach management",
    title="Nourishment design profile",
    client="Example Coastal Authority",
    file="examples/nourishment_profile.py",
    plan_design=design,
    plan_climate=climate,
)
sheet.save("media/nourishment_sheet.png")
print("\nWrote media/nourishment_profile.png, media/nourishment_plan.png "
      "and media/nourishment_sheet.png")

# --- how the answer moves with the borrow source --------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.4))

volumes = np.linspace(10.0, 900.0, 90)
palette = ["#8a2f24", "#c47f1a", "#0b3554", "#1f8f8f", "#2f6b46"]
for key, colour in zip(SOURCES, palette):
    A = dean_scale(key)
    widths = [shoreline_advance(A_native, A, float(v), BERM, CLOSURE)["advance"]
              for v in volumes]
    ax.plot(volumes, widths, lw=1.9, color=colour, label=sediment(key).name)
    critical = critical_volume(A_native, A, BERM, CLOSURE)
    if critical > 0:
        ax.plot([critical], [0.0], "o", ms=5, color=colour,
                markeredgecolor="#16181a", markeredgewidth=0.6)

ax.axhline(0.0, color="#54514b", lw=0.8)
ax.set_xlabel("placed volume (m3 per metre of beach)")
ax.set_ylabel("dry beach gained (m)")
ax.set_title("What a cubic metre buys, by borrow source")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()
ax.annotate("filled circles are the critical volume:\n"
            "below it the fill is entirely submerged",
            xy=(0.52, 0.12), xycoords="axes fraction", fontsize=8.5,
            color="#54514b")

y = np.linspace(0.0, 420.0, 400)
for key, colour in zip(SOURCES, palette):
    A = dean_scale(key)
    ax2.plot(y, -A * y ** (2 / 3), lw=1.7, color=colour,
             label=f"{sediment(key).name}, A = {A:.3f}")
ax2.axhline(-CLOSURE, color="#8a2f24", lw=1.1, ls="--")
ax2.annotate(f"closure {CLOSURE:.0f} m", xy=(300, -CLOSURE), xytext=(0, 6),
             textcoords="offset points", fontsize=8.5, color="#8a2f24")
ax2.set_ylim(-9, 0.5)
ax2.set_xlabel("distance offshore (m)")
ax2.set_ylabel("depth (m)")
ax2.set_title("Equilibrium profiles, h = A y$^{2/3}$")
ax2.legend(loc="lower left", fontsize=8)
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()

fig.suptitle(
    f"Nourishment on {sediment(NATIVE).name.lower()}: the borrow grain size "
    "decides what the sand is worth",
    y=0.98, fontsize=12, fontweight="bold",
)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("media/nourishment_borrow.png", dpi=600, bbox_inches="tight")
print("Wrote media/nourishment_borrow.png")
