"""
Coastal structure design: armour sizing and wave overtopping.

Aimed at design work rather than illustration, so every relation is named,
its source given, and its validity range stated. Where a formula has a
documented range of application the functions say so in their docstrings;
they do not silently extrapolate on your behalf, but neither do they refuse
to compute, since engineering judgement outside a range is your call.

Sources
-------
Van der Meer (1988), "Rock slopes and gravel beaches under wave attack",
    Delft Hydraulics Publication 396. Rock armour stability.

CIRIA/CUR/CETMEF (2007), The Rock Manual, 2nd ed. Armour layer geometry.

Shore Protection Manual (1984), US Army CERC. Hudson formula.

EurOtop (2018), Manual on wave overtopping of sea defences and related
    structures, 2nd ed. Overtopping discharge and tolerable limits.

Conventions
-----------
Wave heights are spectral significant heights Hm0 at the toe. Slopes are
given as cot(alpha), the horizontal run per unit rise, because that is how
they appear on drawings. Discharges are litres per second per metre of
structure, the unit used in the tolerability tables.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..tools.wave import dispersion

G = 9.81


# ---------------------------------------------------------------------------
# Roughness and tolerable discharge data
# ---------------------------------------------------------------------------

#: Armour roughness factor gamma_f for overtopping (EurOtop 2018, Table 6.2).
#: Values are for a permeable core with two armour layers unless noted.
ROUGHNESS_FACTORS = {
    "smooth_concrete": 1.00,
    "grass": 1.00,
    "asphalt": 1.00,
    "rock_one_layer_impermeable": 0.60,
    "rock_two_layer_impermeable": 0.55,
    "rock_two_layer_permeable": 0.40,
    "cubes_one_layer_flat": 0.49,
    "cubes_two_layer_random": 0.47,
    "antifer": 0.47,
    "tetrapod": 0.38,
    "accropode": 0.46,
    "core_loc": 0.44,
    "xbloc": 0.45,
    "dolos": 0.43,
}

#: Tolerable mean overtopping discharge in l/s per m (EurOtop 2018, Tables
#: 3.1 to 3.3). Each entry is (limit, description). These are mean discharges;
#: individual overtopping volumes govern some of the same hazards and are not
#: covered here.
TOLERABLE_DISCHARGE = {
    "pedestrians_unaware": (0.03, "Unaware pedestrians, narrow walkway, clear view of the sea"),
    "pedestrians_aware": (0.1, "Aware pedestrians, able to see and avoid the hazard"),
    "trained_staff": (1.0, "Trained staff, well shod and protected, wide walkway"),
    "buildings_structural": (1.0, "Structural damage to buildings behind the defence"),
    "vehicles_low_speed": (10.0, "Vehicles at low speed on a road behind the crest"),
    "vehicles_moderate_speed": (50.0, "Driving at moderate speed, overtopping by pulsating flows"),
    "embankment_seaward": (50.0, "Damage to a maintained grass or armoured embankment"),
    "harbour_quay_equipment": (0.4, "Damage to equipment set back 5 to 10 m from the crest"),
}


# ---------------------------------------------------------------------------
# Design conditions
# ---------------------------------------------------------------------------


@dataclass
class DesignConditions:
    """Wave and water-level conditions at the toe of a structure.

    Attributes
    ----------
    Hm0 : float
        Spectral significant wave height at the toe [m].
    Tm10 : float
        Spectral period Tm-1,0 = m_-1/m_0 [s]. EurOtop is written around this
        period. If you only have Tp, ``from_peak_period`` converts with the
        standard Tm-1,0 = Tp / 1.1 for a single-peaked spectrum.
    depth : float
        Water depth at the toe [m].
    storm_duration : float
        Duration of the design storm [s]. Used to count waves for armour
        damage progression.
    """

    Hm0: float
    Tm10: float
    depth: float = 15.0
    storm_duration: float = 6 * 3600.0

    def __post_init__(self) -> None:
        if self.Hm0 <= 0:
            raise ValueError(f"Wave height must be positive, got {self.Hm0}")
        if self.Tm10 <= 0:
            raise ValueError(f"Wave period must be positive, got {self.Tm10}")
        if self.depth <= 0:
            raise ValueError(f"Depth must be positive, got {self.depth}")

    @classmethod
    def from_peak_period(cls, Hm0: float, Tp: float, **kwargs) -> "DesignConditions":
        """Build from a peak period, using Tm-1,0 = Tp / 1.1."""
        return cls(Hm0=Hm0, Tm10=Tp / 1.1, **kwargs)

    @property
    def wave_count(self) -> float:
        """Number of waves in the design storm, N = duration / Tm.

        Van der Meer's damage relation saturates near N = 7500, so the count
        is capped there; a longer storm does not keep eroding the slope at
        the same rate.
        """
        return min(self.storm_duration / self.Tm10, 7500.0)

    def deep_water_wavelength(self) -> float:
        """L0 = g T^2 / (2 pi), using Tm-1,0 [m]."""
        return G * self.Tm10**2 / (2 * math.pi)

    def wavelength(self) -> float:
        """Local wavelength at the toe from the dispersion relation [m]."""
        return dispersion(self.Tm10, self.depth)

    def breaker_parameter(self, cot_alpha: float) -> float:
        """Surf similarity parameter xi_m-1,0 = tan(alpha) / sqrt(Hm0 / L0)."""
        s0 = self.Hm0 / self.deep_water_wavelength()
        return (1.0 / cot_alpha) / math.sqrt(s0)


# ---------------------------------------------------------------------------
# Rock armour stability
# ---------------------------------------------------------------------------

#: Damage level S for rock armour (Van der Meer 1988). S = A_e / Dn50^2, the
#: eroded area normalised by the stone size. "Failure" means the underlayer
#: is exposed. The value depends on slope, so a range is given.
DAMAGE_LEVELS = {
    "start_of_damage": 2.0,
    "intermediate": 5.0,
    "failure_1_in_1.5": 8.0,
    "failure_1_in_2": 8.0,
    "failure_1_in_3": 12.0,
    "failure_1_in_4": 17.0,
}


def rock_armour_vandermeer(
    conditions: DesignConditions,
    cot_alpha: float,
    Delta: float = 1.585,
    permeability: float = 0.4,
    damage: float = 2.0,
    safety_factor: float = 1.0,
) -> dict:
    """Nominal rock diameter Dn50 from Van der Meer (1988).

    Two regimes, selected by the surf similarity parameter against a critical
    value ``xi_cr``:

    plunging (xi < xi_cr)
        Hs / (Delta Dn50) = 6.2 P^0.18 (S / sqrt(N))^0.2 xi^-0.5
    surging (xi >= xi_cr)
        Hs / (Delta Dn50) = 1.0 P^-0.13 (S / sqrt(N))^0.2 sqrt(cot a) xi^P

    with xi_cr = (6.2 P^0.31 sqrt(tan a))^(1 / (P + 0.5)).

    Parameters
    ----------
    cot_alpha : float
        Slope, horizontal per vertical. Valid range roughly 1.5 to 6.
    Delta : float
        Relative buoyant density (rho_s / rho_w - 1). 1.585 corresponds to
        2650 kg/m3 rock in seawater of 1025 kg/m3.
    permeability : float
        Notional permeability P (Van der Meer 1988, Figure 8):
        0.1 impermeable core with a filter layer, 0.4 permeable core,
        0.5 homogeneous structure, 0.6 very permeable core.
    damage : float
        Damage level S. See ``DAMAGE_LEVELS``. 2 is start of damage and is
        the usual design condition.
    safety_factor : float
        Divides the stability coefficients, so values above 1 give larger
        stone. Apply your own code's partial factors here.

    Returns
    -------
    dict
        ``Dn50`` [m], ``M50`` [kg] for 2650 kg/m3 rock, the regime that
        governed, ``xi``, and ``xi_cr``.

    Notes
    -----
    Valid for deep-water conditions at the toe and non-depth-limited waves.
    For depth-limited surf, Van der Meer's shallow-water modification or the
    Rock Manual's H2% form should be used instead; this function does not
    apply it.
    """
    if cot_alpha <= 0:
        raise ValueError(f"cot(alpha) must be positive, got {cot_alpha}")
    if not 0.0 < permeability <= 0.7:
        raise ValueError(f"Permeability P must be in (0, 0.7], got {permeability}")
    if damage <= 0:
        raise ValueError(f"Damage level S must be positive, got {damage}")
    if safety_factor <= 0:
        raise ValueError(f"Safety factor must be positive, got {safety_factor}")

    P = permeability
    S = damage
    N = conditions.wave_count
    xi = conditions.breaker_parameter(cot_alpha)
    tan_alpha = 1.0 / cot_alpha

    cp = 6.2 / safety_factor
    cs = 1.0 / safety_factor

    xi_cr = ((cp / cs) * P**0.31 * math.sqrt(tan_alpha)) ** (1.0 / (P + 0.5))
    damage_term = (S / math.sqrt(N)) ** 0.2

    if xi < xi_cr:
        regime = "plunging"
        stability = cp * P**0.18 * damage_term * xi**-0.5
    else:
        regime = "surging"
        stability = cs * P**-0.13 * damage_term * math.sqrt(cot_alpha) * xi**P

    Dn50 = conditions.Hm0 / (Delta * stability)
    return {
        "Dn50": Dn50,
        "M50": 2650.0 * Dn50**3,
        "regime": regime,
        "xi": xi,
        "xi_cr": xi_cr,
        "stability_number": stability,
    }


def rock_armour_hudson(
    conditions: DesignConditions,
    cot_alpha: float,
    Delta: float = 1.585,
    Kd: float = 4.0,
) -> dict:
    """Nominal rock diameter from the Hudson formula (SPM 1984).

    Hs / (Delta Dn50) = (Kd cot a)^(1/3) / 1.27, where the 1.27 converts the
    SPM's H1/10 basis to a significant wave height.

    ``Kd`` is the stability coefficient: 4.0 for rough angular rock in two
    layers on a trunk with breaking waves, 2.0 for a head. Hudson carries no
    dependence on wave period, storm duration, permeability or damage level,
    so it is a first estimate. Prefer ``rock_armour_vandermeer`` for design
    and use Hudson as a cross-check.
    """
    if cot_alpha <= 0:
        raise ValueError(f"cot(alpha) must be positive, got {cot_alpha}")
    if Kd <= 0:
        raise ValueError(f"Kd must be positive, got {Kd}")

    stability = (Kd * cot_alpha) ** (1.0 / 3.0) / 1.27
    Dn50 = conditions.Hm0 / (Delta * stability)
    return {"Dn50": Dn50, "M50": 2650.0 * Dn50**3, "stability_number": stability}


def armour_layer(
    Dn50: float, n_layers: int = 2, layer_coefficient: float = 1.0, porosity: float = 0.37
) -> dict:
    """Armour layer thickness and stone count (Rock Manual, 2007).

    thickness = n * k_delta * Dn50, and the number of stones per unit area is
    n * k_delta * (1 - porosity) / Dn50^2.
    """
    if n_layers < 1:
        raise ValueError(f"Need at least one layer, got {n_layers}")
    if not 0.0 <= porosity < 1.0:
        raise ValueError(f"Porosity must be in [0,1), got {porosity}")

    thickness = n_layers * layer_coefficient * Dn50
    per_area = n_layers * layer_coefficient * (1.0 - porosity) / Dn50**2
    return {
        "thickness": thickness,
        "stones_per_m2": per_area,
        "mass_per_m2": per_area * 2650.0 * Dn50**3,
    }


# ---------------------------------------------------------------------------
# Wave overtopping
# ---------------------------------------------------------------------------


def overtopping_sloped(
    conditions: DesignConditions,
    crest_freeboard: float,
    cot_alpha: float,
    gamma_f: float = 1.0,
    gamma_beta: float = 1.0,
    gamma_b: float = 1.0,
    gamma_v: float = 1.0,
) -> dict:
    """Mean overtopping discharge for a sloping structure (EurOtop 2018).

    Takes the lesser of the breaking-wave and non-breaking expressions,

    breaking (eq. 5.10)
        q / sqrt(g Hm0^3) = (0.023 / sqrt(tan a)) gamma_b xi
                            exp[-(2.7 Rc / (xi Hm0 gamma_b gamma_f gamma_beta gamma_v))^1.3]
    maximum (eq. 5.11)
        q / sqrt(g Hm0^3) = 0.09 exp[-(1.5 Rc / (Hm0 gamma_f gamma_beta))^1.3]

    Parameters
    ----------
    crest_freeboard : float
        Rc, crest height above the still water level [m]. Zero or negative
        freeboard is outside these formulae and raises.
    gamma_f : float
        Roughness factor, see ``ROUGHNESS_FACTORS``.
    gamma_beta : float
        Oblique wave attack factor. 1.0 for normal incidence; use
        ``obliquity_factor``.
    gamma_b : float
        Berm factor, 1.0 for no berm.
    gamma_v : float
        Wave wall factor, 1.0 for no crest wall.

    Returns
    -------
    dict
        ``q`` in l/s per m, the dimensionless discharge, and which branch
        governed.

    Notes
    -----
    These are mean values. EurOtop reports roughly a factor-of-three scatter
    about the mean discharge, so a design check should consider the upper
    confidence band, not the mean alone. ``overtopping_with_uncertainty``
    returns that band.
    """
    if crest_freeboard <= 0:
        raise ValueError(
            f"These formulae need a positive freeboard, got Rc = {crest_freeboard}. "
            "A crest at or below still water level is a different problem."
        )
    for name, value in (("gamma_f", gamma_f), ("gamma_beta", gamma_beta),
                        ("gamma_b", gamma_b), ("gamma_v", gamma_v)):
        if not 0.0 < value <= 1.0:
            raise ValueError(f"{name} must be in (0,1], got {value}")

    Hm0 = conditions.Hm0
    xi = conditions.breaker_parameter(cot_alpha)
    tan_alpha = 1.0 / cot_alpha
    scale = math.sqrt(G * Hm0**3)

    breaking = (
        (0.023 / math.sqrt(tan_alpha))
        * gamma_b
        * xi
        * math.exp(
            -((2.7 * crest_freeboard
               / (xi * Hm0 * gamma_b * gamma_f * gamma_beta * gamma_v)) ** 1.3)
        )
    )
    non_breaking = 0.09 * math.exp(
        -((1.5 * crest_freeboard / (Hm0 * gamma_f * gamma_beta)) ** 1.3)
    )

    if breaking <= non_breaking:
        q_star, governing = breaking, "breaking"
    else:
        q_star, governing = non_breaking, "non-breaking"

    return {
        "q": q_star * scale * 1000.0,     # m3/s/m -> l/s/m
        "q_dimensionless": q_star,
        "governing": governing,
        "xi": xi,
        "relative_freeboard": crest_freeboard / Hm0,
    }


def overtopping_vertical(
    conditions: DesignConditions, crest_freeboard: float, gamma_beta: float = 1.0
) -> dict:
    """Mean overtopping for a plain vertical wall, non-impulsive conditions.

    EurOtop (2018) eq. 7.1:

        q / sqrt(g Hm0^3) = 0.047 exp[-(2.35 Rc / (Hm0 gamma_beta))^1.3]

    Notes
    -----
    Valid for non-impulsive (pulsating) conditions, roughly when the
    impulsiveness parameter h* = 1.35 (h / Hm0) (2 pi h / (g Tm10^2)) exceeds
    about 0.23. Impulsive conditions give far larger discharges and need the
    separate impulsive formulae, which are not implemented here. The returned
    dict reports ``h_star`` and ``impulsive`` so the caller can tell.
    """
    if crest_freeboard <= 0:
        raise ValueError(f"Needs a positive freeboard, got Rc = {crest_freeboard}")

    Hm0, h = conditions.Hm0, conditions.depth
    h_star = 1.35 * (h / Hm0) * (2 * math.pi * h / (G * conditions.Tm10**2))
    q_star = 0.047 * math.exp(-((2.35 * crest_freeboard / (Hm0 * gamma_beta)) ** 1.3))

    return {
        "q": q_star * math.sqrt(G * Hm0**3) * 1000.0,
        "q_dimensionless": q_star,
        "h_star": h_star,
        "impulsive": h_star < 0.23,
        "relative_freeboard": crest_freeboard / Hm0,
    }


def obliquity_factor(beta_degrees: float, kind: str = "overtopping") -> float:
    """Oblique wave attack factor gamma_beta (EurOtop 2018, section 5.4.4).

    For overtopping of a sloping structure,
    gamma_beta = 1 - 0.0063 |beta| for |beta| <= 80 degrees, and the value at
    80 degrees beyond that.
    """
    if kind != "overtopping":
        raise ValueError(f"Unknown factor kind {kind!r}")
    beta = min(abs(beta_degrees), 80.0)
    return 1.0 - 0.0063 * beta


def overtopping_with_uncertainty(result: dict, factor: float = 3.0) -> dict:
    """Bracket a mean discharge with EurOtop's reported scatter.

    EurOtop notes roughly a factor of three about the mean for the sloping
    formulae. Design against the upper bound, not the mean.
    """
    if factor < 1.0:
        raise ValueError(f"Scatter factor must be at least 1, got {factor}")
    q = result["q"]
    return {"q_mean": q, "q_lower": q / factor, "q_upper": q * factor}


def required_crest_freeboard(
    conditions: DesignConditions,
    q_allowable: float,
    cot_alpha: float,
    gamma_f: float = 1.0,
    gamma_beta: float = 1.0,
    gamma_b: float = 1.0,
    gamma_v: float = 1.0,
    vertical: bool = False,
    tolerance: float = 1e-4,
) -> float:
    """Crest freeboard Rc that limits mean overtopping to ``q_allowable``.

    Inverts the relevant EurOtop expression by bisection, since the two
    branches make an analytic inverse awkward. ``q_allowable`` is in l/s per m.
    """
    if q_allowable <= 0:
        raise ValueError(f"Allowable discharge must be positive, got {q_allowable}")

    def discharge(Rc: float) -> float:
        if vertical:
            return overtopping_vertical(conditions, Rc, gamma_beta)["q"]
        return overtopping_sloped(
            conditions, Rc, cot_alpha, gamma_f, gamma_beta, gamma_b, gamma_v
        )["q"]

    low, high = 1e-3, 1.0
    while discharge(high) > q_allowable:
        high *= 2.0
        if high > 1000.0 * conditions.Hm0:
            raise RuntimeError(
                "No freeboard within 1000 Hm0 achieves the allowable discharge."
            )

    while high - low > tolerance:
        mid = 0.5 * (low + high)
        if discharge(mid) > q_allowable:
            low = mid
        else:
            high = mid
    return high


def assess_overtopping(q: float) -> dict:
    """Which uses a given mean discharge is tolerable for.

    ``q`` is in l/s per m. Returns each limit in ``TOLERABLE_DISCHARGE`` with
    whether it is satisfied, sorted from strictest to most permissive.
    """
    out = {}
    for key, (limit, description) in sorted(
        TOLERABLE_DISCHARGE.items(), key=lambda kv: kv[1][0]
    ):
        out[key] = {
            "limit": limit,
            "description": description,
            "acceptable": q <= limit,
        }
    return out


# ---------------------------------------------------------------------------
# Whole-section design
# ---------------------------------------------------------------------------


@dataclass
class BreakwaterDesign:
    """A rubble-mound cross-section sized against a design condition."""

    conditions: DesignConditions
    cot_alpha: float
    Dn50: float
    M50: float
    regime: str
    crest_freeboard: float
    q_mean: float
    q_upper: float
    layer: dict
    armour_type: str
    governing_limit: str | None

    def summary(self) -> str:
        """A short design report."""
        c = self.conditions
        lines = [
            f"Design condition   Hm0 = {c.Hm0:.2f} m, Tm-1,0 = {c.Tm10:.2f} s, "
            f"depth = {c.depth:.1f} m",
            f"Storm              {c.storm_duration / 3600:.1f} h, "
            f"N = {c.wave_count:.0f} waves",
            f"Slope              1 : {self.cot_alpha:g}",
            f"Armour             {self.armour_type}, Dn50 = {self.Dn50:.2f} m, "
            f"M50 = {self.M50 / 1000:.1f} t ({self.regime})",
            f"Layer              {self.layer['thickness']:.2f} m thick, "
            f"{self.layer['stones_per_m2']:.2f} stones/m2",
            f"Crest freeboard    Rc = {self.crest_freeboard:.2f} m "
            f"(Rc/Hm0 = {self.crest_freeboard / c.Hm0:.2f})",
            f"Overtopping        mean {self.q_mean:.3g} l/s/m, "
            f"upper bound {self.q_upper:.3g} l/s/m",
        ]
        if self.governing_limit:
            limit, description = TOLERABLE_DISCHARGE[self.governing_limit]
            lines.append(f"Governing limit    {limit:g} l/s/m, {description}")
        return "\n".join(lines)


def design_rubble_mound(
    conditions: DesignConditions,
    cot_alpha: float = 2.0,
    armour: str = "rock_two_layer_permeable",
    damage: float = 2.0,
    permeability: float = 0.4,
    Delta: float = 1.585,
    tolerable_use: str = "trained_staff",
    safety_factor: float = 1.0,
    scatter_factor: float = 3.0,
) -> BreakwaterDesign:
    """Size armour and crest level for a rubble-mound section.

    Sizes the stone with Van der Meer, then sets the crest so that the
    *upper* confidence bound on overtopping, not the mean, meets the limit
    for ``tolerable_use``. Designing to the mean would be exceeded about half
    the time.
    """
    if armour not in ROUGHNESS_FACTORS:
        raise ValueError(
            f"Unknown armour {armour!r}. Options: {sorted(ROUGHNESS_FACTORS)}"
        )
    if tolerable_use not in TOLERABLE_DISCHARGE:
        raise ValueError(
            f"Unknown use {tolerable_use!r}. Options: {sorted(TOLERABLE_DISCHARGE)}"
        )

    stability = rock_armour_vandermeer(
        conditions, cot_alpha, Delta=Delta, permeability=permeability,
        damage=damage, safety_factor=safety_factor,
    )
    gamma_f = ROUGHNESS_FACTORS[armour]
    q_limit = TOLERABLE_DISCHARGE[tolerable_use][0]

    # Design the crest against the upper bound of the scatter band.
    Rc = required_crest_freeboard(
        conditions, q_limit / scatter_factor, cot_alpha, gamma_f=gamma_f
    )
    q = overtopping_sloped(conditions, Rc, cot_alpha, gamma_f=gamma_f)
    band = overtopping_with_uncertainty(q, scatter_factor)

    return BreakwaterDesign(
        conditions=conditions,
        cot_alpha=cot_alpha,
        Dn50=stability["Dn50"],
        M50=stability["M50"],
        regime=stability["regime"],
        crest_freeboard=Rc,
        q_mean=band["q_mean"],
        q_upper=band["q_upper"],
        layer=armour_layer(stability["Dn50"]),
        armour_type=armour,
        governing_limit=tolerable_use,
    )


# ---------------------------------------------------------------------------
# Toe scour
# ---------------------------------------------------------------------------


def reflection_coefficient(cot_alpha: float, surf_similarity: float,
                           permeable: bool = True) -> float:
    """Reflection coefficient of a rough slope, Seelig and Ahrens (1981).

        Kr = a xi^2 / (b + xi^2)

    with a = 0.6 and b = 6.6 for a permeable rubble mound, and a = 1.0,
    b = 5.5 for a smooth impermeable slope. A vertical wall reflects almost
    everything; a rubble mound dissipates most of it, which is why the
    scour in front of the two is not the same problem.
    """
    if surf_similarity <= 0:
        raise ValueError(f"Surf similarity must be positive, got {surf_similarity}")
    a, b = (0.6, 6.6) if permeable else (1.0, 5.5)
    xi2 = surf_similarity ** 2
    return min(a * xi2 / (b + xi2), 1.0)


def toe_scour(
    bed,
    Hs: float,
    T: float,
    depth: float,
    reflection: float = 1.0,
    coefficient: float = 0.4,
    exponent: float = 1.35,
) -> dict:
    """Equilibrium scour depth at the toe of a marine structure [m].

    The standing-wave form, as for a vertical wall::

        S / Hs = coefficient * Kr / sinh(k h) ** exponent

    Parameters
    ----------
    bed : Sediment or str
        What the bed is made of. This decides whether there is any scour to
        compute: a bed below its threshold of motion in the approach waves
        is in the clear-water regime, where a live-bed relation overstates
        the hole, and a cohesive bed is not governed by this at all.
    reflection : float
        Reflection coefficient Kr of the structure. 1.0 for a vertical
        wall, which recovers Xie (1981) exactly; roughly 0.2 to 0.5 for a
        rubble mound, from :func:`reflection_coefficient`.
    coefficient : float
        0.4 is Xie's value for fine sand under regular waves at a fully
        reflecting wall, and is the usual design number.
    exponent : float
        1.35, from the same work.

    Returns
    -------
    dict
        The ``depth``, the mobility state of the bed, and whether the
        relation is being applied inside the regime it came from.

    Notes
    -----
    Scaling Xie's fully reflecting result by the reflection coefficient is
    an engineering assumption, not a calibrated relation: it has the right
    limits, going to Xie at a vertical wall and to nothing at a perfect
    absorber, and it puts a rubble mound sensibly below a caisson. It is a
    screening number. A scheme whose toe design turns on it wants a mobile
    bed model or a physical model, and the returned dict says as much
    through ``screening_only``.
    """
    from .sediment import bed_mobility, sediment as _lookup

    grains = _lookup(bed) if isinstance(bed, str) else bed
    if not 0.0 <= reflection <= 1.0:
        raise ValueError(f"Reflection coefficient must be in [0,1], got {reflection}")
    if coefficient < 0:
        raise ValueError(f"Coefficient must be non-negative, got {coefficient}")

    L = dispersion(T, depth)
    kh = 2 * math.pi * depth / L
    unlimited = coefficient * reflection * Hs / math.sinh(kh) ** exponent

    mobility = bed_mobility(grains, Hs, T, depth)
    note = mobility["note"]

    if grains.cohesive:
        return {
            "depth": 0.0, "unlimited_depth": unlimited, "reflection": reflection,
            "mobility": mobility, "applies": False, "screening_only": True,
            "note": note,
        }

    # A bed that never moves does not scour to the live-bed depth. The
    # structure still amplifies the flow locally, so this is not zero, but
    # the live-bed number is an overstatement and is reported as such.
    scour = unlimited if mobility["mobile"] else 0.5 * unlimited

    return {
        "depth": scour,
        "unlimited_depth": unlimited,
        "reflection": reflection,
        "relative_depth": kh,
        "mobility": mobility,
        "applies": mobility["mobile"],
        "screening_only": True,
        "note": note,
    }


def breakwater_toe_scour(design, depth: float, bed="medium_sand",
                         permeable: bool = True) -> dict:
    """Toe scour in front of a designed rubble mound.

    Takes the reflection from the slope and the surf similarity of the
    design condition, so a flatter, rougher, more permeable mound is
    correctly predicted to scour its own toe less than a steep one.
    """
    xi = design.conditions.breaker_parameter(design.cot_alpha)
    Kr = reflection_coefficient(design.cot_alpha, xi, permeable)
    result = toe_scour(bed, design.conditions.Hm0, design.conditions.Tm10,
                       depth, reflection=Kr)
    result["surf_similarity"] = xi
    # The apron has to reach past the hole and be heavy enough to stay put.
    result["apron_width"] = max(2.0 * result["depth"], 1.5 * design.Dn50, 2.0)
    return result


# ---------------------------------------------------------------------------
# What the mound stands on
# ---------------------------------------------------------------------------


def mound_foundation(design, depth: float, bed="medium_sand",
                     permeable: bool = True, bedding_material="coarse_sand",
                     settlement_allowance: float = 0.0) -> dict:
    """Bedding blanket, toe berm and geotextile under a rubble mound.

    A trapezoid of rock does not sit straight on the seabed. Under it goes a
    levelling blanket of graded sand and gravel, on a geotextile, carried
    well past both toes so the scour hole forms in the apron rather than
    under the structure. At the foot of the armour sits a berm of the same
    stone as the filter layer, which is what stops the bottom of the
    mantle unravelling.

    Parameters
    ----------
    design : BreakwaterDesign
        The sized mound.
    depth : float
        Water depth at the toe [m].
    bed : Sediment or str
        The natural seabed. Decides the scour, and therefore how far the
        blanket has to reach.
    bedding_material : Sediment or str
        The blanket itself, normally a well graded sand and gravel.
    settlement_allowance : float
        Extra blanket thickness for consolidation of a soft seabed [m].

    Returns
    -------
    dict
        Every dimension the section needs, and the scour result behind it.

    Notes
    -----
    Two rules are doing the work.

    The toe berm takes the same stone as the filter layer rather than the
    armour. It sits low, where the orbital velocities are much smaller than
    at the waterline, and sizing it as armour is expensive without being
    safer. This follows normal Italian and Rock Manual practice.

    The blanket reaches past the toe by whichever is larger of the computed
    scour apron and twice the predicted scour depth, with a floor of three
    metres for something a dredger can actually place. Its job is to keep
    the edge of the hole away from the toe, so it has to be wider than the
    hole is deep.
    """
    from .sediment import sediment as _lookup

    blanket = _lookup(bedding_material) if isinstance(bedding_material, str) \
        else bedding_material
    if settlement_allowance < 0:
        raise ValueError(
            f"Settlement allowance must be non-negative, got {settlement_allowance}"
        )

    scour = breakwater_toe_scour(design, depth, bed=bed, permeable=permeable)

    # Filter stone, a tenth of the armour mass, is what the toe berm takes.
    Dn_filter = design.Dn50 / 10.0 ** (1.0 / 3.0)
    toe_thickness = 2.0 * Dn_filter
    toe_width = max(3.0 * Dn_filter, 0.5 * design.conditions.Hm0, 2.0)

    bedding_thickness = max(0.6, 1.5 * Dn_filter) + settlement_allowance
    extension = max(scour["apron_width"], 2.0 * scour["depth"], 3.0)

    return {
        "scour": scour,
        "toe_Dn50": Dn_filter,
        "toe_M50": 2650.0 * Dn_filter**3,
        "toe_width": toe_width,
        "toe_thickness": toe_thickness,
        "bedding": blanket,
        "bedding_thickness": bedding_thickness,
        "bedding_extension": extension,
        "settlement_allowance": settlement_allowance,
        "geotextile": True,
    }


def crown_wall(design, still_water_level: float, deck_width: float = 7.5,
               parapet_width: float = 2.0, parapet_height: float | None = None,
               base_below_crest: float | None = None) -> dict:
    """A concrete crown block on the crest, in the usual stepped form.

    A parapet on the seaward side to take the run-up, a deck behind it wide
    enough to drive a lorry along for maintenance, and a base bedded into
    the core below the armour crest.

    Returns
    -------
    dict
        Levels and widths for the block, and its concrete volume per metre
        run at 2400 kg/m3.

    Notes
    -----
    The block is proportioned here, not designed. Sliding and overturning
    of a crown wall under wave impact are a separate calculation, and a
    real one also has to survive the uplift that gets under it when the
    core does not drain fast enough.
    """
    crest = still_water_level + design.crest_freeboard
    if parapet_height is None:
        # The parapet stands proud of the armour crest by enough to catch
        # the run-up tongue without becoming a wave-reflecting wall.
        parapet_height = max(0.3 * design.conditions.Hm0, 1.0)
    if base_below_crest is None:
        base_below_crest = design.layer["thickness"]
    if deck_width <= 0 or parapet_width <= 0:
        raise ValueError("Deck and parapet widths must be positive")

    base_level = crest - base_below_crest
    deck_level = crest
    parapet_top = crest + parapet_height

    area = (parapet_width * (parapet_top - base_level)
            + deck_width * (deck_level - base_level))
    return {
        "base_level": base_level,
        "deck_level": deck_level,
        "parapet_top": parapet_top,
        "parapet_width": parapet_width,
        "deck_width": deck_width,
        "total_width": parapet_width + deck_width,
        "concrete_m3_per_m": area,
        "concrete_t_per_m": area * 2.4,
    }
