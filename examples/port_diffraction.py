"""
Port layout study: phase-resolved wave diffraction into a harbour.

Propagates a monochromatic swell into a two-arm harbour, writes an animated
GIF of the instantaneous surface so the diffraction into the basin is visible
wave by wave, and reports the disturbance coefficient at a set of berths.

Run from the repository root:

    python examples/port_diffraction.py
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image

from pyCoastal.applications.port import (
    Breakwater,
    IncidentWave,
    PortLayout,
    harbour_layout,
    rotate_layout,
    simulate_port,
)
from pyCoastal.plotting import (
    LAND_COLOR,
    agitation_colormap,
    land_overlay,
    surface_norm,
    water_colormap,
)

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial"]

# --- case ------------------------------------------------------------------
# Oblique attack is modelled by turning the harbour into the waves and
# driving it shore-normal. A phased oblique source only lights a
# parallelogram of the domain, which would leave part of the harbour in an
# artificial shadow; rotating the layout keeps the incident field uniform.
APPROACH_ANGLE = 25.0

# Plots start downwave of the wavemaker strip and the west sponge, which are
# model machinery rather than part of the harbour.
VIEW_X0 = 320.0

Lx, Ly, dx = 1400.0, 900.0, 4.0
ABSORPTION = 0.35             # rubble-mound armour, Kr around 0.4

# Turn the breakwaters into the waves, but leave the quay along the coast:
# rotating a shore-parallel wall would drive it diagonally across the domain.
arms = rotate_layout(
    harbour_layout(
        Lx=Lx, Ly=Ly, dx=dx, depth=10.0,
        gap=130.0, arm_length=300.0, width=24.0,
        back_wall=False, absorption=ABSORPTION,
    ),
    APPROACH_ANGLE,
)
quay = Breakwater(
    points=[(Lx - 2 * dx, 0.0), (Lx - 2 * dx, Ly)],
    width=2 * dx, absorption=ABSORPTION, name="quay",
)
layout = PortLayout(
    Lx=Lx, Ly=Ly, dx=dx, depth=10.0,
    breakwaters=[*arms.breakwaters, quay],
)
wave = IncidentWave(height=1.5, period=9.0, direction=0.0)

L = wave.wavelength(layout.depth)
print(f"Wavelength        : {L:.1f} m   ({L / layout.dx:.0f} cells per wave)")
print(f"Celerity          : {wave.celerity(layout.depth):.2f} m/s")
print(f"Entrance gap      : 130 m = {130 / L:.2f} wavelengths")
print(f"Approach angle    : {APPROACH_ANGLE:.0f} deg off shore-normal")

result = simulate_port(
    layout,
    wave,
    sponge_sides=("west", "north", "south"),   # the quay reflects
    n_snapshots=90,
    analysis_periods=8.0,
)
print(f"Incident height   : {result.reference_height:.2f} m")

# --- berths ----------------------------------------------------------------
berths = {
    "entrance":    (1020.0, 470.0),
    "outer basin": (1120.0, 500.0),
    "north berth": (1150.0, 640.0),
    "south berth": (1150.0, 300.0),
}
print(f"\n{'berth':>13}{'Kd':>8}{'Hs (m)':>10}")
for name, info in result.berth_report(berths).items():
    print(f"{name:>13}{info['Kd']:>8.2f}{info['Hs']:>10.2f}")

operable = result.operable_fraction(berths, limit=0.5)
print("\nBerths within a 0.5 m operational limit:")
for name, ok in operable.items():
    print(f"   {name:<12} {'yes' if ok else 'no'}")

# --- still figure: disturbance coefficient ---------------------------------
X, Y = layout.meshgrid()
kd = result.disturbance_coefficient

fig, ax = plt.subplots(figsize=(9, 6))
levels = np.linspace(0, 1.6, 33)
cf = ax.contourf(
    X, Y, np.nan_to_num(kd), levels=levels, cmap=agitation_colormap(), extend="max"
)
ax.contour(X, Y, np.nan_to_num(kd), levels=[0.2, 0.4, 0.6], colors="w", linewidths=0.6)
ax.imshow(
    land_overlay(result.land).T,
    extent=[0, layout.Lx, 0, layout.Ly],
    origin="lower", cmap=ListedColormap([LAND_COLOR]), interpolation="nearest",
)
for name, (bx, by) in berths.items():
    ax.plot(bx, by, "o", ms=6, mfc="w", mec="k", mew=1.2)
    ax.annotate(name, (bx, by), textcoords="offset points", xytext=(8, 6), fontsize=8)

ax.set_xlim(VIEW_X0, Lx)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title(f"Disturbance coefficient, H = {wave.height} m, T = {wave.period} s")
ax.set_aspect("equal")
ax.grid(True, which="both", alpha=0.25)
ax.minorticks_on()
fig.colorbar(cf, ax=ax, label="$K_d = H / H_i$", shrink=0.85)
fig.tight_layout()
fig.savefig("media/port_disturbance.png", dpi=600)
print("\nWrote media/port_disturbance.png")

# --- movie: phase-resolved surface -----------------------------------------
norm = surface_norm(result.snapshots)

fig2, ax2 = plt.subplots(figsize=(9, 5.6))
im = ax2.imshow(
    result.snapshots[0].T,
    extent=[0, layout.Lx, 0, layout.Ly],
    origin="lower", cmap=water_colormap(), norm=norm, interpolation="bilinear",
)
ax2.imshow(
    land_overlay(result.land).T,
    extent=[0, layout.Lx, 0, layout.Ly],
    origin="lower", cmap=ListedColormap([LAND_COLOR]), interpolation="nearest",
)
ax2.set_xlim(VIEW_X0, Lx)
ax2.set_xlabel("x (m)")
ax2.set_ylabel("y (m)")
ax2.set_aspect("equal")
title = ax2.set_title("")
fig2.colorbar(im, ax=ax2, label="surface elevation (m)", shrink=0.85)
fig2.tight_layout()


def update(frame):
    im.set_data(result.snapshots[frame].T)
    title.set_text(
        f"Wave diffraction into the harbour, "
        f"{APPROACH_ANGLE:.0f} deg incidence   "
        f"t = {result.times[frame]:.0f} s   "
        f"({result.times[frame] / wave.period:.1f} wave periods)"
    )
    return im, title


anim = FuncAnimation(
    fig2, update, frames=len(result.snapshots), interval=60, blit=False
)
gif_path = "media/port_diffraction.gif"
anim.save(gif_path, writer=PillowWriter(fps=15), dpi=64)

# Matplotlib gives every frame its own palette, which roughly doubles the
# file. Re-encode against one shared adaptive palette.
frames = []
with Image.open(gif_path) as src:
    for k in range(src.n_frames):
        src.seek(k)
        frames.append(src.convert("RGB").copy())

palette = frames[0].quantize(colors=96, method=Image.MEDIANCUT)
quantized = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
quantized[0].save(
    gif_path, save_all=True, append_images=quantized[1:], duration=67, loop=0,
    optimize=True,
)
print(f"Wrote {gif_path}")
