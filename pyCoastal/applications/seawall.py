"""
Vertical seawall design: wave pressures, stability, scour and toe protection.

This is the design half of the seawall product. Give it a design condition
and a set of choices, and it returns a fully dimensioned section: crest
level set by overtopping, base width set by sliding, overturning and bearing
in two load cases, stem and base thickness set by bending and shear, toe
level set by scour, and toe stone sized for stability.
:mod:`pyCoastal.applications.sections` turns the result into a drawing and a
bill of quantities.

Sources
-------
Goda, Y. (1974, 2010), Random Seas and Design of Maritime Structures.
    Wave pressure distribution on a vertical wall, the breaker index used to
    cap the design wave, and the extension to impulsive conditions by
    Takahashi et al. (1994).

EurOtop (2018), Manual on wave overtopping of sea defences, 2nd ed.
    Crest level for a tolerable mean discharge.

Xie, S. L. (1981), Scouring patterns in front of vertical breakwaters,
    Delft University of Technology. Scour depth at a vertical wall.

Tanimoto, K., Yagyu, T. and Goda, Y. (1982), Irregular wave tests for
    composite breakwater foundations, Proc. 18th ICCE, with the extension
    by Takahashi (2002). Toe berm stone in front of a vertical wall.

EN 1992-1-1 (2004), Eurocode 2. Bending and shear resistance of the stem.

Conventions
-----------
Levels are metres above chart datum and increase upward, matching the
package's z convention. Distances are metres landward from the seaward face
of the wall unless stated. Forces are kN per metre run of wall.

Stability is computed on a free body of the wall and the fill standing on
its heel, with total unit weights and every water pressure applied
explicitly: on the seaward face, on the virtual back plane through the rear
of the heel, and under the base. Buoyant weights are not used, because they
assume one water level on both sides of the wall, which is exactly the
condition a seawall does not see.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..tools.wave import dispersion
from .sediment import Sediment, lateral_earth_force, sediment
from .structures import (
    DesignConditions,
    TOLERABLE_DISCHARGE,
    overtopping_vertical,
    overtopping_with_uncertainty,
    required_crest_freeboard,
)

G = 9.81
RHO_W = 1025.0      # seawater
RHO_C = 2400.0      # reinforced concrete
RHO_S = 2650.0      # rock
GAMMA_W = RHO_W * G / 1000.0   # kN/m3
GAMMA_C = RHO_C * G / 1000.0   # kN/m3

#: Concept-design reinforced concrete: C35/45, B500 bars, 1 % tension steel,
#: 100 mm from the face to the bar centroid, ULS load factor 1.35.
F_CK = 35.0
F_YK = 500.0
REINFORCEMENT_RATIO = 0.01
COVER_TO_STEEL = 0.10
ULS_FACTOR = 1.35

#: Retained height above which a cantilever L-wall stops being ordinary
#: practice and a counterforted wall, caisson or anchored wall is the usual
#: form.
L_WALL_PRACTICAL_HEIGHT = 8.0

__all__ = [
    "goda_pressures",
    "goda_breaking_height",
    "bearing_pressures",
    "scour_depth_vertical_wall",
    "toe_stone_size",
    "toe_stone_tanimoto",
    "sliding_safety",
    "overturning_safety",
    "stem_section",
    "SeawallDesign",
    "design_seawall",
    "hydrostatic_force",
]


# ---------------------------------------------------------------------------
# Wave pressures
# ---------------------------------------------------------------------------


def goda_breaking_height(T: float, depth: float, slope: float,
                         coefficient: float = 0.17) -> float:
    """Height of the largest wave a depth can carry, Goda's breaker index.

        Hb = A L0 [1 - exp(-1.5 pi h / L0 (1 + 15 tan^(4/3) theta))]

    with L0 = g T^2 / (2 pi) and A = 0.17 (Goda 2010). Used to cap Hmax at
    the depth five significant wave heights seaward of the wall, where Goda
    sets the breaking point for the design wave.
    """
    if T <= 0 or depth <= 0:
        raise ValueError("Period and depth must be positive")
    L0 = G * T**2 / (2 * math.pi)
    return coefficient * L0 * (
        1.0 - math.exp(-1.5 * math.pi * depth / L0
                       * (1.0 + 15.0 * abs(slope) ** (4.0 / 3.0)))
    )


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
    depth_limit: bool = True,
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
        wave heights seaward and for the breaker index.
    Hmax_factor : float
        Hmax / Hm0 for the design wave. Goda uses 1.8 for non-breaking
        conditions.
    depth_limit : bool
        Cap Hmax at the breaking height from :func:`goda_breaking_height`,
        evaluated at the depth h_b five significant wave heights seaward.

    Returns
    -------
    dict
        Pressures p1, p3, p4 and uplift pu [kPa], the elevation of the
        pressure distribution above the still water level ``eta_star`` [m],
        the horizontal force ``F`` and its lever arm ``arm`` about the
        underside of the wall, and the uplift force ``U`` per metre of base
        width.

    Notes
    -----
    These are the pressures in excess of hydrostatic about the still water
    level. The still-water pressure on the face and under the base is added
    by the caller. This is the standard (non-impulsive) Goda distribution.
    Takahashi's impulsive pressure coefficient alpha_I, which governs when a
    steep mound throws a breaking wave at the wall, is not applied: check
    the mound geometry independently before relying on these numbers for a
    wall on a high berm.
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
    # Depth at five significant wave heights seaward, where breaking is set.
    h_b = depth + 5.0 * Hm0 * slope

    Hmax = Hmax_factor * Hm0
    breaking = goda_breaking_height(T, h_b, slope) if depth_limit else None
    if breaking is not None:
        Hmax = min(Hmax, breaking)
    L = dispersion(T, depth)
    kh = 2 * math.pi * depth / L

    # Goda's lambda factors modify the standard distribution for non-standard
    # sections (a sloping top, a perforated face). Plain wall: all unity.
    lam1 = lam2 = lam3 = 1.0

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

    # Lever arms about the underside of the wall.
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
        "breaking_height": breaking,
        "depth_limited": breaking is not None and Hmax < Hmax_factor * Hm0,
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
    T : float
        Peak period [s], which sets the standing-wave pattern.
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

    This is the toe of a *sloping* rubble structure. For the berm in front
    of a vertical wall use :func:`toe_stone_tanimoto`, which is what
    :func:`design_seawall` does.

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


def toe_stone_tanimoto(
    Hs: float, T: float, berm_depth: float, berm_width: float,
    Delta: float = 1.585, beta_degrees: float = 0.0, alpha_s: float = 0.45,
) -> dict:
    """Stone on the toe berm in front of a vertical wall.

    Tanimoto et al. (1982) as extended by Takahashi (2002)::

        Dn50 = Hs / (Delta Ns)
        Ns = max{1.8, 1.3 (1 - kappa) / kappa^(1/3) h'/Hs
                      + 1.8 exp[-1.5 (1 - kappa)^2 / kappa^(1/3) h'/Hs]}
        kappa  = kappa1 kappa2
        kappa1 = (4 pi h'/L') / sinh(4 pi h'/L')
        kappa2 = max{alpha_s sin^2(beta) cos^2(2 pi B/L' cos beta),
                     cos^2(beta) sin^2(2 pi B/L' cos beta)}

    Parameters
    ----------
    Hs : float
        Significant wave height at the wall [m].
    T : float
        Significant wave period [s]; Tp is a close enough stand-in.
    berm_depth : float
        Water depth over the top of the berm armour, h' [m].
    berm_width : float
        Width of the berm in front of the wall, B_M [m].
    alpha_s : float
        0.45, Takahashi's coefficient for oblique attack.

    Notes
    -----
    Unlike the Van der Meer toe formula this one knows it is in front of a
    wall: kappa2 carries the standing-wave velocity at the berm, which is
    why the berm width appears.
    """
    if Hs <= 0 or T <= 0:
        raise ValueError("Wave height and period must be positive")
    if berm_depth <= 0 or berm_width < 0:
        raise ValueError("Berm depth must be positive and width non-negative")

    L = dispersion(T, berm_depth)
    two_kh = 4.0 * math.pi * berm_depth / L
    kappa1 = two_kh / math.sinh(two_kh)
    beta = math.radians(beta_degrees)
    a = 2.0 * math.pi * berm_width / L * math.cos(beta)
    kappa2 = max(alpha_s * math.sin(beta) ** 2 * math.cos(a) ** 2,
                 math.cos(beta) ** 2 * math.sin(a) ** 2)
    # A berm exactly at a velocity node carries no standing-wave flow at
    # all; the floor keeps the formula finite and the Ns >= 1.8 cap holds.
    kappa = max(kappa1 * kappa2, 1e-6)
    r = berm_depth / Hs
    root = kappa ** (1.0 / 3.0)
    Ns = max(1.8, 1.3 * (1.0 - kappa) / root * r
             + 1.8 * math.exp(-1.5 * (1.0 - kappa) ** 2 / root * r))
    Dn50 = Hs / (Delta * Ns)
    return {
        "Dn50": Dn50,
        "M50": RHO_S * Dn50**3,
        "stability_number": Ns,
        "kappa": kappa,
        "wavelength": L,
    }


# ---------------------------------------------------------------------------
# Stability checks
# ---------------------------------------------------------------------------


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
        Net moment about one edge of the base, restoring less overturning
        [kNm/m]. Its ratio to the normal force locates the resultant from
        that edge. Either edge works: the distribution is symmetric in the
        eccentricity.

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

    x_res = net_moment / normal          # from the reference edge
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


def hydrostatic_force(depth: float, unit_weight: float = GAMMA_W) -> dict:
    """Hydrostatic force on a vertical face and its lever arm [kN/m, m].

    F = 0.5 gamma h^2, acting at h/3 above the bottom of the face.
    """
    if depth < 0:
        raise ValueError(f"Depth must be non-negative, got {depth}")
    return {"force": 0.5 * unit_weight * depth ** 2, "arm": depth / 3.0}


def _uplift(front_head: float, back_head: float, base_width: float) -> dict:
    """Hydrostatic uplift under the base, linear from front to back head.

    The seepage path under the base is short and the heads at its two ends
    are set by the sea in front and the water table behind, so the usual
    linear distribution is taken. Returns the force and its distance from
    the seaward edge.
    """
    hf, hb = max(front_head, 0.0), max(back_head, 0.0)
    force = 0.5 * GAMMA_W * (hf + hb) * base_width
    if hf + hb <= 0:
        return {"force": 0.0, "x": 0.5 * base_width}
    x = base_width * (hf + 2.0 * hb) / (3.0 * (hf + hb))
    return {"force": force, "x": x}


def stem_section(moment: float, shear: float, fck: float = F_CK,
                 fyk: float = F_YK, rho: float = REINFORCEMENT_RATIO,
                 cover: float = COVER_TO_STEEL) -> dict:
    """Thickness a reinforced concrete cantilever needs for M and V.

    Concept design to EN 1992-1-1, per metre width:

    bending
        M_Ed <= 0.9 d rho d f_yd, so d_M = sqrt(M_Ed / (0.9 rho f_yd))
    shear, no links
        V_Ed <= v_Rd,c d with v_Rd,c = max(0.12 k (100 rho f_ck)^(1/3),
        0.035 k^1.5 f_ck^0.5), k = min(1 + sqrt(200 / d[mm]), 2)

    Parameters
    ----------
    moment, shear : float
        Design (factored) values at the critical section [kNm/m, kN/m].
    rho : float
        Tension reinforcement ratio. 1 % is a practical ceiling for a wall
        that has to be built and to crack acceptably.

    Returns
    -------
    dict
        Effective depths for bending and shear and the ``thickness`` that
        satisfies both, rounded up to 50 mm.
    """
    if moment < 0 or shear < 0:
        raise ValueError("Design moment and shear must be non-negative")
    fyd = fyk / 1.15
    d_M = math.sqrt(moment * 1e3 / (0.9 * rho * fyd * 1e6)) if moment > 0 else 0.0

    d_V = 0.2
    for _ in range(50):
        k = min(1.0 + math.sqrt(200.0 / (d_V * 1000.0)), 2.0)
        v_rd = max(0.12 * k * (100.0 * rho * fck) ** (1.0 / 3.0),
                   0.035 * k ** 1.5 * math.sqrt(fck))
        new = shear * 1e3 / (v_rd * 1e6)
        if abs(new - d_V) < 1e-5:
            d_V = new
            break
        d_V = max(new, 0.05)
    d_req = max(d_M, d_V)
    thickness = math.ceil((d_req + cover) / 0.05 - 1e-9) * 0.05
    return {"d_bending": d_M, "d_shear": d_V, "thickness": thickness,
            "moment": moment, "shear": shear}


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
    toe_stability_number: float

    pressures: dict
    wave_force: float
    wave_arm: float
    weight: float
    uplift: float
    static_uplift: float
    sliding_FoS: float
    overturning_FoS: float
    bearing: dict
    allowable_bearing: float | None

    backfill: Sediment
    retained_height: float
    water_table: float
    back_water_level: float
    surcharge: float
    earth_driving: dict
    earth_resisting: dict
    drawdown: dict
    governing_case: str
    stem: dict

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
        bd = self.drawdown["bearing"]
        s = self.stem
        allow = ("" if self.allowable_bearing is None
                 else f" (allowable {self.allowable_bearing:.0f})")
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
            f"Weight, uplift      {self.weight:.0f} kN/m total, "
            f"{self.static_uplift:.0f} kN/m hydrostatic + "
            f"{self.uplift:.0f} kN/m wave",
            "",
            f"Backfill            {self.backfill.name}, phi' = "
            f"{self.backfill.friction_angle:.0f} deg, retained "
            f"{self.retained_height:.2f} m",
            f"Water table         {self.back_water_level:+.2f} m CD behind "
            f"the wall",
            f"Earth pressure      {self.earth_driving['total']:.0f} kN/m at "
            f"{self.earth_driving['arm']:.2f} m "
            f"(K = {self.earth_driving['K']:.3f}, "
            f"{self.earth_driving['soil']:.0f} soil + "
            f"{self.earth_driving['water']:.0f} water)",
            "",
            "Load case 1, wave crest pushing landward",
            f"   sliding          {self.sliding_FoS:.2f}",
            f"   overturning      {self.overturning_FoS:.2f}",
            f"   bearing          p_max = {b['p_max']:.0f} kPa{allow}, "
            f"e = {b['e']:+.2f} m"
            + ("" if b["middle_third"] else "  (outside the middle third)"),
            "Load case 2, trough with the backfill pushing seaward",
            f"   front water      {self.drawdown['front_force']:.0f} kN/m at "
            f"{self.drawdown['trough_level']:+.2f} m CD",
            f"   net seaward      {self.drawdown['net_force']:.0f} kN/m",
            f"   sliding          {self.drawdown['sliding_FoS']:.2f}",
            f"   overturning      {self.drawdown['overturning_FoS']:.2f}",
            f"   bearing          p_max = {bd['p_max']:.0f} kPa{allow}, "
            f"e = {bd['e']:+.2f} m"
            + ("" if bd["middle_third"] else "  (outside the middle third)"),
            f"Governing case      {self.governing_case}",
            "",
            f"Stem at the base    M_Ed = {s['moment']:.0f} kNm/m, "
            f"V_Ed = {s['shear']:.0f} kN/m, needs "
            f"{s['thickness']:.2f} m",
            "",
            f"Toe protection      Dn50 = {self.toe_Dn50:.2f} m, "
            f"M50 = {self.toe_M50 / 1000:.2f} t, berm "
            f"{self.toe_berm_width:.1f} m wide x "
            f"{self.toe_berm_thickness:.2f} m thick (Tanimoto, "
            f"Ns = {self.toe_stability_number:.2f})",
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


def _stem_loads(backfill, pressures, wave_arm, base_thickness, retained,
                water_table, surcharge, trough, swl, base_top) -> tuple:
    """Characteristic moment and shear at the foot of the stem.

    The stem is a cantilever from the top of the base slab. It is bent
    seaward by the backfill at the trough, and landward by the wave, the
    still water in front and whatever the active backfill does not cancel.
    """
    if retained <= 0:
        return 0.0, 0.0
    at_rest = lateral_earth_force(backfill, retained, water_table, surcharge,
                                  kind="at_rest")
    active = lateral_earth_force(backfill, retained, water_table, surcharge,
                                 kind="active")
    front_trough = hydrostatic_force(max(trough - base_top, 0.0))
    front_swl = hydrostatic_force(max(swl - base_top, 0.0))

    V_out = at_rest["total"] - front_trough["force"]
    M_out = (at_rest["moment"]
             - front_trough["force"] * front_trough["arm"])

    F = pressures["F"]
    arm = max(wave_arm - base_thickness, 0.0)
    V_in = F + front_swl["force"] - active["total"]
    M_in = F * arm + front_swl["force"] * front_swl["arm"] - active["moment"]
    return max(abs(M_out), abs(M_in)), max(abs(V_out), abs(V_in))


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
    allowable_bearing: float | None = 300.0,
    scour_coefficient: float = 0.4,
    minimum_embedment: float = 1.0,
    maximum_embedment: float = 3.0,
    stem_thickness: float = 0.5,
    base_thickness: float = 0.6,
    promenade_freeboard: float = 1.0,
    toe_berm_width: float | None = None,
    seabed_slope: float = 1 / 30,
    scatter_factor: float = 3.0,
    max_base_width: float = 30.0,
    step: float = 0.1,
    backfill: "Sediment | str" = "medium_sand",
    water_table: float = 0.0,
    surcharge: float = 10.0,
    earth_pressure_driving: str = "at_rest",
    earth_pressure_resisting: str = "active",
    credit_earth_pressure: bool = True,
    drawdown_level: float | None = None,
) -> SeawallDesign:
    """Size an L-shaped gravity seawall against a design condition.

    The chain is the one a design office follows.

    1. Crest level from EurOtop, set so the *upper* bound of the overtopping
       scatter band meets the limit for ``tolerable_use``, not the mean.
    2. Founding level from the scour allowance, bracketed by
       ``minimum_embedment`` and ``maximum_embedment``. Deeper embedment is
       a piling question, not a gravity-wall one.
    3. Toe stone from Tanimoto's formula for a berm in front of a vertical
       wall, iterated because the berm thickness changes the depth over it.
    4. Goda pressures on the wetted face, from the still water level down to
       the seabed, with Hmax capped by Goda's breaker index.
    5. Stem and base thickness from the bending and shear at the foot of the
       stem, as a reinforced concrete cantilever. The inputs are minimums.
    6. Base width grown in ``step`` increments until both load cases pass
       sliding, overturning, the middle third (if ``require_middle_third``)
       and the ``allowable_bearing`` pressure:

       * wave crest: Goda pressure and uplift plus the still water in
         front, against the active backfill behind;
       * drawdown: the at-rest backfill and its pore water pushing seaward,
         with the sea down at the trough in front.

    Every water pressure is applied explicitly: on the face, on the virtual
    back plane through the rear of the heel, and under the base, where it
    varies linearly from the sea level in front to the water table behind.
    Weights are total weights. The backfill water table is never taken
    below the still water level, since the sea feeds it.

    Parameters
    ----------
    allowable_bearing : float or None
        Allowable base pressure [kPa]. 300 kPa is a presumptive value for a
        medium dense sand bearing stratum and must be replaced by the
        geotechnical designer's figure. None skips the check.
    stem_thickness, base_thickness : float
        Minimum thicknesses [m]. Both grow if the stem needs more; the base
        is never thinner than the stem.

    Notes
    -----
    Full Goda uplift is applied under the base even when the base is
    embedded, where wave pressure would in reality be attenuated through
    the soil. That is deliberately on the safe side. Passive resistance in
    front of the embedment and the vertical component of wall friction are
    both ignored, also on the safe side.

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
    if allowable_bearing is not None and allowable_bearing <= 0:
        raise ValueError(f"Allowable bearing must be positive, got {allowable_bearing}")
    backfill = sediment(backfill) if isinstance(backfill, str) else backfill

    warnings: list[str] = []
    depth = still_water_level - seabed_level
    T_goda = conditions.Tm10 * 1.1       # Goda is written around Ts, not Tm-1,0

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
            "level understates the discharge, and Goda understates the load; "
            "check against the impulsive formulae before fixing the section."
        )

    # 2. Founding level.
    scour = scour_depth_vertical_wall(
        conditions.Hm0, T_goda, depth, coefficient=scour_coefficient
    )
    embedment = min(max(scour, minimum_embedment), maximum_embedment)
    founding_level = seabed_level - embedment
    if scour > maximum_embedment:
        warnings.append(
            f"Predicted scour {scour:.2f} m exceeds the {maximum_embedment:g} m "
            "embedment limit. The section relies on the toe protection to "
            "keep the scour hole away from the wall."
        )

    # 3. Toe protection. The berm thickness sets the depth over the berm,
    # which sets the stone size, which sets the thickness and the width.
    toe_thickness = 0.8
    fixed_width = toe_berm_width
    width = fixed_width if fixed_width is not None else 2.0
    toe: dict = {}
    for _ in range(20):
        toe = toe_stone_tanimoto(conditions.Hm0, T_goda,
                                 max(depth - toe_thickness, 0.2 * depth), width,
                                 beta_degrees=beta_degrees)
        new_thickness = max(2.0 * toe["Dn50"], 0.5)
        new_width = (fixed_width if fixed_width is not None
                     else max(3.0 * toe["Dn50"], 0.4 * conditions.Hm0, 2.0))
        if abs(new_thickness - toe_thickness) < 1e-4 and abs(new_width - width) < 1e-4:
            break
        toe_thickness, width = new_thickness, new_width
    toe_berm_width = width
    berm_depth = max(depth - toe_thickness, 0.2 * depth)
    quarter = 0.25 * dispersion(T_goda, depth)
    if toe_berm_width < quarter:
        warnings.append(
            f"The {toe_berm_width:.1f} m toe berm sits close to the wall, "
            "where the standing wave moves the bed least, which is why "
            f"Tanimoto allows {toe['M50'] / 1000:.2f} t stone. The scour hole "
            f"forms about a quarter wavelength out, {quarter:.0f} m from the "
            "face; widen the berm to reach it if the toe is also the scour "
            "protection, and the stone will grow."
        )

    # 4. Wave pressures. They do not depend on the base width.
    pressures = goda_pressures(
        Hm0=conditions.Hm0, T=T_goda, depth=depth, wall_toe_depth=depth,
        berm_depth=berm_depth, crest_freeboard=Rc,
        beta_degrees=beta_degrees, slope=seabed_slope,
    )
    # The wave presses on the wetted face only. Below the seabed the wall
    # is against soil, so the embedment adds lever arm but not load.
    wave_arm = pressures["arm"] + embedment
    F = pressures["F"]

    # The backfill, once. Neither force depends on the base width, because
    # both act on the virtual vertical plane through the rear of the heel.
    promenade_level = crest_level - promenade_freeboard
    retained_height = promenade_level - founding_level
    # The sea feeds the fill, so its water table is never below still water.
    ceiling = max(promenade_level - still_water_level, 0.0)
    if water_table > ceiling + 1e-9:
        warnings.append(
            f"A water table {water_table:.2f} m below the promenade would sit "
            "below the still water level, which the sea keeps the fill up "
            f"to; {ceiling:.2f} m is used."
        )
    table = min(water_table, ceiling)
    back_water_level = promenade_level - table
    earth_driving = lateral_earth_force(
        backfill, retained_height, table, surcharge,
        kind=earth_pressure_driving)
    earth_resisting = lateral_earth_force(
        backfill, retained_height, table, surcharge,
        kind=earth_pressure_resisting)
    if not credit_earth_pressure:
        earth_resisting = dict(earth_resisting, soil=0.0, water=0.0,
                               total=0.0, moment=0.0, arm=0.0)

    # How far the sea drops at the trough. The backfill does not drain in
    # the few seconds a wave takes, so this is the instant the wall is
    # pushed seaward by soil and pore water with little water left to
    # push back.
    trough = min(drawdown_level if drawdown_level is not None
                 else still_water_level - 0.5 * conditions.Hm0,
                 still_water_level)

    # 5. Stem and base thickness from the cantilever. A thicker base lifts
    # the foot of the stem and eases it, so the two are iterated from the
    # minimums rather than ratcheted up.
    def stem_demand(base_t: float) -> dict:
        top = founding_level + base_t
        retained = promenade_level - top
        M, V = _stem_loads(backfill, pressures, wave_arm, base_t, retained,
                           min(table, max(retained, 0.0)), surcharge, trough,
                           still_water_level, top)
        return stem_section(ULS_FACTOR * M, ULS_FACTOR * V)

    min_stem, min_base = stem_thickness, base_thickness
    base_thickness = max(min_base, min_stem)
    for _ in range(8):
        stem = stem_demand(base_thickness)
        new_stem = max(min_stem, stem["thickness"])
        new_base = max(min_base, new_stem)
        if abs(new_stem - stem_thickness) < 1e-9 and abs(new_base - base_thickness) < 1e-9:
            break
        stem_thickness, base_thickness = new_stem, new_base
    # Whatever the loop settled on, the stem must carry the loads at the
    # base it ended with.
    stem = stem_demand(base_thickness)
    if stem["thickness"] > stem_thickness + 1e-9:
        stem_thickness = stem["thickness"]
        base_thickness = max(base_thickness, stem_thickness)
    base_top = founding_level + base_thickness

    if retained_height > L_WALL_PRACTICAL_HEIGHT:
        warnings.append(
            f"The wall retains {retained_height:.1f} m. A cantilever L-wall "
            f"is ordinary practice up to about {L_WALL_PRACTICAL_HEIGHT:g} m; "
            "beyond that a counterforted wall, a caisson or an anchored "
            "sheet-pile wall is the usual form, and the stem here "
            f"({stem_thickness:.2f} m) shows why."
        )

    # Hydrostatic heads under the base, front and back, and the still water
    # in front of the face, for each case.
    head_back = back_water_level - founding_level
    front_crest = hydrostatic_force(max(still_water_level - founding_level, 0.0))
    front_trough = hydrostatic_force(max(trough - founding_level, 0.0))

    # 6. Base width.
    base_width = min(
        max(0.5 * (crest_level - founding_level), stem_thickness + 0.5),
        max_base_width,
    )
    sliding = overturning = 0.0
    weight = uplift = static_uplift = 0.0
    bearing: dict = {}
    drawdown: dict = {}
    iterations = 0

    def passes(fos_s, fos_o, bear) -> bool:
        ok = fos_s >= target_sliding and fos_o >= target_overturning
        if require_middle_third:
            ok = ok and bear["middle_third"]
        if allowable_bearing is not None:
            ok = ok and bear["p_max"] <= allowable_bearing
        return ok

    for iterations in range(1, 2001):
        B = base_width
        # Total weights and their distance from the seaward face.
        fill_height = max(promenade_level - base_top, 0.0)
        wet = min(max(back_water_level - base_top, 0.0), fill_height)
        dry = fill_height - wet
        heel = B - stem_thickness
        components = [
            (GAMMA_C * B * base_thickness, 0.5 * B),
            (GAMMA_C * stem_thickness * (crest_level - base_top),
             0.5 * stem_thickness),
            ((backfill.dry_unit_weight * dry
              + backfill.saturated_unit_weight * wet) * heel,
             stem_thickness + 0.5 * heel),
        ]
        weight = sum(w for w, _ in components)
        about_toe = sum(w * x for w, x in components)
        about_heel = sum(w * (B - x) for w, x in components)

        # -- case 1: the crest, pushing landward ---------------------------
        up1 = _uplift(still_water_level - founding_level, head_back, B)
        uplift = pressures["U_per_width"] * B          # Goda, peak at the toe
        static_uplift = up1["force"]
        N1 = weight - up1["force"] - uplift
        H1 = F + front_crest["force"] - earth_resisting["total"]
        drive1 = (F * wave_arm + front_crest["force"] * front_crest["arm"]
                  + up1["force"] * (B - up1["x"]) + uplift * (2.0 / 3.0) * B)
        resist1 = about_heel + earth_resisting["moment"]
        if H1 > 1e-6:
            sliding = friction * N1 / H1 if N1 > 0 else 0.0
        else:
            sliding = float("inf")
        overturning = resist1 / drive1 if drive1 > 0 else float("inf")
        bearing = bearing_pressures(N1, B, resist1 - drive1)

        # -- case 2: the trough, pushed seaward ----------------------------
        up2 = _uplift(trough - founding_level, head_back, B)
        N2 = weight - up2["force"]
        H2 = earth_driving["total"] - front_trough["force"]
        drive2 = earth_driving["moment"] + up2["force"] * up2["x"]
        resist2 = about_toe + front_trough["force"] * front_trough["arm"]
        if H2 > 1e-6:
            sliding_out = friction * N2 / H2 if N2 > 0 else 0.0
        else:
            sliding_out = float("inf")
        overturning_out = resist2 / drive2 if drive2 > 0 else float("inf")
        bearing_out = bearing_pressures(N2, B, resist2 - drive2)
        drawdown = {
            "trough_level": trough,
            "front_depth": max(trough - founding_level, 0.0),
            "front_force": front_trough["force"],
            "front_arm": front_trough["arm"],
            "earth_force": earth_driving["total"],
            "earth_arm": earth_driving["arm"],
            "uplift": up2["force"],
            "net_force": H2,
            "normal": N2,
            "sliding_FoS": sliding_out,
            "overturning_FoS": overturning_out,
            "bearing": bearing_out,
        }

        if (passes(sliding, overturning, bearing)
                and passes(sliding_out, overturning_out, bearing_out)):
            break
        if base_width >= max_base_width:
            warnings.append(
                f"Base width reached the {max_base_width:g} m limit with "
                f"sliding FoS {sliding:.2f} landward and {sliding_out:.2f} "
                f"seaward, overturning {overturning:.2f} and "
                f"{overturning_out:.2f}, and peak bearing "
                f"{bearing['p_max']:.0f} and {bearing_out['p_max']:.0f} kPa. "
                "A gravity wall is the wrong form for these conditions; "
                "consider a piled or anchored wall, or a rubble-mound "
                "revetment."
            )
            break
        base_width += step

    # Which case actually sized the wall.
    wave_margin = min(sliding / target_sliding, overturning / target_overturning)
    out_margin = min(drawdown["sliding_FoS"] / target_sliding,
                     drawdown["overturning_FoS"] / target_overturning)
    governing_case = "wave crest" if wave_margin <= out_margin else "drawdown"

    if earth_driving["water_fraction"] > 0.6:
        drained = lateral_earth_force(backfill, retained_height,
                                      ceiling, surcharge,
                                      kind=earth_pressure_driving)["total"]
        warnings.append(
            f"Pore water is {100 * earth_driving['water_fraction']:.0f}% of "
            "the pressure on the back of the wall. A drain holding the water "
            "table at still water level would cut the total from "
            f"{earth_driving['total']:.0f} to about {drained:.0f} kN/m."
        )
    if governing_case == "drawdown":
        warnings.append(
            "The drawdown case governs: the wall is sized by the saturated "
            "backfill pushing it seaward at the trough, so the backfill "
            "grading and the drainage detail set the base width more than "
            "the design wave does."
        )
    if backfill.cohesive:
        warnings.append(
            f"{backfill.name} is cohesive. The active pressure here uses the "
            "drained parameters and cuts off the tension zone; an undrained "
            "short-term check and a long-term swelling check are separate "
            "and can both govern."
        )

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
        toe_stability_number=toe["stability_number"],
        pressures=pressures,
        wave_force=F,
        wave_arm=wave_arm,
        weight=weight,
        uplift=uplift,
        static_uplift=static_uplift,
        sliding_FoS=sliding,
        overturning_FoS=overturning,
        bearing=bearing,
        allowable_bearing=allowable_bearing,
        backfill=backfill,
        retained_height=retained_height,
        water_table=table,
        back_water_level=back_water_level,
        surcharge=surcharge,
        earth_driving=earth_driving,
        earth_resisting=earth_resisting,
        drawdown=drawdown,
        governing_case=governing_case,
        stem=stem,
        q_mean=band["q_mean"],
        q_upper=band["q_upper"],
        governing_limit=tolerable_use,
        impulsive=q["impulsive"],
        iterations=iterations,
        warnings=warnings,
    )
