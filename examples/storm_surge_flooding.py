"""
Storm surge water level and flood mapping.

Builds the water-level budget for a design storm, maps the flooded area on a
synthetic barrier-island terrain, and shows the difference between a plain
elevation threshold and a hydraulically connected flood map.

Run from the repository root:

    python examples/storm_surge_flooding.py
"""

import matplotlib
import matplotlib.pyplot as plt
from pyCoastal.plotting import panel_labels
import numpy as np
from matplotlib.colors import ListedColormap

from pyCoastal.applications.surge import (
    StormConditions,
    bathtub_flood,
    flood_volume,
    flooded_area,
    inundation_limit,
    isolated_low_ground,
    total_water_level,
)

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial"]

# --- design storm ----------------------------------------------------------
storm = StormConditions(
    wind_speed=45.0,           # sustained, 10 m
    central_pressure=94000.0,  # 940 hPa
    tide=0.6,                  # high water at landfall
    Hm0=7.0,
    Tp=13.0,
    fetch=120e3,
    shelf_depth=18.0,
    sea_level_rise=0.0,
)

# A real shelf, shoaling from 60 m to 8 m over the fetch.
shelf = np.linspace(60.0, 8.0, 200)
levels = total_water_level(
    storm, beach_slope=0.04, shelf_depths=shelf, dx=storm.fetch / 199
)

print("Water level budget (m above datum)")
for key in ("tide", "sea_level_rise", "barometric_setup", "wind_setup", "wave_setup"):
    print(f"   {key.replace('_', ' '):>18} {levels[key]:6.2f}")
print(f"   {'still water level':>18} {levels['still_water_level']:6.2f}")
print(f"   {'runup R2%':>18} {levels['runup_R2']:6.2f}")
print(f"   {'total water level':>18} {levels['total_water_level']:6.2f}")

swl = levels["still_water_level"]

# --- terrain: a barrier island with a low-lying bay behind ------------------
nx, ny, dx = 260, 200, 20.0
x = np.arange(nx) * dx
y = np.arange(ny) * dx
X, Y = np.meshgrid(x, y, indexing="ij")

# Shoreface shoaling from -6 m up to the barrier toe at +1 m.
terrain = -6.0 + 7.0 * np.clip((X - 600.0) / 800.0, 0.0, 1.0)

# Barrier ridge, crest at 9 m, well above the design still water level.
ridge = 8.0 * np.exp(-(((X - 1500.0) / 130.0) ** 2))
# A tidal inlet cut clean through it at y = 1.7 km.
ridge *= 1.0 - 0.97 * np.exp(-(((Y - 1700.0) / 120.0) ** 2))
terrain = terrain + ridge

# Low back-barrier bay, then gently rising mainland.
bay = (X > 1750.0) & (X < 3600.0)
terrain[bay] = 0.8
mainland = X >= 3600.0
terrain[mainland] = 0.8 + 0.004 * (X[mainland] - 3600.0)

# A sealed depression, below the water level but with no path to the sea.
pond = ((X - 2600.0) ** 2 / 300.0**2 + (Y - 800.0) ** 2 / 220.0**2) < 1.0
terrain[pond] = -1.5
# A levee ringing the pond, so only connectivity keeps it dry.
ring = ((X - 2600.0) ** 2 / 380.0**2 + (Y - 800.0) ** 2 / 300.0**2)
terrain[(ring >= 1.0) & (ring < 1.45)] = 8.0

# --- flood maps ------------------------------------------------------------
sea = np.zeros_like(terrain, dtype=bool)
sea[0, :] = True                                       # the sea enters at x = 0

connected = bathtub_flood(terrain, swl, seed=sea)
naive = terrain <= swl
isolated = isolated_low_ground(terrain, swl, seed=sea)

print(f"\nStill water level {swl:.2f} m")
print(f"   threshold-only flooded area : {flooded_area(naive, dx) / 1e6:6.2f} km2")
print(f"   connected flooded area      : {flooded_area(connected, dx) / 1e6:6.2f} km2")
print(f"   overstated by the threshold : {flooded_area(isolated, dx) / 1e6:6.2f} km2 "
      f"({100 * isolated.sum() / max(naive.sum(), 1):.0f}% of it)")
print(f"   water volume on land        : {flood_volume(terrain, connected, swl, dx) / 1e6:6.2f} Mm3")

