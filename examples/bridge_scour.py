"""
Total scour at an estuary crossing: all three HEC-18 components.

Local scour at a pier is the one everybody computes, and on a contracted
crossing it is routinely the smallest of the three. HEC-18 splits total
scour into contraction, local and abutment, and this works all three over
a tidal cycle.

Three things worth seeing, none of which survive being reduced to a single
design load case.

**Contraction scour above the threshold does not care how fast the water
goes.** Laursen's live-bed relation is a sediment balance: faster water
carries more, but it also delivers more, and the two cancel. The answer
turns on the width ratio alone. Below the threshold nothing arrives from
upstream and the mode flips entirely, at which point velocity is suddenly
all that matters.

**The components do not peak together.** Contraction follows the discharge
through the opening, the pier follows the flow in it, and the abutment
follows the approach. Each needs its own envelope over the cycle.

**They are not added at one point.** A pier gets contraction plus its own
hole; an abutment gets contraction plus its own. Adding all three gives a
foundation depth for a hole that exists nowhere.

Run from the repository root:

    python examples/bridge_scour.py
"""

import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.scour import (
    BridgeOpening,
    EstuaryConditions,
    Pier,
    PierBase,
    contraction_scour,
    critical_velocity,
    design_bridge_scour,
)
from pyCoastal.applications.sections import (
    bridge_scour_section,
    bridge_scour_sheet,
)
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

OPENING = BridgeOpening(approach_width=140.0, opening_width=80.0,
                        pier_blockage=5.0, abutment_length=22.0,
                        abutment_shape="spill_through", slope=4e-4)
PIER = Pier(diameter=2.5, shape="circular")
BASE = PierBase(width=7.0, length=12.0, height=2.5, top_level=-1.5, skew=20.0)
ESTUARY = EstuaryConditions(
    mean_depth=9.0, tidal_amplitude=2.2, tidal_current=1.1,
    river_current=0.4, Hs=1.2, Tp=5.5, bed="medium_sand",
    current_phase=75.0)

design = design_bridge_scour(OPENING, ESTUARY, PIER, BASE)
state = design.governing["state"]

print(f"Waterway {OPENING.approach_width:.0f} m, opening "
      f"{OPENING.opening_width:.0f} m gross less "
      f"{OPENING.pier_blockage:.0f} m of piers")
print(f"Contraction {OPENING.contraction_ratio:.2f} to 1")
print()
print(f"Governing phase {state['phase']:.0f} deg "
      f"({'ebb' if state['ebb'] else 'flood'})")
print(f"  approach            {abs(state['current']):.2f} m/s in "
      f"{state['depth']:.2f} m")
print(f"  through the opening "
      f"{design.governing['scour']['opening_velocity']:.2f} m/s in "
      f"{design.governing['scour']['opening_depth']:.2f} m")
print()
print(f"  contraction  {design.contraction:6.2f} m")
print(f"  pier local   {design.pier_local:6.2f} m")
print(f"  abutment     {design.abutment:6.2f} m")
print(f"  {'-' * 22}")
print(f"  at a pier    {design.total_at_pier:6.2f} m")
print(f"  at abutment  {design.total_at_abutment:6.2f} m   <- governs"
      if design.governing_location == "abutment" else
      f"  at abutment  {design.total_at_abutment:6.2f} m")
print()
for note in design.notes:
    print(f"  - {note}")

bridge_scour_section(design).save("media/bridge_scour.png")
bridge_scour_sheet(design, project="Example estuary crossing",
                   client="Example Highways Authority",
                   file="examples/bridge_scour.py").save(
                       "media/bridge_scour_sheet.png")

# --- what the tide does to each component ----------------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.4))

phases = design.phases()
palette = {"contraction": "#0b3554", "pier": "#1b6fa0", "abutment": "#c47f1a"}

for name, colour in palette.items():
    series = design.component(name)
    ax.plot(phases, series, lw=2.0, color=colour, label=name)
    peak = phases[series.argmax()]
    ax.plot([peak], [series.max()], "o", ms=5, color=colour)

ax.plot(phases, design.component("total"), lw=2.6, color="#8a2f24",
        label="total at the governing location")

ax.set_xlabel("tidal phase (deg)")
ax.set_ylabel("scour depth (m)")
ax.set_xlim(0, 360)
ax.set_xticks(range(0, 361, 90))
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()
ax.set_ylim(-2.0, None)
ax.legend(loc="lower center", fontsize=8.5, ncol=2, framealpha=0.95)

# --- the regime switch, and the step in it ---------------------------------
# The two modes are separate equations fitted separately, and they do not
# meet at the threshold. Here clear water arrives at the switch a little
# above where live bed leaves it, so the curve steps down as the bed comes
# alive. The step is small in this case; it is not always, and it is worth
# knowing it is there before reading a scour depth off either side of it.
speeds = np.linspace(0.15, 2.0, 400)
depth = ESTUARY.mean_depth
Vc = critical_velocity(ESTUARY.material, depth)

actual, live, clear = [], [], []
for v in speeds:
    actual.append(contraction_scour(OPENING, depth, v, ESTUARY.bed)["depth"])
    live.append(contraction_scour(OPENING, depth, v, ESTUARY.bed,
                                  regime="live")["depth"])
    clear.append(contraction_scour(OPENING, depth, v, ESTUARY.bed,
                                   regime="clear")["depth"])

ax2.plot(speeds, clear, lw=1.4, ls="--", color="#c47f1a",
         label="clear water, if forced")
ax2.plot(speeds, live, lw=1.4, ls="--", color="#1b6fa0",
         label="live bed, if forced")
ax2.plot(speeds, actual, lw=2.6, color="#8a2f24", label="what applies")
ax2.axvline(Vc, color="#54514b", lw=1.0, ls=":")
ax2.annotate(f"threshold of motion\n{Vc:.2f} m/s", xy=(Vc, max(actual) * 0.72),
             xytext=(8, 0), textcoords="offset points", fontsize=9,
             color="#54514b")

ax2.set_xlabel("approach velocity (m/s)")
ax2.set_ylabel("contraction scour (m)")
ax2.set_ylim(0, max(actual) * 1.25)
step = abs(np.interp(Vc * 1.001, speeds, actual)
           - np.interp(Vc * 0.999, speeds, actual))
ax2.annotate(f"the two equations do not meet:\na {step:.2f} m step",
             xy=(Vc, np.interp(Vc, speeds, actual)), xytext=(14, -46),
             textcoords="offset points", fontsize=8.5, color="#8a2f24",
             arrowprops=dict(arrowstyle="-", lw=0.8, color="#8a2f24"))
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()
ax2.legend(loc="upper left", fontsize=8.5)

panel_labels([ax, ax2])
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("media/bridge_scour_components.png", dpi=600, bbox_inches="tight")

print("\nWrote media/bridge_scour.png, media/bridge_scour_sheet.png "
      "and media/bridge_scour_components.png")
