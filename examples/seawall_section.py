"""
Seawall design, from a design condition to a drawing.

Sizes an L-shaped gravity seawall for a promenade, prints the design report,
and writes the dimensioned cross-section plus a DXF of the geometry.

Run from the repository root:

    python examples/seawall_section.py
"""

from pyCoastal.applications.seawall import design_seawall
from pyCoastal.applications.sections import seawall_section
from pyCoastal.applications.structures import DesignConditions, assess_overtopping
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

# --- design basis ----------------------------------------------------------
# Wave height at the toe, after any nearshore transformation. The storm
# still water level already includes surge and tide.
conditions = DesignConditions.from_peak_period(
    Hm0=2.8,              # significant wave height at the toe
    Tp=9.5,               # peak period
    depth=8.5,            # depth at the toe under the design level
    storm_duration=6 * 3600.0,
)

design = design_seawall(
    conditions,
    still_water_level=2.90,   # m CD, surge plus tide
    seabed_level=-5.60,       # m CD
    tolerable_use="trained_staff",
    friction=0.60,            # concrete on a rubble bedding layer
    target_sliding=1.2,
    target_overturning=1.5,
    scour_coefficient=0.4,    # Xie, fine sand
    stem_thickness=1.0,
    base_thickness=1.2,
)

print(design.summary())

print("\nOvertopping tolerability at the design discharge")
for use, check in assess_overtopping(design.q_upper).items():
    mark = "ok " if check["acceptable"] else "no "
    print(f"   {mark} {check['limit']:>5g} l/s/m   {use}")

# --- drawing ---------------------------------------------------------------
dwg = seawall_section(
    design,
    title="Promenade seawall, typical cross-section",
    sea_extent=24.0,
    land_extent=9.0,
)
dwg.save("media/seawall_section.png")
dwg.to_dxf("media/seawall_section.dxf")
print("\nWrote media/seawall_section.png and media/seawall_section.dxf")

# --- drawing sheet ---------------------------------------------------------
# The same design, issued as a drawing: border, title block, notes, and a
# true stated scale rather than plot axes.
from pyCoastal.applications.sections import seawall_sheet

sheet = seawall_sheet(
    design,
    project="Bayfront promenade protection",
    title="Seawall typical cross-section",
    client="Example Port Authority",
    size="A3",
    sea_extent=24.0,
    land_extent=9.0,
    file="examples/seawall_section.py",
)
sheet.save("media/seawall_sheet.png")
print("Wrote media/seawall_sheet.png")
