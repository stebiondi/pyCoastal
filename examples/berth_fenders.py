"""
Berthing energy and fender selection for a container terminal.

A berth fails in three different ways and only one of them is about energy.

The fender can be too small, and the ship reaches the quay. The panel can
be too small, and the fender's reaction dents the side shell even though
the energy was absorbed perfectly. The fenders can be too far apart, and
the hull touches the structure between them, at a point where nothing is
measuring and nobody is watching.

This sizes a fender for a post-Panamax container ship and then checks the
other two, which is where berths actually get into trouble.

Run from the repository root:

    python examples/berth_fenders.py
"""

import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.berthing import (
    ABNORMAL_FACTOR,
    BERTHING_VELOCITY,
    CONE_FENDER,
    berthing_energy,
    design_berth,
    hull_pressure,
    select_fender,
)
from pyCoastal.applications.channel import Vessel
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

SHIP = Vessel(name="Post-Panamax container", length=366.0, beam=48.2,
              draught=15.2, block_coefficient=0.68)
FEEDER = Vessel(name="Feeder", length=140.0, beam=22.0, draught=8.5,
                block_coefficient=0.68)

design = design_berth(SHIP, velocity=0.15, vessel_class="container",
                      configuration="open_piled", depth=17.0,
                      smallest_vessel=FEEDER, panel_aspect=(1.4, 2.2))

print(f"{SHIP.name}: {SHIP.displacement / 1000:.0f} thousand tonnes")
print(f"Approaching at {design.velocity:.2f} m/s")
print()
print(f"  kinetic energy      {design.normal['kinetic']:8.0f} kNm")
print(f"  x Cm {design.normal['Cm']:.3f}          added water")
print(f"  x Ce {design.normal['Ce']:.3f}          rotation about the contact")
print(f"  x Cs {design.normal['Cs']:.3f}          fender softness")
print(f"  x Cc {design.normal['Cc']:.3f}          berth configuration")
print(f"  normal berthing     {design.normal['energy']:8.0f} kNm")
print(f"  x {design.abnormal['factor']:.2f}              abnormal allowance")
print(f"  design energy       {design.energy:8.0f} kNm")
print()
print(f"  fender              {design.fender['height']:.2f} m, "
      f"{design.fender['rated_energy']:.0f} kNm rated "
      f"({100 * design.fender['utilisation']:.0f}% used)")
print(f"  reaction            {design.fender['reaction']:.0f} kN")
print(f"  hull pressure       {design.pressure['pressure']:.0f} kN/m2 "
      f"against {design.pressure['limit']:.0f} allowed")
print(f"  spacing             {design.spacing['spacing']:.1f} m against "
      f"{design.spacing['limit']:.1f} m allowed")
print(f"  ADEQUATE            {design.adequate}")
print()
for note in design.notes:
    print(f"  - {note}")

# --- where the energy actually goes ----------------------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.4))

stages = ["kinetic", "x Cm", "x Ce", "x Cs Cc", "x abnormal"]
n = design.normal
values = [
    n["kinetic"],
    n["kinetic"] * n["Cm"],
    n["kinetic"] * n["Cm"] * n["Ce"],
    n["energy"],
    design.energy,
]
colours = ["#54514b", "#8a2f24", "#2c6b46", "#2c6b46", "#c2501c"]

ax.bar(stages, values, color=colours, width=0.62)
for i, value in enumerate(values):
    ax.annotate(f"{value:.0f}", xy=(i, value), xytext=(0, 4),
                textcoords="offset points", ha="center", fontsize=9)
ax.axhline(n["kinetic"], color="#54514b", lw=1.0, ls=":")
ax.set_ylabel("energy (kNm)")
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)

# --- and what the two design levers do -------------------------------------
# Velocity is squared, so it dominates everything. The abnormal factor is a
# straight multiplier but a large one. Between them they set the fender.
velocities = np.linspace(0.05, 0.40, 200)
for label, factor, colour in (("tanker, 1.25", 1.25, "#0b3554"),
                              ("container, 1.50", 1.50, "#1b6fa0"),
                              ("ro-ro, 2.00", 2.00, "#c2501c")):
    energies = [berthing_energy(SHIP, v)["energy"] * factor for v in velocities]
    ax2.plot(velocities, energies, lw=2.0, color=colour,
             label=f"abnormal {label}")

for height in (1.0, 1.4, 2.0, 2.5):
    rated = CONE_FENDER.energy(height)
    ax2.axhline(rated, color="#85817a", lw=0.8, ls="--")
    ax2.annotate(f"{height:.1f} m fender", xy=(0.052, rated), xytext=(0, 3),
                 textcoords="offset points", fontsize=8, color="#85817a")

ax2.axvline(design.velocity, color="#8a2f24", lw=1.0, ls=":")
ax2.annotate(f"design {design.velocity:.2f} m/s",
             xy=(design.velocity, 6000), xytext=(6, 0),
             textcoords="offset points", fontsize=9, color="#8a2f24")

ax2.set_xlabel("berthing velocity (m/s)")
ax2.set_ylabel("design energy (kNm)")
ax2.set_ylim(0, 9000)
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()
ax2.legend(loc="upper left", fontsize=8.5)

panel_labels([ax, ax2])
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("media/berth_energy.png", dpi=600, bbox_inches="tight")

print("\nWrote media/berth_energy.png")
