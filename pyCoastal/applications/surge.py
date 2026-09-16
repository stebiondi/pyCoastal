"""
Storm surge and coastal flooding.

Builds a total water level from its components, then uses it to find how far
a storm floods: along a cross-shore profile, or over a terrain grid with
hydraulic connectivity so that low ground behind a continuous barrier is not
flooded by a level that cannot physically reach it.

Components of the still water level
-----------------------------------
astronomical tide
    Supplied, not predicted here.
barometric setup
    The inverted-barometer response, about 1 cm per hPa of pressure drop.
wind setup
    Wind stress piling water against the coast across the shelf. Both the
    closed-form estimate over a representative depth and a numerical
    integration across a real shelf profile are provided.
wave setup
    The mean water-level rise inside the surf zone from breaking.

Wave runup is added on top of the still water level for a total water level,
but runup is a swash oscillation rather than a sustained level, so the two
are reported separately: flood extent from sustained level, wave hazard from
runup.

Sources
-------
Dean and Dalrymple (1991), Water Wave Mechanics for Engineers and Scientists.
    Wind setup and the bathystrophic storm tide.
USACE Coastal Engineering Manual (2002), EM 1110-2-1100 Part II. Storm surge.
Stockdon et al. (2006), Coastal Engineering 53, 573-588. Runup.
FEMA (2005), Guidelines and Specifications for Flood Hazard Mapping Partners.
    Total water level and the treatment of wave effects.

Conventions
-----------
Elevations are metres relative to the same vertical datum as the terrain,
positive upward. Cross-shore distance increases landward.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

import numpy as np

from ..tools.wave import dispersion, wave_setup as _surf_zone_setup

G = 9.81
RHO_WATER = 1025.0
STANDARD_PRESSURE = 101325.0

#: Wind-stress coefficient k in the setup relation d(eta)/dx = k W^2 / (g d).
#: Dean and Dalrymple (1991) give 3.0e-6 to 3.6e-6; the midpoint is used.
WIND_STRESS_COEFFICIENT = 3.3e-6


# ---------------------------------------------------------------------------
# Water level components
# ---------------------------------------------------------------------------


def barometric_setup(
    central_pressure: float,
    ambient_pressure: float = STANDARD_PRESSURE,
    rho: float = RHO_WATER,
) -> float:
    """Inverted-barometer rise for a pressure drop [m].

    eta = (p_ambient - p_central) / (rho g), which is close to 1 cm per hPa.
    Pressures are in pascals.

    This is the equilibrium response. A fast-moving storm does not give the
    ocean time to reach it, so this is an upper bound on the barometric part.
    """
    if central_pressure <= 0 or ambient_pressure <= 0:
        raise ValueError("Pressures must be positive and in pascals")
    return (ambient_pressure - central_pressure) / (rho * G)


def wind_setup(
    wind_speed: float,
    fetch: float,
    depth: float,
    wind_angle: float = 0.0,
    k: float = WIND_STRESS_COEFFICIENT,
    return_flow: float = 1.0,
) -> float:
    """Wind setup over a shelf of representative depth [m].

    Integrating d(eta)/dx = k W^2 cos(theta) / (g d) over a fetch at constant
    depth gives

        eta = n k W^2 F cos(theta) / (g d)

    Parameters
    ----------
    wind_speed : float
        Wind speed at 10 m [m/s].
    fetch : float
        Over-water distance the wind acts across [m].
    depth : float
        Representative shelf depth [m]. Setup is inversely proportional to
        it, so a shallow wide shelf sets up far more than a narrow deep one.
    wind_angle : float
        Angle between the wind and the shore-normal [rad].
    return_flow : float
        Factor above 1 for the seaward return flow under the surface, which
        increases the surface slope. 1.15 to 1.30 is common.

    Notes
    -----
    The constant-depth form is a screening estimate. Because setup goes as
    1/d it is dominated by the shallowest part of the shelf, so a single
    representative depth can mislead. Use ``wind_setup_profile`` where the
    bathymetry is known.
    """
    if wind_speed < 0:
        raise ValueError(f"Wind speed cannot be negative, got {wind_speed}")
    if fetch <= 0:
        raise ValueError(f"Fetch must be positive, got {fetch}")
    if depth <= 0:
        raise ValueError(f"Depth must be positive, got {depth}")
    if return_flow < 1.0:
        raise ValueError(f"Return-flow factor must be at least 1, got {return_flow}")

    return return_flow * k * wind_speed**2 * fetch * math.cos(wind_angle) / (G * depth)


def wind_setup_profile(
    depths: np.ndarray,
    dx: float,
    wind_speed: float,
    wind_angle: float = 0.0,
    k: float = WIND_STRESS_COEFFICIENT,
    return_flow: float = 1.0,
) -> np.ndarray:
    """Wind setup integrated landward across a shelf profile [m].

    Integrates d(eta)/dx = k W^2 cos(theta) / (g (d + eta)) from the seaward
    end of ``depths`` toward the coast, carrying the accumulated setup into
    the local depth. That feedback matters: the setup itself deepens the
    water and damps further setup, which the constant-depth form ignores.

    Parameters
    ----------
    depths : np.ndarray
        Still-water depth at each point, seaward end first [m], positive.
    dx : float
        Spacing between points [m].

    Returns
    -------
    np.ndarray
        Setup at each point, the last value being the setup at the coast.
    """
    depths = np.asarray(depths, dtype=float)
    if depths.ndim != 1 or depths.size < 2:
        raise ValueError("Need a 1D profile of at least two depths")
    if np.any(depths <= 0):
        raise ValueError("All depths must be positive; trim the profile to water")
    if dx <= 0:
        raise ValueError(f"Spacing must be positive, got {dx}")

    stress = return_flow * k * wind_speed**2 * math.cos(wind_angle)
    eta = np.zeros_like(depths)
    for i in range(1, depths.size):
        total_depth = 0.5 * (depths[i - 1] + depths[i]) + eta[i - 1]
        eta[i] = eta[i - 1] + stress * dx / (G * max(total_depth, 0.1))
    return eta


def surf_zone_setup(breaking_height: float, gamma: float = 0.8) -> float:
    """Mean water-level rise at the shoreline from wave breaking [m].

    Thin wrapper on ``pyCoastal.tools.wave.wave_setup``, kept here so a
    complete water-level budget reads in one place.
    """
    if breaking_height <= 0:
        raise ValueError(f"Breaking height must be positive, got {breaking_height}")
    return _surf_zone_setup(breaking_height, gamma)


def stockdon_runup(Hm0: float, Tp: float, beach_slope: float) -> dict:
    """2 percent exceedance runup from Stockdon et al. (2006) [m].

    R2 = 1.1 (0.35 beta sqrt(H0 L0)
              + sqrt(H0 L0 (0.563 beta^2 + 0.004)) / 2)

    The two terms are the setup and the swash, returned separately because
    only the setup part is a sustained level; the swash is an oscillation.

    ``beach_slope`` is the foreshore slope tan(beta).
    """
    if Hm0 <= 0 or Tp <= 0:
        raise ValueError("Wave height and period must be positive")
    if beach_slope <= 0:
        raise ValueError(f"Beach slope must be positive, got {beach_slope}")

    L0 = G * Tp**2 / (2 * math.pi)
    root = math.sqrt(Hm0 * L0)
    setup = 0.35 * beach_slope * root
    swash = math.sqrt(Hm0 * L0 * (0.563 * beach_slope**2 + 0.004))

    return {
        "R2": 1.1 * (setup + 0.5 * swash),
        "setup": 1.1 * setup,
        "swash": 1.1 * 0.5 * swash,
        "iribarren": beach_slope / math.sqrt(Hm0 / L0),
    }


# ---------------------------------------------------------------------------
# Total water level
# ---------------------------------------------------------------------------


@dataclass
class StormConditions:
    """Forcing for a design storm.

    Attributes
    ----------
    wind_speed : float
        Sustained wind speed at 10 m [m/s].
    central_pressure : float
        Storm central pressure [Pa].
    tide : float
        Astronomical tide level at the time of landfall [m datum].
    Hm0 : float
        Offshore significant wave height [m].
    Tp : float
        Peak period [s].
    fetch : float
        Over-water distance the wind acts across [m].
    shelf_depth : float
        Representative depth for the closed-form wind setup [m].
    wind_angle : float
        Wind direction relative to shore-normal [rad].
    sea_level_rise : float
        Added relative sea level, for scenario work [m].
    """

    wind_speed: float = 40.0
    central_pressure: float = 95000.0
    tide: float = 0.0
    Hm0: float = 6.0
    Tp: float = 12.0
    fetch: float = 100_000.0
    shelf_depth: float = 20.0
    wind_angle: float = 0.0
    sea_level_rise: float = 0.0

    def __post_init__(self) -> None:
        if self.wind_speed < 0:
            raise ValueError(f"Wind speed cannot be negative, got {self.wind_speed}")
        if self.Hm0 <= 0 or self.Tp <= 0:
            raise ValueError("Wave height and period must be positive")


def total_water_level(
    storm: StormConditions,
    beach_slope: float = 0.05,
    breaker_index: float = 0.78,
    shelf_depths: np.ndarray | None = None,
    dx: float | None = None,
    return_flow: float = 1.15,
) -> dict:
    """Assemble the still water level and the total water level [m datum].

    Returns each component separately, because which ones apply depends on
    what is being assessed. The still water level drives inundation extent;
    runup is added on top for the wave hazard at the shoreline but is a swash
    oscillation, not a sustained level, and should not be used to flood
    terrain far inland.

    Parameters
    ----------
    shelf_depths, dx
        Pass both to integrate wind setup across a real shelf profile instead
        of using the representative depth.
    breaker_index
        Hb / h at breaking, used to estimate the breaking height from the
        offshore height for the surf-zone setup.
    """
    barometric = barometric_setup(storm.central_pressure)

    if shelf_depths is not None:
        if dx is None:
            raise ValueError("Pass dx together with shelf_depths")
        wind = float(
            wind_setup_profile(
                shelf_depths, dx, storm.wind_speed, storm.wind_angle,
                return_flow=return_flow,
            )[-1]
        )
    else:
        wind = wind_setup(
            storm.wind_speed, storm.fetch, storm.shelf_depth,
            storm.wind_angle, return_flow=return_flow,
        )

    # Depth-limited breaking height, from the still water level so far.
    breaking_height = min(storm.Hm0, breaker_index * max(storm.shelf_depth, 0.5))
    wave = surf_zone_setup(breaking_height)

    still_water = (
        storm.tide + storm.sea_level_rise + barometric + wind + wave
    )
    runup = stockdon_runup(storm.Hm0, storm.Tp, beach_slope)

    return {
        "tide": storm.tide,
        "sea_level_rise": storm.sea_level_rise,
        "barometric_setup": barometric,
        "wind_setup": wind,
        "wave_setup": wave,
        "still_water_level": still_water,
        "runup_R2": runup["R2"],
        "total_water_level": still_water + runup["R2"],
        "breaking_height": breaking_height,
    }


# ---------------------------------------------------------------------------
# Inundation
# ---------------------------------------------------------------------------


def inundation_limit(x: np.ndarray, z: np.ndarray, level: float) -> float:
    """Landward limit of *connected* flooding on a cross-shore profile [m].

    Walks landward from the sea and stops at the first ground above
    ``level``, linearly interpolating the crossing. Low ground further inland
    may also lie below the level, but water arriving overland cannot reach it
    while the barrier holds, so it is not counted. That is the same
    connectivity argument as ``bathtub_flood``, in one dimension.

    Returns the seaward end if nothing floods, and the landward end if the
    water is never stopped. Use ``flood_depths`` if you want every cell below
    the level regardless of whether water can get there.
    """
    x = np.asarray(x, dtype=float)
    z = np.asarray(z, dtype=float)
    if x.shape != z.shape or x.ndim != 1:
        raise ValueError("x and z must be 1D arrays of the same length")

    dry = np.nonzero(z > level)[0]
    if dry.size == 0:
        return float(x[-1])

    idx = int(dry[0])
    if idx == 0:
        return float(x[0])

    z0, z1 = z[idx - 1], z[idx]
    if z1 == z0:
        return float(x[idx])
    t = (level - z0) / (z1 - z0)
    return float(x[idx - 1] + t * (x[idx] - x[idx - 1]))


def flood_depths(z: np.ndarray, level: float) -> np.ndarray:
    """Still-water flood depth over terrain [m], zero where dry."""
    return np.maximum(level - np.asarray(z, dtype=float), 0.0)


def bathtub_flood(
    terrain: np.ndarray,
    level: float,
    seed: np.ndarray | None = None,
    connectivity: int = 4,
) -> np.ndarray:
    """Flooded cells at a still-water ``level``, respecting connectivity.

    A plain elevation threshold floods every low cell, including basins
    sealed off from the sea by higher ground. This walks outward from the
    coast instead, so only ground the water can actually reach is flooded.
    That distinction is usually the difference between an alarming map and a
    useful one.

    Parameters
    ----------
    terrain : np.ndarray
        Ground elevation on a 2D grid [m datum], x on axis 0.
    level : float
        Still-water level [m datum].
    seed : np.ndarray, optional
        Boolean array marking where the sea enters. Defaults to any
        below-level cell on the domain edge.
    connectivity : {4, 8}
        Whether water spreads to edge neighbours only, or diagonals too.

    Returns
    -------
    np.ndarray
        Boolean flooded mask.
    """
    terrain = np.asarray(terrain, dtype=float)
    if terrain.ndim != 2:
        raise ValueError("Terrain must be a 2D array")
    if connectivity not in (4, 8):
        raise ValueError(f"Connectivity must be 4 or 8, got {connectivity}")

    below = terrain <= level
    if seed is None:
        seed = np.zeros_like(below)
        seed[0, :] = True
        seed[-1, :] = True
        seed[:, 0] = True
        seed[:, -1] = True
    else:
        seed = np.asarray(seed, dtype=bool)
        if seed.shape != terrain.shape:
            raise ValueError("Seed must match the terrain shape")

    start = below & seed
    flooded = np.zeros_like(below)
    if not start.any():
        return flooded

    if connectivity == 4:
        offsets = ((1, 0), (-1, 0), (0, 1), (0, -1))
    else:
        offsets = (
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        )

    nx, ny = terrain.shape
    queue = deque(zip(*np.nonzero(start)))
    for i, j in queue:
        flooded[i, j] = True

    while queue:
        i, j = queue.popleft()
        for di, dj in offsets:
            a, b = i + di, j + dj
            if 0 <= a < nx and 0 <= b < ny and below[a, b] and not flooded[a, b]:
                flooded[a, b] = True
                queue.append((a, b))

    return flooded


def flooded_area(flooded: np.ndarray, dx: float) -> float:
    """Flooded plan area [m^2]."""
    return float(flooded.sum()) * dx * dx


def flood_volume(terrain: np.ndarray, flooded: np.ndarray, level: float, dx: float) -> float:
    """Water volume held on the flooded terrain [m^3]."""
    depths = np.where(flooded, np.maximum(level - terrain, 0.0), 0.0)
    return float(depths.sum()) * dx * dx


def isolated_low_ground(terrain: np.ndarray, level: float, **kwargs) -> np.ndarray:
    """Cells below the level that the sea cannot actually reach.

    The difference between a naive bathtub map and a connected one. Worth
    plotting, because it is exactly where a threshold-only map overstates
    the hazard.
    """
    below = np.asarray(terrain, dtype=float) <= level
    return below & ~bathtub_flood(terrain, level, **kwargs)
