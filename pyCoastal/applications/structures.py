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
    Delft Hydraulics Publication 396. Rock armour stability, and the cube
    and tetrapod formulae.

Van Gent, M. R. A., Smale, A. J. and Kuiper, C. (2003), "Stability of rock
    slopes with shallow foreshores", Proc. Coastal Structures 2003. The
    form of Van der Meer's rock formula written in Tm-1,0 and H2%, as
    adopted by the Rock Manual (2007).

Pedersen, J. (1996), "Experimental study of wave forces and wave overtopping
    on breakwater crown walls", Series Paper 12, Aalborg University, as
    given in the Coastal Engineering Manual (2011), Table VI-5-61. Crown
    wall loads.

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
RHO_W = 1025.0
RHO_ROCK = 2650.0
RHO_CONCRETE = 2400.0

#: Tm-1,0 / Tm for a single-peaked JONSWAP spectrum: Tp = 1.1 Tm-1,0 and
#: Tp = 1.28 Tm (Goda 2010), so Tm = Tm-1,0 / 1.164. Van der Meer's damage
#: counts and the Pedersen run-up are written in the mean period Tm.
SPECTRAL_TO_MEAN_PERIOD = 1.28 / 1.1


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
    def mean_period(self) -> float:
        """Mean period Tm [s], from Tm-1,0 for a JONSWAP spectrum."""
        return self.Tm10 / SPECTRAL_TO_MEAN_PERIOD

    @property
    def wave_count(self) -> float:
        """Number of waves in the design storm, N = duration / Tm.

        Van der Meer's damage relation saturates near N = 7500, so the count
        is capped there; a longer storm does not keep eroding the slope at
        the same rate.
        """
        return min(self.storm_duration / self.mean_period, 7500.0)

    def mean_steepness(self) -> float:
        """Fictitious steepness s_om = Hm0 / L_om, with L_om from Tm."""
        return self.Hm0 / (G * self.mean_period**2 / (2 * math.pi))

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
    height_ratio: float = 1.4,
) -> dict:
    """Nominal rock diameter Dn50, Van der Meer as modified by Van Gent (2003).

    The Rock Manual (2007) form, written in the spectral period Tm-1,0 and
    the 2 % wave height, which keeps it valid on shallow foreshores:

    plunging (xi < xi_cr)
        Hs / (Delta Dn50) = 8.4 P^0.18 (S / sqrt(N))^0.2 (Hs / H2%) xi^-0.5
    surging (xi >= xi_cr)
        Hs / (Delta Dn50) = 1.3 P^-0.13 (S / sqrt(N))^0.2 (Hs / H2%)
                            sqrt(cot a) xi^P

    with xi = xi_m-1,0 and xi_cr = (8.4 / 1.3 P^0.31 sqrt(tan a))^(1 / (P + 0.5)).
    The original 1988 coefficients (6.2 and 1.0) belong to the mean period
    Tm, and using them with Tm-1,0 undersizes surging stone.

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
    height_ratio : float
        H2% / Hs. 1.4 is the Rayleigh value for deep water. On a shallow
        foreshore the ratio falls (Battjes and Groenendijk 2000), so 1.4
        is conservative there.

    Returns
    -------
    dict
        ``Dn50`` [m], ``M50`` [kg] for 2650 kg/m3 rock, the regime that
        governed, ``xi``, and ``xi_cr``.
    """
    if cot_alpha <= 0:
        raise ValueError(f"cot(alpha) must be positive, got {cot_alpha}")
    if not 0.0 < permeability <= 0.7:
        raise ValueError(f"Permeability P must be in (0, 0.7], got {permeability}")
    if damage <= 0:
        raise ValueError(f"Damage level S must be positive, got {damage}")
    if safety_factor <= 0:
        raise ValueError(f"Safety factor must be positive, got {safety_factor}")
    if height_ratio < 1.0:
        raise ValueError(f"H2%/Hs must be at least 1, got {height_ratio}")

    P = permeability
    S = damage
    N = conditions.wave_count
    xi = conditions.breaker_parameter(cot_alpha)
    tan_alpha = 1.0 / cot_alpha

    cp = 8.4 / safety_factor
    cs = 1.3 / safety_factor

    xi_cr = ((cp / cs) * P**0.31 * math.sqrt(tan_alpha)) ** (1.0 / (P + 0.5))
    damage_term = (S / math.sqrt(N)) ** 0.2 / height_ratio

    if xi < xi_cr:
        regime = "plunging"
        stability = cp * P**0.18 * damage_term * xi**-0.5
    else:
        regime = "surging"
        stability = cs * P**-0.13 * damage_term * math.sqrt(cot_alpha) * xi**P

    Dn50 = conditions.Hm0 / (Delta * stability)
    return {
        "Dn50": Dn50,
        "M50": RHO_ROCK * Dn50**3,
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
    Dn50: float, n_layers: int = 2, layer_coefficient: float = 1.0,
    porosity: float = 0.37, density: float = RHO_ROCK,
) -> dict:
    """Armour layer thickness and unit count (Rock Manual, 2007).

    thickness = n * k_delta * Dn50, and the number of units per unit area is
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
        "mass_per_m2": per_area * density * Dn50**3,
    }


#: Concrete armour units: stability relation and layer geometry.
#: ``formula`` is "cubes" or "tetrapods" for the Van der Meer (1988)
#: relations, "Ns" for a design stability number, and "hudson" for a Hudson
#: KD on Hs. Layer coefficients and porosities are the usual CEM / Rock
#: Manual values and are indicative; the unit supplier's figures govern.
CONCRETE_UNITS = {
    "cubes_two_layer_random": {"formula": "cubes", "layers": 2,
                               "k": 1.10, "porosity": 0.47, "cot": 1.5},
    "cubes_one_layer_flat": {"formula": "cubes", "layers": 1,
                             "k": 1.00, "porosity": 0.30, "cot": 1.5},
    "antifer": {"formula": "cubes", "layers": 2,
                "k": 1.10, "porosity": 0.46, "cot": 1.5},
    "tetrapod": {"formula": "tetrapods", "layers": 2,
                 "k": 1.04, "porosity": 0.50, "cot": 1.5},
    "accropode": {"formula": "Ns", "Ns": 2.7, "layers": 1,
                  "k": 1.51, "porosity": 0.52, "cot": 1.33},
    "core_loc": {"formula": "Ns", "Ns": 2.8, "layers": 1,
                 "k": 1.51, "porosity": 0.60, "cot": 1.33},
    "xbloc": {"formula": "Ns", "Ns": 2.8, "layers": 1,
              "k": 1.40, "porosity": 0.58, "cot": 1.33},
    "dolos": {"formula": "hudson", "KD": 16.0, "layers": 2,
              "k": 0.94, "porosity": 0.56, "cot": 2.0},
}


def concrete_armour(
    conditions: DesignConditions,
    unit: str,
    cot_alpha: float,
    damage: float = 0.5,
    density: float = RHO_CONCRETE,
    safety_factor: float = 1.0,
) -> dict:
    """Nominal size of a concrete armour unit.

    cubes, two layers (Van der Meer 1988)
        Hs / (Delta Dn) = (6.7 Nod^0.4 / N^0.3 + 1.0) s_om^-0.1
    tetrapods, two layers (Van der Meer 1988)
        Hs / (Delta Dn) = (3.75 Nod^0.5 / N^0.25 + 0.85) s_om^-0.2
    single-layer interlocking units
        Hs / (Delta Dn) = Ns, the design stability number: 2.7 for
        Accropode, 2.8 for Core-Loc and Xbloc (CEM Table VI-5-37 and the
        suppliers' guidance), which already carries a margin on the
        start-of-damage value.
    dolos
        Hudson with KD = 16 on Hs.

    Parameters
    ----------
    damage : float
        Nod, units displaced per strip one Dn wide. 0.5 is the start of
        damage and the usual design value.
    density : float
        Concrete density [kg/m3].

    Notes
    -----
    The cube and tetrapod formulae were fitted on a 1:1.5 slope and the
    single-layer design numbers assume about 3:4. The returned
    ``slope_note`` says so when the section departs from that.
    """
    if unit not in CONCRETE_UNITS:
        raise ValueError(f"Unknown concrete unit {unit!r}. Options: "
                         f"{sorted(CONCRETE_UNITS)}")
    if damage <= 0:
        raise ValueError(f"Damage Nod must be positive, got {damage}")
    if safety_factor <= 0:
        raise ValueError(f"Safety factor must be positive, got {safety_factor}")

    spec = CONCRETE_UNITS[unit]
    Delta = density / RHO_W - 1.0
    N = conditions.wave_count
    s_om = conditions.mean_steepness()
    kind = spec["formula"]
    if kind == "cubes":
        Ns = (6.7 * damage**0.4 / N**0.3 + 1.0) * s_om**-0.1
        source = "Van der Meer (1988), cubes"
    elif kind == "tetrapods":
        Ns = (3.75 * damage**0.5 / N**0.25 + 0.85) * s_om**-0.2
        source = "Van der Meer (1988), tetrapods"
    elif kind == "Ns":
        Ns = spec["Ns"]
        source = f"design Ns = {spec['Ns']:g}"
    else:
        Ns = (spec["KD"] * cot_alpha) ** (1.0 / 3.0)
        source = f"Hudson, KD = {spec['KD']:g}"
    Ns /= safety_factor

    Dn = conditions.Hm0 / (Delta * Ns)
    note = None
    if abs(cot_alpha - spec["cot"]) > 0.26:
        note = (f"{unit.replace('_', ' ')} stability was established on a "
                f"1:{spec['cot']:g} slope; this section is 1:{cot_alpha:g}.")
    return {
        "Dn50": Dn,
        "M50": density * Dn**3,
        "stability_number": Ns,
        "source": source,
        "Delta": Delta,
        "density": density,
        "slope_note": note,
        "xi": conditions.breaker_parameter(cot_alpha),
    }


def layer_for(armour: str, Dn50: float, density: float) -> dict:
    """The armour layer of an armour type, from its unit size."""
    spec = CONCRETE_UNITS.get(armour)
    if spec is None:
        return armour_layer(Dn50, density=density)
    return armour_layer(Dn50, n_layers=spec["layers"],
                        layer_coefficient=spec["k"],
                        porosity=spec["porosity"], density=density)


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
    #: "trunk" or "head". The head carries heavier armour for the same wave.
    section: str = "trunk"
    #: KD_head / KD_trunk, set only on a head section.
    kd_ratio: float | None = None
    #: Density of the armour units [kg/m3]: rock or concrete.
    density: float = RHO_ROCK
    warnings: list[str] = field(default_factory=list)

    @property
    def concrete(self) -> bool:
        """True when the armour is a concrete unit rather than rock."""
        return self.armour_type in CONCRETE_UNITS

    @property
    def underlayer_Dn50(self) -> float:
        """Underlayer rock, a tenth of the armour unit mass (Rock Manual)."""
        return (self.M50 / 10.0 / RHO_ROCK) ** (1.0 / 3.0)

    def summary(self) -> str:
        """A short design report."""
        c = self.conditions
        lines = [
            f"Design condition   Hm0 = {c.Hm0:.2f} m, Tm-1,0 = {c.Tm10:.2f} s, "
            f"depth = {c.depth:.1f} m",
            f"Storm              {c.storm_duration / 3600:.1f} h, "
            f"N = {c.wave_count:.0f} waves",
            f"Section            {self.section}"
            + (f", KD ratio {self.kd_ratio:.2f} of the trunk"
               if self.kd_ratio else ""),
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
        if self.warnings:
            lines += ["", "Warnings"] + [f"  - {w}" for w in self.warnings]
        return "\n".join(lines)


def depth_limit_warnings(conditions: DesignConditions) -> list[str]:
    """Flags for a wave height the toe depth cannot carry or barely can."""
    ratio = conditions.Hm0 / conditions.depth
    if ratio > 0.6:
        return [
            f"Hm0 = {conditions.Hm0:.2f} m is {ratio:.2f} of the "
            f"{conditions.depth:.1f} m toe depth. A significant height above "
            "about 0.6 h cannot reach the toe without breaking; the design "
            "wave and the depth are inconsistent and the sizing is not "
            "meaningful until one of them is corrected."
        ]
    if ratio > 0.2:
        return [
            f"Hm0/h = {ratio:.2f}: the toe is in shallow water. H2% is taken "
            "as 1.4 Hs from the Rayleigh distribution, which overstates it "
            "here and errs on the heavy side; Battjes and Groenendijk (2000) "
            "with the foreshore slope gives the real ratio."
        ]
    return []


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
    unit_damage: float = 0.5,
    concrete_density: float = RHO_CONCRETE,
) -> BreakwaterDesign:
    """Size armour and crest level for a rubble-mound section.

    Rock is sized with Van der Meer in the Van Gent (2003) form; concrete
    units with their own relations (:func:`concrete_armour`). The crest is
    set so that the *upper* confidence bound on overtopping, not the mean,
    meets the limit for ``tolerable_use``. Designing to the mean would be
    exceeded about half the time.

    Parameters
    ----------
    damage : float
        Damage level S for rock.
    unit_damage : float
        Damage number Nod for concrete units.
    """
    if armour not in ROUGHNESS_FACTORS:
        raise ValueError(
            f"Unknown armour {armour!r}. Options: {sorted(ROUGHNESS_FACTORS)}"
        )
    if tolerable_use not in TOLERABLE_DISCHARGE:
        raise ValueError(
            f"Unknown use {tolerable_use!r}. Options: {sorted(TOLERABLE_DISCHARGE)}"
        )

    warnings = depth_limit_warnings(conditions)
    if armour in CONCRETE_UNITS:
        stability = concrete_armour(conditions, armour, cot_alpha,
                                    damage=unit_damage,
                                    density=concrete_density,
                                    safety_factor=safety_factor)
        regime = stability["source"]
        density = concrete_density
        if stability["slope_note"]:
            warnings.append(stability["slope_note"])
    else:
        stability = rock_armour_vandermeer(
            conditions, cot_alpha, Delta=Delta, permeability=permeability,
            damage=damage, safety_factor=safety_factor,
        )
        regime = stability["regime"]
        density = RHO_W * (1.0 + Delta)
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
        M50=density * stability["Dn50"] ** 3,
        regime=regime,
        crest_freeboard=Rc,
        q_mean=band["q_mean"],
        q_upper=band["q_upper"],
        layer=layer_for(armour, stability["Dn50"], density),
        armour_type=armour,
        governing_limit=tolerable_use,
        density=density,
        warnings=warnings,
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
    Dn_filter = design.underlayer_Dn50
    toe_thickness = 2.0 * Dn_filter
    toe_width = max(3.0 * Dn_filter, 0.5 * design.conditions.Hm0, 2.0)

    bedding_thickness = max(0.6, 1.5 * Dn_filter) + settlement_allowance
    extension = max(scour["apron_width"], 2.0 * scour["depth"], 3.0)

    return {
        "scour": scour,
        "toe_Dn50": Dn_filter,
        "toe_M50": RHO_ROCK * Dn_filter**3,
        "toe_width": toe_width,
        "toe_thickness": toe_thickness,
        "bedding": blanket,
        "bedding_thickness": bedding_thickness,
        "bedding_extension": extension,
        "settlement_allowance": settlement_allowance,
        "geotextile": True,
    }


def pedersen_crown_loads(conditions: DesignConditions, cot_alpha: float,
                         armour_freeboard: float, berm_width: float,
                         protected_height: float,
                         unprotected_height: float) -> dict:
    """Wave loads on a crown wall behind an armour berm, Pedersen (1996).

    As given in the Coastal Engineering Manual, Table VI-5-61::

        F_h,0.1% = 0.21 sqrt(L_om / B) (1.6 p_m y_eff + A p_m / 2 h')
        M_0.1%   = 0.55 (h' + y_eff) F_h,0.1%
        p_b,0.1% = 1.00 A p_m

    with p_m = rho_w g (R_u,0.1% - A_c), the run-up
    R_u,0.1% = 1.12 Hs xi_m (xi_m <= 1.5) or 1.34 Hs xi_m^0.55, xi_m on the
    mean period, the wedge thickness
    y = (R_u,0.1% - A_c) / sin(a) * sin(15 deg) / cos(a - 15 deg), and
    y_eff = min(y / 2, f_c).

    Parameters
    ----------
    armour_freeboard : float
        A_c, armour crest above still water [m].
    berm_width : float
        B, width of the armour berm in front of the wall [m].
    protected_height : float
        h', height of the wall face below the armour crest [m].
    unprotected_height : float
        f_c, height of the wall face above the armour crest [m].

    Notes
    -----
    A = min(A2 / A1, 1) compares the run-up wedge with the berm cross
    section; it is taken as 1, its upper bound. The horizontal force and
    the uplift do not peak together, so combining them is conservative.
    Pedersen's tests cover xi_m 1.1 to 5.2, Hm0/Ac 0.5 to 1.5, Ac/B 1 to
    2.6, cot a 1.5 to 3.5 and Hm0/h 0.16 to 0.35; ``outside`` lists the
    ranges this section leaves. Norgaard et al. (2013) show the formulae
    overpredict in shallow water, so they err on the safe side there.
    """
    if berm_width <= 0:
        raise ValueError(f"Berm width must be positive, got {berm_width}")
    Hs = conditions.Hm0
    Lom = G * conditions.mean_period**2 / (2 * math.pi)
    alpha = math.atan(1.0 / cot_alpha)
    xi_m = math.tan(alpha) / math.sqrt(Hs / Lom)
    Ru = 1.12 * Hs * xi_m if xi_m <= 1.5 else 1.34 * Hs * xi_m**0.55
    Ac = armour_freeboard
    p_m = max(RHO_W * G * (Ru - Ac) / 1000.0, 0.0)      # kPa
    y = max((Ru - Ac) / math.sin(alpha) * math.sin(math.radians(15.0))
            / math.cos(alpha - math.radians(15.0)), 0.0)
    y_eff = min(y / 2.0, unprotected_height)
    A = 1.0
    scale = 0.21 * math.sqrt(Lom / berm_width)
    Fh = scale * (1.6 * p_m * y_eff + A * p_m / 2.0 * protected_height)
    M = 0.55 * (protected_height + y_eff) * Fh
    pb = 1.00 * A * p_m

    outside = []
    for name, value, low, high in (
        ("xi_m", xi_m, 1.1, 5.2),
        ("Hm0/Ac", Hs / Ac if Ac > 0 else float("inf"), 0.5, 1.5),
        ("Ac/B", Ac / berm_width, 1.0, 2.6),
        ("cot a", cot_alpha, 1.5, 3.5),
        ("Hm0/h", Hs / conditions.depth, 0.16, 0.35),
    ):
        if not low <= value <= high:
            outside.append(f"{name} = {value:.2f} (tested {low:g} to {high:g})")
    return {"Fh": Fh, "M": M, "pb": pb, "p_m": p_m, "Ru": Ru, "xi_m": xi_m,
            "y": y, "y_eff": y_eff, "A": A, "Lom": Lom, "outside": outside}


def crown_wall(design, still_water_level: float, deck_width: float = 7.5,
               parapet_width: float = 2.0, parapet_height: float | None = None,
               base_below_crest: float | None = None,
               berm_width: float | None = None, friction: float = 0.6,
               target_sliding: float = 1.2, target_overturning: float = 1.5,
               max_deck_width: float = 25.0, step: float = 0.25) -> dict:
    """A concrete crown block on the crest, checked for stability.

    A parapet on the seaward side to take the run-up, a deck behind it wide
    enough to drive a lorry along for maintenance, and a base bedded into
    the underlayer below the armour crest. The armour runs on in front of
    the parapet as a berm ``berm_width`` wide.

    The block is loaded with Pedersen's horizontal force and uplift
    (:func:`pedersen_crown_loads`), taken together, and the deck is widened
    until sliding and overturning about the rear heel meet their targets.

    Returns
    -------
    dict
        Levels and widths for the block, its concrete volume per metre run
        at 2400 kg/m3, the loads, both factors of safety and any warnings.
    """
    armour_crest = still_water_level + design.crest_freeboard
    if parapet_height is None:
        # The parapet stands proud of the armour crest by enough to catch
        # the run-up tongue without becoming a wave-reflecting wall.
        parapet_height = max(0.3 * design.conditions.Hm0, 1.0)
    if base_below_crest is None:
        base_below_crest = design.layer["thickness"]
    if berm_width is None:
        berm_width = max(3.0 * design.Dn50, 2.0)
    if deck_width <= 0 or parapet_width <= 0:
        raise ValueError("Deck and parapet widths must be positive")

    base_level = armour_crest - base_below_crest
    deck_level = armour_crest
    parapet_top = armour_crest + parapet_height
    loads = pedersen_crown_loads(design.conditions, design.cot_alpha,
                                 design.crest_freeboard, berm_width,
                                 base_below_crest, parapet_height)
    gamma_c = RHO_CONCRETE * G / 1000.0
    gamma_w = RHO_W * G / 1000.0

    def weight(z0: float, z1: float, width: float) -> float:
        """Weight of a block, buoyant below still water."""
        wet = min(max(still_water_level - z0, 0.0), z1 - z0)
        return (gamma_c * (z1 - z0) - gamma_w * wet) * width

    warnings: list[str] = []
    sliding = overturning = 0.0
    while True:
        total = parapet_width + deck_width
        parts = [
            (weight(base_level, parapet_top, parapet_width),
             total - 0.5 * parapet_width),
            (weight(base_level, deck_level, deck_width), 0.5 * deck_width),
        ]                                             # arm from the rear heel
        W = sum(w for w, _ in parts)
        uplift = 0.5 * loads["pb"] * total            # triangular, peak at front
        if loads["Fh"] > 0:
            sliding = friction * max(W - uplift, 0.0) / loads["Fh"]
            resisting = sum(w * x for w, x in parts) - uplift * (2.0 / 3.0) * total
            overturning = max(resisting, 0.0) / loads["M"]
        else:
            sliding = overturning = float("inf")
        if sliding >= target_sliding and overturning >= target_overturning:
            break
        if deck_width >= max_deck_width:
            warnings.append(
                f"The crown block reached a {total:.1f} m width with sliding "
                f"{sliding:.2f} and overturning {overturning:.2f}. Lower the "
                "parapet, widen the armour berm in front of it or key the "
                "base into the core."
            )
            break
        deck_width += step
    if loads["outside"]:
        warnings.append("Pedersen crown wall loads applied outside the "
                        "tested range: " + "; ".join(loads["outside"]) + ".")

    area = (parapet_width * (parapet_top - base_level)
            + deck_width * (deck_level - base_level))
    return {
        "base_level": base_level,
        "deck_level": deck_level,
        "parapet_top": parapet_top,
        "parapet_width": parapet_width,
        "deck_width": deck_width,
        "total_width": parapet_width + deck_width,
        "berm_width": berm_width,
        "concrete_m3_per_m": area,
        "concrete_t_per_m": area * RHO_CONCRETE / 1000.0,
        "loads": loads,
        "weight": W,
        "uplift": uplift,
        "sliding_FoS": sliding,
        "overturning_FoS": overturning,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# The roundhead
# ---------------------------------------------------------------------------

#: Ratio of the roundhead stability coefficient to the trunk value,
#: KD_head / KD_trunk. Indicative, and slope dependent: the Shore Protection
#: Manual tabulates the two separately and the governing edition should be
#: read rather than this table. The shape is what matters and is not in
#: doubt: interlocking units lose more at the head than rough rock does,
#: because their interlock depends on neighbours a curved surface cannot
#: provide, and every unit loses more on a flatter slope.
ROUNDHEAD_KD_RATIO = {
    "rock": {1.5: 0.95, 2.0: 0.80, 3.0: 0.65},
    "cubes": {1.5: 0.85, 2.0: 0.75, 3.0: 0.60},
    "tetrapod": {1.5: 0.72, 2.0: 0.64, 3.0: 0.50},
    "accropode": {1.5: 0.80, 2.0: 0.75, 3.0: 0.65},
    "dolos": {1.5: 0.65, 2.0: 0.58, 3.0: 0.45},
}

#: Which family an armour type belongs to, for the table above.
ARMOUR_FAMILY = {
    "rock_one_layer_impermeable": "rock",
    "rock_two_layer_impermeable": "rock",
    "rock_two_layer_permeable": "rock",
    "cubes_one_layer_flat": "cubes",
    "cubes_two_layer_random": "cubes",
    "antifer": "cubes",
    "tetrapod": "tetrapod",
    "accropode": "accropode",
    "core_loc": "accropode",
    "xbloc": "accropode",
    "dolos": "dolos",
    "smooth_concrete": "rock",
    "grass": "rock",
    "asphalt": "rock",
}


def roundhead_kd_ratio(armour: str, cot_alpha: float) -> float:
    """KD_head / KD_trunk for an armour type on a given slope.

    Linear in cot(alpha) between the tabulated slopes, and held flat outside
    them rather than extrapolated into values nobody has measured.
    """
    family = ARMOUR_FAMILY.get(armour, "rock")
    table = ROUNDHEAD_KD_RATIO[family]
    slopes = sorted(table)
    if cot_alpha <= slopes[0]:
        return table[slopes[0]]
    if cot_alpha >= slopes[-1]:
        return table[slopes[-1]]
    for low, high in zip(slopes, slopes[1:]):
        if low <= cot_alpha <= high:
            span = (cot_alpha - low) / (high - low)
            return table[low] + span * (table[high] - table[low])
    return table[slopes[-1]]


def roundhead(design, kd_ratio: float | None = None,
              raise_crest: float = 0.0) -> "BreakwaterDesign":
    """The head section of a breakwater, armoured for its exposure.

    A roundhead is attacked from a wider range of directions than the trunk,
    the armour on a convex surface gets less support from its neighbours,
    and the run-down concentrates where the flow turns the corner. Practice
    handles all three by using a lower stability coefficient at the head.

    Since Hudson makes the nominal diameter go as KD to the power minus a
    third, a KD ratio of r gives::

        Dn50_head = Dn50_trunk / r^(1/3)
        M50_head  = M50_trunk  / r

    so a ratio of 0.8 means a quarter more stone by mass, which is the step
    from sixteen to twenty tonne units that a real scheme ends up with.

    Parameters
    ----------
    kd_ratio : float, optional
        KD_head / KD_trunk. Taken from :func:`roundhead_kd_ratio` for the
        design's own armour and slope when not given.
    raise_crest : float
        Extra crest freeboard at the head [m]. Heads are often built higher
        than the trunk, because the overtopping there lands on the part of
        the structure people stand on and the navigation light sits on.

    Returns
    -------
    BreakwaterDesign
        The same design with head armour, its layer recomputed, and
        ``section`` set to "head".

    Notes
    -----
    Only the armour is rescaled. The filter follows it, because the layer
    is recomputed from the new diameter, but the core grading, the crest
    width and the overtopping are left as the trunk's. A real head is also
    usually widened to give the plant somewhere to work and the light
    somewhere to stand.
    """
    from dataclasses import replace

    if kd_ratio is None:
        kd_ratio = roundhead_kd_ratio(design.armour_type, design.cot_alpha)
    if not 0.0 < kd_ratio <= 1.0:
        raise ValueError(
            f"KD ratio must be in (0, 1]; got {kd_ratio}. Above one would "
            "make the head lighter than the trunk, which is backwards."
        )
    if raise_crest < 0:
        raise ValueError(f"Crest rise must be non-negative, got {raise_crest}")

    Dn50 = design.Dn50 / kd_ratio ** (1.0 / 3.0)
    return replace(
        design,
        Dn50=Dn50,
        M50=design.density * Dn50**3,
        layer=layer_for(design.armour_type, Dn50, design.density),
        crest_freeboard=design.crest_freeboard + raise_crest,
        section="head",
        kd_ratio=kd_ratio,
    )