# What does the inlet cost? Seal it and flood the same terrain again.
sealed = terrain.copy()
inlet = (np.abs(Y - 1700.0) < 400.0) & (np.abs(X - 1500.0) < 400.0)
sealed[inlet] = np.maximum(sealed[inlet], 9.0)
sealed_flood = bathtub_flood(sealed, swl, seed=sea)
print()
print(f"   with the inlet open   : {flooded_area(connected, dx) / 1e6:6.2f} km2 flooded")
print(f"   with the inlet sealed : {flooded_area(sealed_flood, dx) / 1e6:6.2f} km2 flooded")
print("   a single breach in the barrier is what floods the bay")

# --- cross-shore transect --------------------------------------------------
j_intact = int(np.argmin(np.abs(y - 500.0)))     # through the intact ridge
j_breach = int(np.argmin(np.abs(y - 1700.0)))    # through the tidal inlet
limit_intact = inundation_limit(x, terrain[:, j_intact], swl)
limit_breach = inundation_limit(x, terrain[:, j_breach], swl)
print(f"\n   inundation limit, intact barrier: {limit_intact:7.0f} m")
print(f"   inundation limit, at the inlet  : {limit_breach:7.0f} m")

# --- figure ----------------------------------------------------------------
fig = plt.figure(figsize=(13, 8.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.28, wspace=0.18)

extent = [0, nx * dx / 1000.0, 0, ny * dx / 1000.0]
panels = []
ax = fig.add_subplot(gs[0, 0])
panels.append(ax)
im = ax.imshow(terrain.T, extent=extent, origin="lower", cmap="terrain",
               vmin=-6, vmax=8, aspect="equal")
ax.contour(X / 1000.0, Y / 1000.0, terrain, levels=[swl], colors="k", linewidths=0.8)
ax.set_xlabel("x (km)")
ax.set_ylabel("y (km)")
fig.colorbar(im, ax=ax, label="elevation (m)", shrink=0.85)

ax = fig.add_subplot(gs[0, 1])
panels.append(ax)
ax.imshow(terrain.T, extent=extent, origin="lower", cmap="gray",
          vmin=-10, vmax=12, aspect="equal", alpha=0.85)
ax.imshow(np.where(connected, 1.0, np.nan).T, extent=extent, origin="lower",
          cmap=ListedColormap(["#1b6fa0"]), aspect="equal", alpha=0.85)
ax.imshow(np.where(isolated, 1.0, np.nan).T, extent=extent, origin="lower",
          cmap=ListedColormap(["#d94a3d"]), aspect="equal", alpha=0.9)
ax.set_xlabel("x (km)")
ax.set_ylabel("y (km)")

for col, (j, label, limit) in enumerate(
    ((j_intact, "intact barrier", limit_intact), (j_breach, "tidal inlet", limit_breach))
):
    ax = fig.add_subplot(gs[1, col])
    panels.append(ax)
    z = terrain[:, j]
    ax.fill_between(x / 1000.0, -8, z, color="#c8b89a", zorder=2)
    # Fill only as far as water can actually reach. Filling every cell below
    # the level would put water behind an intact barrier and contradict the
    # inundation limit drawn alongside it.
    reached = (z <= swl) & (x <= limit)
    ax.fill_between(x / 1000.0, z, swl, where=reached, color="#1b6fa0",
                    alpha=0.75, zorder=1)
    stranded = (z <= swl) & (x > limit)
    if stranded.any():
        ax.fill_between(x / 1000.0, z, swl, where=stranded, color="#d94a3d",
                        alpha=0.30, zorder=1,
                        label="below the level, not reached")
    ax.axhline(swl, color="#0b3554", lw=1.4, ls="--",
               label=f"still water {swl:.2f} m")
    ax.axhline(levels["total_water_level"], color="#8a2f24", lw=1.1, ls=":",
               label=f"with runup {levels['total_water_level']:.2f} m")
    ax.axvline(limit / 1000.0, color="k", lw=1.0, alpha=0.6)
    ax.annotate(f"limit {limit:.0f} m", xy=(limit / 1000.0, 7.5),
                xytext=(6, 0), textcoords="offset points", fontsize=8)
    ax.set_xlabel("x (km)")
    ax.set_ylabel("elevation (m)")
    ax.set_ylim(-8, 9)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    ax.minorticks_on()

panel_labels(panels)
fig.savefig("media/storm_surge_flooding.png", dpi=600, bbox_inches="tight")
print("\nWrote media/storm_surge_flooding.png")
