"""
Vertical seawall design: wave pressures, stability, scour and toe protection.

This is the design half of the seawall product. Give it a design condition
and a set of choices, and it returns a fully dimensioned section: crest
level set by overtopping, base width set by sliding and overturning under
Goda pressures, toe level set by scour, and toe stone sized for stability.
:mod:`pyCoastal.applications.sections` turns the result into a drawing and a
bill of quantities.

Sources
-------
Goda, Y. (1974, 2010), Random Seas and Design of Maritime Structures.
    Wave pressure distribution on a vertical wall, and the extension to
    impulsive conditions by Takahashi et al. (1994).
EurOtop (2018), Manual on wave overtopping of sea defences, 2nd ed.
    Crest level for a tolerable mean discharge.
Xie, S. L. (1981), Scouring patterns in front of vertical breakwaters,
    Delft University of Technology. Scour depth at a vertical wall.
Van der Meer, J. W. (1998), in Rock Manual (CIRIA/CUR/CETMEF, 2007).
    Toe berm stone stability.

Conventions
-----------
Levels are metres above chart datum and increase upward, matching the
package's z convention. Distances are metres seaward-positive from the wall
face unless stated. Forces are kN per metre run of wall.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..tools.wave import dispersion
from .structures import (
    DesignConditions,
    TOLERABLE_DISCHARGE,
    overtopping_vertical,
    overtopping_with_uncertainty,
    required_crest_freeboard,
)

G = 9.81
RHO_W = 1025.0      # seawater
RHO_C = 2400.0      # mass concrete
RHO_S = 2650.0      # rock
RHO_FILL = 1900.0   # granular backfill

__all__ = [
    "goda_pressures",
    "bearing_pressures",
    "scour_depth_vertical_wall",
    "toe_stone_size",
    "sliding_safety",
    "overturning_safety",
    "SeawallDesign",
    "design_seawall",
]


# ---------------------------------------------------------------------------
# Wave pressures
# ---------------------------------------------------------------------------


def goda_pressures(
    Hm0: float,
    T: float,
    depth: float,
    wall_toe_depth: float,
    berm_depth: float | None = None,
    crest_freeboard: float = 5.0,
    beta_degrees: float = 0.0,
    slope: float = 1 / 30,
    Hmax_factor: float = 1.8,
    breaker_index: float = 0.78,
) -> dict:
    """Goda wave pressures on a vertical wall.

    Parameters
    ----------
    Hm0 : float
        Significant wave height at the structure [m].
    T : float
        Period used for the pressure distribution [s]. Goda's method is
        written around the significant period; use Tp or T_1/3, not Tm-1,0.
    depth : float
        Water depth in front of the structure, seaward of the mound [m].
    wall_toe_depth : float
        Depth from the still water level to the underside of the upright
        section, Goda's h' [m].
    berm_depth : float, optional
        Depth over the toe berm, Goda's d [m]. Defaults to ``wall_toe_depth``,
        that is, no berm in front of the wall.
    crest_freeboard : float
        Crest level above the still water level, Rc [m]. Caps the pressure
        distribution at the crest: a wall lower than the run-up wedge is not
        loaded above its own crest.
    beta_degrees : float
        Angle of wave attack from the wall normal [deg].
    slope : float
        Seabed slope in front of the structure, used for the depth at five
        wave heights seaward.
    Hmax_factor : float
        Hmax / Hm0 for the design wave. Goda uses 1.8 for non-breaking
        conditions.
    breaker_index : float
        Depth limit on the design wave, Hmax <= breaker_index * d. Without
        it, 1.8 Hm0 in shallow water asks the wall to survive a wave the
        site cannot deliver. Set it to zero to disable the limit.

    Returns
    -------
    dict
        Pressures p1, p3, p4 and uplift pu [kPa], the elevation of the
        pressure distribution above the still water level ``eta_star`` [m],
        the horizontal force ``F`` and its lever arm ``arm`` about the
        heel, and the uplift force ``U`` per metre of base width.

    Notes
    -----
    This is the standard (non-impulsive) Goda distribution. Takahashi's
    impulsive pressure coefficient alpha_I, which governs when a steep
    mound throws a breaking wave at the wall, is not applied: check the
    mound geometry independently before relying on these numbers for a wall
    on a high berm.
    """
    for name, value in (("Hm0", Hm0), ("T", T), ("depth", depth)):
        if value <= 0:
            raise ValueError(f"{name} must be positive, got {value}")
    if wall_toe_depth <= 0:
        raise ValueError(f"Wall toe depth must be positive, got {wall_toe_depth}")

    d = wall_toe_depth if berm_depth is None else berm_depth
    if d <= 0:
        raise ValueError(f"Berm depth must be positive, got {d}")

    beta = math.radians(beta_degrees)
    d_limit = wall_toe_depth if berm_depth is None else berm_depth
    Hmax = Hmax_factor * Hm0
    if breaker_index > 0:
        Hmax = min(Hmax, breaker_index * d_limit)
    L = dispersion(T, depth)
    kh = 2 * math.pi * depth / L

    # Goda's lambda factors modify the standard distribution for non-standard
    # sections (a sloping top, a perforated face). Plain wall: all unity.
    lam1 = lam2 = lam3 = 1.0

    # Depth at five significant wave heights seaward, where breaking is set.
    h_b = depth + 5.0 * Hm0 * slope

    alpha1 = 0.6 + 0.5 * (2 * kh / math.sinh(2 * kh)) ** 2
    alpha2 = min((h_b - d) / (3.0 * h_b) * (Hmax / d) ** 2, 2.0 * d / Hmax)
    alpha3 = 1.0 - (wall_toe_depth / depth) * (1.0 - 1.0 / math.cosh(kh))

    eta_star = 0.75 * (1.0 + math.cos(beta)) * lam1 * Hmax
    p1 = (
        0.5 * (1.0 + math.cos(beta))
        * (lam1 * alpha1 + lam2 * alpha2 * math.cos(beta) ** 2)
        * RHO_W * G * Hmax
    )
    p3 = alpha3 * p1
    # Height of wall actually wetted above still water.
    hc_star = min(eta_star, crest_freeboard)
    p4 = p1 * (1.0 - hc_star / eta_star) if eta_star > 0 else 0.0
    pu = 0.5 * (1.0 + math.cos(beta)) * lam3 * alpha1 * alpha3 * RHO_W * G * Hmax

    # Horizontal force: trapezoid above still water plus trapezoid below.
    F_above = 0.5 * (p1 + p4) * hc_star
    F_below = 0.5 * (p1 + p3) * wall_toe_depth
    F = F_above + F_below

    # Lever arms about the heel (underside of the wall).
    arm_above = wall_toe_depth + hc_star * (2.0 * p1 + p4) / (3.0 * (p1 + p4))
    arm_below = wall_toe_depth * (p1 + 2.0 * p3) / (3.0 * (p1 + p3))
    arm = (F_above * arm_above + F_below * arm_below) / F if F > 0 else 0.0

    return {
        "p1": p1 / 1000.0,
        "p3": p3 / 1000.0,
        "p4": p4 / 1000.0,
        "pu": pu / 1000.0,
        "eta_star": eta_star,
        "hc_star": hc_star,
        "Hmax": Hmax,
        "depth_limited": breaker_index > 0 and Hmax < Hmax_factor * Hm0,
        "wavelength": L,
        "alpha1": alpha1,
        "alpha2": alpha2,
        "alpha3": alpha3,
        "F": F / 1000.0,
        "arm": arm,
        "U_per_width": 0.5 * pu / 1000.0,
    }


# ---------------------------------------------------------------------------
# Scour and toe
# ---------------------------------------------------------------------------


def scour_depth_vertical_wall(
    Hm0: float, T: float, depth: float, coefficient: float = 0.4
) -> float:
    """Equilibrium scour depth at the toe of a vertical wall [m].

    Xie (1981), for fine sediment under a standing wave in front of a
    reflecting wall::

        S / H = coefficient / sinh(k h) ** 1.35

    The scour hole sits a quarter wavelength from the wall, where the
    standing-wave node drives the largest near-bed velocity.

    Parameters
    ----------
    coefficient : float
        0.4 is Xie's value for regular waves on fine sand, and is the usual
        design value. Irregular waves smear the nodal structure and give a
        smaller, wider hole, so a lower coefficient is defensible; coarse
        sediment reduces it further. Set it deliberately rather than
        trusting the default.

    Notes
    -----
    This is the equilibrium depth after a long exposure, not the depth
    after one storm. It is a scour *allowance* for setting the founding
    level, and does not replace a check that the toe protection stays in
    place.
    """
    if coefficient < 0:
        raise ValueError(f"Coefficient must be non-negative, got {coefficient}")
    L = dispersion(T, depth)
    kh = 2 * math.pi * depth / L
    return coefficient * Hm0 / math.sinh(kh) ** 1.35


def toe_stone_size(
    Hm0: float, toe_depth: float, water_depth: float, Delta: float = 1.585,
    damage: float = 0.5,
) -> dict:
    """Toe berm stone size from the Van der Meer toe formula.

        Hs / (Delta Dn50) = (2 + 6.2 (ht/h)^2.7) Nod^0.15

    Parameters
    ----------
    toe_depth : float
        Water depth over the toe berm, ht [m].
    water_depth : float
        Water depth at the structure, h [m].
    damage : float
        Damage number Nod, stones displaced out of the berm per Dn50 width.
        0.5 is effectively no damage, 2 is acceptable damage, 4 is severe.

    Notes
    -----
    The formula is calibrated for 0.4 < ht/h < 0.9. A toe set very deep or
    very shallow relative to the water depth falls outside it, and the
    returned dict says so rather than silently extrapolating.
    """
    if toe_depth <= 0 or water_depth <= 0:
        raise ValueError("Depths must be positive")
    if damage <= 0:
        raise ValueError(f"Damage number must be positive, got {damage}")

    ratio = toe_depth / water_depth
    stability = (2.0 + 6.2 * ratio**2.7) * damage**0.15
    Dn50 = Hm0 / (Delta * stability)
    return {
        "Dn50": Dn50,
        "M50": RHO_S * Dn50**3,
        "stability_number": stability,
        "depth_ratio": ratio,
        "within_range": 0.4 - 1e-9 <= ratio <= 0.9 + 1e-9,
    }


# ---------------------------------------------------------------------------
# Stability checks
# ---------------------------------------------------------------------------


def _block(x0: float, x1: float, z0: float, z1: float, rho: float,
           water_level: float) -> tuple[float, float]:
    """Weight and centroid of a rectangular block, buoyant below water.

    Returns (weight in kN/m, centroid x in m). The block is split at the
    water level: the submerged part weighs (rho - rho_w) g V, the part above
    weighs rho g V. Ignoring the split overstates the restoring weight of a
    wall that is mostly under water.
    """
    width, height = x1 - x0, z1 - z0
    if width <= 0 or height <= 0:
        return 0.0, 0.5 * (x0 + x1)
    z_split = min(max(water_level, z0), z1)
    submerged = (z_split - z0) * width
    dry = (z1 - z_split) * width
    weight = (submerged * max(rho - RHO_W, 0.0) + dry * rho) * G / 1000.0
    return weight, 0.5 * (x0 + x1)


def sliding_safety(F: float, weight: float, uplift: float,
                   friction: float = 0.6) -> float:
    """Factor of safety against sliding on the base.

    FoS = friction * (W - U) / F, all forces per metre run. 0.6 is the usual
    design friction coefficient between concrete and a rubble bedding layer,
    and 1.2 the conventional requirement under the design wave. Returns 0
    when the uplift exceeds the weight, which is failure by flotation and
    not a sliding problem at all.
    """
    if F <= 0:
        raise ValueError(f"Horizontal force must be positive, got {F}")
    net = weight - uplift
    if net <= 0:
        return 0.0
    return friction * net / F


def overturning_safety(F: float, arm: float, restoring_moment: float,
                       uplift: float, base_width: float) -> float:
    """Factor of safety against overturning about the rear heel.

    The wave pushes shoreward, so the wall tips about its landward heel.
    Goda uplift is triangular with its peak at the seaward edge, putting its
    centroid two thirds of the base width from the rear heel.

    Parameters
    ----------
    F, arm : float
        Horizontal wave force [kN/m] and its lever arm above the base [m].
    restoring_moment : float
        Sum of W_i * (B - x_i) for every weight component, taken about the
        rear heel [kNm/m]. For a single uniform block this is W * B / 2.
    """
    if F <= 0 or arm <= 0:
        raise ValueError("Overturning needs a positive force and lever arm")
    if base_width <= 0:
        raise ValueError(f"Base width must be positive, got {base_width}")
    net = restoring_moment - uplift * (2.0 / 3.0) * base_width
    if net <= 0:
        return 0.0
    return net / (F * arm)


def bearing_pressures(normal: float, base_width: float,
                      net_moment: float) -> dict:
    """Base pressure distribution under a gravity wall.

    Parameters
    ----------
    normal : float
        Net vertical force on the base, weight less uplift [kN/m].
    base_width : float
        Base width B [m].
    net_moment : float
        Net moment about the rear heel, restoring less overturning
        [kNm/m]. Its ratio to the normal force locates the resultant.

    Returns
    -------
    dict
        ``p_max``, ``p_min`` [kPa], the eccentricity ``e`` from the centre
        of the base, and ``middle_third``, which is False when the
        resultant falls outside the middle third of the base and the heel
        goes into tension. Outside the middle third the no-tension
        distribution is used, so p_max is the triangular peak.
    """
    if base_width <= 0:
        raise ValueError(f"Base width must be positive, got {base_width}")
    if normal <= 0:
        return {"p_max": float("inf"), "p_min": 0.0, "e": float("nan"),
                "middle_third": False}

    x_res = net_moment / normal          # from the rear heel
    e = 0.5 * base_width - x_res
    if abs(e) <= base_width / 6.0:
        p_max = normal / base_width * (1.0 + 6.0 * abs(e) / base_width)
        p_min = normal / base_width * (1.0 - 6.0 * abs(e) / base_width)
        return {"p_max": p_max, "p_min": p_min, "e": e, "middle_third": True}

    # No tension: the contact length shortens to three times the distance
    # from the resultant to the nearest edge.
    a = min(x_res, base_width - x_res)
    if a <= 0:
        return {"p_max": float("inf"), "p_min": 0.0, "e": e,
                "middle_third": False}
    return {"p_max": 2.0 * normal / (3.0 * a), "p_min": 0.0, "e": e,
            "middle_third": False}


# ---------------------------------------------------------------------------
# The whole section
# ---------------------------------------------------------------------------


@dataclass
class SeawallDesign:
    """A dimensioned L-shaped gravity seawall.

    Levels are metres above chart datum. Distances are metres landward from
    the seaward face of the stem, which is the origin of the section.
    Everything is per metre run of wall.
    """

    conditions: DesignConditions
    still_water_level: float
    seabed_level: float

    crest_level: float
    crest_freeboard: float
    promenade_level: float

    base_width: float
    stem_thickness: float
    base_thickness: float
    founding_level: float
    embedment: float
    scour_depth: float

    toe_berm_width: float
    toe_berm_thickness: float
    toe_Dn50: float
    toe_M50: float
    toe_within_range: bool

    pressures: dict
    wave_force: float
    wave_arm: float
    weight: float
    uplift: float
    sliding_FoS: float
    overturning_FoS: float
    bearing: dict

    q_mean: float
    q_upper: float
    governing_limit: str
    impulsive: bool
    iterations: int = 0
    warnings: list[str] = field(default_factory=list)

    @property
    def wall_height(self) -> float:
        """Founding level to crest."""
        return self.crest_level - self.founding_level

    @property
    def heel_width(self) -> float:
        """Landward projection of the base beyond the stem."""
        return self.base_width - self.stem_thickness

    @property
    def water_depth(self) -> float:
        """Depth at the wall under the design still water level."""
        return self.still_water_level - self.seabed_level

    def quantities(self) -> dict:
        """Take-off per metre run of wall.

        Rock tonnage uses a 0.37 layer porosity, so it is placed tonnage
        rather than solid volume times density.
        """
        base = self.base_width * self.base_thickness
        stem = self.stem_thickness * (
            self.crest_level - self.founding_level - self.base_thickness
        )
        fill = self.heel_width * max(
            self.promenade_level - (self.founding_level + self.base_thickness), 0.0
        )
        berm = self.toe_berm_width * self.toe_berm_thickness
        return {
            "concrete_base_m3_per_m": base,
            "concrete_stem_m3_per_m": stem,
            "concrete_total_m3_per_m": base + stem,
            "concrete_mass_t_per_m": (base + stem) * RHO_C / 1000.0,
            "backfill_m3_per_m": fill,
            "toe_rock_m3_per_m": berm,
            "toe_rock_t_per_m": berm * (1.0 - 0.37) * RHO_S / 1000.0,
            "excavation_m3_per_m": self.base_width * self.embedment,
        }

    def summary(self) -> str:
        """A short design report, in the order an engineer checks it."""
        c = self.conditions
        q = self.quantities()
        b = self.bearing
        lines = [
            f"Design condition    Hm0 = {c.Hm0:.2f} m, Tm-1,0 = {c.Tm10:.2f} s",
            f"Water level         SWL {self.still_water_level:+.2f} m CD, "
            f"depth at wall {self.water_depth:.2f} m",
            "",
            f"Crest level         {self.crest_level:+.2f} m CD "
            f"(Rc = {self.crest_freeboard:.2f} m, Rc/Hm0 = "
            f"{self.crest_freeboard / c.Hm0:.2f})",
            f"Promenade level     {self.promenade_level:+.2f} m CD",
            f"Founding level      {self.founding_level:+.2f} m CD "
            f"(embedment {self.embedment:.2f} m, scour {self.scour_depth:.2f} m)",
            f"Wall height         {self.wall_height:.2f} m",
            f"Base                {self.base_width:.2f} m wide x "
            f"{self.base_thickness:.2f} m thick, stem "
            f"{self.stem_thickness:.2f} m",
            f"Sizing              {self.iterations} iterations on base width",
            "",
            f"Goda Hmax           {self.pressures['Hmax']:.2f} m"
            + ("  (depth limited)" if self.pressures.get("depth_limited") else ""),
            f"Pressures           p1 = {self.pressures['p1']:.1f} kPa, "
            f"p3 = {self.pressures['p3']:.1f} kPa, "
            f"pu = {self.pressures['pu']:.1f} kPa",
            f"Wave force          {self.wave_force:.0f} kN/m at "
            f"{self.wave_arm:.2f} m above the base",
            f"Weight, uplift      {self.weight:.0f} kN/m, {self.uplift:.0f} kN/m",
            f"Sliding FoS         {self.sliding_FoS:.2f}",
            f"Overturning FoS     {self.overturning_FoS:.2f}",
            f"Bearing             p_max = {b['p_max']:.0f} kPa, "
            f"e = {b['e']:+.2f} m"
            + ("" if b["middle_third"] else "  (outside the middle third)"),
            "",
            f"Toe protection      Dn50 = {self.toe_Dn50:.2f} m, "
            f"M50 = {self.toe_M50 / 1000:.2f} t, berm "
            f"{self.toe_berm_width:.1f} m wide x "
            f"{self.toe_berm_thickness:.2f} m thick",
            f"Overtopping         mean {self.q_mean:.3g} l/s/m, "
            f"upper bound {self.q_upper:.3g} l/s/m",
            f"Governing limit     "
            f"{TOLERABLE_DISCHARGE[self.governing_limit][0]:g} l/s/m, "
            f"{TOLERABLE_DISCHARGE[self.governing_limit][1].lower()}",
            "",
            f"Concrete            {q['concrete_total_m3_per_m']:.2f} m3/m "
            f"({q['concrete_mass_t_per_m']:.1f} t/m)",
            f"Backfill            {q['backfill_m3_per_m']:.2f} m3/m",
            f"Toe rock            {q['toe_rock_t_per_m']:.2f} t/m",
            f"Excavation          {q['excavation_m3_per_m']:.2f} m3/m",
        ]
        if self.warnings:
            lines += ["", "Warnings"]
            lines += [f"  - {w}" for w in self.warnings]
        return "\n".join(lines)


def design_seawall(
    conditions: DesignConditions,
    still_water_level: float,
    seabed_level: float,
    tolerable_use: str = "pedestrians_aware",
    beta_degrees: float = 0.0,
    friction: float = 0.6,
    target_sliding: float = 1.2,
    target_overturning: float = 1.5,
    require_middle_third: bool = True,
    scour_coefficient: float = 0.4,
    minimum_embedment: float = 1.0,
    maximum_embedment: float = 3.0,
    stem_thickness: float = 1.0,
    base_thickness: float = 1.2,
    promenade_freeboard: float = 1.0,
    toe_berm_width: float | None = None,
    toe_damage: float = 0.5,
    seabed_slope: float = 1 / 30,
    scatter_factor: float = 3.0,
    max_base_width: float = 30.0,
    step: float = 0.1,
) -> SeawallDesign:
    """Size an L-shaped gravity seawall against a design condition.

    The chain is the one a design office follows.

    1. Crest level from EurOtop, set so the *upper* bound of the overtopping
       scatter band meets the limit for ``tolerable_use``, not the mean.
    2. Founding level from the scour allowance, bracketed by
       ``minimum_embedment`` and ``maximum_embedment``. Deeper embedment is
       a piling question, not a gravity-wall one.
    3. Goda pressures on the wetted face, from the still water level down to
       the seabed.
    4. Base width grown in ``step`` increments until sliding, overturning
       and, if ``require_middle_third``, the base pressure check all pass.
       Keeping the resultant in the middle third stops the heel lifting off
       the bedding, which is what turns a wide safe base into a rocking one. The backfill over the landward heel is counted as
       restoring weight; passive resistance on the buried front face and
       active earth pressure from the fill are both ignored, which is
       conservative for the wave-loading case.
    5. Toe stone from the Van der Meer toe formula, iterated because the
       berm thickness changes the depth over the berm.

    Notes
    -----
    Full Goda uplift is applied under the base even when the base is
    embedded, where wave pressure would in reality be attenuated through
    the soil. That is deliberately on the safe side. It is also what makes
    the base come out wide: uplift grows with the base width just as the
    restoring weight does, so a wall in shallow water with a large wave is
    driven by flotation as much as by sliding.

    Returns
    -------
    SeawallDesign
        Fully dimensioned, with ``summary()`` and ``quantities()``.
    """
    if still_water_level <= seabed_level:
        raise ValueError("Still water level must be above the seabed")
    if tolerable_use not in TOLERABLE_DISCHARGE:
        raise ValueError(
            f"Unknown use {tolerable_use!r}. Options: {sorted(TOLERABLE_DISCHARGE)}"
        )
    if step <= 0:
        raise ValueError(f"Sizing step must be positive, got {step}")

    warnings: list[str] = []
    depth = still_water_level - seabed_level

    # 1. Crest level, against the upper bound of the scatter band.
    q_limit = TOLERABLE_DISCHARGE[tolerable_use][0]
    Rc = required_crest_freeboard(
        conditions, q_limit / scatter_factor, cot_alpha=0.0, vertical=True
    )
    crest_level = still_water_level + Rc
    q = overtopping_vertical(conditions, Rc)
    band = overtopping_with_uncertainty(q, scatter_factor)
    if q["impulsive"]:
        warnings.append(
            f"h* = {q['h_star']:.2f} is below 0.23, so the conditions are "
            "impulsive. The non-impulsive EurOtop formula used for the crest "
            "level understates the discharge; check against the impulsive "
            "formulae before fixing the crest."
        )

    # 2. Founding level.
    scour = scour_depth_vertical_wall(
        conditions.Hm0, conditions.Tm10, depth, coefficient=scour_coefficient
    )
    embedment = min(max(scour, minimum_embedment), maximum_embedment)
    founding_level = seabed_level - embedment
    if scour > maximum_embedment:
        warnings.append(
            f"Predicted scour {scour:.2f} m exceeds the {maximum_embedment:g} m "
            "embedment limit. The section relies on the toe protection to "
            "keep the scour hole away from the wall."
        )

    # 3. Toe protection. Two passes: the berm thickness sets the depth over
    # the berm, which sets the stone size, which sets the thickness.
    toe_thickness = 0.8
    toe = {}
    for _ in range(6):
        toe = toe_stone_size(
            conditions.Hm0, max(depth - toe_thickness, 0.2 * depth), depth,
            damage=toe_damage,
        )
        new_thickness = max(2.0 * toe["Dn50"], 0.5)
        if abs(new_thickness - toe_thickness) < 1e-3:
            break
        toe_thickness = new_thickness
    if toe_berm_width is None:
        toe_berm_width = max(3.0 * toe["Dn50"], 0.4 * conditions.Hm0, 2.0)
    if not toe["within_range"]:
        warnings.append(
            f"Toe depth ratio ht/h = {toe['depth_ratio']:.2f} is outside the "
            "0.4 to 0.9 calibration range of the Van der Meer toe formula."
        )

    # 4. Base width, iterated because the uplift grows with it.
    promenade_level = crest_level - promenade_freeboard
    base_top = founding_level + base_thickness
    base_width = max(0.5 * (crest_level - founding_level), stem_thickness + 0.5)
    pressures: dict = {}
    sliding = overturning = 0.0
    weight = uplift = wave_arm = 0.0
    bearing: dict = {}
    iterations = 0

    for iterations in range(1, 2001):
        pressures = goda_pressures(
            Hm0=conditions.Hm0,
            T=conditions.Tm10 * 1.1,     # Goda is written around Ts, not Tm-1,0
            depth=depth,
            wall_toe_depth=depth,
            berm_depth=max(depth - toe_thickness, 0.2 * depth),
            crest_freeboard=Rc,
            beta_degrees=beta_degrees,
            slope=seabed_slope,
        )
        # The wave presses on the wetted face only. Below the seabed the wall
        # is against soil, so the embedment adds lever arm but not load.
        wave_arm = pressures["arm"] + embedment
        F = pressures["F"]

        components = [
            _block(0.0, base_width, founding_level, base_top, RHO_C,
                   still_water_level),
            _block(0.0, stem_thickness, base_top, crest_level, RHO_C,
                   still_water_level),
            _block(stem_thickness, base_width, base_top, promenade_level,
                   RHO_FILL, still_water_level),
        ]
        weight = sum(w for w, _ in components)
        restoring = sum(w * (base_width - x) for w, x in components)
        uplift = pressures["U_per_width"] * base_width

        sliding = sliding_safety(F, weight, uplift, friction)
        overturning = overturning_safety(F, wave_arm, restoring, uplift,
                                         base_width)
        bearing = bearing_pressures(
            weight - uplift, base_width,
            restoring - uplift * (2.0 / 3.0) * base_width - F * wave_arm,
        )
        passed = (
            sliding >= target_sliding
            and overturning >= target_overturning
            and (bearing["middle_third"] or not require_middle_third)
        )
        if passed:
            break
        if base_width >= max_base_width:
            warnings.append(
                f"Base width reached the {max_base_width:g} m limit with "
                f"sliding FoS {sliding:.2f}, overturning FoS "
                f"{overturning:.2f} and the resultant "
                + ("inside" if bearing["middle_third"] else "outside")
                + " the middle third. A gravity wall is the wrong form for "
                "these conditions; consider a piled or anchored wall, or a "
                "rubble-mound revetment."
            )
            break
        base_width += step

    return SeawallDesign(
        conditions=conditions,
        still_water_level=still_water_level,
        seabed_level=seabed_level,
        crest_level=crest_level,
        crest_freeboard=Rc,
        promenade_level=promenade_level,
        base_width=base_width,
        stem_thickness=stem_thickness,
        base_thickness=base_thickness,
        founding_level=founding_level,
        embedment=embedment,
        scour_depth=scour,
        toe_berm_width=toe_berm_width,
        toe_berm_thickness=toe_thickness,
        toe_Dn50=toe["Dn50"],
        toe_M50=toe["M50"],
        toe_within_range=toe["within_range"],
        pressures=pressures,
        wave_force=pressures["F"],
        wave_arm=wave_arm,
        weight=weight,
        uplift=uplift,
        sliding_FoS=sliding,
        overturning_FoS=overturning,
        bearing=bearing,
        q_mean=band["q_mean"],
        q_upper=band["q_upper"],
        governing_limit=tolerable_use,
        impulsive=q["impulsive"],
        iterations=iterations,
        warnings=warnings,
    )
