"""
Approach channel design: how deep, how wide, and how much dredging.

Sizes an approach channel for a post-Panamax container ship, prints the
depth chain and the width build-up, and issues the cross-section as a
drawing sheet.

Also shows what the answer is sensitive to. The depth is usually argued
over in centimetres and won or lost in metres, because a single judgement
call, the fraction of the wave height taken as vertical vessel motion,
moves it more than every tolerance put together.

Run from the repository root:

    python examples/navigation_channel.py
"""

import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np

from pyCoastal.applications.channel import (
    Vessel,
    design_channel,
    squat_barrass,
    squat_icorels,
    turning_basin_diameter,
)
from pyCoastal.applications.sections import channel_section, channel_sheet
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

# --- the design vessel -----------------------------------------------------
vessel = Vessel(
    name="Post-Panamax container ship",
    length=336.0,
    beam=48.2,
    draught=14.5,
    block_coefficient=0.68,
)

# --- conditions in the channel --------------------------------------------
# Each width class is stated. Anything left out is silently taken at its most
# benign value, which is how a channel ends up too narrow on paper.
CONDITIONS = {
    "speed": "slow",
    "crosswind": "moderate",
    "crosscurrent": "low",
    "longitudinal_current": "low",
    "waves": "moderate",
    "aids_to_navigation": "good",
    "bottom_surface": "smooth_and_soft",
    "depth_of_waterway": "shallow",
    "cargo_hazard": "low",
}

design = design_channel(
    vessel,
    speed=8.0,                    # knots through the water
    design_water_level=1.20,      # m CD, the level the depth is referred to
    Hs=1.8,                       # significant wave height in the channel
    Tp=9.0,
    wave_factor=0.5,
    net_clearance=0.8,            # over a soft bed
    water_level_allowance=0.3,
    dredging_tolerance=0.3,
    survey_tolerance=0.2,
    siltation_allowance=0.2,
    side_slope=5.0,
    existing_bed=-11.5,
    manoeuvrability="moderate",
    section="outer",
    two_way=True,
    speed_class="moderate",
    bank="sloping_channel_edges",
    conditions=CONDITIONS,
)

print(design.summary())

basin = turning_basin_diameter(vessel, assisted=True, current=True)
print(f"\nTurning basin       {basin['diameter']:.0f} m "
      f"({basin['factor']:.1f} x Loa, assisted, current running)")

# --- cross-checks and sensitivities ---------------------------------------
depth = design.required_depth
print("\nSquat, two ways")
for speed in (6.0, 8.0, 10.0, 12.0):
    icorels = squat_icorels(vessel, speed, depth)
    barrass = squat_barrass(vessel, speed, depth)
    flag = "  (beyond range)" if icorels["beyond_range"] else ""
    print(f"   {speed:4.1f} kn   ICORELS {icorels['squat']:.2f} m   "
          f"Barrass {barrass['squat']:.2f} m   "
          f"Fnh {icorels['froude']:.2f}{flag}")

print("\nWhat moves the dredge level")
base = design.required_depth
for label, kwargs in (
    ("wave factor 0.3 rather than 0.5", dict(wave_factor=0.3)),
    ("wave factor 0.7 rather than 0.5", dict(wave_factor=0.7)),
    ("speed 12 kn rather than 8 kn", dict(speed=12.0)),
    ("net clearance 1.5 m rather than 0.8 m", dict(net_clearance=1.5)),
    ("no siltation allowance", dict(siltation_allowance=0.0)),
):
    variant = design_channel(
        vessel, speed=kwargs.pop("speed", 8.0), design_water_level=1.20,
        Hs=1.8, Tp=9.0, wave_factor=kwargs.pop("wave_factor", 0.5),
        net_clearance=kwargs.pop("net_clearance", 0.8),
        water_level_allowance=0.3, dredging_tolerance=0.3,
        survey_tolerance=0.2,
        siltation_allowance=kwargs.pop("siltation_allowance", 0.2),
        side_slope=5.0, existing_bed=-11.5, conditions=CONDITIONS,
        two_way=True,
    )
    change = variant.required_depth - base
    volume = ((variant.dredge_volume(1000.0) - design.dredge_volume(1000.0))
              / 1e3)
    print(f"   {label:<38}{change:+5.2f} m   {volume:+8.0f} k m3/km")

