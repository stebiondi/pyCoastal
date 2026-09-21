"""
Open channel hydraulics: normal and critical depth, backwater, and afflux.

The foundation the fluvial side of a crossing stands on. Everything a
bridge does to a river, it does by changing the depth: it squeezes the
flow, the water backs up, and that backwater reaches upstream for a
distance nobody guesses correctly by eye.

Two depths govern a reach, and almost every question is really about which
of them the flow is between.

**Normal depth** is where the bed slope and the friction balance, so the
flow would stay there forever in a prismatic channel. **Critical depth** is
where the specific energy is least and the Froude number is one. Whether
normal is above or below critical decides whether the reach is mild or
steep, which decides which way a disturbance travels: on a mild slope the
backwater from a bridge runs upstream, on a steep one it cannot, and the
bridge is felt downstream instead.

A note on where this joins the coast
------------------------------------
:func:`flow_distribution` is the reason this module exists alongside
:mod:`pyCoastal.applications.scour`. Contraction scour needs to know what
fraction of the discharge actually goes through the opening rather than
staying out on the floodplain, and that fraction is a conveyance
calculation, not a guess. Feeding a guessed ``flow_fraction`` into a scour
depth and then quoting it to two decimals is a way of hiding the largest
assumption in the chain behind the most precise-looking number.

References
----------
Chow, V.T. (1959). Open-Channel Hydraulics. McGraw-Hill.

Henderson, F.M. (1966). Open Channel Flow. Macmillan.

Yarnell, D.L. (1934). Bridge piers as channel obstructions. Technical
Bulletin 442, US Department of Agriculture.

Hydrologic Engineering Center (2016). HEC-RAS River Analysis System
Hydraulic Reference Manual, Version 5.0. US Army Corps of Engineers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "G",
    "MANNING",
    "PIER_SHAPE",
    "Channel",
    "normal_depth",
    "critical_depth",
    "froude_number",
    "specific_energy",
    "friction_slope",
    "classify_slope",
    "profile_type",
    "gvf_profile",
    "BackwaterResult",
    "yarnell_afflux",
    "flow_distribution",
]

G = 9.81

#: Manning's n for natural and made channels.
#:
#: The roughest input in open channel hydraulics, and the one that moves
#: the answer most. A reach quoted at 0.030 might reasonably be 0.025 or
#: 0.040, which is a third either way on the conveyance.
MANNING = {
    "concrete_smooth": 0.013,
    "concrete_rough": 0.017,
    "earth_clean": 0.022,
    "earth_weedy": 0.030,
    "gravel": 0.028,
    "cobbles": 0.035,
    "natural_clean": 0.030,
    "natural_weedy": 0.045,
    "floodplain_pasture": 0.035,
    "floodplain_brush": 0.070,
    "floodplain_trees": 0.100,
}

#: Yarnell pier shape coefficient K.
PIER_SHAPE = {
    "semicircular_nose": 0.90,
    "twin_cylinder": 0.95,
    "ninety_degree_wedge": 1.05,
    "square_nose": 1.25,
    "ten_pile_trestle": 2.50,
}


@dataclass
class Channel:
    """A trapezoidal prismatic channel.

    Attributes
    ----------
    width : float
        Bottom width [m]. Zero gives a triangular section.
    side_slope : float
        Horizontal run per unit rise, z in 1V:zH. Zero is rectangular.
    roughness : float or str
        Manning's n, or a key into :data:`MANNING`.
    """

    width: float = 30.0
    side_slope: float = 2.0
    roughness: float | str = "natural_clean"

    def __post_init__(self) -> None:
        if self.width < 0:
            raise ValueError(f"Width cannot be negative, got {self.width}")
        if self.side_slope < 0:
            raise ValueError("Side slope cannot be negative")
        if self.width == 0 and self.side_slope == 0:
            raise ValueError("A channel needs either a width or a side slope")
        if isinstance(self.roughness, str):
            if self.roughness not in MANNING:
                raise ValueError(
                    f"Unknown roughness {self.roughness!r}. "
                    f"Options: {sorted(MANNING)}")
        elif self.roughness <= 0:
            raise ValueError("Manning's n must be positive")

    @property
    def n(self) -> float:
        """Manning's n."""
        return (MANNING[self.roughness] if isinstance(self.roughness, str)
                else float(self.roughness))

    def area(self, depth: float) -> float:
        """Flow area [m2]."""
        return (self.width + self.side_slope * depth) * depth

    def perimeter(self, depth: float) -> float:
        """Wetted perimeter [m]."""
        return self.width + 2.0 * depth * math.sqrt(1.0 + self.side_slope**2)

    def top_width(self, depth: float) -> float:
        """Width at the water surface [m]."""
        return self.width + 2.0 * self.side_slope * depth

    def hydraulic_radius(self, depth: float) -> float:
        """A / P [m]."""
        perimeter = self.perimeter(depth)
        return self.area(depth) / perimeter if perimeter > 0 else 0.0

    def conveyance(self, depth: float) -> float:
        """K = A R^(2/3) / n, so that Q = K sqrt(S)."""
        if depth <= 0:
            return 0.0
        return (self.area(depth)
                * self.hydraulic_radius(depth) ** (2.0 / 3.0) / self.n)

    def velocity(self, discharge: float, depth: float) -> float:
        """Mean velocity [m/s]."""
        area = self.area(depth)
        return discharge / area if area > 0 else 0.0


