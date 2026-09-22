# `pyCoastal.applications.river`

Source: [`pyCoastal/applications/river.py`](../../pyCoastal/applications/river.py)

Open channel hydraulics: normal and critical depth, backwater, and afflux.

The foundation the fluvial side of a crossing stands on. Everything a
bridge does to a river, it does by changing the depth: it squeezes the
flow, the water backs up, and that backwater reaches upstream for a
distance nobody guesses correctly by eye.

Two depths govern a reach, and almost every question is really about which
of them the flow is between.

**Normal depth** is where the bed slope and the friction balance, so the
flow would stay there forever in a prismatic channel. **Critical depth** is
where the specific energy is least and the Froude number is one. Whether
normal is above or below critical decides whether the reach is mild or
steep, which decides which way a disturbance travels: on a mild slope the
backwater from a bridge runs upstream, on a steep one it cannot, and the
bridge is felt downstream instead.

A note on where this joins the coast
------------------------------------
:func:`flow_distribution` is the reason this module exists alongside
:mod:`pyCoastal.applications.scour`. Contraction scour needs to know what
fraction of the discharge actually goes through the opening rather than
staying out on the floodplain, and that fraction is a conveyance
calculation, not a guess. Feeding a guessed ``flow_fraction`` into a scour
depth and then quoting it to two decimals is a way of hiding the largest
assumption in the chain behind the most precise-looking number.

References
----------
Chow, V.T. (1959). Open-Channel Hydraulics. McGraw-Hill.

Henderson, F.M. (1966). Open Channel Flow. Macmillan.

Yarnell, D.L. (1934). Bridge piers as channel obstructions. Technical
Bulletin 442, US Department of Agriculture.

Hydrologic Engineering Center (2016). HEC-RAS River Analysis System
Hydraulic Reference Manual, Version 5.0. US Army Corps of Engineers.

## `G`

```python
G = 9.81
```

## `MANNING`

```python
MANNING = {'concrete_smooth': 0.013, 'concrete_rough': 0.017, 'earth_clean': 0.022, 'earth_weedy': 0.03, 'gravel': 0.028, 'cobbles': 0.035, 'natural_clean': 0.03, 'natural_weedy': 0.045, 'floodplain_pasture': 0.035, 'floodplain_brush': 0.07, 'floodplain_trees': 0.1}
```

## `PIER_SHAPE`

```python
PIER_SHAPE = {'semicircular_nose': 0.9, 'twin_cylinder': 0.95, 'ninety_degree_wedge': 1.05, 'square_nose': 1.25, 'ten_pile_trestle': 2.5}
```

## `Channel`

```python
class Channel
    width: float = 30.0
    side_slope: float = 2.0
    roughness: float | str = 'natural_clean'
```

```text
A trapezoidal prismatic channel.

Attributes
----------
width : float
    Bottom width [m]. Zero gives a triangular section.
side_slope : float
    Horizontal run per unit rise, z in 1V:zH. Zero is rectangular.
roughness : float or str
    Manning's n, or a key into :data:`MANNING`.
```

### `Channel.n` (property)

```python
Channel.n(self) -> float
```

```text
Manning's n.
```

### `Channel.area` (method)

```python
Channel.area(self, depth: float) -> float
```

```text
Flow area [m2].
```

### `Channel.perimeter` (method)

```python
Channel.perimeter(self, depth: float) -> float
```

```text
Wetted perimeter [m].
```

### `Channel.top_width` (method)

```python
Channel.top_width(self, depth: float) -> float
```

```text
Width at the water surface [m].
```

### `Channel.hydraulic_radius` (method)

```python
Channel.hydraulic_radius(self, depth: float) -> float
```

```text
A / P [m].
```

### `Channel.conveyance` (method)

```python
Channel.conveyance(self, depth: float) -> float
```

```text
K = A R^(2/3) / n, so that Q = K sqrt(S).
```

### `Channel.velocity` (method)

```python
Channel.velocity(self, discharge: float, depth: float) -> float
```

```text
Mean velocity [m/s].
```

## `normal_depth`

```python
def normal_depth(channel: Channel, discharge: float, slope: float, limit: float=1000.0) -> float
```

```text
Depth at which friction balances the bed slope [m].

Solves Manning, ``Q = K sqrt(S0)``, for the depth. This is where the
flow would settle if the channel ran straight and prismatic forever,
and it is one of the two depths a backwater profile is drawn between.

Raises
------
ValueError
    On a horizontal or adverse slope, where uniform flow does not
    exist and normal depth is undefined. That is a real condition, not
    an edge case: a ponded reach behind a structure has no normal
    depth, and a profile there is classified H or A instead.
```

## `critical_depth`

```python
def critical_depth(channel: Channel, discharge: float, limit: float=1000.0) -> float
```

```text
Depth of least specific energy [m], where the Froude number is one.

Solves ``Q^2 T / (g A^3) = 1``. Above it the flow is subcritical and
disturbances travel upstream; below it they cannot, which is why a
bridge on a steep reach is not felt by the reach above it.
```

## `froude_number`

```python
def froude_number(channel: Channel, discharge: float, depth: float) -> float
```

