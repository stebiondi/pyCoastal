# `pyCoastal.applications.berthing`

Source: [`pyCoastal/applications/berthing.py`](../../pyCoastal/applications/berthing.py)

Berthing energy and fender selection.

A ship comes alongside carrying kinetic energy, and something has to absorb
it. Get the fender too soft and the ship reaches the quay; too hard and the
fender survives while the hull plating does not. The whole design is the
arithmetic between those two failures.

PIANC's formulation is a chain of four factors on the kinetic energy, and
the interesting thing about it is that three of the four reduce the answer.
Only the added mass of the water the ship drags with it increases it.
Between them they typically leave the fender somewhere between a half and
four fifths of the energy the ship arrived with, and every one of those
reductions is a modelling assumption that has to be defensible.

    E = 0.5 M V^2 Cm Ce Cs Cc

The one that is neither a reduction nor physics is the abnormal berthing
factor, applied afterwards. It covers the day something goes wrong: a
parted tug line, an engine that does not go astern, a master misjudging the
approach in a cross-current. PIANC sets it between 1.25 and 2.0 depending
on how much worse than usual that day can be, and for many berths it is the
single largest number in the calculation.

What this module is not
-----------------------
Fender performance here is a scaling model, not a catalogue. A real
selection is made against the manufacturer's tested energy and reaction
curves at the design temperature, angle and velocity, because those curves
are what is guaranteed and they differ materially between makers for the
same nominal size. :func:`select_fender` sizes the fender you should be
asking for; it does not choose a product.

References
----------
PIANC (2002). Guidelines for the design of fender systems. Report of
Working Group 33, Maritime Navigation Commission.

Vasco Costa, F. (1964). The berthing ship: the effect of impact on the
design of fenders and other structures. The Dock and Harbour Authority.

Brolsma, J.U., Hirs, J.A. and Langeveld, J.M. (1977). On fender design and
berthing velocities. PIANC 24th Congress.

BS 6349-4 (2014). Maritime works. Code of practice for design of fendering
and mooring systems. British Standards Institution.

## `RHO_SEAWATER`

```python
RHO_SEAWATER = 1025.0
```

## `BERTHING_VELOCITY`

```python
BERTHING_VELOCITY = {'easy_sheltered': {'small': 0.2, 'medium': 0.15, 'large': 0.1}, 'difficult_sheltered': {'small': 0.3, 'medium': 0.2, 'large': 0.15}, 'easy_exposed': {'small': 0.4, 'medium': 0.3, 'large': 0.2}, 'good_exposed': {'small': 0.5, 'medium': 0.4, 'large': 0.25}, 'difficult_exposed': {'small': 0.8, 'medium': 0.6, 'large': 0.4}}
```

## `ABNORMAL_FACTOR`

```python
ABNORMAL_FACTOR = {'tanker_large': 1.25, 'tanker_small': 1.75, 'bulk_carrier': 1.5, 'container': 1.5, 'general_cargo': 1.75, 'ro_ro': 2.0, 'ferry': 2.0, 'tug_workboat': 2.0}
```

## `HULL_PRESSURE_LIMIT`

```python
HULL_PRESSURE_LIMIT = {'tanker_large': 150.0, 'tanker_small': 200.0, 'bulk_carrier': 200.0, 'container': 400.0, 'general_cargo': 400.0, 'ro_ro': 400.0, 'ferry': 400.0, 'tug_workboat': 700.0}
```

## `BERTH_CONFIGURATION`

```python
BERTH_CONFIGURATION = {'solid_quay': 0.8, 'semi_solid': 0.9, 'open_piled': 1.0}
```

## `berthing_velocity`

```python
def berthing_velocity(vessel: Vessel, condition: str='easy_sheltered') -> dict
```

```text
Indicative design berthing velocity normal to the berth [m/s].

Raises
------
ValueError
    If the condition is not one of :data:`BERTHING_VELOCITY`.
```

## `added_mass_factor`

```python
def added_mass_factor(vessel: Vessel, depth: float | None=None) -> dict
```

