"""
Navigation channel design: squat, underkeel clearance, depth and width.

How deep and how wide does the approach channel have to be? The answer is a
stack of allowances, each small, each defensible, and together often several
metres. This module builds that stack explicitly so it can be argued over
line by line, which is how a dredging budget actually gets agreed.

The depth chain
---------------
Start at the design water level, subtract the vessel's static draught, then
subtract, in turn, the squat as she moves, her vertical response to waves,
the net clearance the pilot and the authority require over the bed, and the
tolerances the dredger and the survey cannot beat. What is left is the
dredge level.

The width chain
---------------
A basic manoeuvring lane, widened for everything that pushes the vessel off
line (speed, wind, cross current, waves, poor marking, a hostile bottom),
plus clearance to each bank, and doubled with a passing distance if the
channel is two-way.

Sources
-------
PIANC (2014), Harbour Approach Channels Design Guidelines, report 121.
    The concept design method reproduced here: the width components, the
    underkeel clearance components, and the squat formulations.

ICORELS (1980), as given in PIANC. The squat formula used by default.

Barrass, C. B. (1979), "A unified approach to squat calculations for
    ships". The screening formula.

Conventions
-----------
Levels are metres to chart datum and increase upward. Depths and draughts
are positive numbers of metres. Speeds are in knots where a formula is
written in knots and metres per second elsewhere; every function says which.

Caution
-------
The width components and the manoeuvring lane widths here follow the PIANC
concept-design structure with the indicative values commonly quoted. They
are exposed as editable tables rather than buried, because the governing
edition of the guideline, and the pilots on the day, decide the numbers on
a real scheme. Concept design only: a real channel is confirmed by
simulation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

G = 9.81
KNOT = 0.514444          # m/s

__all__ = [
    "Vessel",
    "squat_icorels",
    "squat_barrass",
    "wave_response_allowance",
    "MANOEUVRING_LANE",
    "WIDTH_COMPONENTS",
    "BANK_CLEARANCE",
    "PASSING_DISTANCE",
    "channel_width",
    "underkeel_clearance",
    "ChannelDesign",
    "design_channel",
    "turning_basin_diameter",
]


# ---------------------------------------------------------------------------
# The vessel
# ---------------------------------------------------------------------------


@dataclass
class Vessel:
    """The design vessel.

    Attributes
    ----------
    name : str
        For the drawing and the report.
    length : float
        Length overall Loa [m].
    length_pp : float
        Length between perpendiculars [m]. Defaults to 0.96 Loa, the usual
        ratio for a merchant hull, because the squat formulae are written
        around Lpp and getting it wrong by four per cent is not the largest
        error in the chain.
    beam : float
        Moulded beam B [m].
    draught : float
        Static draught at the design loading T [m].
    block_coefficient : float
        Cb, the fraction of the enclosing box the hull fills. About 0.85 for
        a bulk carrier, 0.65 for a container ship, 0.55 for a fast ferry.
    """

    name: str
    length: float
    beam: float
    draught: float
    block_coefficient: float = 0.75
    length_pp: float | None = None

    def __post_init__(self) -> None:
        for field_name in ("length", "beam", "draught"):
            if getattr(self, field_name) <= 0:
                raise ValueError(f"{field_name} must be positive")
        if not 0.3 <= self.block_coefficient <= 1.0:
            raise ValueError(
                f"Block coefficient {self.block_coefficient} is outside 0.3 to 1.0"
            )
        if self.length_pp is None:
            self.length_pp = 0.96 * self.length

    @property
    def displaced_volume(self) -> float:
        """Displaced volume from the block coefficient [m3]."""
        return self.block_coefficient * self.length_pp * self.beam * self.draught

    @property
    def displacement(self) -> float:
        """Displacement in tonnes, at 1025 kg/m3."""
        return self.displaced_volume * 1.025


# ---------------------------------------------------------------------------
# Squat
# ---------------------------------------------------------------------------


def squat_icorels(vessel: Vessel, speed: float, depth: float,
                  coefficient: float = 2.4) -> dict:
    """Bow squat by the ICORELS formula, as given in PIANC.

        S = C * (V / Lpp^2) * Fnh^2 / sqrt(1 - Fnh^2)

    where the displacement volume replaces V and Fnh is the depth Froude
    number, ``u / sqrt(g h)``.

    Parameters
    ----------
    speed : float
        Vessel speed through the water [knots].
    depth : float
        Water depth [m].
    coefficient : float
        2.4 is the value PIANC gives for an open or a wide channel. A
        confined channel squats more; the guideline's correction factor is
        applied through this coefficient.

    Returns
    -------
    dict
        ``squat`` [m], the depth Froude number, and a flag for whether the
        speed is close enough to the critical speed that the formula is
        unusable.

    Notes
    -----
    The formula blows up as Fnh approaches one, where the vessel is at
    the critical speed and the whole notion of a steady squat fails. It is
    normally kept to Fnh below about 0.7, and no vessel is navigated a
    channel anywhere near that. The returned dict flags it rather than
    returning a number that is arithmetically fine and physically absurd.
    """
    if speed < 0:
        raise ValueError(f"Speed must be non-negative, got {speed}")
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")

    u = speed * KNOT
    froude = u / math.sqrt(G * depth)
    unusable = froude >= 0.7
    if froude >= 0.99:
        raise ValueError(
            f"Depth Froude number {froude:.2f} is at or above the critical "
            "speed; the squat formula has no meaning there"
        )

    squat = (coefficient * vessel.displaced_volume / vessel.length_pp**2
             * froude**2 / math.sqrt(1.0 - froude**2))
    return {"squat": squat, "froude": froude, "speed_ms": u,
            "beyond_range": unusable}


def squat_barrass(vessel: Vessel, speed: float, depth: float,
                  confined: bool = False) -> dict:
    """Bow squat by Barrass's screening formula.

        S_max = Cb * V^2 / 100     in open water
        S_max = Cb * V^2 / 50      in a confined channel

    with the speed in knots. Deliberately crude, and useful exactly because
    of it: a number to sanity-check the ICORELS result against, on the back
    of an envelope, before trusting either.
    """
    if speed < 0:
        raise ValueError(f"Speed must be non-negative, got {speed}")
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")
    divisor = 50.0 if confined else 100.0
    return {
        "squat": vessel.block_coefficient * speed**2 / divisor,
        "froude": speed * KNOT / math.sqrt(G * depth),
        "confined": confined,
    }


def wave_response_allowance(Hs: float, factor: float = 0.5,
                            period: float | None = None,
                            vessel: Vessel | None = None) -> dict:
    """Vertical vessel motion allowance from wave height [m].

    Parameters
    ----------
    Hs : float
        Significant wave height in the channel [m].
    factor : float
        Fraction of Hs taken as the vertical motion of the keel. PIANC's
        concept-design guidance spans roughly 0.3 for a long vessel in short
        head seas up to about 0.7 for a short vessel in long beam seas, and
        0.5 is the usual starting point. This is the single largest
        judgement in the depth chain when there is any swell at all, so set
        it deliberately.
    period, vessel : optional
        Used only to report the ratio of wave length to vessel length, which
        is what governs whether the vessel contours the wave or bridges it.
        A ratio near one is the worst case and argues for a higher factor.

    Returns
    -------
    dict
        The ``allowance`` and, when the optional arguments are given, the
        wave length and its ratio to the vessel length.
    """
    if Hs < 0:
        raise ValueError(f"Wave height must be non-negative, got {Hs}")
    if not 0.0 <= factor <= 1.5:
        raise ValueError(f"Factor {factor} is outside any defensible range")

    out = {"allowance": factor * Hs, "factor": factor}
    if period is not None and vessel is not None:
        wavelength = G * period**2 / (2 * math.pi)
        out["wavelength"] = wavelength
        out["length_ratio"] = wavelength / vessel.length
        out["near_resonant"] = 0.7 <= out["length_ratio"] <= 1.4
    return out


# ---------------------------------------------------------------------------
# Width components
# ---------------------------------------------------------------------------

#: Basic manoeuvring lane as a multiple of the beam, by manoeuvrability.
MANOEUVRING_LANE = {"good": 1.3, "moderate": 1.5, "poor": 1.8}

#: Additional width components, as multiples of the beam. Each entry is
#: keyed by the condition and gives (outer channel, inner channel). These
#: follow the PIANC concept-design structure; confirm against the governing
#: edition before using them on a scheme.
WIDTH_COMPONENTS: dict[str, dict[str, tuple[float, float]]] = {
    "speed": {                         # vessel speed through the water
        "fast": (0.1, 0.1),            # above 12 knots
        "moderate": (0.0, 0.0),        # 8 to 12 knots
        "slow": (0.0, 0.0),            # 5 to 8 knots
    },
    "crosswind": {                     # beam wind
        "mild": (0.1, 0.1),            # up to 15 knots
        "moderate": (0.3, 0.4),        # 15 to 33 knots
        "severe": (0.6, 0.8),          # 33 to 48 knots
    },
    "crosscurrent": {
        "negligible": (0.0, 0.0),      # under 0.2 knots
        "low": (0.2, 0.3),             # 0.2 to 0.5 knots
        "moderate": (0.5, 0.7),        # 0.5 to 1.5 knots
        "strong": (1.0, 1.3),          # 1.5 to 2.0 knots
    },
    "longitudinal_current": {
        "low": (0.0, 0.0),             # under 1.5 knots
        "moderate": (0.1, 0.1),        # 1.5 to 3 knots
        "strong": (0.2, 0.2),          # above 3 knots
    },
    "waves": {                         # significant height in the channel
        "low": (0.0, 0.0),             # under 1 m
        "moderate": (0.5, 0.0),        # 1 to 3 m
        "high": (1.0, 0.0),            # above 3 m
    },
    "aids_to_navigation": {
        "excellent": (0.0, 0.0),
        "good": (0.2, 0.2),
        "moderate": (0.4, 0.4),
    },
    "bottom_surface": {
        "smooth_and_soft": (0.1, 0.1),
        "smooth_or_sloping": (0.1, 0.1),
        "rough_and_hard": (0.2, 0.2),
    },
    "depth_of_waterway": {             # depth as a multiple of draught
        "deep": (0.0, 0.0),            # more than 1.5 T
        "moderate": (0.1, 0.2),        # 1.25 to 1.5 T
        "shallow": (0.2, 0.4),         # less than 1.25 T
    },
    "cargo_hazard": {
        "low": (0.0, 0.0),
        "medium": (0.5, 0.4),
        "high": (1.0, 0.8),
    },
}

#: Bank clearance as a multiple of the beam, by bank type and vessel speed.
BANK_CLEARANCE = {
    "sloping_channel_edges": {"fast": 0.7, "moderate": 0.5, "slow": 0.3},
    "sloping_and_shoals": {"fast": 0.7, "moderate": 0.5, "slow": 0.3},
    "steep_and_hard": {"fast": 1.3, "moderate": 1.0, "slow": 0.5},
}

#: Passing distance in a two-way channel, as a multiple of the beam.
PASSING_DISTANCE = {"fast": 2.0, "moderate": 1.6, "slow": 1.2}


def channel_width(
    vessel: Vessel,
    manoeuvrability: str = "moderate",
    section: str = "outer",
    two_way: bool = False,
    speed_class: str = "moderate",
    bank: str = "sloping_channel_edges",
    conditions: dict | None = None,
) -> dict:
    """Channel width by the PIANC concept-design build-up.

    Parameters
    ----------
    manoeuvrability : str
        Key into :data:`MANOEUVRING_LANE`.
    section : str
        "outer" for an exposed approach, "inner" for a sheltered reach. The
        two columns of :data:`WIDTH_COMPONENTS` differ because an exposed
        channel has waves and a sheltered one has banks close by.
    two_way : bool
        Whether two design vessels pass.
    speed_class : str
        "fast", "moderate" or "slow", used for the bank clearance and the
        passing distance.
    conditions : dict, optional
        One key per entry in :data:`WIDTH_COMPONENTS`, naming the class that
        applies. Anything omitted is taken as its most benign class, and is
        reported as such so the omission is visible.

    Returns
    -------
    dict
        The total ``width``, the ``components`` that built it, and the
        assumptions filled in for anything not specified.
    """
    if manoeuvrability not in MANOEUVRING_LANE:
        raise ValueError(
            f"Unknown manoeuvrability {manoeuvrability!r}. "
            f"Options: {sorted(MANOEUVRING_LANE)}"
        )
    if section not in ("outer", "inner"):
        raise ValueError(f"Section must be 'outer' or 'inner', got {section!r}")
    if speed_class not in PASSING_DISTANCE:
        raise ValueError(
            f"Unknown speed class {speed_class!r}. Options: {sorted(PASSING_DISTANCE)}"
        )
    if bank not in BANK_CLEARANCE:
        raise ValueError(
            f"Unknown bank type {bank!r}. Options: {sorted(BANK_CLEARANCE)}"
        )

    conditions = dict(conditions or {})
    column = 0 if section == "outer" else 1

    components: dict[str, float] = {}
    assumed: list[str] = []
    basic = MANOEUVRING_LANE[manoeuvrability] * vessel.beam
    components["basic manoeuvring lane"] = basic

    additional = 0.0
    for name, classes in WIDTH_COMPONENTS.items():
        if name in conditions:
            key = conditions[name]
            if key not in classes:
                raise ValueError(
                    f"Unknown {name} class {key!r}. Options: {sorted(classes)}"
                )
        else:
            # The most benign class, chosen by the smallest additional width.
            key = min(classes, key=lambda k: classes[k][column])
            assumed.append(f"{name} = {key}")
        value = classes[key][column] * vessel.beam
        if value > 0:
            components[f"{name} ({key})"] = value
        additional += value

    lanes = 2 if two_way else 1
    clearance = BANK_CLEARANCE[bank][speed_class] * vessel.beam
    components["bank clearance, each side"] = clearance

    passing = PASSING_DISTANCE[speed_class] * vessel.beam if two_way else 0.0
    if two_way:
        components["passing distance"] = passing

    width = lanes * (basic + additional) + passing + 2.0 * clearance
    return {
        "width": width,
        "width_in_beams": width / vessel.beam,
        "components": components,
        "assumed": assumed,
        "lanes": lanes,
        "section": section,
    }


# ---------------------------------------------------------------------------
# Depth
# ---------------------------------------------------------------------------


def underkeel_clearance(
    vessel: Vessel,
    squat: float,
    wave_allowance: float,
    net_clearance: float = 0.6,
    water_level_allowance: float = 0.0,
    dredging_tolerance: float = 0.3,
    survey_tolerance: float = 0.2,
    siltation_allowance: float = 0.2,
    density_allowance: float = 0.0,
) -> dict:
    """Build the underkeel clearance stack [m].

    Parameters
    ----------
    net_clearance : float
        The clearance that must remain under the keel at the worst instant,
        after every other allowance has been used up. Commonly 0.5 to 1.0 m
        over a soft bed and more over rock, and often set by the port's own
        rules rather than by a calculation.
    water_level_allowance : float
        Uncertainty in the predicted water level: the difference between
        the predicted and the actual tide, and any negative surge.
    dredging_tolerance, survey_tolerance : float
        What the dredger can hold and what the survey can see. Both are
        real, both are always there, and leaving them out is the most
        common way a channel ends up shallower than its drawing.
    siltation_allowance : float
        Material expected between maintenance campaigns.
    density_allowance : float
        Extra draught in brackish or fresh water, where the vessel floats
        deeper than in the salt water her marks were set in.

    Returns
    -------
    dict
        Each allowance, the ``gross`` total below the keel, and the total
        ``required_depth`` below the design water level.
    """
    parts = {
        "squat": squat,
        "wave response": wave_allowance,
        "density": density_allowance,
        "net clearance": net_clearance,
        "water level uncertainty": water_level_allowance,
        "dredging tolerance": dredging_tolerance,
        "survey tolerance": survey_tolerance,
        "siltation": siltation_allowance,
    }
    for name, value in parts.items():
        if value < 0:
            raise ValueError(f"Allowance {name!r} must be non-negative, got {value}")

    gross = sum(parts.values())
    return {
        "components": parts,
        "gross": gross,
        "required_depth": vessel.draught + gross,
        "draught": vessel.draught,
    }


@dataclass
class ChannelDesign:
    """A dimensioned approach channel."""

    vessel: Vessel
    design_water_level: float
    dredge_level: float
    required_depth: float
    clearance: dict
    squat: dict
    waves: dict
    width_result: dict
    side_slope: float
    speed: float
    existing_bed: float | None = None
    warnings: list[str] = field(default_factory=list)

    @property
    def width(self) -> float:
        """Channel bed width [m]."""
        return self.width_result["width"]

    @property
    def top_width(self) -> float:
        """Width at the existing bed, including the side slopes [m]."""
        if self.existing_bed is None:
            return self.width
        rise = max(self.existing_bed - self.dredge_level, 0.0)
        return self.width + 2.0 * self.side_slope * rise

    def dredge_volume(self, length: float) -> float:
        """Capital dredge volume over a length of channel [m3].

        A trapezoid over a flat existing bed. A real take-off works from a
        survey surface, and will differ; this is the number to size a
        campaign with, not to pay a contractor on.
        """
        if self.existing_bed is None:
            raise RuntimeError("No existing bed level was given")
        rise = max(self.existing_bed - self.dredge_level, 0.0)
        area = self.width * rise + self.side_slope * rise**2
        return area * length

    def summary(self) -> str:
        """A short design report, depth chain first."""
        v = self.vessel
        lines = [
            f"Design vessel       {v.name}",
            f"                    {v.length:.0f} x {v.beam:.1f} x "
            f"{v.draught:.1f} m, Cb = {v.block_coefficient:.2f}, "
            f"{v.displacement:,.0f} t",
            f"Speed               {self.speed:.1f} knots "
            f"(Fnh = {self.squat['froude']:.2f})",
            "",
            "Depth chain (m below the design water level)",
            f"   {'static draught':<26}{v.draught:6.2f}",
        ]
        for name, value in self.clearance["components"].items():
            lines.append(f"   {name:<26}{value:6.2f}")
        lines += [
            f"   {'required depth':<26}{self.required_depth:6.2f}",
            "",
            f"Design water level  {self.design_water_level:+.2f} m CD",
            f"Dredge level        {self.dredge_level:+.2f} m CD",
            "",
            f"Channel width       {self.width:.0f} m "
            f"({self.width_result['width_in_beams']:.1f} beams, "
            f"{self.width_result['lanes']}-way)",
        ]
        for name, value in self.width_result["components"].items():
            lines.append(f"   {name:<26}{value:6.1f}")
        if self.existing_bed is not None:
            lines += [
                "",
                f"Existing bed        {self.existing_bed:+.2f} m CD",
                f"Dredge depth        "
                f"{self.existing_bed - self.dredge_level:.2f} m",
                f"Top width           {self.top_width:.0f} m at 1:"
                f"{self.side_slope:g} side slopes",
                f"Volume              "
                f"{self.dredge_volume(1000.0) / 1e3:,.0f} thousand m3 per km",
            ]
        if self.warnings:
            lines += ["", "Warnings"] + [f"  - {w}" for w in self.warnings]
        return "\n".join(lines)


def design_channel(
    vessel: Vessel,
    speed: float,
    design_water_level: float,
    Hs: float = 0.0,
    Tp: float | None = None,
    wave_factor: float = 0.5,
    net_clearance: float = 0.6,
    water_level_allowance: float = 0.3,
    dredging_tolerance: float = 0.3,
    survey_tolerance: float = 0.2,
    siltation_allowance: float = 0.2,
    density_allowance: float = 0.0,
    squat_coefficient: float = 2.4,
    side_slope: float = 5.0,
    existing_bed: float | None = None,
    **width_kwargs,
) -> ChannelDesign:
    """Size an approach channel: depth from the clearance stack, width from PIANC.

    The squat depends on the water depth, which depends on the squat, so the
    depth is solved by a short fixed-point iteration rather than by guessing
    a depth and hoping.

    Extra keyword arguments go to :func:`channel_width`.
    """
    if speed < 0:
        raise ValueError(f"Speed must be non-negative, got {speed}")

    warnings: list[str] = []
    waves = wave_response_allowance(Hs, wave_factor, Tp, vessel)
    if waves.get("near_resonant"):
        warnings.append(
            f"Wave length is {waves['length_ratio']:.2f} times the vessel "
            "length, which is the worst case for vertical motion. A wave "
            f"factor above the {wave_factor:.2f} used here is likely."
        )

    # Fixed point on the depth, since the squat depends on it. The starting
    # depth is set so the first evaluation is comfortably subcritical: the
    # iteration only ever deepens, so if it starts subcritical it stays
    # there, and a shallow-draught vessel at speed does not trip the
    # critical-speed guard on a depth the design was never going to use.
    subcritical = (speed * KNOT / 0.8) ** 2 / G
    depth = max(vessel.draught + 1.0, subcritical)
    squat: dict = {}
    clearance: dict = {}
    for _ in range(80):
        # The iteration can converge downward, and a shallow-draught vessel
        # driven hard can chase it into the critical-speed region. That is a
        # real constraint on the scheme, not a numerical problem: the vessel
        # would be at the critical speed in the channel she needs. Say so,
        # with the speed that would work.
        froude = speed * KNOT / math.sqrt(G * depth)
        if froude >= 0.95:
            workable = 0.6 * math.sqrt(G * depth) / KNOT
            raise ValueError(
                f"At {speed:g} knots the depth chain converges on about "
                f"{depth:.1f} m, where the depth Froude number is "
                f"{froude:.2f}. The vessel would be at the critical speed in "
                "her own channel, and no squat formula applies. Reduce the "
                f"design speed below about {workable:.0f} knots, or fix the "
                "channel depth by another means."
            )
        squat = squat_icorels(vessel, speed, depth, squat_coefficient)
        clearance = underkeel_clearance(
            vessel, squat["squat"], waves["allowance"],
            net_clearance=net_clearance,
            water_level_allowance=water_level_allowance,
            dredging_tolerance=dredging_tolerance,
            survey_tolerance=survey_tolerance,
            siltation_allowance=siltation_allowance,
            density_allowance=density_allowance,
        )
        new_depth = clearance["required_depth"]
        if abs(new_depth - depth) < 1e-4:
            depth = new_depth
            break
        depth = new_depth

    if squat["beyond_range"]:
        warnings.append(
            f"Depth Froude number {squat['froude']:.2f} is above 0.7, where "
            "the squat formula is no longer reliable. Reduce the design "
            "speed or check with a manoeuvring simulation."
        )
    ratio = depth / vessel.draught
    if ratio < 1.1:
        warnings.append(
            f"Depth is only {ratio:.2f} times the draught. Squat and "
            "manoeuvrability both degrade sharply below about 1.1."
        )

    screening = squat_barrass(vessel, speed, depth)
    if screening["squat"] > 2.0 * squat["squat"]:
        warnings.append(
            f"Barrass screening gives {screening['squat']:.2f} m of squat "
            f"against the ICORELS {squat['squat']:.2f} m. Check which is "
            "appropriate for this channel before fixing the dredge level."
        )

    width = channel_width(vessel, **width_kwargs)
    dredge_level = design_water_level - depth

    if existing_bed is not None and existing_bed < dredge_level:
        warnings.append(
            f"The existing bed at {existing_bed:+.2f} m CD is already below "
            f"the dredge level {dredge_level:+.2f} m CD. No capital dredging "
            "is needed for depth."
        )

    return ChannelDesign(
        vessel=vessel,
        design_water_level=design_water_level,
        dredge_level=dredge_level,
        required_depth=depth,
        clearance=clearance,
        squat=squat,
        waves=waves,
        width_result=width,
        side_slope=side_slope,
        speed=speed,
        existing_bed=existing_bed,
        warnings=warnings,
    )


def turning_basin_diameter(vessel: Vessel, assisted: bool = True,
                           current: bool = False) -> dict:
    """Turning basin diameter as a multiple of the vessel length [m].

    Indicative concept-design values: 1.5 Loa where tugs or thrusters turn
    the vessel on the spot, 2.0 Loa for an unassisted turn, and a further
    half a length where a current runs through the basin. A real basin is
    confirmed by simulation, and the shape is rarely a circle.
    """
    factor = 1.5 if assisted else 2.0
    if current:
        factor += 0.5
    return {"diameter": factor * vessel.length, "factor": factor,
            "assisted": assisted}
