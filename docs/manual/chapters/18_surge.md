# Storm surge and coastal flooding {#sec:surge}

*Module:* `pyCoastal.applications.surge`. *Example:*
`examples/storm_surge_flooding.py`.

The module builds a total water level from its components and then finds
how far a storm floods: along a cross-shore profile, or over a terrain grid
with hydraulic connectivity, so that low ground behind a continuous barrier
is not flooded by a level that cannot physically reach it.

## The water level budget

The still water level is the sum of the astronomical tide (supplied, not
predicted), any sea-level rise, and three setups:

- **Barometric setup**, the inverted-barometer response,
  $\eta_p = (p_a - p_c)/(\rho g)$, close to 1 cm per hPa
  (`barometric_setup`). It is the equilibrium response and an upper bound
  for a fast-moving storm.
- **Wind setup**, from integrating
  $\mathrm{d}\eta/\mathrm{d}x = nkW^2\cos\theta/(gd)$ over the fetch, with
  $k = 3.3\times10^{-6}$ and a return-flow factor $n$ of 1.15 to 1.30.
  Over a constant depth (@eq:wind-setup),

  $$ \eta_w = \frac{nkW^2F\cos\theta}{gd}, $$ {#eq:wind-setup}

  (`wind_setup`). Because setup goes as $1/d$ it is dominated by the
  shallowest part of the shelf, so `wind_setup_profile(depths, dx, ...)`
  integrates across a real shelf, carrying the accumulated setup into the
  local depth $d + \eta$, which damps further setup.
- **Wave setup** in the surf zone, from the breaking height
  (`surf_zone_setup(breaking_height, gamma=0.8)`).

Runup is added on top for the total water level, from Stockdon et al. (2006) (@eq:stockdon):

$$ R_{2\%} = 1.1\left(0.35\beta\sqrt{H_0L_0} + \frac{\sqrt{H_0L_0(0.563\beta^2 + 0.004)}}{2}\right), $$ {#eq:stockdon}

returned as setup and swash separately (`stockdon_runup`). Runup is a swash
oscillation, not a sustained level, so flood extent is taken from the still
water level and the wave hazard at the shoreline from the total.

`StormConditions(wind_speed=40, central_pressure=95000, tide=0, Hm0=6,
Tp=12, fetch=100e3, shelf_depth=20, wind_angle=0, sea_level_rise=0)` is the
storm; `total_water_level(storm, beach_slope=0.05, breaker_index=0.78,
shelf_depths=None, dx=None, return_flow=1.15)` returns every component, the
still water level, and the total water level.

## Flood mapping

A plain elevation threshold floods every low cell, including basins sealed
off from the sea by higher ground. `bathtub_flood(terrain, level, seed=None,
connectivity=4)` walks outward from the coast instead, so only ground the
water can reach is flooded; `seed` marks where the sea enters (default: any
below-level cell on the domain edge) and `connectivity` is 4 or 8.
`isolated_low_ground` returns the cells below the level that the sea cannot
reach, `flooded_area(flooded, dx)` and `flood_volume(terrain, flooded, level,
dx)` quantify the map, and `flood_depths(z, level)` gives depths regardless
of connectivity. On a profile, `inundation_limit(x, z, level)` walks landward
and stops at the first ground above the level.

```python
import numpy as np
from pyCoastal.applications.surge import (
    StormConditions, total_water_level, bathtub_flood, isolated_low_ground,
)

storm = StormConditions(wind_speed=45, central_pressure=94000, tide=0.6,
                        Hm0=7.0, Tp=13.0, fetch=120e3)
shelf = np.linspace(60.0, 8.0, 200)
levels = total_water_level(storm, shelf_depths=shelf, dx=120e3 / 199)

sea = np.zeros_like(terrain, dtype=bool); sea[0, :] = True
flooded = bathtub_flood(terrain, levels["still_water_level"], seed=sea)
stranded = isolated_low_ground(terrain, levels["still_water_level"], seed=sea)
```

## Worked example

<!-- output: storm_surge_flooding -->

Connectivity matters: on the synthetic barrier island, a single breach in
the barrier is the difference between 5.45 km$^2$ and 18.82 km$^2$ flooded.

![Storm surge flood mapping on a barrier-island terrain: threshold-only against connected flooding, with the inlet open and sealed.](media/storm_surge_flooding.png){#fig:surge}