```text
Virtual mass coefficient Cm, Vasco Costa (1964)::

    Cm = 1 + 2 D / B

A ship moving sideways drags a body of water with it, and that water
has to be stopped too. The shallower the berth the more of it there is,
which is why ``Cm`` is written on the draught to beam ratio: a deeply
laden ship in a tight berth carries proportionally more.

This is the only one of the four factors that makes the energy larger.

Parameters
----------
depth : float, optional
    Water depth at the berth [m]. Used only to warn: below about 1.1
    draughts the water has nowhere to go and Vasco Costa's form starts
    to understate the added mass.
```

## `eccentricity_factor`

```python
def eccentricity_factor(vessel: Vessel, contact_distance: float | None=None, approach_angle: float=90.0) -> dict
```

```text
Eccentricity coefficient Ce.

A ship rarely arrives flat against the berth. It touches at one point,
usually a quarter of its length from the bow, and then rotates about
that point. The rotation carries away energy the fender never sees::

    Ce = (K^2 + R^2 cos^2 g) / (K^2 + R^2)
    K  = (0.19 Cb + 0.11) Lpp

where ``R`` is the distance along the berth from the contact point to
the ship's centre of mass and ``g`` is the angle between the approach
velocity and the line joining them.

Parameters
----------
contact_distance : float, optional
    ``R`` [m]. Defaults to the quarter point, ``Lpp/4``, which is the
    usual design assumption for a ship coming alongside under control.
    Zero means the ship lands flat on its midships and nothing is
    carried away by rotation, which gives ``Ce = 1``.
approach_angle : float
    ``g`` in degrees. 90 is the standard assumption, the velocity being
    normal to the berth.
```

## `berthing_energy`

```python
def berthing_energy(vessel: Vessel, velocity: float, contact_distance: float | None=None, approach_angle: float=90.0, softness: float=1.0, configuration: str='open_piled', depth: float | None=None) -> dict
```

```text
Normal berthing energy [kNm], PIANC::

    E = 0.5 M V^2 Cm Ce Cs Cc

Returns every factor as well as the product, because the product on its
own tells a reviewer nothing about which assumption to argue with.

Parameters
----------
velocity : float
    Approach velocity normal to the berth [m/s]. Squared, so this is
    the assumption worth the most scrutiny.
softness : float
    Cs. 1.0 for a soft fender, which is nearly all of them; 0.9 where
    the fender is stiff enough that the hull deflects with it.
configuration : str
    Keys :data:`BERTH_CONFIGURATION`.
```

## `abnormal_energy`

```python
def abnormal_energy(normal: float, vessel_class: str='container', factor: float | None=None) -> dict
```

```text
The energy the fender is actually designed for [kNm].

PIANC's abnormal factor covers the berthing that goes wrong rather than
the one that goes normally. It is a multiplier on an already-reduced
number and is frequently the largest single term in the chain, so it is
reported separately rather than folded in.
```

## `FenderFamily`

```python
class FenderFamily
    name: str = 'Cone fender, mid grade'
    reference_height: float = 1.0
    reference_energy: float = 500.0
    reference_reaction: float = 1000.0
    deflection: float = 0.72
    heights: tuple = (0.3, 0.4, 0.5, 0.65, 0.8, 1.0, 1.2, 1.4, 1.6, 2.0, 2.5)
```

```text
A geometrically similar range of fenders.

Within one family and one rubber grade, performance scales with size:
energy absorbed goes with the volume of rubber and so with the cube of
the height, while the reaction goes with the cross-section and so with
the square::

    E = E0 (H/H0)^3        R = R0 (H/H0)^2

That is why a fender chosen to absorb twice the energy pushes back only
about 1.6 times as hard, and why the answer to a too-high reaction is
usually a bigger fender rather than a smaller one.

The reference values are a mid-grade cone fender and are indicative.
Substitute the manufacturer's own to size against a real product.
```

### `FenderFamily.energy` (method)

```python
FenderFamily.energy(self, height: float) -> float
```

```text
Rated energy of one size [kNm].
```

### `FenderFamily.reaction` (method)

```python
FenderFamily.reaction(self, height: float) -> float
```

```text
Rated reaction of one size [kN].
```

### `FenderFamily.height_for` (method)

```python
FenderFamily.height_for(self, energy: float) -> float
```

```text
The height that would absorb exactly this energy [m].
```

## `CONE_FENDER`

```python
CONE_FENDER = FenderFamily()
```

## `select_fender`

```python
def select_fender(energy: float, family: FenderFamily=CONE_FENDER) -> dict
```

