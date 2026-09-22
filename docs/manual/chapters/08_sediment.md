# Sediment and soil {#sec:sediment}

*Module:* `pyCoastal.applications.sediment`.

Every structure in this package sits on, in, or behind something. This
module makes that something a material with properties that propagate: the
grain size that decides whether the bed moves at all, the friction angle
that decides how hard the backfill pushes on a wall, and the unit weight
that decides how much of that push is soil and how much is water. The
seawall, breakwater, channel, pile, scour, and nourishment modules all take
a `Sediment` or a catalogue key.

Two families of relation live here. **Mobility** (grain size, fall
velocity, the Shields threshold) gates scour: a bed that never reaches its
threshold does not scour, whatever the wave height. **Earth pressure**
(Rankine and Coulomb coefficients, and the pressure diagram with the water
table and surcharge in the right places) loads the back of a wall.

## The material catalogue

`Sediment(name, d50, specific_gravity=2.65, porosity=0.4,
friction_angle=32, cohesion=0, phi_sorting=0.6, d90=None, description="")`
stores a material, with derived `relative_density` ($s - 1$),
`dry_unit_weight`, `saturated_unit_weight`, `submerged_unit_weight`,
`grading` ($d_{90}/d_{50}$, with $d_{90}$ defaulting to $2.5\,d_{50}$), and
`cohesive`. `sediment(key)` looks up the catalogue (@tbl:sediments) and
names the options on a bad key.

: The built-in material catalogue. {#tbl:sediments}

| Key | $d_{50}$ (mm) | $\phi'$ (deg) | Description |
|-----|---------------|---------------|-------------|
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
Whitehouse 1997), and the settling velocity (Soulsby 1997) are

$$ \begin{aligned}
D_* &= d_{50}\left[\frac{g(s-1)}{\nu^2}\right]^{1/3},\\
\theta_{cr} &= \frac{0.30}{1 + 1.2D_*} + 0.055\left[1 - e^{-0.020D_*}\right],\\
w_s &= \frac{\nu}{d_{50}}\left[\sqrt{10.36^2 + 1.049D_*^3} - 10.36\right].
\end{aligned} $$ {#eq:soulsby}

The fall velocity relation is valid from silt to gravel, which is why it is
preferred to Stokes at one end and a drag law at the other.

Under waves, `wave_orbital_velocity(Hs, T, depth)` gives the near-bed
orbital amplitude from linear theory and `wave_shields(material, Hs, T,
depth)` the Shields parameter, with the Swart friction factor for a rough
turbulent bed and a Nikuradse roughness $k_s = 2.5\,d_{50}$:

$$ f_w = \exp\left[5.213\left(\frac{A}{k_s}\right)^{-0.194} - 5.977\right],\quad f_w \le 0.3. $$ {#eq:swart}

`bed_mobility(material, Hs, T, depth)` is the gate the scour functions use.
It returns whether the bed is live, the regime (live bed, clear water, or
cohesive), and by how much the threshold is exceeded. Scour relations are
almost all live-bed results, and applying one to a bed that never reaches
its threshold predicts a hole that will not form.

## Earth pressure

`earth_pressure_coefficient(friction_angle, kind="active", wall_friction=0,
backslope=0)` returns the Rankine coefficient for `"active"`,
`"at_rest"` ($K_0 = 1 - \sin\phi'$), or `"passive"`; a non-zero wall
friction switches the active case to Coulomb, which is the honest choice for
a rough concrete face and gives a smaller force. Which coefficient applies
is a question about movement, not about soil: a wall that cannot move the
millimeter or two that mobilizes the active state carries at-rest pressure,
roughly half as large again. Choosing "active" because it is smaller is the
most common way a retaining structure is under-designed.

`lateral_earth_pressure(material, height, water_table=0, surcharge=0,
kind="active")` builds the pressure diagram with effective stress and pore
water apart; `lateral_earth_force(...)` integrates it into `soil`, `water`,
and `total` forces with the lever arm of the total. Below the water table
the soil pushes with its submerged unit weight and the water separately
with its full hydrostatic gradient, $K = 1$. The sum is larger than dry soil
alone would give, which is why drainage behind a seawall is a structural
matter and not a detail. The soil force can be argued down with a better
backfill; the water force can only be drained away.

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
