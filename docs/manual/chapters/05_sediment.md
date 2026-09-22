# Sediment and soil {#sec:sediment}

*Module:* `pyCoastal.applications.sediment`.

The module defines bed and backfill materials and the relations that use
them. Material properties propagate into the other design modules: the grain
size controls bed mobility, the friction angle controls the lateral pressure
of a backfill, and the unit weight sets the split between effective stress
and pore pressure. The seawall, breakwater, channel, pile, scour and
nourishment modules accept a `Sediment` instance or a catalogue key.

The module implements two groups of relation. **Mobility** (grain size, fall
velocity, Shields threshold) determines whether the bed is in motion and
gates the scour relations. **Earth pressure** (Rankine and Coulomb
coefficients, and the pressure diagram including the water table and any
surcharge) supplies the load on the back of a wall.

## The material catalogue

`Sediment(name, d50, specific_gravity=2.65, porosity=0.4,
friction_angle=32, cohesion=0, phi_sorting=0.6, d90=None, description="")`
stores a material, with derived `relative_density` ($s - 1$),
`dry_unit_weight`, `saturated_unit_weight`, `submerged_unit_weight`,
`grading` ($d_{90}/d_{50}$, with $d_{90}$ defaulting to $2.5\,d_{50}$), and
`cohesive`. `sediment(key)` returns a catalogue material
(@tbl:sediments); an unknown key raises with the available keys listed.

: The built-in material catalogue. {#tbl:sediments}

| Key | $d_{50}$ (mm) | $\phi'$ (deg) | Description |
|------------------|------------|------------|------------------------------------------|
| `soft_clay` | cohesive | 22 | normally consolidated, undrained strength governs |
| `stiff_clay` | cohesive | 26 | overconsolidated |
| `silt` | 0.03 | 28 | mobile at almost any wave |
| `very_fine_sand` | 0.09 | 29 | suspends readily, high siltation |
| `fine_sand` | 0.19 | 31 | the usual beach and nearshore sand |
| `medium_sand` | 0.38 | 33 | typical dredged fill |
| `coarse_sand` | 0.75 | 35 | good drained backfill |
| `fine_gravel` | 6 | 38 | free draining |
| `coarse_gravel` | 30 | 40 | shingle beach |
| `rock_fill` | 150 | 42 | engineered granular backfill |

## Mobility

The dimensionless grain size, the critical Shields parameter (Soulsby and
Whitehouse 1997), and the settling velocity (Soulsby 1997) are given by @eq:soulsby:

$$ \begin{aligned}
D_* &= d_{50}\left[\frac{g(s-1)}{\nu^2}\right]^{1/3},\\
\theta_{cr} &= \frac{0.30}{1 + 1.2D_*} + 0.055\left[1 - e^{-0.020D_*}\right],\\
w_s &= \frac{\nu}{d_{50}}\left[\sqrt{10.36^2 + 1.049D_*^3} - 10.36\right].
\end{aligned} $$ {#eq:soulsby}

The fall velocity relation applies from silt to gravel and covers the full
grain-size range of the catalogue.

Under waves, `wave_orbital_velocity(Hs, T, depth)` gives the near-bed
orbital amplitude from linear theory and `wave_shields(material, Hs, T,
depth)` the Shields parameter, with the Swart friction factor for a rough
turbulent bed and a Nikuradse roughness $k_s = 2.5\,d_{50}$ (@eq:swart):

$$ f_w = \exp\left[5.213\left(\frac{A}{k_s}\right)^{-0.194} - 5.977\right],\quad f_w \le 0.3. $$ {#eq:swart}

`bed_mobility(material, Hs, T, depth)` returns the mobility state used by
the scour functions: whether the bed is live, the regime (live bed, clear
water or cohesive), and the ratio of the Shields parameter to its critical
value. The scour relations implemented in this package are live-bed results
and are gated on this state.

## Earth pressure

`earth_pressure_coefficient(friction_angle, kind="active", wall_friction=0,
backslope=0)` returns the Rankine coefficient for `"active"`, `"at_rest"`
($K_0 = 1 - \sin\phi'$) or `"passive"`. A non-zero wall friction selects the
Coulomb active coefficient, which applies to a rough wall face and returns a
smaller force.

Selection between the coefficients is governed by wall movement. A wall free
to move by the displacement that mobilizes the active state carries active
pressure. A wall restrained against that displacement carries at-rest
pressure, which is approximately 1.5 times the active value for the
materials in the catalogue.

`lateral_earth_pressure(material, height, water_table=0, surcharge=0,
kind="active")` returns the pressure diagram with effective stress and pore
pressure as separate arrays. `lateral_earth_force(...)` integrates the
diagram into `soil`, `water` and `total` forces and the lever arm of the
total. Below the water table the soil contributes its submerged unit weight
and the pore water contributes the full hydrostatic gradient at $K = 1$. The
total therefore exceeds the dry-soil value. The soil component depends on
the backfill material; the water component is removed only by drainage.

```python
from pyCoastal.applications.sediment import (
    sediment, critical_shields, fall_velocity, wave_shields, lateral_earth_force,
)

sand = sediment("medium_sand")
critical_shields(sand), fall_velocity(sand)           # about 0.035 and 0.05 m/s
wave_shields(sand, Hs=2.0, T=9.0, depth=8.0)["mobile"]
lateral_earth_force(sand, height=10.0, water_table=0.0, surcharge=10.0,
                    kind="at_rest")["total"]          # kN/m
```
