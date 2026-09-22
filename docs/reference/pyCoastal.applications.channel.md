# `pyCoastal.applications.channel`

Source: [`pyCoastal/applications/channel.py`](../../pyCoastal/applications/channel.py)

Navigation channel design: squat, underkeel clearance, depth and width.

How deep and how wide does the approach channel have to be? The answer is a
stack of allowances, each small, each defensible, and together often several
metres. This module builds that stack explicitly so it can be argued over
line by line, which is how a dredging budget actually gets agreed.

The depth chain
---------------
Start at the design water level, subtract the vessel's static draught, then
subtract, in turn, the squat as she moves, her vertical response to waves,
the net clearance the pilot and the authority require over the bed, and the
tolerances the dredger and the survey cannot beat. What is left is the
dredge level.

The width chain
---------------
A basic manoeuvring lane, widened for everything that pushes the vessel off
line (speed, wind, cross current, waves, poor marking, a hostile bottom),
plus clearance to each bank, and doubled with a passing distance if the
channel is two-way.

Sources
-------
PIANC (2014), Harbour Approach Channels Design Guidelines, report 121.
    The concept design method reproduced here: the width components, the
    underkeel clearance components, and the squat formulations.

ICORELS (1980), as given in PIANC. The squat formula used by default.

Barrass, C. B. (1979), "A unified approach to squat calculations for
    ships". The screening formula.

Conventions
-----------
Levels are metres to chart datum and increase upward. Depths and draughts
are positive numbers of metres. Speeds are in knots where a formula is
written in knots and metres per second elsewhere; every function says which.

Caution
-------
The width components and the manoeuvring lane widths here follow the PIANC
concept-design structure with the indicative values commonly quoted. They
are exposed as editable tables rather than buried, because the governing
edition of the guideline, and the pilots on the day, decide the numbers on
a real scheme. Concept design only: a real channel is confirmed by
simulation.

## `G`

```python
G = 9.81
```

## `KNOT`

```python
KNOT = 0.514444
```

## `Vessel`

```python
class Vessel
    name: str
    length: float
    beam: float
    draught: float
    block_coefficient: float = 0.75
    length_pp: float | None = None
```

```text
The design vessel.

Attributes
----------
name : str
    For the drawing and the report.
length : float
    Length overall Loa [m].
length_pp : float
    Length between perpendiculars [m]. Defaults to 0.96 Loa, the usual
    ratio for a merchant hull, because the squat formulae are written
    around Lpp and getting it wrong by four per cent is not the largest
    error in the chain.
beam : float
    Moulded beam B [m].
draught : float
    Static draught at the design loading T [m].
block_coefficient : float
    Cb, the fraction of the enclosing box the hull fills. About 0.85 for
    a bulk carrier, 0.65 for a container ship, 0.55 for a fast ferry.
```

### `Vessel.displaced_volume` (property)

```python
Vessel.displaced_volume(self) -> float
```

```text
Displaced volume from the block coefficient [m3].
```

### `Vessel.displacement` (property)

```python
Vessel.displacement(self) -> float
```

```text
Displacement in tonnes, at 1025 kg/m3.
```

## `squat_icorels`

```python
def squat_icorels(vessel: Vessel, speed: float, depth: float, coefficient: float=2.4) -> dict
```

```text
Bow squat by the ICORELS formula, as given in PIANC.

    S = C * (V / Lpp^2) * Fnh^2 / sqrt(1 - Fnh^2)

where the displacement volume replaces V and Fnh is the depth Froude
number, ``u / sqrt(g h)``.

Parameters
----------
speed : float
    Vessel speed through the water [knots].
depth : float
    Water depth [m].
coefficient : float
    2.4 is the value PIANC gives for an open or a wide channel. A
    confined channel squats more; the guideline's correction factor is
    applied through this coefficient.

Returns
-------
dict
    ``squat`` [m], the depth Froude number, and a flag for whether the
    speed is close enough to the critical speed that the formula is
    unusable.

Notes
-----
The formula blows up as Fnh approaches one, where the vessel is at
the critical speed and the whole notion of a steady squat fails. It is
normally kept to Fnh below about 0.7, and no vessel is navigated a
channel anywhere near that. The returned dict flags it rather than
returning a number that is arithmetically fine and physically absurd.
```

## `squat_barrass`

```python
def squat_barrass(vessel: Vessel, speed: float, depth: float, confined: bool=False) -> dict
```

