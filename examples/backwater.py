"""
Backwater at a bridge, and the flow split that feeds contraction scour.

Two things this example is for.

**A backwater curve has no end.** It approaches normal depth
asymptotically, so "the extent of backwater" is always a convention rather
than a measurement, and the number moves by more than a factor of two
across conventions a reasonable engineer might choose. Quoting an extent
without quoting the criterion says nothing.

**The flow split is computed, not guessed.** Contraction scour needs the
fraction of the discharge that actually goes through the opening.
Conveyance decides that, and conveyance is not width: a wooded floodplain
can be three quarters of the section and carry a sixth of the flow.
Guessing it is the largest assumption in a scour calculation, and it hides
behind the most precise-looking number in the output.

Run from the repository root:

    python examples/backwater.py
"""

import matplotlib.pyplot as plt
import numpy as np

from pyCoastal.applications.river import (
    Channel,
    classify_slope,
    critical_depth,
    flow_distribution,
    gvf_profile,
    normal_depth,
    yarnell_afflux,
)
from pyCoastal.applications.scour import (
    BridgeOpening,
    contraction_scour,
)
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

CHANNEL = Channel(width=30.0, side_slope=2.0, roughness="natural_clean")
FLOODPLAIN = Channel(width=120.0, side_slope=3.0, roughness="floodplain_trees")
Q = 250.0
SLOPE = 0.0008

state = classify_slope(CHANNEL, Q, SLOPE)
yn, yc = state["normal"], state["critical"]

print(f"{Q:.0f} m3/s on a {SLOPE:.4f} bed, {CHANNEL.roughness}")
print(f"  normal depth   {yn:.2f} m")
print(f"  critical depth {yc:.2f} m")
print(f"  reach is {state['kind']}, so a bridge backs water up upstream")

# --- the bridge, and the afflux it causes ----------------------------------
BLOCKAGE = 0.18
afflux = yarnell_afflux(CHANNEL, Q, yn, BLOCKAGE, shape="semicircular_nose")
print()
print(f"Piers blocking {100 * BLOCKAGE:.0f}% of the section, Froude "
      f"{afflux['froude']:.2f}")
print(f"  afflux {afflux['afflux']:.3f} m, so the control sits at "
      f"{afflux['upstream_depth']:.2f} m")

profile = gvf_profile(CHANNEL, Q, SLOPE, afflux["upstream_depth"])
print(f"  {profile.profile} profile reaching {profile.reach / 1000:.2f} km")
for note in profile.notes:
    print(f"  - {note}")

# --- what the floodplain actually carries ----------------------------------
OVERBANK = 1.2
split = flow_distribution(CHANNEL, yn, SLOPE, [(FLOODPLAIN, OVERBANK)])
channel_width = CHANNEL.top_width(yn)
plain_width = FLOODPLAIN.top_width(OVERBANK)

print()
print(f"In flood, {OVERBANK:.1f} m over a wooded floodplain:")
print(f"  the channel is {100 * channel_width / (channel_width + plain_width):.0f}% "
      f"of the width")
print(f"  and carries {100 * split['main_fraction']:.0f}% of the flow")

opening = BridgeOpening(approach_width=channel_width + plain_width,
                        opening_width=0.55 * (channel_width + plain_width),
                        abutment_length=20.0,
                        flow_fraction=split["main_fraction"])
guessed = BridgeOpening(approach_width=opening.approach_width,
                        opening_width=opening.opening_width,
                        abutment_length=20.0, flow_fraction=1.0)

computed = contraction_scour(opening, yn, CHANNEL.velocity(Q, yn), "medium_sand")
assumed = contraction_scour(guessed, yn, CHANNEL.velocity(Q, yn), "medium_sand")
print(f"  contraction scour {computed['depth']:.2f} m with the computed split,"
      f" {assumed['depth']:.2f} m if it is assumed to be all of it")

# --- the profile, drawn ----------------------------------------------------
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4))

# Depth rather than level. Over this reach the bed rises four metres while
# the depth changes by seven centimetres, so on a true longitudinal section
# the backwater curve is invisible underneath the slope. Plotting the depth
# removes the bed and leaves the thing the plot is about.
x = profile.distance / 1000.0
ax.fill_between(x, yn, profile.depth, color="#c3dce7", zorder=1.5,
                label="water held above normal depth")
ax.plot(x, profile.depth, lw=2.4, color="#0b3554",
        label=f"depth ({profile.profile} profile)", zorder=4)
ax.axhline(yn, lw=1.3, ls="--", color="#2c6b46",
           label=f"normal depth {yn:.2f} m", zorder=3)

# Critical depth is 1.7 m below this view. Drawing it would set the scale
# and squash the whole backwater, which spans seven centimetres, into a
# line. It matters for naming the profile and not for its shape, so it
# belongs in the title.
ax.annotate(f"bridge holds {afflux['afflux'] * 1000:.0f} mm",
            xy=(0, profile.depth[0]), xytext=(34, -6),
            textcoords="offset points", fontsize=9, color="#0b3554",
            arrowprops=dict(arrowstyle="->", lw=0.9, color="#0b3554"))
ax.annotate("approaching, never arriving",
            xy=(x[-1], profile.depth[-1]), xytext=(-14, 20),
            textcoords="offset points", fontsize=9, ha="right",
            color="#2c6b46",
            arrowprops=dict(arrowstyle="->", lw=0.9, color="#2c6b46"))

span = profile.depth[0] - yn
ax.set_xlabel("distance upstream of the bridge (km)")
ax.set_ylabel("depth (m)")
ax.set_ylim(yn - 0.18 * span, profile.depth[0] + 0.30 * span)
ax.set_title(f"{profile.profile} on a mild reach "
             f"(critical depth {yc:.2f} m, far below this view)")
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()
ax.legend(loc="upper right", fontsize=8.5)

# --- the extent is whatever you decide it is -------------------------------
criteria = np.linspace(0.80, 0.999, 60)
reaches = [gvf_profile(CHANNEL, Q, SLOPE, afflux["upstream_depth"],
                       approach=float(a)).reach / 1000.0 for a in criteria]

ax2.plot(100 * criteria, reaches, lw=2.4, color="#8a2f24")
for mark in (0.90, 0.95, 0.99):
    reach = gvf_profile(CHANNEL, Q, SLOPE, afflux["upstream_depth"],
                        approach=mark).reach / 1000.0
    ax2.plot([100 * mark], [reach], "o", ms=6, color="#8a2f24")
    ax2.annotate(f"{100 * mark:.0f}%: {reach:.2f} km",
                 xy=(100 * mark, reach), xytext=(-8, 8),
                 textcoords="offset points", fontsize=9, ha="right",
                 color="#8a2f24")

ax2.set_xlabel("how close to normal depth you decide to call it (%)")
ax2.set_ylabel("quoted extent of backwater (km)")
ax2.set_title("An asymptote has no end, so this is a choice")
ax2.grid(True, which="both", alpha=0.3)
ax2.minorticks_on()

fig.suptitle(
    "Backwater at a bridge: the profile is physics, the extent quoted for "
    "it is a convention",
    y=0.98, fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("media/backwater.png", dpi=600, bbox_inches="tight")

print("\nWrote media/backwater.png")
