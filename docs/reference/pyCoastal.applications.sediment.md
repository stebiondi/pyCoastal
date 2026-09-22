# `pyCoastal.applications.sediment`

Source: [`pyCoastal/applications/sediment.py`](../../pyCoastal/applications/sediment.py)

Sediment and soil: what the bed is made of, and what that costs you.

Every structure in this package sits on, in, or behind something. Until now
that something was a number typed into a signature. This module makes it a
material with properties that propagate: the grain size that decides whether
the bed moves at all, the friction angle that decides how hard the backfill
pushes on the wall, the unit weight that decides how much of that push is
soil and how much is water.

Two families of relation live here, and they are not the same subject.

Mobility
    Whether, and how fast, grains move. Grain size, fall velocity, and the
    Shields threshold. This is what gates scour: a bed that never reaches
    its threshold does not scour, whatever the wave height.
Earth pressure
    What retained soil does to a wall. Rankine and Coulomb coefficients, and
    the pressure diagram integrated over the retained height with the water
    table and any surcharge in the right places.

Sources
-------
Soulsby, R. L. (1997), Dynamics of Marine Sands. Dimensionless grain size,
    fall velocity, and the threshold of motion.

Soulsby, R. L. and Whitehouse, R. J. S. (1997), "Threshold of sediment
    motion in coastal environments". The critical Shields curve fitted here.

Rankine, W. J. M. (1857) and Coulomb, C. A. (1776), through any soil
    mechanics text. Lateral earth pressure coefficients.

CIRIA/CUR/CETMEF (2007), The Rock Manual. Typical properties for the
    granular materials in the catalogue.

Conventions
-----------
Grain sizes are metres, not millimetres, to stay consistent with the rest of
the package. Unit weights are kN/m3 and forces kN per metre run. Angles are
degrees on the way in, because that is how a geotechnical report states
them, and radians internally.

## `G`

```python
G = 9.81
```

## `RHO_W`

```python
RHO_W = 1025.0
```

## `GAMMA_W`

```python
GAMMA_W = RHO_W * G / 1000.0
```

## `NU`

```python
NU = 1.19e-06
```

## `Sediment`

```python
class Sediment
    name: str
    d50: float
    specific_gravity: float = 2.65
    porosity: float = 0.4
    friction_angle: float = 32.0
    cohesion: float = 0.0
    phi_sorting: float = 0.6
    d90: float | None = None
    description: str = ''
```

```text
A bed or backfill material.

Attributes
----------
name : str
    For the report and the drawing.
d50 : float
    Median grain size [m]. Zero for a cohesive material, where grain
    size is not what governs.
specific_gravity : float
    Grain density over water density. 2.65 for quartz sand.
porosity : float
    Voids as a fraction of total volume, in place.
friction_angle : float
    Effective angle of shearing resistance phi' [deg]. This is the one
    number that decides how hard a backfill pushes on a wall, and it is
    the one most worth getting from a real site investigation.
cohesion : float
    Effective cohesion c' [kPa]. Zero for anything granular.
phi_sorting : float
    Standard deviation of the grading on the phi scale, sigma_phi.
    Below about 0.5 is well sorted, above 1.0 poorly sorted. It is what
    decides how much of a borrow source winnows away rather than staying
    on the beach.
d90 : float, optional
    Ninety per cent passing size [m]. Defaults to 2.5 d50, a reasonable
    ratio for a moderately graded marine sand.
description : str
    What a person would call it.
```

### `Sediment.relative_density` (property)

```python
Sediment.relative_density(self) -> float
```

```text
s - 1, the buoyant density ratio that drives every mobility number.
```

### `Sediment.dry_unit_weight` (property)

```python
Sediment.dry_unit_weight(self) -> float
```

```text
Unit weight of the drained material [kN/m3].
```

### `Sediment.saturated_unit_weight` (property)

```python
Sediment.saturated_unit_weight(self) -> float
```

```text
Unit weight with the voids full of water [kN/m3].
```