```text
Bow squat by Barrass's screening formula.

    S_max = Cb * V^2 / 100     in open water
    S_max = Cb * V^2 / 50      in a confined channel

with the speed in knots. Deliberately crude, and useful exactly because
of it: a number to sanity-check the ICORELS result against, on the back
of an envelope, before trusting either.
```

## `wave_response_allowance`

```python
def wave_response_allowance(Hs: float, factor: float=0.5, period: float | None=None, vessel: Vessel | None=None) -> dict
```

```text
Vertical vessel motion allowance from wave height [m].

Parameters
----------
Hs : float
    Significant wave height in the channel [m].
factor : float
    Fraction of Hs taken as the vertical motion of the keel. PIANC's
    concept-design guidance spans roughly 0.3 for a long vessel in short
    head seas up to about 0.7 for a short vessel in long beam seas, and
    0.5 is the usual starting point. This is the single largest
    judgement in the depth chain when there is any swell at all, so set
    it deliberately.
period, vessel : optional
    Used only to report the ratio of wave length to vessel length, which
    is what governs whether the vessel contours the wave or bridges it.
    A ratio near one is the worst case and argues for a higher factor.

Returns
-------
dict
    The ``allowance`` and, when the optional arguments are given, the
    wave length and its ratio to the vessel length.
```

## `MANOEUVRING_LANE`

```python
MANOEUVRING_LANE = {'good': 1.3, 'moderate': 1.5, 'poor': 1.8}
```

## `WIDTH_COMPONENTS`

```python
WIDTH_COMPONENTS = {'speed': {'fast': (0.1, 0.1), 'moderate': (0.0, 0.0), 'slow': (0.0, 0.0)}, 'crosswind': {'mild': (0.1, 0.1), 'moderate': (0.3, 0.4), 'severe': (0.6, 0.8)}, 'crosscurrent': {'negligible': (0.0, 0.0), 'low': (0.2, 0.3), 'moderate': (0.5, 0.7), 'strong': (1.0, 1.3)}, 'longitudinal_current': {'low': (0.0, 0.0), 'moderate': (0.1, 0.1), 'strong': (0.2, 0.2)}, 'waves': {'low': (0.0, 0.0), 'moderate': (0.5, 0.0), 'high': (1.0, 0.0)}, 'aids_to_navigation': {'excellent': (0.0, 0.0), 'good': (0.2, 0.2), 'moderate': (0.4, 0.4)}, 'bottom_surface': {'smooth_and_soft': (0.1, 0.1), 'smooth_or_sloping': (0.1, 0.1), 'rough_and_hard': (0.2, 0.2)}, 'depth_of_waterway': {'deep': (0.0, 0.0), 'moderate': (0.1, 0.2), 'shallow': (0.2, 0.4)}, 'cargo_hazard': {'low': (0.0, 0.0), 'medium': (0.5, 0.4), 'high': (1.0, 0.8)}}
```

## `BANK_CLEARANCE`

```python
BANK_CLEARANCE = {'sloping_channel_edges': {'fast': 0.7, 'moderate': 0.5, 'slow': 0.3}, 'sloping_and_shoals': {'fast': 0.7, 'moderate': 0.5, 'slow': 0.3}, 'steep_and_hard': {'fast': 1.3, 'moderate': 1.0, 'slow': 0.5}}
```

## `PASSING_DISTANCE`

```python
PASSING_DISTANCE = {'fast': 2.0, 'moderate': 1.6, 'slow': 1.2}
```

## `channel_width`

```python
def channel_width(vessel: Vessel, manoeuvrability: str='moderate', section: str='outer', two_way: bool=False, speed_class: str='moderate', bank: str='sloping_channel_edges', conditions: dict | None=None) -> dict
```

```text
Channel width by the PIANC concept-design build-up.

Parameters
----------
manoeuvrability : str
    Key into :data:`MANOEUVRING_LANE`.
section : str
    "outer" for an exposed approach, "inner" for a sheltered reach. The
    two columns of :data:`WIDTH_COMPONENTS` differ because an exposed
    channel has waves and a sheltered one has banks close by.
two_way : bool
    Whether two design vessels pass.
speed_class : str
    "fast", "moderate" or "slow", used for the bank clearance and the
    passing distance.
conditions : dict, optional
    One key per entry in :data:`WIDTH_COMPONENTS`, naming the class that
    applies. Anything omitted is taken as its most benign class, and is
    reported as such so the omission is visible.

Returns
-------
dict
    The total ``width``, the ``components`` that built it, and the
    assumptions filled in for anything not specified.
```

## `underkeel_clearance`

