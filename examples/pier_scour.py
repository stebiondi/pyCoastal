"""
Scour at an estuary pier: tide, river and waves, and where the base sits.

A bridge pier in an estuary is asked to stand in a flow that reverses twice
a day, is biased seaward by the river, changes depth under a four metre
tide, and carries a wind chop on top. None of those peak together.

Two findings come out of working the cycle rather than a load case, and
neither is obvious from a spreadsheet of design values.

**The governing phase is not peak current.** Once the footing is exposed,
the flow-weighted obstacle width depends on how much of the water column
the wide base occupies, so low water counts for more than fast water. The
worst phase here is well after peak ebb.

**The burial depth of the base is a cliff, not a slope.** Bury the footing
deeper than the bare stem would scour and nothing happens. Bury it a metre
shallower and the hole reaches it, the obstacle widens, the hole deepens,
and it runs away to almost twice the depth, undermining the foundation.
There is no gentle middle.

Run from the repository root:

    python examples/pier_scour.py
"""

import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.scour import (
    EstuaryConditions,
    Pier,
    PierBase,
    design_pier_scour,
    equilibrium_scour,
    tidal_state,
)
from pyCoastal.applications.sections import pier_scour_section, pier_scour_sheet
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

PIER = Pier(diameter=2.5, shape="circular")
BASE = PierBase(width=7.0, length=12.0, height=2.5, top_level=-1.5, skew=20.0)
ESTUARY = EstuaryConditions(
    mean_depth=9.0, tidal_amplitude=2.2, tidal_current=1.1,
    river_current=0.4, Hs=1.2, Tp=5.5, bed="medium_sand",
    current_phase=75.0)

design = design_pier_scour(PIER, ESTUARY, BASE)
state = design.governing["state"]

print(f"Pier {PIER.diameter:.1f} m on a {BASE.width:.0f} x {BASE.length:.0f} m "
      f"base, top {BASE.top_level:+.1f} m to the bed")
print(f"Peak ebb {ESTUARY.peak_ebb_current:.2f} m/s, "
      f"peak flood {ESTUARY.peak_flood_current:.2f} m/s")
print()
print(f"Governing phase       {state['phase']:.0f} deg "
      f"({'ebb' if state['ebb'] else 'flood'})")
print(f"  current             {abs(state['current']):.2f} m/s "
      f"(peak is {ESTUARY.peak_ebb_current:.2f})")
print(f"  depth               {state['depth']:.2f} m")
print(f"  effective diameter  {design.governing['scour']['D_e']:.2f} m "
      f"(stem is {PIER.diameter:.2f})")
print(f"  equilibrium scour   {design.equilibrium:.2f} m")
print(f"  one tidal half      {design.tidal_limited:.2f} m "
      f"(time scale {design.time_scale / 3600:.1f} h)")
print(f"  base                "
      f"{'UNDERMINED' if design.undermined else 'exposed' if design.base_exposed else 'buried'}")
print()
for note in design.notes:
    print(f"  - {note}")

pier_scour_section(design).save("media/pier_scour.png")
pier_scour_sheet(design, project="Example estuary crossing",
                 client="Example Highways Authority",
                 file="examples/pier_scour.py").save("media/pier_scour_sheet.png")

# --- what the tide actually does -------------------------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.4))

phases = design.phases()
scour = design.envelope()
depths = np.array([s["state"]["depth"] for s in design.states])
currents = np.array([s["state"]["current"] for s in design.states])

# What varies through the cycle is the scour the conditions *demand* at
# that instant, not the hole itself. The hole does not refill at slack
# water, so what the pier actually ends up with is the envelope: the
# deepest demand the tide ever makes on it.
ax.fill_between(phases, 0, scour, color="#8a2f24", alpha=0.10)
ax.plot(phases, scour, lw=2.0, color="#8a2f24",
        label="demanded by the conditions at that phase")
ax.axhline(design.equilibrium, color="#8a2f24", lw=1.8, ls="--",
           label=f"envelope, and the design value: {design.equilibrium:.2f} m")

ax.axvline(state["phase"], color="#8a2f24", lw=1.0, ls=":")
ax.annotate(f"governs at {state['phase']:.0f} deg",
            xy=(state["phase"], design.equilibrium), xytext=(8, -16),
            textcoords="offset points", fontsize=9, color="#8a2f24")

peak = phases[np.argmax(np.abs(currents))]
ax.axvline(peak, color="#0b3554", lw=1.0, ls=":")
ax.annotate(f"peak current at {peak:.0f} deg", xy=(peak, 0.35 * scour.max()),
            xytext=(8, 0), textcoords="offset points", fontsize=9,
            color="#0b3554")

ax.annotate("slack water demands nothing,\nbut the hole stays",
            xy=(185, 0.1), xytext=(0, 30), textcoords="offset points",
            fontsize=8.5, ha="center", color="#54514b")

ax.set_xlabel("tidal phase (deg)")
ax.set_ylabel("equilibrium scour (m)")
ax.set_xlim(0, 360)
ax.set_ylim(0, 1.35 * scour.max())
ax.set_xticks(range(0, 361, 90))
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()
ax.legend(loc="upper center", fontsize=8, framealpha=0.95)

twin = ax.twinx()
twin.plot(phases, np.abs(currents), lw=1.5, color="#0b3554", alpha=0.85,
          label="current")
twin.plot(phases, depths, lw=1.5, color="#2f93b8", alpha=0.85, ls="--",
          label="depth")
twin.set_ylabel("current (m/s, solid)   and   depth (m, dashed)")
twin.set_ylim(0, 1.35 * max(depths.max(), np.abs(currents).max()))

# --- the cliff --------------------------------------------------------------
tops = np.linspace(-7.0, 0.5, 220)
depths_for = []
for top in tops:
    got = design_pier_scour(
        PIER, ESTUARY,
        PierBase(width=BASE.width, length=BASE.length, height=BASE.height,
                 top_level=float(top), skew=BASE.skew),
        samples=25)
    depths_for.append(got.equilibrium)
depths_for = np.array(depths_for)

bare = design_pier_scour(PIER, ESTUARY, samples=25).equilibrium

ax2.plot(tops, depths_for, lw=2.4, color="#8a2f24")
ax2.axhline(bare, color="#0b3554", lw=1.2, ls="--")
ax2.annotate(f"bare stem alone: {bare:.2f} m", xy=(-6.8, bare),
             xytext=(0, 8), textcoords="offset points", fontsize=9,
             color="#0b3554")
ax2.axvline(-bare, color="#54514b", lw=1.0, ls=":")
ax2.annotate("base below this level:\nscour of the bare stem",
             xy=(-bare, 0.5 * (bare + depths_for.max())), xytext=(-10, 0),
             textcoords="offset points", fontsize=9, ha="right",
             color="#54514b")

ax2.fill_between(tops, bare, depths_for, where=depths_for > bare + 1e-6,
                 color="#8a2f24", alpha=0.12)
ax2.set_xlabel("level of the base top, relative to the initial bed (m)")
ax2.set_ylabel("equilibrium scour (m)")
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()

panel_labels([ax, ax2])
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("media/pier_scour_tide.png", dpi=600, bbox_inches="tight")

print("\nWrote media/pier_scour.png, media/pier_scour_sheet.png "
      "and media/pier_scour_tide.png")
