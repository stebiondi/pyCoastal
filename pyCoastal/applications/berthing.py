"""
Berthing energy and fender selection.

A ship comes alongside carrying kinetic energy, and something has to absorb
it. Get the fender too soft and the ship reaches the quay; too hard and the
fender survives while the hull plating does not. The whole design is the
arithmetic between those two failures.

PIANC's formulation is a chain of four factors on the kinetic energy, and
the interesting thing about it is that three of the four reduce the answer.
Only the added mass of the water the ship drags with it increases it.
Between them they typically leave the fender somewhere between a half and
four fifths of the energy the ship arrived with, and every one of those
reductions is a modelling assumption that has to be defensible.

    E = 0.5 M V^2 Cm Ce Cs Cc

The one that is neither a reduction nor physics is the abnormal berthing
factor, applied afterwards. It covers the day something goes wrong: a
parted tug line, an engine that does not go astern, a master misjudging the
approach in a cross-current. PIANC sets it between 1.25 and 2.0 depending
on how much worse than usual that day can be, and for many berths it is the
single largest number in the calculation.

What this module is not
-----------------------
Fender performance here is a scaling model, not a catalogue. A real
selection is made against the manufacturer's tested energy and reaction
curves at the design temperature, angle and velocity, because those curves
are what is guaranteed and they differ materially between makers for the
same nominal size. :func:`select_fender` sizes the fender you should be
asking for; it does not choose a product.

References
----------
PIANC (2002). Guidelines for the design of fender systems. Report of
Working Group 33, Maritime Navigation Commission.

Vasco Costa, F. (1964). The berthing ship: the effect of impact on the
design of fenders and other structures. The Dock and Harbour Authority.

Brolsma, J.U., Hirs, J.A. and Langeveld, J.M. (1977). On fender design and
berthing velocities. PIANC 24th Congress.

BS 6349-4 (2014). Maritime works. Code of practice for design of fendering
and mooring systems. British Standards Institution.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .channel import Vessel

__all__ = [
    "RHO_SEAWATER",
    "BERTHING_VELOCITY",
    "ABNORMAL_FACTOR",
    "HULL_PRESSURE_LIMIT",
    "BERTH_CONFIGURATION",
    "berthing_velocity",
    "added_mass_factor",
    "eccentricity_factor",
    "berthing_energy",
    "abnormal_energy",
    "FenderFamily",
    "CONE_FENDER",
    "select_fender",
    "hull_pressure",
    "fender_spacing",
    "BerthDesign",
    "design_berth",
]

RHO_SEAWATER = 1025.0

#: Indicative design berthing velocities [m/s], normal to the berth.
#:
#: Bands by displacement and by how hard the approach is. These are the
#: shape of Brolsma's curves rather than the curves themselves: the real
#: design value comes off those, against the actual displacement, and
#: depends on whether tugs assist. Treat these as a starting point and a
#: sanity check, not as the answer.
#:
#: Velocity is squared in the energy, so this is the most expensive
#: assumption in the calculation. Doubling it quadruples the fender.
BERTHING_VELOCITY = {
    "easy_sheltered": {"small": 0.20, "medium": 0.15, "large": 0.10},
    "difficult_sheltered": {"small": 0.30, "medium": 0.20, "large": 0.15},
    "easy_exposed": {"small": 0.40, "medium": 0.30, "large": 0.20},
    "good_exposed": {"small": 0.50, "medium": 0.40, "large": 0.25},
    "difficult_exposed": {"small": 0.80, "medium": 0.60, "large": 0.40},
}

#: PIANC abnormal berthing factors, by what is being berthed.
#:
#: The allowance for the berthing that goes wrong. Small vessels get the
#: larger factors: they are handled less carefully, often without tugs, and
#: the consequence of a hard landing is a bigger fraction of their normal
#: energy.
ABNORMAL_FACTOR = {
    "tanker_large": 1.25,
    "tanker_small": 1.75,
    "bulk_carrier": 1.50,
    "container": 1.50,
    "general_cargo": 1.75,
    "ro_ro": 2.00,
    "ferry": 2.00,
    "tug_workboat": 2.00,
}

#: Allowable hull contact pressure [kN/m2].
#:
#: The limit that decides the fender panel, and the one most often found
#: too late. A fender sized only on energy can easily present a reaction
#: over a small panel that the side shell cannot take.
HULL_PRESSURE_LIMIT = {
    "tanker_large": 150.0,
    "tanker_small": 200.0,
    "bulk_carrier": 200.0,
    "container": 400.0,
    "general_cargo": 400.0,
    "ro_ro": 400.0,
    "ferry": 400.0,
    "tug_workboat": 700.0,
}

#: Berth configuration factor Cc.
#:
#: A solid quay traps a cushion of water between hull and wall that takes
#: some of the energy; an open piled deck lets it through and takes none.
BERTH_CONFIGURATION = {
    "solid_quay": 0.80,
    "semi_solid": 0.90,
    "open_piled": 1.00,
}


def _size_band(displacement: float) -> str:
    """Which displacement band a vessel falls in [tonnes]."""
    if displacement < 10_000:
        return "small"
    if displacement < 50_000:
        return "medium"
    return "large"


def berthing_velocity(vessel: Vessel, condition: str = "easy_sheltered") -> dict:
    """Indicative design berthing velocity normal to the berth [m/s].

    Raises
    ------
    ValueError
        If the condition is not one of :data:`BERTHING_VELOCITY`.
    """
    if condition not in BERTHING_VELOCITY:
        raise ValueError(
            f"Unknown berthing condition {condition!r}. "
            f"Options: {sorted(BERTHING_VELOCITY)}")
    band = _size_band(vessel.displacement)
    return {
        "velocity": BERTHING_VELOCITY[condition][band],
        "band": band,
        "condition": condition,
        "displacement": vessel.displacement,
    }


def added_mass_factor(vessel: Vessel, depth: float | None = None) -> dict:
    """Virtual mass coefficient Cm, Vasco Costa (1964)::

        Cm = 1 + 2 D / B

    A ship moving sideways drags a body of water with it, and that water
    has to be stopped too. The shallower the berth the more of it there is,
    which is why ``Cm`` is written on the draught to beam ratio: a deeply
    laden ship in a tight berth carries proportionally more.

    This is the only one of the four factors that makes the energy larger.

    Parameters
    ----------
    depth : float, optional
        Water depth at the berth [m]. Used only to warn: below about 1.1
        draughts the water has nowhere to go and Vasco Costa's form starts
        to understate the added mass.
    """
    cm = 1.0 + 2.0 * vessel.draught / vessel.beam
    note = ""
    if depth is not None:
        if depth <= vessel.draught:
            raise ValueError(
                f"The berth is {depth} m deep and the ship draws "
                f"{vessel.draught} m")
        clearance = depth / vessel.draught
        if clearance < 1.1:
            note = (
                f"Underkeel clearance is {100 * (clearance - 1):.0f}% of the "
                "draught. Below about 10% the displaced water cannot escape "
                "beneath the hull and the added mass grows faster than this "
                "relation allows; take Cm from a berth-specific study.")
    return {"Cm": cm, "note": note,
            "draught_beam_ratio": vessel.draught / vessel.beam}


def eccentricity_factor(vessel: Vessel, contact_distance: float | None = None,
                        approach_angle: float = 90.0) -> dict:
    """Eccentricity coefficient Ce.

    A ship rarely arrives flat against the berth. It touches at one point,
    usually a quarter of its length from the bow, and then rotates about
    that point. The rotation carries away energy the fender never sees::

        Ce = (K^2 + R^2 cos^2 g) / (K^2 + R^2)
        K  = (0.19 Cb + 0.11) Lpp

    where ``R`` is the distance along the berth from the contact point to
    the ship's centre of mass and ``g`` is the angle between the approach
    velocity and the line joining them.

    Parameters
    ----------
    contact_distance : float, optional
        ``R`` [m]. Defaults to the quarter point, ``Lpp/4``, which is the
        usual design assumption for a ship coming alongside under control.
        Zero means the ship lands flat on its midships and nothing is
        carried away by rotation, which gives ``Ce = 1``.
    approach_angle : float
        ``g`` in degrees. 90 is the standard assumption, the velocity being
        normal to the berth.
    """
    Lpp = vessel.length_pp
    K = (0.19 * vessel.block_coefficient + 0.11) * Lpp
    R = 0.25 * Lpp if contact_distance is None else contact_distance
    if R < 0:
        raise ValueError(f"Contact distance cannot be negative, got {R}")

    g = math.radians(approach_angle)
    ce = (K**2 + R**2 * math.cos(g) ** 2) / (K**2 + R**2)

    return {"Ce": ce, "K": K, "R": R, "approach_angle": approach_angle,
            "quarter_point": contact_distance is None}


def berthing_energy(vessel: Vessel, velocity: float,
                    contact_distance: float | None = None,
                    approach_angle: float = 90.0,
                    softness: float = 1.0,
                    configuration: str = "open_piled",
                    depth: float | None = None) -> dict:
    """Normal berthing energy [kNm], PIANC::

        E = 0.5 M V^2 Cm Ce Cs Cc

    Returns every factor as well as the product, because the product on its
    own tells a reviewer nothing about which assumption to argue with.

    Parameters
    ----------
    velocity : float
        Approach velocity normal to the berth [m/s]. Squared, so this is
        the assumption worth the most scrutiny.
    softness : float
        Cs. 1.0 for a soft fender, which is nearly all of them; 0.9 where
        the fender is stiff enough that the hull deflects with it.
    configuration : str
        Keys :data:`BERTH_CONFIGURATION`.
    """
    if velocity <= 0:
        raise ValueError(f"Berthing velocity must be positive, got {velocity}")
    if not 0.9 <= softness <= 1.0:
        raise ValueError(f"Softness factor must be 0.9 to 1.0, got {softness}")
    if configuration not in BERTH_CONFIGURATION:
        raise ValueError(
            f"Unknown berth configuration {configuration!r}. "
            f"Options: {sorted(BERTH_CONFIGURATION)}")

    mass = vessel.displacement * 1000.0        # tonnes to kg
    added = added_mass_factor(vessel, depth)
    eccentric = eccentricity_factor(vessel, contact_distance, approach_angle)
    cc = BERTH_CONFIGURATION[configuration]

    kinetic = 0.5 * mass * velocity**2         # joules
    energy = kinetic * added["Cm"] * eccentric["Ce"] * softness * cc

    return {
        "energy": energy / 1000.0,             # kNm
        "kinetic": kinetic / 1000.0,
        "Cm": added["Cm"],
        "Ce": eccentric["Ce"],
        "Cs": softness,
        "Cc": cc,
        "mass": mass,
        "velocity": velocity,
        "retained_fraction": energy / kinetic,
        "added_mass": added,
        "eccentricity": eccentric,
        "configuration": configuration,
    }


def abnormal_energy(normal: float, vessel_class: str = "container",
                    factor: float | None = None) -> dict:
    """The energy the fender is actually designed for [kNm].

    PIANC's abnormal factor covers the berthing that goes wrong rather than
    the one that goes normally. It is a multiplier on an already-reduced
    number and is frequently the largest single term in the chain, so it is
    reported separately rather than folded in.
    """
    if normal <= 0:
        raise ValueError(f"Normal energy must be positive, got {normal}")
    if factor is None:
        if vessel_class not in ABNORMAL_FACTOR:
            raise ValueError(
                f"Unknown vessel class {vessel_class!r}. "
                f"Options: {sorted(ABNORMAL_FACTOR)}")
        factor = ABNORMAL_FACTOR[vessel_class]
    if factor < 1.0:
        raise ValueError(f"Abnormal factor cannot be below 1, got {factor}")

    return {"energy": normal * factor, "factor": factor,
            "vessel_class": vessel_class, "normal": normal}


# ---------------------------------------------------------------------------
# Fenders
# ---------------------------------------------------------------------------


@dataclass
class FenderFamily:
    """A geometrically similar range of fenders.

    Within one family and one rubber grade, performance scales with size:
    energy absorbed goes with the volume of rubber and so with the cube of
    the height, while the reaction goes with the cross-section and so with
    the square::

        E = E0 (H/H0)^3        R = R0 (H/H0)^2

    That is why a fender chosen to absorb twice the energy pushes back only
    about 1.6 times as hard, and why the answer to a too-high reaction is
    usually a bigger fender rather than a smaller one.

    The reference values are a mid-grade cone fender and are indicative.
    Substitute the manufacturer's own to size against a real product.
    """

    name: str = "Cone fender, mid grade"
    reference_height: float = 1.0
    reference_energy: float = 500.0        # kNm at rated deflection
    reference_reaction: float = 1000.0     # kN at rated deflection
    deflection: float = 0.72               # fraction of height at rating
    heights: tuple = (0.3, 0.4, 0.5, 0.65, 0.8, 1.0, 1.2, 1.4, 1.6, 2.0, 2.5)

    def __post_init__(self) -> None:
        if self.reference_height <= 0:
            raise ValueError("Reference height must be positive")
        if self.reference_energy <= 0 or self.reference_reaction <= 0:
            raise ValueError("Reference energy and reaction must be positive")
        if not 0 < self.deflection < 1:
            raise ValueError("Deflection must be a fraction in (0,1)")
        if not self.heights:
            raise ValueError("A family needs at least one size")

    def energy(self, height: float) -> float:
        """Rated energy of one size [kNm]."""
        return self.reference_energy * (height / self.reference_height) ** 3

    def reaction(self, height: float) -> float:
        """Rated reaction of one size [kN]."""
        return self.reference_reaction * (height / self.reference_height) ** 2

    def height_for(self, energy: float) -> float:
        """The height that would absorb exactly this energy [m]."""
        if energy <= 0:
            raise ValueError("Energy must be positive")
        return self.reference_height * (energy / self.reference_energy) ** (1 / 3)


#: A typical mid-grade cone fender range.
CONE_FENDER = FenderFamily()


def select_fender(energy: float, family: FenderFamily = CONE_FENDER) -> dict:
    """Smallest standard size in the family that absorbs ``energy`` [kNm].

    Returns the chosen size, its rated energy and reaction, and how much of
    its capacity the design actually uses. A fender working at 40% of its
    rating is oversized and stiff, and will hand the hull a reaction it did
    not need to take.
    """
    if energy <= 0:
        raise ValueError(f"Energy must be positive, got {energy}")

    exact = family.height_for(energy)
    fits = [h for h in sorted(family.heights) if family.energy(h) >= energy]

    if not fits:
        largest = max(family.heights)
        return {
            "height": None,
            "exact_height": exact,
            "rated_energy": family.energy(largest),
            "reaction": family.reaction(largest),
            "utilisation": energy / family.energy(largest),
            "adequate": False,
            "note": (
                f"No size in this family reaches {energy:.0f} kNm; the "
                f"largest, {largest:.2f} m, absorbs "
                f"{family.energy(largest):.0f} kNm. Use two fenders in "
                "contact, a larger family, or a harder grade."),
        }

    height = fits[0]
    rated = family.energy(height)
    return {
        "height": height,
        "exact_height": exact,
        "rated_energy": rated,
        "reaction": family.reaction(height),
        "utilisation": energy / rated,
        "adequate": True,
        "deflection": family.deflection * height,
        "note": "",
    }


def hull_pressure(reaction: float, panel_width: float, panel_height: float,
                  vessel_class: str = "container") -> dict:
    """Contact pressure on the side shell [kN/m2].

    The check that sizes the panel rather than the rubber. A fender chosen
    on energy alone presents its reaction over whatever area happens to be
    there, and for a tanker that limit is a quarter of a container ship's.
    """
    if reaction <= 0:
        raise ValueError("Reaction must be positive")
    if panel_width <= 0 or panel_height <= 0:
        raise ValueError("Panel dimensions must be positive")
    if vessel_class not in HULL_PRESSURE_LIMIT:
        raise ValueError(
            f"Unknown vessel class {vessel_class!r}. "
            f"Options: {sorted(HULL_PRESSURE_LIMIT)}")

    area = panel_width * panel_height
    pressure = reaction / area
    limit = HULL_PRESSURE_LIMIT[vessel_class]

    return {
        "pressure": pressure,
        "limit": limit,
        "area": area,
        "utilisation": pressure / limit,
        "acceptable": pressure <= limit,
        "required_area": reaction / limit,
    }


def fender_spacing(vessel: Vessel, spacing: float, projection: float,
                   bow_radius: float | None = None,
                   smallest_vessel: Vessel | None = None,
                   clearance: float = 0.15) -> dict:
    """Whether a ship can touch the quay between two fenders.

    Two checks, and a berth has to pass both.

    The geometric one: a hull is curved, so between two fenders it reaches
    closer to the wall than at them. With the fenders compressed, the
    remaining standoff has to exceed the sagitta of the hull across the
    gap::

        spacing <= 2 sqrt(Rb^2 - (Rb - p + c)^2)

    The practical one: the smallest ship using the berth has to reach two
    fenders at once, or it will sit on one and pivot. The usual limit is
    about 0.15 of its length between perpendiculars.

    Parameters
    ----------
    projection : float
        Standoff from the quay face to the hull with the fender at its
        design deflection [m].
    bow_radius : float, optional
        Radius of the hull curvature in plan at the point of contact [m].
        Left out, the contact is taken on the parallel midbody, which is
        straight, so the geometric check cannot bind and the vessel length
        rule governs. Supply a radius for the end fenders, where the bow or
        stern flare curves away from the quay and a ship can tuck in behind
        a fender that a straight hull could not.
    smallest_vessel : Vessel, optional
        The smallest ship expected to use the berth. The practical rule is
        about *that* ship reaching two fenders, not the design one, so
        leaving this out uses the design vessel and gives a limit that is
        too generous for a berth with mixed traffic.
    clearance : float
        Gap that must remain between hull and structure [m].
    """
    if spacing <= 0 or projection <= 0:
        raise ValueError("Spacing and projection must be positive")
    if clearance < 0:
        raise ValueError("Clearance cannot be negative")

    standoff = projection - clearance

    if bow_radius is None:
        # Parallel midbody: the hull is straight here, so it cannot reach
        # between two fenders however far apart they are.
        Rb = None
        geometric = math.inf
    else:
        Rb = bow_radius
        if Rb <= 0:
            raise ValueError("Bow radius must be positive")
        if standoff <= 0:
            geometric = 0.0
        elif standoff >= Rb:
            geometric = math.inf      # the curve cannot reach past the fender
        else:
            geometric = 2.0 * math.sqrt(Rb**2 - (Rb - standoff) ** 2)

    reference = smallest_vessel or vessel
    practical = 0.15 * reference.length_pp

    limit = min(geometric, practical)
    return {
        "spacing": spacing,
        "geometric_limit": geometric,
        "practical_limit": practical,
        "limit": limit,
        "acceptable": spacing <= limit + 1e-9,
        "bow_radius": Rb,
        "standoff": standoff,
        "reference_vessel": reference.name,
        "midbody": bow_radius is None,
        "governing": ("hull curvature" if geometric < practical
                      else "vessel length"),
    }


# ---------------------------------------------------------------------------
# The berth
# ---------------------------------------------------------------------------


@dataclass
class BerthDesign:
    """The outcome of :func:`design_berth`."""

    vessel: Vessel
    velocity: float
    normal: dict
    abnormal: dict
    fender: dict
    panel: dict
    pressure: dict
    spacing: dict
    family: FenderFamily
    notes: list[str] = field(default_factory=list)

    @property
    def adequate(self) -> bool:
        """Whether the berth passes energy, hull pressure and spacing."""
        return bool(self.fender["adequate"]
                    and self.pressure["acceptable"]
                    and self.spacing["acceptable"])

    @property
    def energy(self) -> float:
        """The design energy, which is the abnormal one [kNm]."""
        return self.abnormal["energy"]


def design_berth(vessel: Vessel,
                 velocity: float | None = None,
                 condition: str = "easy_sheltered",
                 vessel_class: str = "container",
                 configuration: str = "open_piled",
                 depth: float | None = None,
                 contact_distance: float | None = None,
                 approach_angle: float = 90.0,
                 softness: float = 1.0,
                 abnormal_factor: float | None = None,
                 spacing: float | None = None,
                 smallest_vessel: Vessel | None = None,
                 bow_radius: float | None = None,
                 clearance: float = 0.15,
                 panel_aspect: tuple[float, float] = (1.2, 2.0),
                 family: FenderFamily = CONE_FENDER) -> BerthDesign:
    """Size a fender for a berth, and check what it does to the hull.

    The chain, in order: kinetic energy, the four PIANC factors, the
    abnormal allowance, a fender that absorbs it, the reaction that fender
    hands back, the panel needed to spread that reaction to something the
    side shell can take, and the spacing that stops the ship touching
    between fenders.

    Each step can fail on its own and the failures are different. Too small
    a fender lets the ship reach the quay. Too small a panel dents the hull.
    Too wide a spacing does both, at a point where nothing is measuring.

    Parameters
    ----------
    velocity : float, optional
        Approach velocity [m/s]. Taken from :data:`BERTHING_VELOCITY` for
        the ``condition`` if not given, which is a starting point rather
        than a design value.
    panel_aspect : tuple
        Panel width and height as multiples of the fender height. The
        default is a common proportion; a panel is cheap next to a hull
        repair, so widen it rather than accept a marginal pressure.

    Returns
    -------
    BerthDesign
    """
    if velocity is None:
        picked = berthing_velocity(vessel, condition)
        velocity = picked["velocity"]
    else:
        picked = None

    normal = berthing_energy(
        vessel, velocity, contact_distance=contact_distance,
        approach_angle=approach_angle, softness=softness,
        configuration=configuration, depth=depth)
    abnormal = abnormal_energy(normal["energy"], vessel_class, abnormal_factor)
    fender = select_fender(abnormal["energy"], family)

    height = fender["height"] or max(family.heights)
    panel_width = panel_aspect[0] * height
    panel_height = panel_aspect[1] * height
    panel = {"width": panel_width, "height": panel_height,
             "aspect": panel_aspect}

    pressure = hull_pressure(fender["reaction"], panel_width, panel_height,
                             vessel_class)

    projection = height * (1.0 - family.deflection) + 0.3   # panel thickness
    if spacing is None:
        spacing = 0.12 * (smallest_vessel or vessel).length_pp
    gaps = fender_spacing(vessel, spacing, projection, bow_radius=bow_radius,
                          smallest_vessel=smallest_vessel, clearance=clearance)

    notes = _berth_notes(vessel, velocity, picked, normal, abnormal, fender,
                         panel, pressure, gaps, vessel_class, family)

    return BerthDesign(vessel=vessel, velocity=velocity, normal=normal,
                       abnormal=abnormal, fender=fender, panel=panel,
                       pressure=pressure, spacing=gaps, family=family,
                       notes=notes)


def _berth_notes(vessel, velocity, picked, normal, abnormal, fender, panel,
                 pressure, gaps, vessel_class, family) -> list[str]:
    """The findings, in the order a reviewer would work through them."""
    notes = []

    notes.append(
        f"{vessel.name}: {vessel.length:.0f} m by {vessel.beam:.1f} m, "
        f"{vessel.draught:.1f} m draught, "
        f"{vessel.displacement / 1000:.0f} thousand tonnes displacement.")

    if picked is not None:
        notes.append(
            f"Berthing at {velocity:.2f} m/s, the indicative value for a "
            f"{picked['band']} vessel in "
            f"{picked['condition'].replace('_', ' ')} conditions. Velocity "
            "is squared here, so this is the assumption to confirm first: "
            "take it from Brolsma against the actual displacement and tug "
            "assistance before it is relied on.")
    else:
        notes.append(
            f"Berthing at {velocity:.2f} m/s, as specified. Velocity is "
            "squared in the energy, so it carries more of the answer than "
            "anything else here.")

    notes.append(
        f"Factors: Cm {normal['Cm']:.2f} adds the water the ship drags, "
        f"Ce {normal['Ce']:.2f} takes away what the ship rotates out, "
        f"Cs {normal['Cs']:.2f} and Cc {normal['Cc']:.2f} take away a "
        f"little more. Net, the fender sees "
        f"{100 * normal['retained_fraction']:.0f}% of the "
        f"{normal['kinetic']:.0f} kNm the ship arrived with.")

    if normal["added_mass"]["note"]:
        notes.append(normal["added_mass"]["note"])

    if normal["eccentricity"]["quarter_point"]:
        notes.append(
            "Eccentricity is taken at the quarter point, the usual design "
            "assumption. A ship that lands flat on its midships rotates "
            "about nothing and hands the fender all of it: Ce becomes 1 and "
            f"the energy rises by {1 / normal['Ce']:.2f} times.")

    notes.append(
        f"Abnormal factor {abnormal['factor']:.2f} for a "
        f"{vessel_class.replace('_', ' ')}, taking the design energy from "
        f"{abnormal['normal']:.0f} to {abnormal['energy']:.0f} kNm. This is "
        "the allowance for the berthing that goes wrong, and it is the "
        "largest single term in this calculation.")

    if fender["adequate"]:
        notes.append(
            f"{family.name}, {fender['height']:.2f} m: "
            f"{fender['rated_energy']:.0f} kNm rated against "
            f"{abnormal['energy']:.0f} kNm required, so it works at "
            f"{100 * fender['utilisation']:.0f}% of capacity and pushes "
            f"back {fender['reaction']:.0f} kN.")
        if fender["utilisation"] < 0.5:
            notes.append(
                "Under half its rating. An oversized fender is a stiff one, "
                "and it will hand the hull a reaction the design never "
                "needed. Check the next size down against the abnormal case "
                "before accepting this.")
    else:
        notes.append(fender["note"])

    if pressure["acceptable"]:
        notes.append(
            f"Hull pressure {pressure['pressure']:.0f} kN/m2 over a "
            f"{panel['width']:.1f} by {panel['height']:.1f} m panel, within "
            f"the {pressure['limit']:.0f} kN/m2 allowed for this class.")
    else:
        notes.append(
            f"Hull pressure {pressure['pressure']:.0f} kN/m2 exceeds the "
            f"{pressure['limit']:.0f} kN/m2 this class can take. The panel "
            f"needs at least {pressure['required_area']:.1f} m2 against the "
            f"{pressure['area']:.1f} m2 it has. Widen the panel: it is far "
            "cheaper than the alternative, which is repairing side shell.")

    if gaps["acceptable"]:
        notes.append(
            f"Fenders at {gaps['spacing']:.1f} m centres, inside the "
            f"{gaps['limit']:.1f} m limit set by {gaps['governing']} for "
            f"{gaps['reference_vessel']}."
            + (" Contact is on the parallel midbody, which is straight, so "
               "only the vessel length rule binds; check the end fenders "
               "separately with a bow radius."
               if gaps["midbody"] else ""))
    else:
        notes.append(
            f"Fenders at {gaps['spacing']:.1f} m centres exceed the "
            f"{gaps['limit']:.1f} m limit set by {gaps['governing']}. The "
            "hull will reach the structure between them, at a point where "
            "no fender is measuring and no one is watching.")

    notes.append(
        "Fender performance here is a scaling model within one family, not "
        "a catalogue. Size the fender you are asking for from this, then "
        "select against the manufacturer's tested curves at the design "
        "temperature, angle and velocity, which is what they guarantee.")

    return notes