def _solve(f, lo: float, hi: float, tolerance: float = 1e-10,
           iterations: int = 200) -> float:
    """Bisection on a monotone function that changes sign in [lo, hi]."""
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError("The solution is not bracketed")
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if hi - lo < tolerance:
            return mid
        if flo * fmid <= 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)


def normal_depth(channel: Channel, discharge: float, slope: float,
                 limit: float = 1000.0) -> float:
    """Depth at which friction balances the bed slope [m].

    Solves Manning, ``Q = K sqrt(S0)``, for the depth. This is where the
    flow would settle if the channel ran straight and prismatic forever,
    and it is one of the two depths a backwater profile is drawn between.

    Raises
    ------
    ValueError
        On a horizontal or adverse slope, where uniform flow does not
        exist and normal depth is undefined. That is a real condition, not
        an edge case: a ponded reach behind a structure has no normal
        depth, and a profile there is classified H or A instead.
    """
    if discharge <= 0:
        raise ValueError(f"Discharge must be positive, got {discharge}")
    if slope <= 0:
        raise ValueError(
            f"Normal depth is undefined on a slope of {slope}. Uniform flow "
            "needs a falling bed; a horizontal or adverse reach carries an "
            "H or A profile instead.")

    target = discharge / math.sqrt(slope)
    return _solve(lambda y: channel.conveyance(y) - target, 1e-9, limit)


def critical_depth(channel: Channel, discharge: float,
                   limit: float = 1000.0) -> float:
    """Depth of least specific energy [m], where the Froude number is one.

    Solves ``Q^2 T / (g A^3) = 1``. Above it the flow is subcritical and
    disturbances travel upstream; below it they cannot, which is why a
    bridge on a steep reach is not felt by the reach above it.
    """
    if discharge <= 0:
        raise ValueError(f"Discharge must be positive, got {discharge}")

    def residual(y):
        area = channel.area(y)
        if area <= 0:
            return -math.inf
        return discharge**2 * channel.top_width(y) / (G * area**3) - 1.0

    return _solve(residual, 1e-9, limit)


def froude_number(channel: Channel, discharge: float, depth: float) -> float:
    """Fr = V / sqrt(g A / T), the form that is right for any section."""
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")
    area = channel.area(depth)
    hydraulic_depth = area / channel.top_width(depth)
    return channel.velocity(discharge, depth) / math.sqrt(G * hydraulic_depth)


def specific_energy(channel: Channel, discharge: float, depth: float) -> float:
    """E = y + V^2 / 2g, measured from the bed [m]."""
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")
    velocity = channel.velocity(discharge, depth)
    return depth + velocity**2 / (2.0 * G)


def friction_slope(channel: Channel, discharge: float, depth: float) -> float:
    """Slope of the energy grade line, from Manning."""
    conveyance = channel.conveyance(depth)
    if conveyance <= 0:
        return math.inf
    return (discharge / conveyance) ** 2


def classify_slope(channel: Channel, discharge: float, slope: float) -> dict:
    """Mild, steep, critical, horizontal or adverse.

    The classification is about the channel and the discharge together, not
    the bed alone: the same reach is mild in flood and can be steep at low
    flow, because critical depth moves with the discharge and normal depth
    moves faster.
    """
    if slope < 0:
        return {"kind": "adverse", "normal": None,
                "critical": critical_depth(channel, discharge)}
    if slope == 0:
        return {"kind": "horizontal", "normal": None,
                "critical": critical_depth(channel, discharge)}

    yn = normal_depth(channel, discharge, slope)
    yc = critical_depth(channel, discharge)
    if abs(yn - yc) < 1e-6 * max(yn, yc):
        kind = "critical"
    elif yn > yc:
        kind = "mild"
    else:
        kind = "steep"
    return {"kind": kind, "normal": yn, "critical": yc,
            "ratio": yn / yc if yc > 0 else math.inf}


