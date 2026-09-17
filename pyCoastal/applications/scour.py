"""
Scour at a pier in an estuary: waves, tide and river current together.

The hard part of estuarine scour is not any single relation. It is that the
three drivers do not peak together and do not even point the same way. The
tide reverses twice a day, the river does not, the waves come and go with
the wind, and the water depth changes under all of it. A scour calculation
done at "the design current" and "the design wave" without asking whether
they can occur at the same moment is either optimistic or absurd, and it is
usually not obvious which.

So this module works a tidal cycle rather than a load case. It evaluates
the combined scour at every phase and reports the envelope, which phase
governs, and by how much. In a river-fed estuary that is nearly always peak
ebb, where the tidal current and the river run the same way and the water
is shallow, but it is worth seeing rather than assuming.

The pier is a stem on a base, because that is what piers are, and the base
is where the interesting failure lives. A buried pile cap does nothing
until the scour hole reaches it. Then it is exposed, it is wider than the
stem, and the scour deepens because of it, which exposes more of it. That
feedback is iterated here rather than ignored, and a design that is stable
against it looks very different from one that is not.

What is modelled and what is not
--------------------------------
Modelled: combined wave and current scour, non-uniform pier geometry
through an equivalent diameter, progressive base exposure, flow
misalignment on the reversing tide, depth limitation, and the time scale of
scour development against the tidal half cycle.

Not modelled: a pile cap resting at bed level can behave as a collar and
*reduce* scour by deflecting the downflow. That is real and documented, and
crediting it here would be unconservative, so it is not credited. Cohesive
beds are refused rather than guessed at. Scour from a contracted section or
from the estuary's own channel migration is a different problem and a
larger one.

References
----------
Sumer, B.M., Fredsoe, J. and Christiansen, N. (1992). Scour around
vertical pile in waves. Journal of Waterway, Port, Coastal and Ocean
Engineering, 118(1), 15-31.

Sumer, B.M., Christiansen, N. and Fredsoe, J. (1992). Time scale of scour
around a vertical pile. Proc. 2nd Int. Offshore and Polar Engineering
Conference, 308-315.

Sumer, B.M. and Fredsoe, J. (2001). Scour around pile in combined waves
and current. Journal of Hydraulic Engineering, 127(5), 403-411.

Sumer, B.M. and Fredsoe, J. (2002). The Mechanics of Scour in the Marine
Environment. World Scientific.

Breusers, H.N.C., Nicollet, G. and Shen, H.W. (1977). Local scour around
cylindrical piers. Journal of Hydraulic Research, 15(3), 211-252.

Richardson, E.V. and Davis, S.R. (2001). Evaluating scour at bridges.
HEC-18, 4th ed. Federal Highway Administration.

Lagasse, P.F. et al. (2009). Bridge scour and stream instability
countermeasures. HEC-23, 3rd ed. Federal Highway Administration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .sediment import RHO_W, sediment, critical_shields, wave_orbital_velocity

__all__ = [
    "G",
    "M2_PERIOD",
    "Pier",
    "PierBase",
    "EstuaryConditions",
    "SHAPE_FACTOR",
    "shape_factor",
    "alignment_factor",
    "equivalent_diameter",
    "keulegan_carpenter",
    "velocity_ratio",
    "scour_ratio_combined",
    "depth_limitation",
    "current_shields",
    "scour_time_scale",
    "scour_development",
    "tidal_state",
    "equilibrium_scour",
    "riprap_size",
    "scour_protection",
    "PierScourDesign",
    "design_pier_scour",
]

G = 9.81

#: Principal lunar semidiurnal tidal period [s].
M2_PERIOD = 12.4206012 * 3600.0


# ---------------------------------------------------------------------------
# The pier
# ---------------------------------------------------------------------------

#: HEC-18 nose shape factor K1.
SHAPE_FACTOR = {
    "circular": 1.0,
    "round_nose": 1.0,
    "square": 1.1,
    "rectangular": 1.1,
    "sharp_nose": 0.9,
    "group": 1.0,
}


def shape_factor(shape: str) -> float:
    """HEC-18 nose shape factor K1, for the pier plan form."""
    if shape not in SHAPE_FACTOR:
        raise ValueError(
            f"Unknown shape {shape!r}. Options: {sorted(SHAPE_FACTOR)}")
    return SHAPE_FACTOR[shape]


def alignment_factor(width: float, length: float,
                     skew_degrees: float) -> float:
    """HEC-18 flow alignment factor K2::

        K2 = (cos theta + (L/a) sin theta) ** 0.65

    A long base presents its width to the flow when aligned and most of its
    length when it is not, so skew matters enormously for anything that is
    not square in plan. This is the factor that makes a tidal estuary
    awkward: a base set square to the ebb is skewed to the flood, and a
    pier aligned to neither is skewed to both.

    ``L/a`` is capped at 12, past which HEC-18 stops claiming accuracy.
    """
    if width <= 0 or length <= 0:
        raise ValueError("Base width and length must be positive")
    theta = math.radians(abs(skew_degrees) % 180.0)
    if theta > math.pi / 2:
        theta = math.pi - theta          # 170 degrees skew is 10 the other way
    ratio = min(length / width, 12.0)
    return (math.cos(theta) + ratio * math.sin(theta)) ** 0.65


@dataclass
class Pier:
    """The column itself, above the base.

    Attributes
    ----------
    diameter : float
        Stem width across the flow [m].
    shape : str
        Plan form, keying :data:`SHAPE_FACTOR`.
    length : float, optional
        Stem length along the flow [m]. Defaults to the diameter, which is
        right for a circular pier and wrong for a blade.
    """

    diameter: float = 2.0
    shape: str = "circular"
    length: float | None = None

    def __post_init__(self) -> None:
        if self.diameter <= 0:
            raise ValueError(f"Diameter must be positive, got {self.diameter}")
        shape_factor(self.shape)
        if self.length is None:
            self.length = self.diameter
        elif self.length <= 0:
            raise ValueError(f"Length must be positive, got {self.length}")


@dataclass
class PierBase:
    """The footing, pile cap or caisson the stem stands on.

    Attributes
    ----------
    width : float
        Across the flow [m].
    length : float
        Along the flow [m].
    height : float
        Thickness of the base [m].
    top_level : float
        Level of the top of the base relative to the *initial* bed.
        Negative means buried, which is the usual design intent, and is
        also the case worth watching: a base buried half a metre is
        invisible until the scour hole finds it.
    skew : float
        Angle between the base's long axis and the flow [deg]. In a
        reversing tidal flow this is the ebb alignment; the flood value is
        taken as the supplement.
    """

    width: float = 6.0
    length: float = 6.0
    height: float = 2.0
    top_level: float = -1.0
    skew: float = 0.0

    def __post_init__(self) -> None:
        if self.width <= 0 or self.length <= 0:
            raise ValueError("Base width and length must be positive")
        if self.height <= 0:
            raise ValueError(f"Base height must be positive, got {self.height}")

    @property
    def bottom_level(self) -> float:
        """Level of the underside of the base, relative to the initial bed."""
        return self.top_level - self.height

    @property
    def buried(self) -> bool:
        """Whether the base starts below the bed."""
        return self.top_level < 0.0


def equivalent_diameter(pier: Pier, base: PierBase | None, depth: float,
                        scour: float = 0.0, skew_degrees: float | None = None
                        ) -> dict:
    """Effective obstacle width seen by the flow [m].

    A pier of two widths is reduced to one by weighting each element over
    the depth of flow it occupies::

        D_e = [D_base h_base + D_stem (h - h_base)] / h

    where ``h_base`` is how much of the base stands proud of the *scoured*
    bed. That last word is the whole point. A base buried below the initial
    bed contributes nothing at first, and contributes more and more as the
    hole deepens, so ``D_e`` is a function of the scour it is being used to
    predict. :func:`equilibrium_scour` iterates it.

    Both elements also carry their own shape and alignment factors, so a
    long rectangular cap skewed to the flow is correctly worse than a
    round one.

    Parameters
    ----------
    scour : float
        Scour depth already developed [m], measured down from the initial
        bed. Sets how much of a buried base is exposed.

    Returns
    -------
    dict
        ``D_e`` plus the exposed base height and the factors used.
    """
    if depth <= 0:
        raise ValueError(f"Water depth must be positive, got {depth}")
    if scour < 0:
        raise ValueError(f"Scour cannot be negative, got {scour}")

    stem_width = pier.diameter * shape_factor(pier.shape)
    if base is None:
        return {
            "D_e": stem_width,
            "stem_width": stem_width,
            "base_width": 0.0,
            "exposed_height": 0.0,
            "base_exposed": False,
            "fully_exposed": False,
        }

    skew = base.skew if skew_degrees is None else skew_degrees
    base_width = (base.width * shape_factor("rectangular")
                  * alignment_factor(base.width, base.length, skew))

    # How much base stands above the scoured bed. The bed is at -scour, so
    # a base whose top is at top_level shows (top_level + scour) of itself,
    # never more than its own height and never more than the water depth.
    exposed = min(max(base.top_level + scour, 0.0), base.height)
    exposed = min(exposed, depth)

    above = max(depth - exposed, 0.0)
    D_e = (base_width * exposed + stem_width * above) / depth

    return {
        "D_e": D_e,
        "stem_width": stem_width,
        "base_width": base_width,
        "exposed_height": exposed,
        "base_exposed": exposed > 0.0,
        "fully_exposed": exposed >= base.height - 1e-12,
        "alignment_factor": alignment_factor(base.width, base.length, skew),
        "skew": skew,
    }


# ---------------------------------------------------------------------------
# The flow
# ---------------------------------------------------------------------------


def keulegan_carpenter(Um: float, period: float, diameter: float) -> float:
    """KC = Um T / D, on the *near-bed* orbital velocity.

    Scour is a bed process, so the velocity that matters is the one at the
    bed, not the one at the surface. This is the convention Sumer and
    Fredsoe's relations are written in, and using a surface orbital
    velocity here would overstate KC badly in deep water.
    """
    if diameter <= 0:
        raise ValueError(f"Diameter must be positive, got {diameter}")
    if period <= 0:
        raise ValueError(f"Period must be positive, got {period}")
    return abs(Um) * period / diameter


def velocity_ratio(current: float, orbital: float) -> float:
    """Ucw = Uc / (Uc + Um), the current's share of the near-bed flow.

    Zero is a pure wave case, one is a pure current. It is the parameter
    Sumer and Fredsoe's combined relation turns on, and a surprising amount
    of estuarine scour sits near 0.7 to 0.9, where the current dominates but
    the waves still matter.
    """
    total = abs(current) + abs(orbital)
    if total == 0:
        return 0.0
    return abs(current) / total


def scour_ratio_combined(KC: float, Ucw: float,
                         current_ratio: float = 1.3,
                         current_live_bed: bool | None = None) -> dict:
    """S/D in combined waves and current, Sumer and Fredsoe (2001)::

        S/D = 1.3 {1 - exp[-A (KC - B)]}     for KC >= B
        A   = 0.03 + (3/4) Ucw^2.6
        B   = 6 exp(-4.7 Ucw)

    The two limits are worth checking, because they are what make the
    relation trustworthy across the middle:

    - ``Ucw = 0`` gives A = 0.03 and B = 6, which is exactly the waves-only
      relation of Sumer, Fredsoe and Christiansen (1992), including the
      threshold at KC = 6 below which the horseshoe vortex does not form.
    - ``Ucw = 1`` gives B = 0.055, so the threshold vanishes, and S/D tends
      to 1.3, the steady-current value, **as KC grows**.

    The steady-current floor
    ------------------------
    That last clause is the trap, and ``current_live_bed`` is the answer to
    it. KC is built on the *wave* orbital velocity, so a strong current
    under small waves has a high Ucw and a low KC at the same time, and the
    formula then returns almost no scour. Read literally it says a pier in
    a 1.5 m/s current scours less than the same pier in still water with a
    ripple on it, which is nonsense.

    The resolution is that a steady current is the ``KC -> infinity`` limit
    of an oscillatory flow, not the ``KC -> 0`` one. A current that can
    move the bed on its own digs its own horseshoe vortex whatever the
    waves are doing, and adding waves to a current does not abolish it. So
    when the approach current alone is live-bed, the ratio is floored at
    the steady-current value.

    This floor is an addition to the published relation, not part of it.
    It is flagged in the result as ``current_governs`` so it is never
    silently applied.

    Parameters
    ----------
    current_live_bed : bool, optional
        Whether the steady current alone exceeds the threshold of motion.
        ``None`` disables the floor and gives the bare published relation.

    Returns
    -------
    dict
        ``ratio`` S/D, the coefficients, and which branch governed.
    """
    if KC < 0:
        raise ValueError(f"KC cannot be negative, got {KC}")
    if not 0.0 <= Ucw <= 1.0:
        raise ValueError(f"Ucw must be in [0,1], got {Ucw}")

    A = 0.03 + 0.75 * Ucw**2.6
    B = 6.0 * math.exp(-4.7 * Ucw)

    if KC <= B:
        published = 0.0
    else:
        published = current_ratio * (1.0 - math.exp(-A * (KC - B)))

    # The published branch tends to the steady-current value from below,
    # so at large KC it sits a few parts in a billion under it. Flag the
    # floor as governing only where it makes a difference worth knowing
    # about, or every high-KC case reports a floor that changed nothing.
    ratio = published
    current_governs = False
    if current_live_bed and published < current_ratio * (1.0 - 1e-3):
        ratio = current_ratio
        current_governs = True
    elif current_live_bed:
        ratio = max(published, current_ratio)

    return {
        "ratio": ratio,
        "published": published,
        "current_governs": current_governs,
        "A": A,
        "B": B,
        "KC": KC,
        "Ucw": Ucw,
        "below_threshold": KC <= B,
    }


def depth_limitation(depth: float, diameter: float) -> float:
    """Shallow-water reduction on the scour depth, ``tanh(h/D)``.

    A scour hole needs room to form. Where the water is shallow compared
    with the obstacle the horseshoe vortex is squeezed and the hole is
    smaller, which is the Breusers, Nicollet and Shen (1977) depth
    limitation. Above about ``h/D = 3`` it is worth nothing (tanh 3 =
    0.995) and can be ignored; below ``h/D = 1`` it takes a quarter off.

    It matters here because a wide caisson base in an estuary at low water
    can easily sit at ``h/D`` well under one, which is exactly where the
    unlimited relations start promising holes deeper than the water.
    """
    if depth <= 0 or diameter <= 0:
        raise ValueError("Depth and diameter must be positive")
    return math.tanh(depth / diameter)


def current_shields(material, velocity: float, depth: float,
                    roughness: float | None = None) -> dict:
    """Skin-friction Shields parameter under a depth-averaged current.

    Uses a logarithmic velocity profile to get the bed shear stress,

        u* = U kappa / ln(11 h / k_s)

    with ``k_s = 2.5 d50`` unless given, then ``theta = u*^2 / (g (s-1) d50)``.
    The result drives the scour time scale and says whether the bed is live
    or in clear water, which decides how long the hole takes to form even
    though it barely changes how deep it ends up.
    """
    grains = sediment(material) if isinstance(material, str) else material
    if grains.d50 <= 0:
        raise ValueError(
            f"{grains.name} is cohesive; these scour relations are for "
            "sands and gravels.")
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")

    ks = 2.5 * grains.d50 if roughness is None else roughness
    ratio = max(11.0 * depth / ks, math.e)          # keep the log positive
    u_star = abs(velocity) * 0.40 / math.log(ratio)
    theta = u_star**2 / (G * (grains.specific_gravity - 1.0) * grains.d50)
    theta_cr = critical_shields(grains)

    return {
        "u_star": u_star,
        "theta": theta,
        "theta_critical": theta_cr,
        "live_bed": theta > theta_cr,
        "mobility": theta / theta_cr if theta_cr > 0 else math.inf,
        "bed_shear": RHO_W * u_star**2,
    }


def scour_time_scale(material, diameter: float, depth: float,
                     theta: float) -> dict:
    """How long the scour hole takes to form [s].

    Sumer, Christiansen and Fredsoe (1992) give a dimensionless time scale

        T* = (1/2000) (h/D) theta^-2.2

    which is made dimensional by

        T = T* D^2 / sqrt(g (s-1) d50^3)

    and the hole then develops as ``S(t) = S_eq [1 - exp(-t/T)]``.

    In a tidal estuary this is not a detail. The time scale for a pier a
    couple of metres across is typically most of a day, while the tide
    reverses every six hours, so the hole never reaches the equilibrium
    depth that a steady-current calculation hands you. Ignoring that is
    conservative for the pier and expensive for the client; relying on it
    without checking the spring tide is neither.

    Raises
    ------
    ValueError
        If the bed is not live. The relation is a live-bed result and
        diverges as theta goes to zero.
    """
    grains = sediment(material) if isinstance(material, str) else material
    if grains.d50 <= 0:
        raise ValueError(f"{grains.name} is cohesive; no time scale applies.")
    if theta <= 0:
        raise ValueError(f"Shields parameter must be positive, got {theta}")
    if diameter <= 0 or depth <= 0:
        raise ValueError("Diameter and depth must be positive")

    star = (1.0 / 2000.0) * (depth / diameter) * theta**-2.2
    scale = math.sqrt(G * (grains.specific_gravity - 1.0) * grains.d50**3)
    return {
        "T_star": star,
        "T": star * diameter**2 / scale,
        "sediment_scale": scale,
    }


def scour_development(equilibrium: float, elapsed: float,
                      time_scale: float) -> float:
    """Scour depth after ``elapsed`` seconds [m].

        S(t) = S_eq [1 - exp(-t / T)]

    The exponential approach is the one universally observed, whatever
    disagreement there is about the time scale itself.
    """
    if elapsed < 0:
        raise ValueError(f"Elapsed time cannot be negative, got {elapsed}")
    if time_scale <= 0:
        raise ValueError(f"Time scale must be positive, got {time_scale}")
    return equilibrium * (1.0 - math.exp(-elapsed / time_scale))


# ---------------------------------------------------------------------------
# The estuary
# ---------------------------------------------------------------------------


@dataclass
class EstuaryConditions:
    """Tide, river and waves at the pier.

    Sign convention: positive is ebb, seaward. The river current is always
    positive, the tidal current changes sign, and the two therefore add on
    the ebb and oppose on the flood. That asymmetry is why estuarine scour
    is an ebb problem far more often than a flood one.

    Attributes
    ----------
    mean_depth : float
        Water depth at mean tide level [m].
    tidal_amplitude : float
        Half the tidal range [m].
    tidal_current : float
        Amplitude of the depth-averaged tidal current [m/s].
    river_current : float
        Depth-averaged river current [m/s], steady and seaward.
    Hs, Tp : float
        Significant wave height and peak period at the pier [m, s].
    tidal_period : float
        Defaults to M2.
    current_phase : float
        Phase lead of the current over the elevation [deg]. 90 is a
        standing wave, where slack water coincides with high and low water;
        0 is a progressive wave, where the strongest currents do. Real
        estuaries sit between, and the answer moves with it, so it is an
        input rather than a buried assumption.
    bed : str
        Sediment key.
    wave_follows_tide : bool
        Whether the wave height is taken to scale with the water depth,
        as it does for a depth-limited estuary chop, or to stay constant.
    """

    mean_depth: float = 10.0
    tidal_amplitude: float = 2.0
    tidal_current: float = 1.0
    river_current: float = 0.3
    Hs: float = 1.0
    Tp: float = 5.0
    tidal_period: float = M2_PERIOD
    current_phase: float = 90.0
    bed: str = "medium_sand"
    wave_follows_tide: bool = False

    def __post_init__(self) -> None:
        if self.mean_depth <= 0:
            raise ValueError(f"Mean depth must be positive, got {self.mean_depth}")
        if self.tidal_amplitude < 0:
            raise ValueError("Tidal amplitude cannot be negative")
        if self.tidal_amplitude >= self.mean_depth:
            raise ValueError(
                f"A {self.tidal_amplitude} m amplitude dries out a "
                f"{self.mean_depth} m mean depth at low water")
        if self.Hs <= 0 or self.Tp <= 0:
            raise ValueError("Wave height and period must be positive")
        if self.tidal_period <= 0:
            raise ValueError("Tidal period must be positive")
        material = sediment(self.bed)
        if material.d50 <= 0:
            raise ValueError(
                f"{material.name} is cohesive. Scour in cohesive beds is "
                "governed by erodibility testing, not by these relations.")

    @property
    def material(self):
        return sediment(self.bed)

    @property
    def peak_ebb_current(self) -> float:
        """The worst steady current: tide and river running together."""
        return self.tidal_current + self.river_current

    @property
    def peak_flood_current(self) -> float:
        """Tide against river, so the smaller of the two peaks."""
        return abs(self.tidal_current - self.river_current)


def tidal_state(conditions: EstuaryConditions, phase_degrees: float) -> dict:
    """Depth, current and wave orbital velocity at one phase of the tide.

    Returns
    -------
    dict
        ``depth``, ``elevation``, ``current`` (signed, positive ebb),
        ``Um`` near-bed orbital velocity, and the wave height used.
    """
    angle = math.radians(phase_degrees)
    elevation = conditions.tidal_amplitude * math.cos(angle)
    depth = conditions.mean_depth + elevation
    if depth <= 0:
        raise ValueError("The pier dries out at this phase")

    lead = math.radians(conditions.current_phase)
    tidal = conditions.tidal_current * math.cos(angle - lead)
    current = tidal + conditions.river_current

    Hs = conditions.Hs
    if conditions.wave_follows_tide:
        Hs *= depth / conditions.mean_depth
    Um = wave_orbital_velocity(Hs, conditions.Tp, depth)

    return {
        "phase": phase_degrees,
        "elevation": elevation,
        "depth": depth,
        "tidal_current": tidal,
        "current": current,
        "Um": Um,
        "Hs": Hs,
        "ebb": current > 0,
    }


# ---------------------------------------------------------------------------
# Putting it together
# ---------------------------------------------------------------------------


def equilibrium_scour(pier: Pier, base: PierBase | None, depth: float,
                      current: float, Um: float, period: float,
                      skew_degrees: float | None = None,
                      limit_by_depth: bool = True, bed=None,
                      iterations: int = 80, tolerance: float = 1e-9) -> dict:
    """Equilibrium scour depth for one steady set of conditions [m].

    Solves the feedback between scour depth and effective diameter. The
    scour depends on the obstacle width; the obstacle width depends on how
    much of the base the scour has exposed; so the two are found together
    by fixed-point iteration rather than by evaluating the relation once at
    the initial geometry.

    Where there is no base, or the base is deep enough never to be reached,
    this converges on the first pass and costs nothing.

    Pass ``bed`` to enable the steady-current floor described in
    :func:`scour_ratio_combined`. Without it the bare published relation is
    used, which understates a current-dominated case badly.

    Returns
    -------
    dict
        ``depth`` of scour, the converged ``D_e``, the geometry at
        convergence, and whether the iteration settled.
    """
    if iterations < 1:
        raise ValueError("Need at least one iteration")

    live = None
    if bed is not None:
        live = current_shields(bed, current, depth)["live_bed"]

    detail: dict = {}

    def predict(trial: float) -> tuple[float, dict, dict]:
        """Scour predicted for a hole that has already reached ``trial``."""
        geometry = equivalent_diameter(pier, base, depth, trial, skew_degrees)
        D_e = geometry["D_e"]
        KC = keulegan_carpenter(Um, period, D_e)
        got = scour_ratio_combined(KC, velocity_ratio(current, Um),
                                   current_live_bed=live)
        value = got["ratio"] * D_e
        if limit_by_depth:
            value *= depth_limitation(depth, D_e)
        return value, geometry, got

    # The feedback runs away rather than settling gently. Once the hole
    # reaches the base, exposure widens the obstacle, which deepens the
    # hole, which exposes more, and the system jumps to a much deeper
    # state: for a 2.5 m stem on a 9 m base the shallow root is 3.2 m and
    # the real one is 4.9 m.
    #
    # There can therefore be more than one self-consistent depth, and
    # iterating up from zero stalls on the shallow one at the very moment
    # the base is first touched. That answer is both numerically fragile
    # and physically wrong: a scour hole does not refill, so any storm or
    # spring tide that reaches the base commits the pier to the deeper
    # state permanently.
    #
    # Predicted scour is monotone non-decreasing in the depth already
    # reached, so g(S) = predict(S) - S starts positive and ends negative,
    # and the DEEPEST self-consistent depth is its last sign change. That
    # is the one to design to.
    #
    # Bisection rather than a fixed-point iteration: the feedback is very
    # nearly neutral near the root (successive substitution converges at
    # about 0.93 per step here), so iterating would need hundreds of passes
    # to tighten what bisection does in fifty.
    upper, _, _ = predict(depth + (base.height if base else 0.0))
    converged = True

    if predict(0.0)[0] <= 0.0:
        scour = 0.0
    else:
        lo, hi = 0.0, upper
        for _ in range(iterations):
            if hi - lo < tolerance:
                break
            mid = 0.5 * (lo + hi)
            if predict(mid)[0] - mid > 0.0:
                lo = mid
            else:
                hi = mid
        else:
            converged = hi - lo < tolerance
        scour = 0.5 * (lo + hi)

    _, geometry, detail = predict(scour)

    return {
        "depth": scour,
        "ratio": detail.get("ratio", 0.0),
        "D_e": geometry["D_e"],
        "KC": detail.get("KC", 0.0),
        "Ucw": detail.get("Ucw", 0.0),
        "A": detail.get("A"),
        "B": detail.get("B"),
        "below_threshold": detail.get("below_threshold", False),
        "current_governs": detail.get("current_governs", False),
        "published_ratio": detail.get("published", 0.0),
        "current_live_bed": live,
        "geometry": geometry,
        "converged": converged,
        "depth_factor": (depth_limitation(depth, geometry["D_e"])
                         if limit_by_depth else 1.0),
    }


def riprap_size(velocity: float, material_density: float = 2650.0,
                shape: str = "round_nose") -> dict:
    """Median stone size for scour protection at a pier [m].

    HEC-23 design guideline 12::

        d50 = 0.692 (K V)^2 / (2 g (s - 1))

    with K = 1.5 for a round-nosed pier and 1.7 for a rectangular one. The
    factor accounts for the flow accelerating around the pier: the stone
    has to survive the local velocity, not the approach velocity, and the
    difference is a factor of two in speed and four in stone weight.
    """
    if velocity <= 0:
        raise ValueError(f"Velocity must be positive, got {velocity}")
    K = 1.7 if shape in ("square", "rectangular") else 1.5
    s = material_density / RHO_W
    if s <= 1:
        raise ValueError("Stone must be denser than water")

    d50 = 0.692 * (K * velocity) ** 2 / (2.0 * G * (s - 1.0))
    return {
        "d50": d50,
        "K": K,
        "mass": material_density * math.pi / 6.0 * d50**3,
        "specific_gravity": s,
        "design_velocity": velocity,
    }


def scour_protection(pier: Pier, base: PierBase | None, velocity: float,
                     scour: float, material_density: float = 2650.0) -> dict:
    """A rock apron sized to the pier and the flow.

    Extent follows HEC-23: the apron reaches two obstacle widths from the
    face, and is at least three stones thick. The width it is measured from
    is the base where there is one, because that is what the flow sees once
    the hole has formed.

    The apron does not remove the scour, it relocates it. An edge scour
    hole forms at the perimeter instead, and a rigid apron that cannot
    settle into it will undermine and unravel from the edge inwards. That
    is why the apron is specified as a falling apron with a launch
    allowance rather than as a slab.
    """
    stone = riprap_size(velocity, material_density, pier.shape)
    obstacle = base.width if base is not None else pier.diameter

    extent = 2.0 * obstacle
    thickness = max(3.0 * stone["d50"], 0.3)
    area = math.pi * ((0.5 * obstacle + extent) ** 2 - (0.5 * obstacle) ** 2)

    # The edge hole forms at the apron perimeter, and the apron has to
    # carry enough stone to blanket the slope it launches down. Taking the
    # launched face at 1V:2H, its slope length is sqrt(5) times its height.
    launch = scour if scour > 0 else 0.0
    perimeter = math.pi * (obstacle + 2.0 * extent)
    launch_volume = perimeter * launch * math.sqrt(5.0) * thickness

    return {
        **stone,
        "extent": extent,
        "thickness": thickness,
        "launch_allowance": launch,
        "launch_volume": launch_volume,
        "plan_area": area,
        "volume": area * thickness + launch_volume,
        "note": (
            f"Apron {extent:.1f} m beyond the face, {thickness:.2f} m thick, "
            f"with {launch:.1f} m of launch allowance for the edge hole. "
            "Specify as a falling apron: it must be free to settle into the "
            "edge scour rather than span it."),
    }


@dataclass
class PierScourDesign:
    """The outcome of :func:`design_pier_scour`."""

    pier: Pier
    base: PierBase | None
    conditions: EstuaryConditions
    states: list[dict]
    governing: dict
    equilibrium: float
    tidal_limited: float
    time_scale: float
    protection: dict
    notes: list[str] = field(default_factory=list)

    @property
    def base_exposed(self) -> bool:
        """Whether the governing scour hole reaches the base."""
        return bool(self.governing["scour"]["geometry"]["base_exposed"])

    @property
    def undermined(self) -> bool:
        """Whether the hole reaches below the underside of the base."""
        if self.base is None:
            return False
        return self.equilibrium > -self.base.bottom_level

    def envelope(self) -> np.ndarray:
        """Scour depth at each phase of the tide [m]."""
        return np.array([s["scour"]["depth"] for s in self.states])

    def phases(self) -> np.ndarray:
        return np.array([s["state"]["phase"] for s in self.states])


def design_pier_scour(pier: Pier, conditions: EstuaryConditions,
                      base: PierBase | None = None,
                      samples: int = 73,
                      limit_by_depth: bool = True,
                      protection_factor: float = 1.0) -> PierScourDesign:
    """Work a tidal cycle and report the scour envelope at a pier.

    Evaluates the combined wave and current scour at every phase of the
    tide, with the water depth, the current and the wave orbital velocity
    all moving together, and reports the deepest.

    Two depths come out of it and they answer different questions.
    ``equilibrium`` is what the governing condition would eventually
    produce if it were held indefinitely, and is the right number for
    sizing scour protection and for the long-term foundation check.
    ``tidal_limited`` is what that condition can actually achieve in the
    half cycle it lasts, and is the right number for asking what happens
    during a single spring tide.

    Which of the two is smaller is not obvious in advance, which is why it
    is computed rather than assumed. A vigorously live bed cuts its hole in
    an hour or two and reaches equilibrium well inside one half cycle; a
    barely mobile bed under a big pier takes days and never gets close.
    Either way ``equilibrium`` is the number to design protection on, since
    the hole does not refill on the reverse flow and successive tides work
    it deeper.

    Parameters
    ----------
    samples : int
        Phases to evaluate over the full cycle.
    protection_factor : float
        Multiplier on the equilibrium scour used to size the apron launch
        allowance. 1.0 sizes for the predicted hole; a value above one buys
        margin against a relation whose scatter is substantial.

    Returns
    -------
    PierScourDesign
    """
    if samples < 3:
        raise ValueError(f"Need at least three phases, got {samples}")

    states = []
    for phase in np.linspace(0.0, 360.0, samples):
        state = tidal_state(conditions, float(phase))
        # The base is set square to the ebb, so the flood runs across it at
        # the supplement of the design skew.
        skew = base.skew if base is not None else 0.0
        if base is not None and not state["ebb"]:
            skew = 180.0 - base.skew
        scour = equilibrium_scour(
            pier, base, state["depth"], state["current"], state["Um"],
            conditions.Tp, skew_degrees=skew, limit_by_depth=limit_by_depth,
            bed=conditions.material)
        states.append({"state": state, "scour": scour, "skew": skew})

    governing = max(states, key=lambda s: s["scour"]["depth"])
    equilibrium = governing["scour"]["depth"]

    gs = governing["state"]
    flow = current_shields(conditions.material, gs["current"], gs["depth"])
    if flow["live_bed"]:
        scale = scour_time_scale(conditions.material,
                                 governing["scour"]["D_e"], gs["depth"],
                                 flow["theta"])["T"]
    else:
        scale = math.inf

    half_cycle = 0.5 * conditions.tidal_period
    limited = (scour_development(equilibrium, half_cycle, scale)
               if math.isfinite(scale) else 0.0)

    protection = scour_protection(
        pier, base, abs(gs["current"]) + gs["Um"],
        protection_factor * equilibrium)

    notes = _scour_notes(pier, base, conditions, governing, equilibrium,
                         limited, scale, flow, half_cycle)

    return PierScourDesign(
        pier=pier, base=base, conditions=conditions, states=states,
        governing=governing, equilibrium=equilibrium,
        tidal_limited=limited, time_scale=scale, protection=protection,
        notes=notes)


def _scour_notes(pier, base, conditions, governing, equilibrium, limited,
                 scale, flow, half_cycle) -> list[str]:
    """Plain-language findings, in the order a reviewer would want them."""
    gs = governing["state"]
    sc = governing["scour"]
    notes = []

    notes.append(
        f"Governing phase {gs['phase']:.0f} deg, on the "
        f"{'ebb' if gs['ebb'] else 'flood'}: {abs(gs['current']):.2f} m/s "
        f"current and {gs['Um']:.2f} m/s near-bed orbital velocity in "
        f"{gs['depth']:.2f} m of water.")

    notes.append(
        f"Ucw = {sc['Ucw']:.2f}, so the "
        + ("current dominates and the waves modify it."
           if sc["Ucw"] > 0.7 else
           "waves and current both matter."
           if sc["Ucw"] > 0.3 else
           "waves dominate.")
        + f" KC = {sc['KC']:.1f} against a threshold of {sc['B']:.2f}.")

    if sc["below_threshold"]:
        notes.append(
            "KC is below the threshold for a horseshoe vortex, so this "
            "relation gives no scour. That is a statement about this "
            "mechanism only; contraction and channel scour are untouched "
            "by it.")

    notes.append(
        f"Equilibrium scour {equilibrium:.2f} m, "
        f"{sc['ratio']:.2f} times the effective diameter of "
        f"{sc['D_e']:.2f} m.")

    if sc["depth_factor"] < 0.95:
        notes.append(
            f"Shallow water takes {100 * (1 - sc['depth_factor']):.0f}% off "
            f"the unlimited depth: h/D = {gs['depth'] / sc['D_e']:.1f}.")

    if base is not None:
        geometry = sc["geometry"]
        if geometry["fully_exposed"]:
            notes.append(
                f"The hole exposes the base completely ({base.height:.1f} m) "
                "and reaches its underside. The foundation is undermined, "
                "not merely exposed, and the bearing check has to be redone "
                "on the scoured section.")
        elif geometry["base_exposed"]:
            notes.append(
                f"The hole exposes {geometry['exposed_height']:.2f} m of the "
                f"{base.height:.1f} m base, which widens the obstacle from "
                f"{geometry['stem_width']:.2f} m to {sc['D_e']:.2f} m and "
                "deepens the hole further. That feedback is included here; "
                "the converged depth already accounts for it.")
        else:
            margin = -base.top_level - equilibrium
            notes.append(
                f"The base stays buried, with {margin:.2f} m of cover "
                "remaining under the predicted hole. Check this against the "
                "scatter on the relation before relying on it.")
        if geometry.get("alignment_factor", 1.0) > 1.2:
            notes.append(
                f"Flow misalignment multiplies the base width by "
                f"{geometry['alignment_factor']:.2f} at {governing['skew']:.0f} "
                "deg of skew. A base set square to one direction of a "
                "reversing tide is skewed to the other.")

    if math.isfinite(scale):
        notes.append(
            f"Scour time scale {scale / 3600:.1f} hours against a "
            f"{half_cycle / 3600:.1f} hour tidal half cycle, so one half "
            f"cycle reaches {limited:.2f} m, "
            f"{100 * limited / equilibrium:.0f}% of equilibrium."
            + (" The bed is mobile enough to cut the full hole within one "
               "half cycle."
               if limited > 0.9 * equilibrium else
               " The hole does not refill on the reverse flow, so successive "
               "tides work it deeper towards the equilibrium.")
            + " Size protection on the equilibrium either way.")
    else:
        notes.append(
            f"The bed is not live at the governing phase "
            f"(theta = {flow['theta']:.3f} against "
            f"{flow['theta_critical']:.3f} critical), so this is clear-water "
            "scour. The equilibrium depth is similar but takes very much "
            "longer to develop.")

    notes.append(
        "Sumer and Fredsoe's relations carry a standard deviation near 0.7 "
        "diameters in steady current. Treat the number as a mean, not a "
        "bound, and design protection with margin on it.")

    return notes