### `Sediment.submerged_unit_weight` (property)

```python
Sediment.submerged_unit_weight(self) -> float
```

```text
Buoyant unit weight below the water table [kN/m3].

This is the number that makes a submerged backfill push so much less
hard than a drained one: roughly six kN/m3 rather than eighteen.
The water it displaces pushes separately, and harder.
```

### `Sediment.cohesive` (property)

```python
Sediment.cohesive(self) -> bool
```

### `Sediment.grading` (method)

```python
Sediment.grading(self) -> float
```

```text
d90 / d50, the spread of the grading.
```

### `Sediment.summary` (method)

```python
Sediment.summary(self) -> str
```

## `SEDIMENTS`

```python
SEDIMENTS = {'soft_clay': Sediment('Soft clay', d50=0.0, specific_gravity=2.7, porosity=0.55, friction_angle=22.0, cohesion=15.0, phi_sorting=2.0, description='normally consolidated, undrained strength governs'), 'stiff_clay': Sediment('Stiff clay', d50=0.0, specific_gravity=2.72, porosity=0.42, friction_angle=26.0, cohesion=40.0, phi_sorting=2.0, description='overconsolidated'), 'silt': Sediment('Silt', d50=3e-05, specific_gravity=2.65, porosity=0.48, friction_angle=28.0, phi_sorting=1.6, description='mobile at almost any wave'), 'very_fine_sand': Sediment('Very fine sand', d50=9e-05, porosity=0.45, friction_angle=29.0, phi_sorting=0.55, description='suspends readily, high siltation'), 'fine_sand': Sediment('Fine sand', d50=0.00019, porosity=0.43, friction_angle=31.0, phi_sorting=0.45, description='the usual beach and nearshore sand'), 'medium_sand': Sediment('Medium sand', d50=0.00038, porosity=0.4, friction_angle=33.0, phi_sorting=0.55, description='typical dredged fill'), 'coarse_sand': Sediment('Coarse sand', d50=0.00075, porosity=0.38, friction_angle=35.0, phi_sorting=0.7, description='good drained backfill'), 'fine_gravel': Sediment('Fine gravel', d50=0.006, porosity=0.35, friction_angle=38.0, phi_sorting=0.95, description='free draining'), 'coarse_gravel': Sediment('Coarse gravel', d50=0.03, porosity=0.35, friction_angle=40.0, phi_sorting=1.1, description='shingle beach'), 'rock_fill': Sediment('Quarry rock fill', d50=0.15, porosity=0.37, friction_angle=42.0, phi_sorting=1.4, description='engineered granular backfill')}
```

## `sediment`

```python
def sediment(key: str) -> Sediment
```

```text
Look a material up by key, with the options named on failure.
```

## `dimensionless_grain_size`

```python
def dimensionless_grain_size(material, viscosity: float=NU) -> float
```

```text
D* = d50 [g (s - 1) / nu^2]^(1/3), Soulsby (1997).

The single parameter that collapses the threshold of motion and the fall
velocity across grain sizes. Below about 4 the grain is in the viscous
range; above about 100 it is fully rough.
```

## `critical_shields`

```python
def critical_shields(material, viscosity: float=NU) -> float
```

```text
Critical Shields parameter, Soulsby and Whitehouse (1997)::

    theta_cr = 0.30 / (1 + 1.2 D*) + 0.055 [1 - exp(-0.020 D*)]

A fitted curve through the Shields data that behaves at both ends,
unlike reading a value off the original diagram.
```

## `fall_velocity`

```python
def fall_velocity(material, viscosity: float=NU) -> float
```

```text
Settling velocity of a single grain [m/s], Soulsby (1997)::

    w_s = nu / d [ sqrt(10.36^2 + 1.049 D*^3) - 10.36 ]

Valid across the whole range from silt to gravel, which is why it is
preferred to Stokes at one end and a drag law at the other.
```

## `wave_orbital_velocity`