```python
def underkeel_clearance(vessel: Vessel, squat: float, wave_allowance: float, net_clearance: float=0.6, water_level_allowance: float=0.0, dredging_tolerance: float=0.3, survey_tolerance: float=0.2, siltation_allowance: float=0.2, density_allowance: float=0.0) -> dict
```

```text
Build the underkeel clearance stack [m].

Parameters
----------
net_clearance : float
    The clearance that must remain under the keel at the worst instant,
    after every other allowance has been used up. Commonly 0.5 to 1.0 m
    over a soft bed and more over rock, and often set by the port's own
    rules rather than by a calculation.
water_level_allowance : float
    Uncertainty in the predicted water level: the difference between
    the predicted and the actual tide, and any negative surge.
dredging_tolerance, survey_tolerance : float
    What the dredger can hold and what the survey can see. Both are
    real, both are always there, and leaving them out is the most
    common way a channel ends up shallower than its drawing.
siltation_allowance : float
    Material expected between maintenance campaigns.
density_allowance : float
    Extra draught in brackish or fresh water, where the vessel floats
    deeper than in the salt water her marks were set in.

Returns
-------
dict
    Each allowance, the ``gross`` total below the keel, and the total
    ``required_depth`` below the design water level.
```

## `dredged_side_slope`

```python
def dredged_side_slope(bed, factor: float=2.0) -> dict
```

```text
Stable side slope for a dredged channel, from the bed material.

    cot(beta) = factor / tan(phi')

The default factor of 2 on the tangent covers two things at once: the
partial factor on a submerged granular slope carrying no surcharge, and
the overcut and slumping that dredging adds on top of it. It lands on
the slopes that actually get built, roughly 1:2.6 in gravel and 1:3.8
in silt.

Notes
-----
Set ``factor`` to 1.5 for the geotechnical lower bound on its own, which
is the steepest the material will stand at and steeper than anything a
dredger will leave behind. A cohesive bed can stand far steeper in the
short term and is not covered by this at all; an exposed reach worked on
by waves ends up flatter than either number.
```

## `ChannelDesign`

```python
class ChannelDesign
    vessel: Vessel
    design_water_level: float
    dredge_level: float
    required_depth: float
    clearance: dict
    squat: dict
    waves: dict
    width_result: dict
    side_slope: float
    speed: float
    bed: 'Sediment | None' = None
    existing_bed: float | None = None
    warnings: list[str] = field(default_factory=list)
```

```text
A dimensioned approach channel.
```

### `ChannelDesign.width` (property)

```python
ChannelDesign.width(self) -> float
```

```text
Channel bed width [m].
```

### `ChannelDesign.top_width` (property)

```python
ChannelDesign.top_width(self) -> float
```

```text
Width at the existing bed, including the side slopes [m].
```

### `ChannelDesign.dredge_volume` (method)

```python
ChannelDesign.dredge_volume(self, length: float) -> float
```

```text
Capital dredge volume over a length of channel [m3].

A trapezoid over a flat existing bed. A real take-off works from a
survey surface, and will differ; this is the number to size a
campaign with, not to pay a contractor on.
```

### `ChannelDesign.summary` (method)

```python
ChannelDesign.summary(self) -> str
```

```text
A short design report, depth chain first.
```

## `design_channel`

```python
def design_channel(vessel: Vessel, speed: float, design_water_level: float, Hs: float=0.0, Tp: float | None=None, wave_factor: float=0.5, net_clearance: float=0.6, water_level_allowance: float=0.3, dredging_tolerance: float=0.3, survey_tolerance: float=0.2, siltation_allowance: float=0.2, density_allowance: float=0.0, squat_coefficient: float=2.4, side_slope: float | None=None, bed: 'Sediment | str'='medium_sand', existing_bed: float | None=None, **width_kwargs) -> ChannelDesign
```

```text
Size an approach channel: depth from the clearance stack, width from PIANC.

The squat depends on the water depth, which depends on the squat, so the
depth is solved by a short fixed-point iteration rather than by guessing
a depth and hoping.

Extra keyword arguments go to :func:`channel_width`.
```

## `turning_basin_diameter`

```python
def turning_basin_diameter(vessel: Vessel, assisted: bool=True, current: bool=False) -> dict
```

```text
Turning basin diameter as a multiple of the vessel length [m].

Indicative concept-design values: 1.5 Loa where tugs or thrusters turn
the vessel on the spot, 2.0 Loa for an unassisted turn, and a further
half a length where a current runs through the basin. A real basin is
confirmed by simulation, and the shape is rarely a circle.
```