```text
Smallest standard size in the family that absorbs ``energy`` [kNm].

Returns the chosen size, its rated energy and reaction, and how much of
its capacity the design actually uses. A fender working at 40% of its
rating is oversized and stiff, and will hand the hull a reaction it did
not need to take.
```

## `hull_pressure`

```python
def hull_pressure(reaction: float, panel_width: float, panel_height: float, vessel_class: str='container') -> dict
```

```text
Contact pressure on the side shell [kN/m2].

The check that sizes the panel rather than the rubber. A fender chosen
on energy alone presents its reaction over whatever area happens to be
there, and for a tanker that limit is a quarter of a container ship's.
```

## `fender_spacing`

```python
def fender_spacing(vessel: Vessel, spacing: float, projection: float, bow_radius: float | None=None, smallest_vessel: Vessel | None=None, clearance: float=0.15) -> dict
```

```text
Whether a ship can touch the quay between two fenders.

Two checks, and a berth has to pass both.

The geometric one: a hull is curved, so between two fenders it reaches
closer to the wall than at them. With the fenders compressed, the
remaining standoff has to exceed the sagitta of the hull across the
gap::

    spacing <= 2 sqrt(Rb^2 - (Rb - p + c)^2)

The practical one: the smallest ship using the berth has to reach two
fenders at once, or it will sit on one and pivot. The usual limit is
about 0.15 of its length between perpendiculars.

Parameters
----------
projection : float
    Standoff from the quay face to the hull with the fender at its
    design deflection [m].
bow_radius : float, optional
    Radius of the hull curvature in plan at the point of contact [m].
    Left out, the contact is taken on the parallel midbody, which is
    straight, so the geometric check cannot bind and the vessel length
    rule governs. Supply a radius for the end fenders, where the bow or
    stern flare curves away from the quay and a ship can tuck in behind
    a fender that a straight hull could not.
smallest_vessel : Vessel, optional
    The smallest ship expected to use the berth. The practical rule is
    about *that* ship reaching two fenders, not the design one, so
    leaving this out uses the design vessel and gives a limit that is
    too generous for a berth with mixed traffic.
clearance : float
    Gap that must remain between hull and structure [m].
```

## `BerthDesign`

```python
class BerthDesign
    vessel: Vessel
    velocity: float
    normal: dict
    abnormal: dict
    fender: dict
    panel: dict
    pressure: dict
    spacing: dict
    family: FenderFamily
    notes: list[str] = field(default_factory=list)
```

```text
The outcome of :func:`design_berth`.
```

### `BerthDesign.adequate` (property)

```python
BerthDesign.adequate(self) -> bool
```

```text
Whether the berth passes energy, hull pressure and spacing.
```

### `BerthDesign.energy` (property)

```python
BerthDesign.energy(self) -> float
```

```text
The design energy, which is the abnormal one [kNm].
```

## `design_berth`

```python
def design_berth(vessel: Vessel, velocity: float | None=None, condition: str='easy_sheltered', vessel_class: str='container', configuration: str='open_piled', depth: float | None=None, contact_distance: float | None=None, approach_angle: float=90.0, softness: float=1.0, abnormal_factor: float | None=None, spacing: float | None=None, smallest_vessel: Vessel | None=None, bow_radius: float | None=None, clearance: float=0.15, panel_aspect: tuple[float, float]=(1.2, 2.0), family: FenderFamily=CONE_FENDER) -> BerthDesign
```

```text
Size a fender for a berth, and check what it does to the hull.

The chain, in order: kinetic energy, the four PIANC factors, the
abnormal allowance, a fender that absorbs it, the reaction that fender
hands back, the panel needed to spread that reaction to something the
side shell can take, and the spacing that stops the ship touching
between fenders.

Each step can fail on its own and the failures are different. Too small
a fender lets the ship reach the quay. Too small a panel dents the hull.
Too wide a spacing does both, at a point where nothing is measuring.

Parameters
----------
velocity : float, optional
    Approach velocity [m/s]. Taken from :data:`BERTHING_VELOCITY` for
    the ``condition`` if not given, which is a starting point rather
    than a design value.
panel_aspect : tuple
    Panel width and height as multiples of the fender height. The
    default is a common proportion; a panel is cheap next to a hull
    repair, so widen it rather than accept a marginal pressure.

Returns
-------
BerthDesign
```