def profile_type(depth: float, classification: dict) -> str:
    """Name the backwater profile, in Chow's notation.

    ``M1`` is the one a bridge makes on a mild reach: the flow is deeper
    than normal and deeper than critical, and the surface runs back
    upstream asymptotically towards normal depth. ``M2`` is a drawdown to a
    free overfall. ``S1`` sits behind a structure on a steep reach and is
    short, because the flow is supercritical and the disturbance cannot
    propagate far.
    """
    kind = classification["kind"]
    yn = classification["normal"]
    yc = classification["critical"]
    if depth <= 0:
        raise ValueError("Depth must be positive")

    letter = {"mild": "M", "steep": "S", "critical": "C",
              "horizontal": "H", "adverse": "A"}[kind]

    if kind in ("horizontal", "adverse"):
        # No normal depth, so only zones 2 and 3 exist.
        return f"{letter}{'2' if depth > yc else '3'}"

    upper, lower = max(yn, yc), min(yn, yc)
    if depth > upper:
        zone = "1"
    elif depth > lower:
        zone = "2"
    else:
        zone = "3"
    return f"{letter}{zone}"


@dataclass
class BackwaterResult:
    """The outcome of :func:`gvf_profile`."""

    distance: np.ndarray
    depth: np.ndarray
    channel: Channel
    discharge: float
    slope: float
    classification: dict
    profile: str
    notes: list[str] = field(default_factory=list)

    @property
    def water_surface(self) -> np.ndarray:
        """Water level, taking the bed as zero at the control [m]."""
        return self.depth + self.bed_level

    @property
    def bed_level(self) -> np.ndarray:
        """Bed level along the reach, rising upstream [m]."""
        return self.slope * self.distance

    @property
    def reach(self) -> float:
        """How far the profile extends from the control [m]."""
        return float(abs(self.distance[-1]))

    def depth_at(self, distance: float) -> float:
        """Depth interpolated at one distance from the control [m]."""
        return float(np.interp(abs(distance), np.abs(self.distance),
                               self.depth))


def gvf_profile(channel: Channel, discharge: float, slope: float,
                control_depth: float, steps: int = 200,
                approach: float = 0.99) -> BackwaterResult:
    """Gradually varied flow profile by the direct step method.

    Integrates

        dx = dE / (S0 - Sf)

    away from a control depth, where ``E`` is specific energy and ``Sf``
    the friction slope. Exact for a prismatic channel, which is what makes
    the direct step the right tool here: the depths are chosen and the
    distances computed, rather than the other way round, so the profile
    never has to iterate.

    The integration stops as the depth approaches normal, because it gets
    there only asymptotically and the step length goes to infinity. That
    is not a numerical failure, it is the physics: a backwater curve has no
    end, so what is quoted as "the extent of backwater" is always a
    convention. ``approach`` sets the one used here.

    Parameters
    ----------
    control_depth : float
        Depth at the control, which is where the profile starts. A bridge
        or a weir sets this.
    approach : float
        Fraction of the way to normal depth at which to stop. 0.99 is the
        usual convention; 0.95 gives a noticeably shorter reach and is also
        defensible, which is the point.

    Returns
    -------
    BackwaterResult
        Distances are measured from the control and are positive going
        upstream for a subcritical profile.
    """
    if control_depth <= 0:
        raise ValueError("Control depth must be positive")
    if steps < 2:
        raise ValueError("Need at least two steps")
    if not 0 < approach < 1:
        raise ValueError("Approach must be a fraction in (0,1)")

    classification = classify_slope(channel, discharge, slope)
    yc = classification["critical"]
    yn = classification["normal"]
    profile = profile_type(control_depth, classification)
    notes = []

    if yn is None:
        # No normal depth to approach: integrate towards critical instead.
        target = yc * (1.0 + 1e-3) if control_depth > yc else yc * (1 - 1e-3)
        notes.append(
            f"No normal depth on a {classification['kind']} reach, so the "
            "profile is integrated towards critical depth instead.")
    else:
        target = control_depth + approach * (yn - control_depth)
        if abs(yn - control_depth) < 1e-9:
            notes.append(
                "The control is already at normal depth, so the profile is "
                "uniform and has no length.")
            return BackwaterResult(
                np.array([0.0]), np.array([control_depth]), channel,
                discharge, slope, classification, profile, notes)

    depths = np.linspace(control_depth, target, steps)
    energies = np.array([specific_energy(channel, discharge, y) for y in depths])
    frictions = np.array([friction_slope(channel, discharge, y) for y in depths])

    distance = np.zeros_like(depths)
    for i in range(1, len(depths)):
        mean_friction = 0.5 * (frictions[i] + frictions[i - 1])
        denominator = slope - mean_friction
        if abs(denominator) < 1e-15:
            distance[i] = distance[i - 1]
            continue
        distance[i] = distance[i - 1] + (energies[i] - energies[i - 1]) / denominator

    # Positive going upstream, which is where a subcritical backwater goes.
    distance = np.abs(distance)

    notes.append(
        f"{profile} profile on a {classification['kind']} reach. Control at "
        f"{control_depth:.2f} m against "
        + (f"normal {yn:.2f} m and " if yn is not None else "")
        + f"critical {yc:.2f} m.")
    notes.append(
        f"Backwater reaches {distance[-1] / 1000:.2f} km to get "
        f"{100 * approach:.0f}% of the way to normal depth. The curve is "
        "asymptotic, so that figure is a convention and moves a long way "
        "with it: quoting an extent without quoting the criterion is "
        "meaningless.")

    return BackwaterResult(distance, depths, channel, discharge, slope,
                           classification, profile, notes)