# --- drawings --------------------------------------------------------------
section = channel_section(design, margin=90.0)
section.save("media/navigation_channel.png")

sheet = channel_sheet(
    design,
    project="Container terminal approach",
    title="Navigation channel typical section",
    client="Example Port Authority",
    size="A3",
    margin=90.0,
    file="examples/navigation_channel.py",
)
sheet.save("media/navigation_channel_sheet.png")
sheet.to_dxf("media/navigation_channel.dxf")
print("\nWrote media/navigation_channel.png, "
      "media/navigation_channel_sheet.png and media/navigation_channel.dxf")

# --- how the depth chain is made up ---------------------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.6),
                              gridspec_kw={"width_ratios": [1.15, 1.0]})

names = ["static draught"] + [
    k for k, v in design.clearance["components"].items() if v > 0
]
values = [vessel.draught] + [
    v for v in design.clearance["components"].values() if v > 0
]
bottoms = np.concatenate(([0.0], np.cumsum(values)[:-1]))
colours = ["#0b3554"] + ["#1b6fa0", "#2f93b8", "#79c6d6", "#c3e8ee",
                         "#e6d5ad", "#d8b978", "#c47f1a", "#8a2f24"][:len(values) - 1]

for name, value, bottom, colour in zip(names, values, bottoms, colours):
    ax.barh(0, value, left=bottom, height=0.55, color=colour,
            edgecolor="#1a1a1a", linewidth=0.6)
    if value > 0.18:
        ax.text(bottom + 0.5 * value, 0, f"{value:.2f}", ha="center",
                va="center", fontsize=8,
                color="white" if colour in ("#0b3554", "#1b6fa0", "#8a2f24")
                else "#1a1a1a")
    ax.text(bottom + 0.5 * value, 0.42, name, rotation=45, ha="left",
            va="bottom", fontsize=7.5)

ax.set_xlim(0, sum(values) * 1.02)
ax.set_ylim(-0.5, 1.5)
ax.set_yticks([])
ax.set_xlabel("depth below the design water level (m)")
ax.grid(True, axis="x", which="both", alpha=0.3)
ax.minorticks_on()

factors = np.linspace(0.2, 0.8, 25)
depths, volumes = [], []
for factor in factors:
    variant = design_channel(
        vessel, speed=8.0, design_water_level=1.20, Hs=1.8, Tp=9.0,
        wave_factor=float(factor), net_clearance=0.8,
        water_level_allowance=0.3, dredging_tolerance=0.3,
        survey_tolerance=0.2, siltation_allowance=0.2, side_slope=5.0,
        existing_bed=-11.5, conditions=CONDITIONS, two_way=True,
    )
    depths.append(variant.required_depth)
    volumes.append(variant.dredge_volume(1000.0) / 1e3)

ax2.plot(factors, volumes, color="#0b3554", lw=1.8)
ax2.axvline(0.5, color="#8a2f24", lw=1.2, ls="--", label="value used, 0.50")
ax2.fill_between(factors, volumes, min(volumes), color="#9fc4d6", alpha=0.35)
ax2.set_xlabel("wave response allowance, as a fraction of Hs")
ax2.set_ylabel("capital dredging (thousand m3 per km)")
ax2.legend(loc="upper left")
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()
span = max(volumes) - min(volumes)
ax2.annotate(
    f"{span:,.0f} thousand m3 per km\nacross the defensible range",
    xy=(0.62, 0.5 * (max(volumes) + min(volumes))),
    xytext=(0, 0), textcoords="offset points", fontsize=8.5, ha="center",
)

fig.subplots_adjust(wspace=0.26, top=0.84)
panel_labels([ax, ax2])
fig.savefig("media/channel_depth_chain.png", dpi=600, bbox_inches="tight")
print("Wrote media/channel_depth_chain.png")