```python
def wave_orbital_velocity(Hs: float, T: float, depth: float, wavelength: float | None=None) -> float
```

```text
Near-bed orbital velocity amplitude under a linear wave [m/s].

U_w = pi Hs / (T sinh(k h))
```

## `wave_shields`

```python
def wave_shields(material, Hs: float, T: float, depth: float, wavelength: float | None=None) -> dict
```

```text
Shields parameter under waves, and whether the bed is moving.

Uses the Swart wave friction factor for a rough turbulent bed, with the
orbital excursion over the Nikuradse roughness of 2.5 d50::

    f_w = exp[5.213 (A / k_s)^-0.194 - 5.977],  capped at 0.3

Returns
-------
dict
    The orbital velocity and excursion, the friction factor, the Shields
    parameter, its critical value, and ``mobile``.
```

## `bed_mobility`

```python
def bed_mobility(material, Hs: float, T: float, depth: float) -> dict
```

```text
Whether the bed at a structure is live, and by how much.

Scour relations are almost all live-bed results. Applying one to a bed
that never reaches its threshold predicts a hole that will not form.
This is the gate the scour functions use.
```

## `earth_pressure_coefficient`

```python
def earth_pressure_coefficient(friction_angle: float, kind: str='active', wall_friction: float=0.0, backslope: float=0.0) -> float
```

```text
Lateral earth pressure coefficient.

Parameters
----------
friction_angle : float
    Effective angle of shearing resistance phi' [deg].
kind : str
    "active" for a wall free to move away from the soil, "at_rest" for
    one that cannot, "passive" for one pushed into it.
wall_friction : float
    Angle of friction on the wall face delta [deg]. Non-zero switches
    the active case from Rankine to Coulomb, which is the honest choice
    for a rough concrete face and gives a smaller force.
backslope : float
    Slope of the retained surface [deg], for the Rankine sloping-backfill
    form.

Notes
-----
Which coefficient applies is a question about movement, not about soil.
A gravity seawall on a rubble bedding can move the millimetre or two
that mobilises the active state; one cast against rock, or restrained by
a slab, cannot, and then at-rest governs and the force is roughly half
as large again. Choosing "active" because it is smaller is the most
common way a retaining structure is under-designed.
```

## `lateral_earth_pressure`

```python
def lateral_earth_pressure(material, height: float, water_table: float=0.0, surcharge: float=0.0, kind: str='active', wall_friction: float=0.0, points: int=201) -> dict
```

```text
Pressure diagram on the back of a wall, effective stress and water apart.

Parameters
----------
height : float
    Retained height H [m], measured from the top of the retained surface
    down to the base of the wall.
water_table : float
    Depth of the water table below the retained surface [m]. Zero means
    the backfill is saturated to the top, which is the condition behind
    a seawall with a blocked drain and is the one that breaks walls.
surcharge : float
    Uniform surcharge on the retained surface [kPa].
kind, wall_friction
    Passed to :func:`earth_pressure_coefficient`.

Returns
-------
dict
    ``depth`` and the three pressure arrays (``effective``, ``pore``,
    ``total``) in kPa, plus the coefficient used.

Notes
-----
Below the water table the soil pushes with its *submerged* unit weight
and the water pushes separately with its full hydrostatic gradient. The
sum is larger than the dry soil alone would give, because water has no
friction angle to lean on: it presses with K = 1. This is why drainage
behind a seawall is a structural matter and not a detail.
```

## `lateral_earth_force`

```python
def lateral_earth_force(material, height: float, water_table: float=0.0, surcharge: float=0.0, kind: str='active', wall_friction: float=0.0, points: int=401) -> dict
```

```text
Total horizontal force from retained soil and water [kN/m].

Returns
-------
dict
    ``soil`` and ``water`` forces and the ``total``, the lever ``arm``
    of the total above the base of the wall, and the pressure diagram
    that produced them.

Notes
-----
The split matters. The soil force scales with the friction angle and can
be argued down with a better backfill; the water force cannot be argued
with at all, only drained away.
```

