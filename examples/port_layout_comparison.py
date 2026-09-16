"""
Compare the built-in port layouts under the same design wave.

Runs every layout in ``pyCoastal.applications.port.LAYOUTS``, maps the
disturbance coefficient, and ranks them by how quiet they keep the basin.

Run from the repository root:

    python examples/port_layout_comparison.py
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, LogNorm

from pyCoastal.applications.port import LAYOUTS, IncidentWave, simulate_port
from pyCoastal.plotting import LAND_COLOR, agitation_colormap, land_overlay

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial"]

LX, LY = 1400.0, 900.0   # one domain for every layout, so the runs compare
DX = 8.0
ABSORPTION = 0.35          # rubble-mound armour on every structure
WAVE = IncidentWave(height=1.5, period=9.0, direction=0.0)
VIEW_X0 = 320.0            # hide the wavemaker strip and the west sponge

TITLES = {
    "two_arm": "Two arms, straight gap",
    "offset_entrance": "Overlapping arms, dog-leg",
    "hooked": "Hooked main breakwater",
    "detached_screen": "Detached screen off the gap",
    "marina": "Outer harbour and inner basin",
}


def basin_statistics(result, layout):
    """Mean and worst Kd in the sheltered part of the domain.

    The same box is used for every layout so the numbers are comparable,
    even though the structures that protect it differ.
    """
    inside = result.x > 0.84 * layout.Lx
    water = np.zeros_like(result.land, dtype=bool)
    water[inside, :] = True
    water &= ~result.land

    kd = result.wave_height[water] / result.reference_height
    return float(kd.mean()), float(np.percentile(kd, 95))


results = {}
for name, builder in LAYOUTS.items():
    layout = builder(Lx=LX, Ly=LY, dx=DX, absorption=ABSORPTION)
    result = simulate_port(
        layout,
        WAVE,
        sponge_sides=("west", "north", "south"),   # the quay reflects
        n_snapshots=2,
        analysis_periods=10.0,
    )
    results[name] = (layout, result, *basin_statistics(result, layout))
    print(f"ran {name}")

print(f"\n{'layout':>32}{'mean Kd':>10}{'95th pct Kd':>14}")
ranked = sorted(results.items(), key=lambda kv: kv[1][2])
for name, (_, _, mean_kd, p95) in ranked:
    print(f"{TITLES[name]:>32}{mean_kd:>10.3f}{p95:>14.3f}")

best = ranked[0][0]
worst = ranked[-1][0]
print(
    f"\nQuietest basin: {TITLES[best]} "
    f"({results[best][2]:.3f} mean Kd)\n"
    f"Noisiest basin: {TITLES[worst]} "
    f"({results[worst][2]:.3f} mean Kd)"
)

# --- figure ----------------------------------------------------------------
n = len(results)
fig, axes = plt.subplots(1, n, figsize=(4.0 * n, 4.4), sharey=True)
# Kd runs from about 0.005 in a well sheltered basin to above 1 outside,
# so a linear scale would render every good layout as identical black.
levels = np.logspace(np.log10(0.005), np.log10(1.5), 28)
norm = LogNorm(vmin=levels[0], vmax=levels[-1])
land_cmap = ListedColormap([LAND_COLOR])

for ax, (name, (layout, result, mean_kd, _)) in zip(axes, results.items()):
    X, Y = layout.meshgrid()
    kd = np.nan_to_num(result.disturbance_coefficient, nan=0.0)
    cf = ax.contourf(
        X, Y, np.clip(kd, levels[0], None),
        levels=levels, norm=norm, cmap=agitation_colormap(), extend="both",
    )
    ax.imshow(
        land_overlay(result.land).T,
        extent=[0, layout.Lx, 0, layout.Ly],
        origin="lower", cmap=land_cmap, interpolation="nearest",
    )
    ax.set_title(f"{TITLES[name]}\nmean basin $K_d$ = {mean_kd:.2f}", fontsize=10)
    ax.set_xlim(VIEW_X0, layout.Lx)
    ax.set_xlabel("x (m)")
    ax.set_aspect("equal")
    ax.grid(True, which="both", alpha=0.25)
    ax.minorticks_on()

axes[0].set_ylabel("y (m)")
cb = fig.colorbar(cf, ax=axes, label="$K_d = H / H_i$  (log scale)",
                  shrink=0.8, pad=0.02, ticks=[0.005, 0.02, 0.05, 0.2, 0.5, 1.0])
cb.ax.set_yticklabels(["0.005", "0.02", "0.05", "0.2", "0.5", "1.0"])
fig.suptitle(
    f"Harbour layouts under H = {WAVE.height} m, T = {WAVE.period} s, "
    f"armour absorption {ABSORPTION}",
    y=1.02,
)
fig.savefig("media/port_layouts.png", dpi=600, bbox_inches="tight")
print("\nWrote media/port_layouts.png")
