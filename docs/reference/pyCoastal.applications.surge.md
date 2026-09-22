# `pyCoastal.applications.surge`

Source: [`pyCoastal/applications/surge.py`](../../pyCoastal/applications/surge.py)

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

## `G`

```python
G = 9.81
```

## `RHO_WATER`

```python
RHO_WATER = 1025.0
```

## `STANDARD_PRESSURE`

```python
STANDARD_PRESSURE = 101325.0
```

## `WIND_STRESS_COEFFICIENT`

```python
WIND_STRESS_COEFFICIENT = 3.3e-06
```

## `barometric_setup`

```python
def barometric_setup(central_pressure: float, ambient_pressure: float=STANDARD_PRESSURE, rho: float=RHO_WATER) -> float
```

```text
Inverted-barometer rise for a pressure drop [m].

eta = (p_ambient - p_central) / (rho g), which is close to 1 cm per hPa.
Pressures are in pascals.

This is the equilibrium response. A fast-moving storm does not give the
ocean time to reach it, so this is an upper bound on the barometric part.
```

## `wind_setup`

```python
def wind_setup(wind_speed: float, fetch: float, depth: float, wind_angle: float=0.0, k: float=WIND_STRESS_COEFFICIENT, return_flow: float=1.0) -> float
```

```text
Wind setup over a shelf of representative depth [m].

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
```

## `wind_setup_profile`

```python
def wind_setup_profile(depths: np.ndarray, dx: float, wind_speed: float, wind_angle: float=0.0, k: float=WIND_STRESS_COEFFICIENT, return_flow: float=1.0) -> np.ndarray
```

```text
Wind setup integrated landward across a shelf profile [m].

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
```

## `surf_zone_setup`

```python
def surf_zone_setup(breaking_height: float, gamma: float=0.8) -> float
```

```text
Mean water-level rise at the shoreline from wave breaking [m].

Thin wrapper on ``pyCoastal.tools.wave.wave_setup``, kept here so a
complete water-level budget reads in one place.
```

## `stockdon_runup`

```python
def stockdon_runup(Hm0: float, Tp: float, beach_slope: float) -> dict
```

```text
2 percent exceedance runup from Stockdon et al. (2006) [m].

R2 = 1.1 (0.35 beta sqrt(H0 L0)
          + sqrt(H0 L0 (0.563 beta^2 + 0.004)) / 2)

The two terms are the setup and the swash, returned separately because
only the setup part is a sustained level; the swash is an oscillation.

``beach_slope`` is the foreshore slope tan(beta).
```

## `StormConditions`

```python
class StormConditions
    wind_speed: float = 40.0
    central_pressure: float = 95000.0
    tide: float = 0.0
    Hm0: float = 6.0
    Tp: float = 12.0
    fetch: float = 100000.0
    shelf_depth: float = 20.0
    wind_angle: float = 0.0
    sea_level_rise: float = 0.0
```

```text
Forcing for a design storm.

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
```

## `total_water_level`

```python
def total_water_level(storm: StormConditions, beach_slope: float=0.05, breaker_index: float=0.78, shelf_depths: np.ndarray | None=None, dx: float | None=None, return_flow: float=1.15) -> dict
```

```text
Assemble the still water level and the total water level [m datum].

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
```

## `inundation_limit`

```python
def inundation_limit(x: np.ndarray, z: np.ndarray, level: float) -> float
```

```text
Landward limit of *connected* flooding on a cross-shore profile [m].

Walks landward from the sea and stops at the first ground above
``level``, linearly interpolating the crossing. Low ground further inland
may also lie below the level, but water arriving overland cannot reach it
while the barrier holds, so it is not counted. That is the same
connectivity argument as ``bathtub_flood``, in one dimension.

Returns the seaward end if nothing floods, and the landward end if the
water is never stopped. Use ``flood_depths`` if you want every cell below
the level regardless of whether water can get there.
```

## `flood_depths`

```python
def flood_depths(z: np.ndarray, level: float) -> np.ndarray
```

```text
Still-water flood depth over terrain [m], zero where dry.
```

## `bathtub_flood`

```python
def bathtub_flood(terrain: np.ndarray, level: float, seed: np.ndarray | None=None, connectivity: int=4) -> np.ndarray
```

```text
Flooded cells at a still-water ``level``, respecting connectivity.

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
```

## `flooded_area`

```python
def flooded_area(flooded: np.ndarray, dx: float) -> float
```

```text
Flooded plan area [m^2].
```

## `flood_volume`

```python
def flood_volume(terrain: np.ndarray, flooded: np.ndarray, level: float, dx: float) -> float
```

```text
Water volume held on the flooded terrain [m^3].
```

## `isolated_low_ground`

```python
def isolated_low_ground(terrain: np.ndarray, level: float, **kwargs) -> np.ndarray
```

```text
Cells below the level that the sea cannot actually reach.

The difference between a naive bathtub map and a connected one. Worth
plotting, because it is exactly where a threshold-only map overstates
the hazard.
```