```text
Fr = V / sqrt(g A / T), the form that is right for any section.
```

## `specific_energy`

```python
def specific_energy(channel: Channel, discharge: float, depth: float) -> float
```

```text
E = y + V^2 / 2g, measured from the bed [m].
```

## `friction_slope`

```python
def friction_slope(channel: Channel, discharge: float, depth: float) -> float
```

```text
Slope of the energy grade line, from Manning.
```

## `classify_slope`

```python
def classify_slope(channel: Channel, discharge: float, slope: float) -> dict
```

```text
Mild, steep, critical, horizontal or adverse.

The classification is about the channel and the discharge together, not
the bed alone: the same reach is mild in flood and can be steep at low
flow, because critical depth moves with the discharge and normal depth
moves faster.
```

## `profile_type`

```python
def profile_type(depth: float, classification: dict) -> str
```

```text
Name the backwater profile, in Chow's notation.

``M1`` is the one a bridge makes on a mild reach: the flow is deeper
than normal and deeper than critical, and the surface runs back
upstream asymptotically towards normal depth. ``M2`` is a drawdown to a
free overfall. ``S1`` sits behind a structure on a steep reach and is
short, because the flow is supercritical and the disturbance cannot
propagate far.
```

## `BackwaterResult`

```python
class BackwaterResult
    distance: np.ndarray
    depth: np.ndarray
    channel: Channel
    discharge: float
    slope: float
    classification: dict
    profile: str
    notes: list[str] = field(default_factory=list)
```

```text
The outcome of :func:`gvf_profile`.
```

### `BackwaterResult.water_surface` (property)

```python
BackwaterResult.water_surface(self) -> np.ndarray
```

```text
Water level, taking the bed as zero at the control [m].
```

### `BackwaterResult.bed_level` (property)

```python
BackwaterResult.bed_level(self) -> np.ndarray
```

```text
Bed level along the reach, rising upstream [m].
```

### `BackwaterResult.reach` (property)

```python
BackwaterResult.reach(self) -> float
```

```text
How far the profile extends from the control [m].
```

### `BackwaterResult.depth_at` (method)

```python
BackwaterResult.depth_at(self, distance: float) -> float
```

```text
Depth interpolated at one distance from the control [m].
```

## `gvf_profile`

```python
def gvf_profile(channel: Channel, discharge: float, slope: float, control_depth: float, steps: int=200, approach: float=0.99) -> BackwaterResult
```

```text
Gradually varied flow profile by the direct step method.

Integrates

    dx = dE / (S0 - Sf)

away from a control depth, where ``E`` is specific energy and ``Sf``
the friction slope. Exact for a prismatic channel, which is what makes
the direct step the right tool here: the depths are chosen and the
distances computed, rather than the other way round, so the profile
never has to iterate.

The integration stops as the depth approaches normal, because it gets
there only asymptotically and the step length goes to infinity. That
is not a numerical failure, it is the physics: a backwater curve has no
end, so what is quoted as "the extent of backwater" is always a
convention. ``approach`` sets the one used here.

Parameters
----------
control_depth : float
    Depth at the control, which is where the profile starts. A bridge
    or a weir sets this.
approach : float
    Fraction of the way to normal depth at which to stop. 0.99 is the
    usual convention; 0.95 gives a noticeably shorter reach and is also
    defensible, which is the point.

Returns
-------
BackwaterResult
    Distances are measured from the control and are positive going
    upstream for a subcritical profile.
```

## `yarnell_afflux`

```python
def yarnell_afflux(channel: Channel, discharge: float, downstream_depth: float, blockage: float, shape: str='semicircular_nose') -> dict
```

```text
Afflux across a line of bridge piers, Yarnell (1934)::

    H = K (K + 5 Fr^2 - 0.6) (a + 15 a^4) Fr^2 y

where ``a`` is the fraction of the channel area the piers block and
``Fr`` is the downstream Froude number. The fourth power on the
blockage is what makes this bite: doubling the pier area does far more
than double the afflux.

Yarnell's tests were on piers in a rectangular flume at blockages up to
about 0.4, with the flow class unchanged through the bridge. Outside
that, and particularly where the bridge chokes the flow to critical,
the energy or momentum methods in HEC-RAS are the right tools.
```

## `flow_distribution`

```python
def flow_distribution(main: Channel, main_depth: float, slope: float, floodplains: list[tuple[Channel, float]] | None=None) -> dict
```

```text
How the discharge divides between channel and floodplains.

Split by conveyance, which is what actually decides it::

    Q_i / Q = K_i / sum(K)      K = A R^(2/3) / n

This is the number :class:`~pyCoastal.applications.scour.BridgeOpening`
calls ``flow_fraction``, and it is worth computing rather than
assuming. A wooded floodplain has perhaps a third of the channel's
roughness coefficient working against it and a fraction of its
hydraulic radius, so it can be half the width of the section and carry
a tenth of the flow. Guessing it high makes contraction scour look
worse than it is; guessing it low is the mistake that matters.

Parameters
----------
floodplains : list of (Channel, depth)
    Each overbank panel and the depth of flow on it. An empty list
    means the bridge spans the whole waterway and the fraction is one.
```

