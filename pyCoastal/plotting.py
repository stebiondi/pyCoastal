"""
Plot helpers shared by the examples.

Importing this module needs matplotlib, which is not a runtime dependency of
the package. Install it with the ``plots`` extra::

    pip install pyCoastal[plots]

The colour maps here are built to look like water rather than to be
perceptually uniform. For quantitative fields such as a disturbance
coefficient use ``agitation_colormap`` or a standard scientific map; keep
``water_colormap`` for the instantaneous surface, where the point is to read
the wave pattern at a glance.
"""

from __future__ import annotations

import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

__all__ = [
    "water_colormap",
    "agitation_colormap",
    "LAND_COLOR",
    "land_overlay",
    "surface_norm",
]

#: Concrete-grey used for breakwaters and quays.
LAND_COLOR = "#6b6f73"


def water_colormap(name: str = "pyCoastal_water") -> LinearSegmentedColormap:
    """Diverging map for instantaneous surface elevation.

    Troughs run to deep navy, still water sits at a mid ocean blue, and
    crests lift through turquoise to a pale foam white. Reading it as a
    photograph of the sea surface: dark water in the hollows, light broken
    water on the crests.
    """
    colors = [
        (0.00, "#05182b"),   # deep trough
        (0.22, "#0b3554"),
        (0.42, "#14567f"),
        (0.50, "#1b6fa0"),   # still water
        (0.60, "#2f93b8"),
        (0.78, "#79c6d6"),
        (0.92, "#c3e8ee"),
        (1.00, "#f2fbfc"),   # foam on the crest
    ]
    return LinearSegmentedColormap.from_list(name, colors)


def agitation_colormap(name: str = "pyCoastal_agitation") -> LinearSegmentedColormap:
    """Sequential map for wave height or disturbance coefficient.

    Calm water is dark and quiet; agitation brightens through green to a hot
    yellow, so the berths in trouble stand out.
    """
    colors = [
        (0.00, "#0a2239"),
        (0.25, "#11557a"),
        (0.50, "#1f8f8f"),
        (0.72, "#63c07a"),
        (0.88, "#c9df6a"),
        (1.00, "#fdf3a0"),
    ]
    return LinearSegmentedColormap.from_list(name, colors)


def surface_norm(snapshots: np.ndarray, percentile: float = 99.5) -> TwoSlopeNorm:
    """Symmetric colour scale centred on still water.

    The limit comes from a high percentile rather than the maximum, so a
    single sharp spike near a structure does not flatten the whole field.
    """
    amp = float(np.nanpercentile(np.abs(snapshots), percentile))
    if amp <= 0:
        amp = 1.0
    return TwoSlopeNorm(vmin=-amp, vcenter=0.0, vmax=amp)


def land_overlay(land: np.ndarray) -> np.ndarray:
    """Float array that is 1.0 on structures and NaN on water.

    Draw it over a field with a solid colour map so breakwaters read as
    material rather than as an extreme value of the field.
    """
    return np.where(land, 1.0, np.nan)


def panel_labels(axes, labels=None, loc: str = "upper left",
                 fontsize: float = 10.0, offset: float = 0.02):
    """Label each panel of a multi-panel figure with (a), (b), (c), ...

    The figures in ``examples/`` carry no titles. Panel letters identify the
    panels, and the caption of the figure states what each one shows.

    Parameters
    ----------
    axes : sequence of matplotlib Axes
        Panels in reading order. A 2D array from ``plt.subplots`` is
        flattened.
    labels : sequence of str, optional
        Replacement labels. Defaults to "(a)", "(b)", ...
    loc : {"upper left", "upper right", "lower left", "lower right"}
        Corner of the panel, in axes coordinates.
    offset : float
        Inset from the corner, as a fraction of the panel.

    Returns
    -------
    list
        The created text artists.
    """
    import numpy as _np

    flat = list(_np.ravel(_np.asarray(axes, dtype=object)))
    if labels is None:
        labels = [f"({chr(ord('a') + i)})" for i in range(len(flat))]
    vertical, horizontal = loc.split()
    x = offset if horizontal == "left" else 1.0 - offset
    y = 1.0 - offset if vertical == "upper" else offset
    out = []
    for ax, label in zip(flat, labels):
        out.append(ax.text(
            x, y, label, transform=ax.transAxes, fontsize=fontsize,
            fontweight="bold", ha=horizontal, va="top" if vertical == "upper" else "bottom",
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#c9c7c0", alpha=0.85),
        ))
    return out