def yarnell_afflux(channel: Channel, discharge: float, downstream_depth: float,
                   blockage: float, shape: str = "semicircular_nose") -> dict:
    """Afflux across a line of bridge piers, Yarnell (1934)::

        H = K (K + 5 Fr^2 - 0.6) (a + 15 a^4) Fr^2 y

    where ``a`` is the fraction of the channel area the piers block and
    ``Fr`` is the downstream Froude number. The fourth power on the
    blockage is what makes this bite: doubling the pier area does far more
    than double the afflux.

    Yarnell's tests were on piers in a rectangular flume at blockages up to
    about 0.4, with the flow class unchanged through the bridge. Outside
    that, and particularly where the bridge chokes the flow to critical,
    the energy or momentum methods in HEC-RAS are the right tools.
    """
    if not 0 <= blockage < 1:
        raise ValueError(f"Blockage must be in [0,1), got {blockage}")
    if shape not in PIER_SHAPE:
        raise ValueError(
            f"Unknown pier shape {shape!r}. Options: {sorted(PIER_SHAPE)}")

    K = PIER_SHAPE[shape]
    Fr = froude_number(channel, discharge, downstream_depth)
    afflux = (K * (K + 5.0 * Fr**2 - 0.6) * (blockage + 15.0 * blockage**4)
              * Fr**2 * downstream_depth)

    return {
        "afflux": afflux,
        "upstream_depth": downstream_depth + afflux,
        "froude": Fr,
        "K": K,
        "blockage": blockage,
        "in_range": blockage <= 0.4 and Fr < 0.8,
        "note": ("" if blockage <= 0.4 and Fr < 0.8 else
                 f"Blockage {blockage:.2f} and Froude {Fr:.2f} are outside "
                 "the range Yarnell tested (blockage to about 0.4, "
                 "subcritical throughout). Use an energy or momentum "
                 "method."),
    }


def flow_distribution(main: Channel, main_depth: float, slope: float,
                      floodplains: list[tuple[Channel, float]] | None = None
                      ) -> dict:
    """How the discharge divides between channel and floodplains.

    Split by conveyance, which is what actually decides it::

        Q_i / Q = K_i / sum(K)      K = A R^(2/3) / n

    This is the number :class:`~pyCoastal.applications.scour.BridgeOpening`
    calls ``flow_fraction``, and it is worth computing rather than
    assuming. A wooded floodplain has perhaps a third of the channel's
    roughness coefficient working against it and a fraction of its
    hydraulic radius, so it can be half the width of the section and carry
    a tenth of the flow. Guessing it high makes contraction scour look
    worse than it is; guessing it low is the mistake that matters.

    Parameters
    ----------
    floodplains : list of (Channel, depth)
        Each overbank panel and the depth of flow on it. An empty list
        means the bridge spans the whole waterway and the fraction is one.
    """
    if main_depth <= 0:
        raise ValueError("Main channel depth must be positive")
    if slope <= 0:
        raise ValueError("Conveyance needs a falling bed")

    main_k = main.conveyance(main_depth)
    panels = [("main", main_k)]
    for index, (panel, depth) in enumerate(floodplains or []):
        panels.append((f"floodplain_{index + 1}", panel.conveyance(depth)))

    total = sum(k for _, k in panels)
    if total <= 0:
        raise ValueError("The section carries no flow at these depths")

    shares = {name: k / total for name, k in panels}
    root = math.sqrt(slope)
    return {
        "shares": shares,
        "main_fraction": shares["main"],
        "conveyance": dict(panels),
        "total_conveyance": total,
        "discharge": total * root,
        "main_discharge": main_k * root,
    }
