"""
Beach nourishment simulator.

A beach fill is a perturbation to an otherwise straight shoreline. Under
small wave angles the one-line model reduces to a diffusion equation, so the
fill spreads alongshore and the placed sand leaves the project area over
time. This module sizes that behaviour: it builds the initial planform from
a design, evolves it with the one-line model in ``pyCoastal.tools.shoreline``,
and reports volume retained, project design life, and a renourishment
schedule.

The linearized solution (Pelnard-Considere, 1956) is provided separately as
``pelnard_considere`` and is used to verify the numerical solver.

Coordinates follow the package convention: x is alongshore, y is the
cross-shore shoreline offset (positive seaward), z is elevation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ..tools.shoreline import (
    OneLineParams,
    apply_bcs,
    field_or_scalar_to_array,
    rhs_y_t,
    suggest_dt,
)

SECONDS_PER_YEAR = 365.25 * 24 * 3600.0


def _erf(z: np.ndarray) -> np.ndarray:
    """Vectorized error function without requiring SciPy."""
    return np.vectorize(math.erf, otypes=[float])(z)


def cerc_coefficient(
    K: float = 0.39,
    s: float = 2.65,
    gamma_b: float = 0.78,
    g: float = 9.81,
) -> float:
    """CERC alongshore transport coefficient in the SI form this model needs.

    The CERC (SPM 1984) formula for the immersed-weight transport rate gives a
    volumetric flux

        Q = K sqrt(g / gamma_b) Hb^(5/2) sin(2 alpha) / (16 (s - 1))

    which is a *solid* sediment volume, excluding voids. That is the form
    required here, because ``tools.shoreline.rhs_y_t`` divides by (1 - p)
    itself. Supplying a bulk-volume coefficient instead double-counts porosity.

    Parameters
    ----------
    K : float
        Dimensionless CERC coefficient for the immersed-weight transport rate.
        0.39 is the SPM value for significant wave height; values near 0.2 are
        commonly back-calculated from field data.
    s : float
        Sediment specific gravity [-].
    gamma_b : float
        Breaker index Hb/hb [-].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    float
        Coefficient such that Q [m^3/s per m of beach] = coeff Hb^(5/2) sin(2 alpha).
    """
    return K * math.sqrt(g / gamma_b) / (16.0 * (s - 1.0))


#: Solid-volume CERC coefficient for default sand properties.
KCERC_DEFAULT = cerc_coefficient()


@dataclass
class WaveClimate:
    """Wave conditions driving alongshore transport.

    Attributes
    ----------
    Hb : float
        Representative breaking wave height [m].
    T : float
        Representative wave period [s]. Carried for reporting; the CERC flux
        itself depends on Hb and the breaking angle.
    alpha0 : float
        Breaking wave angle relative to the unperturbed shoreline [rad].
        Zero means shore-normal incidence, for which the fill diffuses
        symmetrically without migrating alongshore.
    Kcerc : float
        CERC alongshore transport coefficient, in SI units such that the
        solid-volume flux Q is m^3/s. Defaults to ``cerc_coefficient()`` for
        standard sand. Note this is *not* the dimensionless CERC K.
    """

    Hb: float = 1.0
    T: float = 8.0
    alpha0: float = 0.0
    Kcerc: float = KCERC_DEFAULT

    def __post_init__(self) -> None:
        if self.Hb <= 0:
            raise ValueError(f"Breaking wave height must be positive, got {self.Hb}")
        if self.T <= 0:
            raise ValueError(f"Wave period must be positive, got {self.T}")
        if self.Kcerc <= 0:
            raise ValueError(f"Kcerc must be positive, got {self.Kcerc}")


@dataclass
class NourishmentDesign:
    """Geometry and sediment properties of a beach fill.

    The fill is placed as a berm of width ``berm_width`` (the seaward advance
    of the shoreline) over a length ``length``, with linear tapers of length
    ``taper`` at each end.

    Attributes
    ----------
    length : float
        Alongshore length of the full-width section [m].
    berm_width : float
        Shoreline advance at placement [m].
    taper : float
        Alongshore length of the linear taper at each end [m].
    center : float, optional
        Alongshore position of the fill centre [m]. Defaults to the centre
        of the model domain.
    D : float
        Depth of closure [m]: the offshore limit of the active profile.
    B : float
        Berm height above mean sea level [m].
    porosity : float
        Sediment porosity [-].
    """

    length: float = 1000.0
    berm_width: float = 30.0
    taper: float = 100.0
    center: float | None = None
    D: float = 8.0
    B: float = 2.0
    porosity: float = 0.4

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError(f"Fill length must be positive, got {self.length}")
        if self.berm_width <= 0:
            raise ValueError(f"Berm width must be positive, got {self.berm_width}")
        if self.taper < 0:
            raise ValueError(f"Taper cannot be negative, got {self.taper}")
        if not 0 <= self.porosity < 1:
            raise ValueError(f"Porosity must be in [0,1), got {self.porosity}")

    @property
    def active_height(self) -> float:
        """Vertical extent of the active profile, D + B [m]."""
        return self.D + self.B

    @property
    def placed_volume(self) -> float:
        """In-situ volume of sand placed [m^3].

        Trapezoidal planform (full-width section plus two linear tapers)
        multiplied by the active profile height.
        """
        planform_area = self.berm_width * (self.length + self.taper)
        return planform_area * self.active_height


def longshore_diffusivity(climate: WaveClimate, design: NourishmentDesign) -> float:
    """Alongshore diffusivity of the linearized one-line model [m^2/s].

    Linearizing Q = K Hb^(5/2) sin(2 alpha) for small angles gives

        dy/dt = eps d2y/dx2,   eps = 2 K Hb^(5/2) / ((1 - p) (D + B))

    This is the same group that sets the explicit stability limit in
    ``pyCoastal.tools.shoreline.suggest_dt``.
    """
    return (
        2.0
        * climate.Kcerc
        * climate.Hb**2.5
        / ((1.0 - design.porosity) * design.active_height)
    )


def _center_of(design: NourishmentDesign, x: np.ndarray) -> float:
    if design.center is not None:
        return float(design.center)
    return 0.5 * (float(x[0]) + float(x[-1]))


def initial_planform(x: np.ndarray, design: NourishmentDesign) -> np.ndarray:
    """Shoreline offset y(x) immediately after placement [m].

    A flat-topped berm over ``design.length`` with linear tapers of length
    ``design.taper`` at both ends.
    """
    center = _center_of(design, x)
    s = np.abs(x - center)
    half = 0.5 * design.length

    y = np.zeros_like(x, dtype=float)
    y[s <= half] = design.berm_width

    if design.taper > 0:
        shoulder = (s > half) & (s <= half + design.taper)
        y[shoulder] = design.berm_width * (1.0 - (s[shoulder] - half) / design.taper)

    return y


def pelnard_considere(
    x: np.ndarray,
    t: float,
    design: NourishmentDesign,
    climate: WaveClimate,
) -> np.ndarray:
    """Analytical planform of a rectangular fill after time ``t`` [s].

    Pelnard-Considere (1956) solution of the linearized one-line equation for
    an initially rectangular fill of width W and length L:

        y(x,t) = (W/2) [ erf((a - x')/(2 sqrt(eps t)))
                       + erf((a + x')/(2 sqrt(eps t))) ]

    with a = L/2 and x' measured from the fill centre. Tapers are not
    represented: this is the reference solution used to verify the numerical
    solver, not a substitute for it.
    """
    center = _center_of(design, x)
    xp = x - center
    a = 0.5 * design.length

    if t <= 0:
        y = np.zeros_like(x, dtype=float)
        y[np.abs(xp) <= a] = design.berm_width
        return y

    eps = longshore_diffusivity(climate, design)
    denom = 2.0 * math.sqrt(eps * t)
    return 0.5 * design.berm_width * (_erf((a - xp) / denom) + _erf((a + xp) / denom))


def _trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    """np.trapezoid on new NumPy, np.trapz on older releases."""
    integrate = getattr(np, "trapezoid", None) or np.trapz
    return float(integrate(y, x))


def _volume_in_project_area(
    x: np.ndarray, y: np.ndarray, design: NourishmentDesign
) -> float:
    """Sand volume still inside the original project footprint [m^3]."""
    center = _center_of(design, x)
    half = 0.5 * design.length + design.taper
    inside = np.abs(x - center) <= half
    if not inside.any():
        return 0.0
    return _trapezoid(y[inside], x[inside]) * design.active_height


@dataclass
class NourishmentResult:
    """Output of a nourishment simulation.

    Attributes
    ----------
    x : np.ndarray
        Alongshore coordinate [m].
    times : np.ndarray
        Output times [s].
    planforms : np.ndarray
        Shoreline offset at each output time, shape (n_times, n_x) [m].
    volume_retained : np.ndarray
        Volume remaining inside the project footprint at each time [m^3].
    placed_volume : float
        Volume placed at construction [m^3].
    """

    x: np.ndarray
    times: np.ndarray
    planforms: np.ndarray
    volume_retained: np.ndarray
    placed_volume: float
    design: NourishmentDesign
    climate: WaveClimate

    @property
    def times_years(self) -> np.ndarray:
        return self.times / SECONDS_PER_YEAR

    @property
    def retained_fraction(self) -> np.ndarray:
        """Fraction of the placed volume still in the project area [-]."""
        return self.volume_retained / self.placed_volume

    @property
    def berm_width(self) -> np.ndarray:
        """Shoreline offset at the fill centre through time [m]."""
        center = _center_of(self.design, self.x)
        i = int(np.argmin(np.abs(self.x - center)))
        return self.planforms[:, i]

    def design_life(self, threshold: float = 0.5) -> float:
        """Time until the retained fraction first falls below ``threshold`` [s].

        Linearly interpolated between output times. Returns ``inf`` if the
        threshold is never crossed within the simulated period.
        """
        frac = self.retained_fraction
        below = np.nonzero(frac < threshold)[0]
        if below.size == 0:
            return float("inf")
        i = int(below[0])
        if i == 0:
            return float(self.times[0])
        f0, f1 = frac[i - 1], frac[i]
        t0, t1 = self.times[i - 1], self.times[i]
        if f1 == f0:
            return float(t1)
        return float(t0 + (threshold - f0) * (t1 - t0) / (f1 - f0))


def simulate_nourishment(
    design: NourishmentDesign,
    climate: WaveClimate,
    duration: float,
    domain_length: float | None = None,
    dx: float = 10.0,
    n_outputs: int = 25,
    bc: str = "fixed_ends",
    cfl: float = 0.9,
) -> NourishmentResult:
    """Evolve a beach fill with the one-line model.

    Parameters
    ----------
    design, climate
        Fill geometry and driving wave conditions.
    duration : float
        Simulated period [s]. Use ``years * SECONDS_PER_YEAR``.
    domain_length : float, optional
        Alongshore extent of the model domain [m]. Defaults to five times the
        total fill footprint, keeping the fixed-end boundaries far enough away
        not to influence the spreading.
    dx : float
        Alongshore grid spacing [m].
    n_outputs : int
        Number of stored output times, including t = 0.
    bc : {"fixed_ends", "zero_slope"}
        Boundary treatment, passed to ``tools.shoreline.apply_bcs``.
    cfl : float
        Safety factor on the diffusive stability limit.

    Returns
    -------
    NourishmentResult
    """
    if duration <= 0:
        raise ValueError(f"Duration must be positive, got {duration}")
    if n_outputs < 2:
        raise ValueError(f"Need at least two output times, got {n_outputs}")

    if domain_length is None:
        # The fill spreads a diffusive length sqrt(eps * duration) in each
        # direction. Sizing the domain on the fill alone lets that front reach
        # the boundary, where "fixed_ends" absorbs sand and silently destroys
        # volume. Leave several diffusive lengths of clearance.
        footprint = design.length + 2.0 * design.taper
        spread = math.sqrt(longshore_diffusivity(climate, design) * duration)
        domain_length = max(5.0 * footprint, footprint + 8.0 * spread)

    x = np.arange(0.0, domain_length + dx, dx)
    design = _recentred(design, x)
    y = initial_planform(x, design)

    pars = OneLineParams(
        D=design.active_height,
        p=design.porosity,
        Kcerc=climate.Kcerc,
        Hfree=climate.Hb,
        alpha0=climate.alpha0,
        Kt=1.0,
    )

    kd = np.ones_like(x)
    Hfree = field_or_scalar_to_array(climate.Hb, x)
    Kt = field_or_scalar_to_array(1.0, x)
    alpha0 = field_or_scalar_to_array(climate.alpha0, x)

    dt = cfl * suggest_dt(x, pars, kd * Kt * Hfree)
    out_times = np.linspace(0.0, duration, n_outputs)

    planforms = [y.copy()]
    volumes = [_volume_in_project_area(x, y, design)]

    t = 0.0
    for t_target in out_times[1:]:
        while t < t_target - 1e-9:
            step = min(dt, t_target - t)
            dydt, _, _, _ = rhs_y_t(x, y, pars, kd, Hfree, Kt, alpha0)
            y = y + step * dydt
            y = apply_bcs(y, bc)
            t += step
        planforms.append(y.copy())
        volumes.append(_volume_in_project_area(x, y, design))

    return NourishmentResult(
        x=x,
        times=out_times,
        planforms=np.array(planforms),
        volume_retained=np.array(volumes),
        placed_volume=design.placed_volume,
        design=design,
        climate=climate,
    )


def _recentred(design: NourishmentDesign, x: np.ndarray) -> NourishmentDesign:
    """Return ``design`` centred in the domain when no centre was given."""
    if design.center is not None:
        return design
    return NourishmentDesign(
        length=design.length,
        berm_width=design.berm_width,
        taper=design.taper,
        center=0.5 * (float(x[0]) + float(x[-1])),
        D=design.D,
        B=design.B,
        porosity=design.porosity,
    )


def renourishment_schedule(
    design: NourishmentDesign,
    climate: WaveClimate,
    horizon: float,
    threshold: float = 0.5,
    **kwargs,
) -> dict:
    """Plan repeated renourishment over a planning horizon.

    Each cycle restores the fill to its design width, so under constant wave
    forcing the cycles are of equal length. Returns the interval, the number
    of renourishments needed within ``horizon``, the placement times, and the
    total volume required.

    Parameters
    ----------
    horizon : float
        Planning horizon [s].
    threshold : float
        Retained-volume fraction that triggers renourishment.
    **kwargs
        Passed through to ``simulate_nourishment``.
    """
    kwargs.pop("duration", None)
    result = simulate_nourishment(design, climate, horizon, **kwargs)
    interval = result.design_life(threshold)

    if not math.isfinite(interval):
        return {
            "interval": float("inf"),
            "n_renourishments": 0,
            "placement_times": [0.0],
            "total_volume": design.placed_volume,
            "initial_result": result,
        }

    times = [0.0]
    t = interval
    while t < horizon:
        times.append(t)
        t += interval

    return {
        "interval": interval,
        "n_renourishments": len(times) - 1,
        "placement_times": times,
        "total_volume": design.placed_volume * len(times),
        "initial_result": result,
    }
