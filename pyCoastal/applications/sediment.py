"""
Sediment and soil: what the bed is made of, and what that costs you.

Every structure in this package sits on, in, or behind something. Until now
that something was a number typed into a signature. This module makes it a
material with properties that propagate: the grain size that decides whether
the bed moves at all, the friction angle that decides how hard the backfill
pushes on the wall, the unit weight that decides how much of that push is
soil and how much is water.

Two families of relation live here, and they are not the same subject.

Mobility
    Whether, and how fast, grains move. Grain size, fall velocity, and the
    Shields threshold. This is what gates scour: a bed that never reaches
    its threshold does not scour, whatever the wave height.
Earth pressure
    What retained soil does to a wall. Rankine and Coulomb coefficients, and
    the pressure diagram integrated over the retained height with the water
    table and any surcharge in the right places.

Sources
-------
Soulsby, R. L. (1997), Dynamics of Marine Sands. Dimensionless grain size,
    fall velocity, and the threshold of motion.

Soulsby, R. L. and Whitehouse, R. J. S. (1997), "Threshold of sediment
    motion in coastal environments". The critical Shields curve fitted here.

Rankine, W. J. M. (1857) and Coulomb, C. A. (1776), through any soil
    mechanics text. Lateral earth pressure coefficients.

CIRIA/CUR/CETMEF (2007), The Rock Manual. Typical properties for the
    granular materials in the catalogue.

Conventions
-----------
Grain sizes are metres, not millimetres, to stay consistent with the rest of
the package. Unit weights are kN/m3 and forces kN per metre run. Angles are
degrees on the way in, because that is how a geotechnical report states
them, and radians internally.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

G = 9.81
RHO_W = 1025.0
GAMMA_W = RHO_W * G / 1000.0        # kN/m3, seawater
NU = 1.19e-6                        # kinematic viscosity of seawater at 15 C

__all__ = [
    "Sediment",
    "SEDIMENTS",
    "sediment",
    "dimensionless_grain_size",
    "critical_shields",
    "fall_velocity",
    "wave_orbital_velocity",
    "wave_shields",
    "bed_mobility",
    "earth_pressure_coefficient",
    "lateral_earth_pressure",
    "lateral_earth_force",
]


# ---------------------------------------------------------------------------
# The material
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Sediment:
    """A bed or backfill material.

    Attributes
    ----------
    name : str
        For the report and the drawing.
    d50 : float
        Median grain size [m]. Zero for a cohesive material, where grain
        size is not what governs.
    specific_gravity : float
        Grain density over water density. 2.65 for quartz sand.
    porosity : float
        Voids as a fraction of total volume, in place.
    friction_angle : float
        Effective angle of shearing resistance phi' [deg]. This is the one
        number that decides how hard a backfill pushes on a wall, and it is
        the one most worth getting from a real site investigation.
    cohesion : float
        Effective cohesion c' [kPa]. Zero for anything granular.
    d90 : float, optional
        Ninety per cent passing size [m]. Defaults to 2.5 d50, a reasonable
        ratio for a moderately graded marine sand.
    description : str
        What a person would call it.
    """

    name: str
    d50: float
    specific_gravity: float = 2.65
    porosity: float = 0.40
    friction_angle: float = 32.0
    cohesion: float = 0.0
    d90: float | None = None
    description: str = ""

    def __post_init__(self) -> None:
        if self.d50 < 0:
            raise ValueError(f"Grain size must be non-negative, got {self.d50}")
        if not 1.0 < self.specific_gravity < 5.0:
            raise ValueError(
                f"Specific gravity {self.specific_gravity} is outside any real material"
            )
        if not 0.0 < self.porosity < 0.8:
            raise ValueError(f"Porosity {self.porosity} is outside 0 to 0.8")
        if not 0.0 <= self.friction_angle < 60.0:
            raise ValueError(
                f"Friction angle {self.friction_angle} is outside 0 to 60 degrees"
            )

    @property
    def relative_density(self) -> float:
        """s - 1, the buoyant density ratio that drives every mobility number."""
        return self.specific_gravity - 1.0

    @property
    def dry_unit_weight(self) -> float:
        """Unit weight of the drained material [kN/m3]."""
        return (1.0 - self.porosity) * self.specific_gravity * GAMMA_W

    @property
    def saturated_unit_weight(self) -> float:
        """Unit weight with the voids full of water [kN/m3]."""
        return self.dry_unit_weight + self.porosity * GAMMA_W

    @property
    def submerged_unit_weight(self) -> float:
        """Buoyant unit weight below the water table [kN/m3].

        This is the number that makes a submerged backfill push so much less
        hard than a drained one: roughly six kN/m3 rather than eighteen.
        The water it displaces pushes separately, and harder.
        """
        return self.saturated_unit_weight - GAMMA_W

    @property
    def cohesive(self) -> bool:
        return self.cohesion > 0.0

    def grading(self) -> float:
        """d90 / d50, the spread of the grading."""
        return (self.d90 or 2.5 * self.d50) / self.d50 if self.d50 > 0 else float("nan")

    def summary(self) -> str:
        lines = [
            f"{self.name}  ({self.description})" if self.description else self.name,
            f"  d50                {self.d50 * 1000:.3g} mm"
            if self.d50 > 0 else "  d50                cohesive, not governed by grain size",
            f"  friction angle     {self.friction_angle:.0f} deg",
            f"  cohesion           {self.cohesion:.0f} kPa",
            f"  unit weight        {self.dry_unit_weight:.1f} kN/m3 dry, "
            f"{self.saturated_unit_weight:.1f} saturated, "
            f"{self.submerged_unit_weight:.1f} submerged",
        ]
        if self.d50 > 0:
            lines.append(f"  fall velocity      {fall_velocity(self) * 1000:.1f} mm/s")
            lines.append(f"  critical Shields   {critical_shields(self):.3f}")
        return "\n".join(lines)


#: Catalogue of the materials a coastal scheme actually meets. The values are
#: typical, not measured: a real design takes them from the site
#: investigation, and the friction angle in particular moves a wall design
#: more than most people expect.
SEDIMENTS: dict[str, Sediment] = {
    "soft_clay": Sediment(
        "Soft clay", d50=0.0, specific_gravity=2.70, porosity=0.55,
        friction_angle=22.0, cohesion=15.0,
        description="normally consolidated, undrained strength governs"),
    "stiff_clay": Sediment(
        "Stiff clay", d50=0.0, specific_gravity=2.72, porosity=0.42,
        friction_angle=26.0, cohesion=40.0,
        description="overconsolidated"),
    "silt": Sediment(
        "Silt", d50=0.03e-3, specific_gravity=2.65, porosity=0.48,
        friction_angle=28.0, description="mobile at almost any wave"),
    "very_fine_sand": Sediment(
        "Very fine sand", d50=0.09e-3, porosity=0.45, friction_angle=29.0,
        description="suspends readily, high siltation"),
    "fine_sand": Sediment(
        "Fine sand", d50=0.19e-3, porosity=0.43, friction_angle=31.0,
        description="the usual beach and nearshore sand"),
    "medium_sand": Sediment(
        "Medium sand", d50=0.38e-3, porosity=0.40, friction_angle=33.0,
        description="typical dredged fill"),
    "coarse_sand": Sediment(
        "Coarse sand", d50=0.75e-3, porosity=0.38, friction_angle=35.0,
        description="good drained backfill"),
    "fine_gravel": Sediment(
        "Fine gravel", d50=6.0e-3, porosity=0.35, friction_angle=38.0,
        description="free draining"),
    "coarse_gravel": Sediment(
        "Coarse gravel", d50=30.0e-3, porosity=0.35, friction_angle=40.0,
        description="shingle beach"),
    "rock_fill": Sediment(
        "Quarry rock fill", d50=150.0e-3, porosity=0.37, friction_angle=42.0,
        description="engineered granular backfill"),
}


def sediment(key: str) -> Sediment:
    """Look a material up by key, with the options named on failure."""
    if key not in SEDIMENTS:
        raise ValueError(
            f"Unknown sediment {key!r}. Options: {sorted(SEDIMENTS)}"
        )
    return SEDIMENTS[key]


# ---------------------------------------------------------------------------
# Mobility
# ---------------------------------------------------------------------------


def _grains(material) -> Sediment:
    if isinstance(material, str):
        return sediment(material)
    return material


def dimensionless_grain_size(material, viscosity: float = NU) -> float:
    """D* = d50 [g (s - 1) / nu^2]^(1/3), Soulsby (1997).

    The single parameter that collapses the threshold of motion and the fall
    velocity across grain sizes. Below about 4 the grain is in the viscous
    range; above about 100 it is fully rough.
    """
    grains = _grains(material)
    if grains.d50 <= 0:
        raise ValueError(
            f"{grains.name} is cohesive: grain size does not govern its "
            "behaviour, and a Shields threshold is meaningless for it"
        )
    return grains.d50 * (G * grains.relative_density / viscosity**2) ** (1.0 / 3.0)


def critical_shields(material, viscosity: float = NU) -> float:
    """Critical Shields parameter, Soulsby and Whitehouse (1997)::

        theta_cr = 0.30 / (1 + 1.2 D*) + 0.055 [1 - exp(-0.020 D*)]

    A fitted curve through the Shields data that behaves at both ends,
    unlike reading a value off the original diagram.
    """
    d_star = dimensionless_grain_size(material, viscosity)
    return 0.30 / (1.0 + 1.2 * d_star) + 0.055 * (1.0 - math.exp(-0.020 * d_star))


def fall_velocity(material, viscosity: float = NU) -> float:
    """Settling velocity of a single grain [m/s], Soulsby (1997)::

        w_s = nu / d [ sqrt(10.36^2 + 1.049 D*^3) - 10.36 ]

    Valid across the whole range from silt to gravel, which is why it is
    preferred to Stokes at one end and a drag law at the other.
    """
    grains = _grains(material)
    d_star = dimensionless_grain_size(grains, viscosity)
    return (viscosity / grains.d50) * (
        math.sqrt(10.36**2 + 1.049 * d_star**3) - 10.36
    )


def wave_orbital_velocity(Hs: float, T: float, depth: float,
                          wavelength: float | None = None) -> float:
    """Near-bed orbital velocity amplitude under a linear wave [m/s].

        U_w = pi Hs / (T sinh(k h))
    """
    if Hs <= 0 or T <= 0 or depth <= 0:
        raise ValueError("Wave height, period and depth must be positive")
    if wavelength is None:
        from ..tools.wave import dispersion
        wavelength = dispersion(T, depth)
    k = 2 * math.pi / wavelength
    return math.pi * Hs / (T * math.sinh(k * depth))


def wave_shields(material, Hs: float, T: float, depth: float,
                 wavelength: float | None = None) -> dict:
    """Shields parameter under waves, and whether the bed is moving.

    Uses the Swart wave friction factor for a rough turbulent bed, with the
    orbital excursion over the Nikuradse roughness of 2.5 d50::

        f_w = exp[5.213 (A / k_s)^-0.194 - 5.977],  capped at 0.3

    Returns
    -------
    dict
        The orbital velocity and excursion, the friction factor, the Shields
        parameter, its critical value, and ``mobile``.
    """
    grains = _grains(material)
    u_w = wave_orbital_velocity(Hs, T, depth, wavelength)
    excursion = u_w * T / (2 * math.pi)
    roughness = 2.5 * grains.d50

    ratio = max(excursion / roughness, 1.0)
    f_w = min(math.exp(5.213 * ratio**-0.194 - 5.977), 0.3)
    shear = 0.5 * RHO_W * f_w * u_w**2
    theta = shear / ((grains.specific_gravity - 1.0) * RHO_W * G * grains.d50)
    theta_cr = critical_shields(grains)

    return {
        "orbital_velocity": u_w,
        "excursion": excursion,
        "friction_factor": f_w,
        "shear_stress": shear,
        "shields": theta,
        "critical_shields": theta_cr,
        "mobility": theta / theta_cr if theta_cr > 0 else float("inf"),
        "mobile": theta > theta_cr,
    }


def bed_mobility(material, Hs: float, T: float, depth: float) -> dict:
    """Whether the bed at a structure is live, and by how much.

    Scour relations are almost all live-bed results. Applying one to a bed
    that never reaches its threshold predicts a hole that will not form.
    This is the gate the scour functions use.
    """
    grains = _grains(material)
    if grains.cohesive:
        return {
            "mobile": False, "regime": "cohesive",
            "note": (f"{grains.name} is cohesive. Scour is governed by "
                     "erodibility and duration, not by a Shields threshold, "
                     "and needs a site-specific erosion test."),
            "mobility": float("nan"),
        }
    result = wave_shields(grains, Hs, T, depth)
    if result["mobile"]:
        regime = "live bed" if result["mobility"] > 2.0 else "near threshold"
    else:
        regime = "clear water"
    result["regime"] = regime
    result["note"] = {
        "live bed": "Bed is in motion away from the structure; live-bed "
                    "scour relations apply.",
        "near threshold": "Bed is only just mobile. Scour will develop "
                          "slowly and the equilibrium depth is uncertain.",
        "clear water": "Bed is below its threshold in the approach flow. "
                       "Scour can still occur where the structure amplifies "
                       "the flow, but live-bed relations will overstate it.",
    }[regime]
    return result


# ---------------------------------------------------------------------------
# Earth pressure
# ---------------------------------------------------------------------------


def earth_pressure_coefficient(friction_angle: float, kind: str = "active",
                               wall_friction: float = 0.0,
                               backslope: float = 0.0) -> float:
    """Lateral earth pressure coefficient.

    Parameters
    ----------
    friction_angle : float
        Effective angle of shearing resistance phi' [deg].
    kind : str
        "active" for a wall free to move away from the soil, "at_rest" for
        one that cannot, "passive" for one pushed into it.
    wall_friction : float
        Angle of friction on the wall face delta [deg]. Non-zero switches
        the active case from Rankine to Coulomb, which is the honest choice
        for a rough concrete face and gives a smaller force.
    backslope : float
        Slope of the retained surface [deg], for the Rankine sloping-backfill
        form.

    Notes
    -----
    Which coefficient applies is a question about movement, not about soil.
    A gravity seawall on a rubble bedding can move the millimetre or two
    that mobilises the active state; one cast against rock, or restrained by
    a slab, cannot, and then at-rest governs and the force is roughly half
    as large again. Choosing "active" because it is smaller is the most
    common way a retaining structure is under-designed.
    """
    if kind not in ("active", "at_rest", "passive"):
        raise ValueError(f"Unknown earth pressure kind {kind!r}")
    if not 0.0 <= friction_angle < 60.0:
        raise ValueError(f"Friction angle {friction_angle} is outside 0 to 60")

    phi = math.radians(friction_angle)

    if kind == "at_rest":
        # Jaky, for normally consolidated soil.
        return 1.0 - math.sin(phi)

    if abs(backslope) > 1e-9:
        beta = math.radians(backslope)
        if abs(beta) >= phi:
            raise ValueError(
                f"A backslope of {backslope} deg cannot stand in a soil with "
                f"phi' = {friction_angle} deg"
            )
        root = math.sqrt(math.cos(beta) ** 2 - math.cos(phi) ** 2)
        factor = (math.cos(beta) - root) / (math.cos(beta) + root)
        return math.cos(beta) * factor if kind == "active" else \
            math.cos(beta) * (math.cos(beta) + root) / (math.cos(beta) - root)

    if abs(wall_friction) > 1e-9:
        delta = math.radians(wall_friction)
        if kind == "active":
            numerator = math.cos(phi) ** 2
            denominator = math.cos(delta) * (
                1.0 + math.sqrt(math.sin(phi + delta) * math.sin(phi)
                                / math.cos(delta))
            ) ** 2
            return numerator / denominator
        numerator = math.cos(phi) ** 2
        denominator = math.cos(delta) * (
            1.0 - math.sqrt(math.sin(phi + delta) * math.sin(phi)
                            / math.cos(delta))
        ) ** 2
        return numerator / denominator

    if kind == "active":
        return (1.0 - math.sin(phi)) / (1.0 + math.sin(phi))
    return (1.0 + math.sin(phi)) / (1.0 - math.sin(phi))


def lateral_earth_pressure(material, height: float, water_table: float = 0.0,
                           surcharge: float = 0.0, kind: str = "active",
                           wall_friction: float = 0.0, points: int = 201) -> dict:
    """Pressure diagram on the back of a wall, effective stress and water apart.

    Parameters
    ----------
    height : float
        Retained height H [m], measured from the top of the retained surface
        down to the base of the wall.
    water_table : float
        Depth of the water table below the retained surface [m]. Zero means
        the backfill is saturated to the top, which is the condition behind
        a seawall with a blocked drain and is the one that breaks walls.
    surcharge : float
        Uniform surcharge on the retained surface [kPa].
    kind, wall_friction
        Passed to :func:`earth_pressure_coefficient`.

    Returns
    -------
    dict
        ``depth`` and the three pressure arrays (``effective``, ``pore``,
        ``total``) in kPa, plus the coefficient used.

    Notes
    -----
    Below the water table the soil pushes with its *submerged* unit weight
    and the water pushes separately with its full hydrostatic gradient. The
    sum is larger than the dry soil alone would give, because water has no
    friction angle to lean on: it presses with K = 1. This is why drainage
    behind a seawall is a structural matter and not a detail.
    """
    grains = _grains(material)
    if height <= 0:
        raise ValueError(f"Retained height must be positive, got {height}")
    if water_table < 0:
        raise ValueError(f"Water table depth must be non-negative, got {water_table}")
    if surcharge < 0:
        raise ValueError(f"Surcharge must be non-negative, got {surcharge}")
    if points < 3:
        raise ValueError(f"Need at least three points, got {points}")

    K = earth_pressure_coefficient(grains.friction_angle, kind, wall_friction)
    z = np.linspace(0.0, height, points)
    dry_depth = np.minimum(z, water_table)
    wet_depth = np.maximum(z - water_table, 0.0)

    vertical_effective = (surcharge
                          + grains.dry_unit_weight * dry_depth
                          + grains.submerged_unit_weight * wet_depth)
    horizontal_effective = K * vertical_effective

    if grains.cohesive:
        # Cohesion reduces the active pressure and can put the top of the
        # wall into tension. Soil cannot pull, so the diagram is cut off
        # there: the tension crack is real and fills with water.
        horizontal_effective = horizontal_effective - 2.0 * grains.cohesion * math.sqrt(K)
        horizontal_effective = np.maximum(horizontal_effective, 0.0)

    pore = GAMMA_W * wet_depth
    return {
        "depth": z,
        "effective": horizontal_effective,
        "pore": pore,
        "total": horizontal_effective + pore,
        "K": K,
        "kind": kind,
        "sediment": grains,
    }


def lateral_earth_force(material, height: float, water_table: float = 0.0,
                        surcharge: float = 0.0, kind: str = "active",
                        wall_friction: float = 0.0, points: int = 401) -> dict:
    """Total horizontal force from retained soil and water [kN/m].

    Returns
    -------
    dict
        ``soil`` and ``water`` forces and the ``total``, the lever ``arm``
        of the total above the base of the wall, and the pressure diagram
        that produced them.

    Notes
    -----
    The split matters. The soil force scales with the friction angle and can
    be argued down with a better backfill; the water force cannot be argued
    with at all, only drained away.
    """
    diagram = lateral_earth_pressure(material, height, water_table, surcharge,
                                     kind, wall_friction, points)
    z = diagram["depth"]
    arm_from_base = height - z

    soil = float(np.trapezoid(diagram["effective"], z))
    water = float(np.trapezoid(diagram["pore"], z))
    total = soil + water
    moment = float(np.trapezoid(diagram["total"] * arm_from_base, z))

    return {
        "soil": soil,
        "water": water,
        "total": total,
        "moment": moment,
        "arm": moment / total if total > 0 else 0.0,
        "K": diagram["K"],
        "kind": kind,
        "diagram": diagram,
        "water_fraction": water / total if total > 0 else 0.0,
    }
