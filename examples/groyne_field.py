"""
Groynes and detached breakwaters: two ways to hold a beach, and what each costs.

The same eroding frontage, offered two schemes.

A **groyne field** blocks the alongshore drift. It works, and the analytical
solution says exactly how well: the fillet against each groyne, the time to
bypassing, and an erosion limb downdrift that is the same size as the
accretion. That last part is not a side effect, it is arithmetic. Sand held
in front of one town is sand not delivered to the next, and the only way to
have the beach without the bill is to pay for the sand at the outset.

A **detached breakwater scheme** shelters instead of blocking. It can build
a beach without the same downdrift debt, but what it builds is much less
certain: the published classification rules disagree with each other at the
ratio most schemes are actually designed at.

Run from the repository root:

    python examples/groyne_field.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from pyCoastal.applications.groynes import (
    SECONDS_PER_YEAR,
    DetachedBreakwater,
    LittoralCell,
    design_detached_scheme,
    design_groyne_field,
    fillet_geometry,
    shoreline_response,
)
from pyCoastal.applications.nourishment import WaveClimate
from pyCoastal.applications.sections import (
    detached_scheme_plan,
    detached_scheme_sheet,
    groyne_field_plan,
    groyne_field_sheet,
)
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

# --- the frontage ----------------------------------------------------------
CELL = LittoralCell(D=6.0, B=2.0, bed="medium_sand")
CLIMATE = WaveClimate(Hb=1.0, T=7.0, alpha0=math.radians(4.0))
HORIZON = 0.3 * SECONDS_PER_YEAR

drift = (math.tan(CLIMATE.alpha0) * CELL.diffusivity(CLIMATE)
         * CELL.active_height)
print(f"Frontage: {CELL.material.name.lower()}, active profile "
      f"{CELL.active_height:.1f} m")
print(f"Littoral drift {drift * SECONDS_PER_YEAR / 1e3:.0f} thousand m3/yr "
      f"at {math.degrees(CLIMATE.alpha0):.0f} deg obliquity")

# --- scheme 1: groynes -----------------------------------------------------
field = design_groyne_field(CELL, CLIMATE, length=60.0, spacing=150.0,
                            count=5, horizon=HORIZON)
state = fillet_geometry(field.groyne, CELL, CLIMATE, HORIZON)

print("\nGroyne field")
print(f"  {field.count} groynes, {field.groyne.length:.0f} m at "
      f"{field.spacing:.0f} m centres ({field.spacing_ratio:.1f} lengths)")
print(f"  bays reach equilibrium in {field.relaxation_time / 86400:.1f} days, "
      f"tilting +/- {field.fillet_drop / 2:.1f} m")
print(f"  updrift groyne bypasses at "
      f"{state['bypassing_time'] / SECONDS_PER_YEAR:.2f} yr, "
      f"having impounded {state['capacity'] / 1e3:.0f} thousand m3")
print(f"  downdrift deficit over {HORIZON / SECONDS_PER_YEAR:.1f} yr: "
      f"{field.downdrift_deficit / 1e3:.0f} thousand m3")
for note in field.notes:
    print(f"    - {note}")

groyne_field_plan(field).save("media/groyne_field.png")
groyne_field_sheet(field, project="Example coast protection scheme",
                   client="Example Coastal Authority",
                   file="examples/groyne_field.py").save("media/groyne_sheet.png")

# --- scheme 2: detached breakwaters ----------------------------------------
breakwater = DetachedBreakwater(length=120.0, offshore=90.0, gap=60.0,
                                crest_level=1.5)
scheme = design_detached_scheme(CELL, CLIMATE, breakwater, frontage=900.0,
                                Hs=2.0, period=8.0, Dn50=1.1)

print("\nDetached breakwaters")
print(f"  Ls/X = {breakwater.ratio:.2f}, verdict: {scheme.verdict}")
for key, verdict in scheme.response["verdicts"].items():
    print(f"    {key:<20} {verdict}")
print(f"  transmission Kt = {scheme.transmission['Kt']:.2f}")
for note in scheme.notes:
    print(f"    - {note}")

detached_scheme_plan(scheme).save("media/detached_scheme.png")
detached_scheme_sheet(scheme, project="Example coast protection scheme",
                      client="Example Coastal Authority",
                      file="examples/groyne_field.py").save("media/detached_sheet.png")

# --- where the criteria part company ---------------------------------------
# The classification is the whole basis of a detached breakwater layout, so
# it is worth seeing how much of the verdict is the data and how much is
# which paper you happened to open.
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2))

ratios = np.linspace(0.2, 2.6, 400)
order = ["no sinuosity", "salient", "periodic tombolo", "tombolo"]
palette = ["#0b3554", "#1b6fa0", "#c47f1a"]
sources = ["spm_1984", "dally_pope_1986", "suh_dalrymple_1987"]

for key, colour, offset in zip(sources, palette, (0.06, 0.0, -0.06)):
    ranks = [order.index(shoreline_response(
        DetachedBreakwater(length=r * 100.0, offshore=100.0),
        criterion=key)["verdicts"][key]) for r in ratios]
    ax.step(ratios, np.array(ranks) + offset, where="post", lw=2.0,
            color=colour, label=key.replace("_", " "))

disputed = [not shoreline_response(
    DetachedBreakwater(length=r * 100.0, offshore=100.0))["unanimous"]
    for r in ratios]
ax.fill_between(ratios, -0.5, 3.5, where=disputed, color="#8a2f24", alpha=0.12,
                label="criteria disagree", step="post")

ax.set_yticks(range(len(order)))
ax.set_yticklabels(order)
ax.set_ylim(-0.5, 3.5)
ax.set_xlabel("Ls / X")
ax.set_title("What the beach does, according to whom")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

# --- and the groyne trade-off ----------------------------------------------
# V_full = pi L^2 (D+B) / 4m, so what a groyne takes out of the drift before
# it fills goes as the square of its length and as the *inverse* of the wave
# obliquity. The second one catches people out: a gently oblique climate
# impounds more sand, not less, because the fillet is long and shallow and
# has to fill a far greater length of coast before it stands as high as the
# groyne. It is also slower to do it, so the damage arrives gradually and
# lasts longer.
lengths = np.linspace(20.0, 120.0, 60)
for degrees, colour in zip((2.0, 4.0, 8.0), palette):
    climate = WaveClimate(Hb=CLIMATE.Hb, T=CLIMATE.T,
                          alpha0=math.radians(degrees))
    taken, times = [], []
    for L in lengths:
        state = fillet_geometry(
            design_groyne_field(CELL, climate, length=L, spacing=150.0,
                                count=5).groyne, CELL, climate, 1.0)
        taken.append(state["capacity"] / 1e3)
        times.append(state["bypassing_time"] / SECONDS_PER_YEAR)
    ax2.plot(lengths, taken, lw=2.0, color=colour,
             label=f"waves at {degrees:.0f} deg")
    ax2.annotate(f"fills in {times[-1]:.1f} yr",
                 xy=(lengths[-1], taken[-1]), xytext=(-6, 6),
                 textcoords="offset points", fontsize=8, ha="right",
                 color=colour)

ax2.set_xlabel("groyne length (m)")
ax2.set_ylabel("sand impounded before bypassing (thousand m3)")
ax2.set_title("Gentler waves impound more sand, and take longer over it")
ax2.legend(loc="upper left", fontsize=8)
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()

fig.suptitle(
    "Holding a beach: a groyne field pays for itself downdrift, a "
    "detached scheme pays for itself in uncertainty",
    y=0.98, fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("media/groyne_tradeoff.png", dpi=600, bbox_inches="tight")

print("\nWrote media/groyne_field.png, media/groyne_sheet.png, "
      "media/detached_scheme.png, media/detached_sheet.png "
      "and media/groyne_tradeoff.png")
