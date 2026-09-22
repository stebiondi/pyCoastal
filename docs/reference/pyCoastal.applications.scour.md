# `pyCoastal.applications.scour`

Source: [`pyCoastal/applications/scour.py`](../../pyCoastal/applications/scour.py)

Scour at a pier in an estuary: waves, tide and river current together.

The hard part of estuarine scour is not any single relation. It is that the
three drivers do not peak together and do not even point the same way. The
tide reverses twice a day, the river does not, the waves come and go with
the wind, and the water depth changes under all of it. A scour calculation
done at "the design current" and "the design wave" without asking whether
they can occur at the same moment is either optimistic or absurd, and it is
usually not obvious which.

So this module works a tidal cycle rather than a load case. It evaluates
the combined scour at every phase and reports the envelope, which phase
governs, and by how much. In a river-fed estuary that is nearly always peak
ebb, where the tidal current and the river run the same way and the water
is shallow, but it is worth seeing rather than assuming.

The pier is a stem on a base, because that is what piers are, and the base
is where the interesting failure lives. A buried pile cap does nothing
until the scour hole reaches it. Then it is exposed, it is wider than the
stem, and the scour deepens because of it, which exposes more of it. That
feedback is iterated here rather than ignored, and a design that is stable
against it looks very different from one that is not.

What is modelled and what is not
--------------------------------
Modelled: combined wave and current scour, non-uniform pier geometry
through an equivalent diameter, progressive base exposure, flow
misalignment on the reversing tide, depth limitation, and the time scale of
scour development against the tidal half cycle.

Not modelled: a pile cap resting at bed level can behave as a collar and
*reduce* scour by deflecting the downflow. That is real and documented, and
crediting it here would be unconservative, so it is not credited. Cohesive
beds are refused rather than guessed at. Scour from a contracted section or
from the estuary's own channel migration is a different problem and a
larger one.

References
----------
Sumer, B.M., Fredsoe, J. and Christiansen, N. (1992). Scour around
vertical pile in waves. Journal of Waterway, Port, Coastal and Ocean
Engineering, 118(1), 15-31.

Sumer, B.M., Christiansen, N. and Fredsoe, J. (1992). Time scale of scour
around a vertical pile. Proc. 2nd Int. Offshore and Polar Engineering
Conference, 308-315.

Sumer, B.M. and Fredsoe, J. (2001). Scour around pile in combined waves
and current. Journal of Hydraulic Engineering, 127(5), 403-411.

Sumer, B.M. and Fredsoe, J. (2002). The Mechanics of Scour in the Marine
Environment. World Scientific.

Breusers, H.N.C., Nicollet, G. and Shen, H.W. (1977). Local scour around
cylindrical piers. Journal of Hydraulic Research, 15(3), 211-252.

Richardson, E.V. and Davis, S.R. (2001). Evaluating scour at bridges.
HEC-18, 4th ed. Federal Highway Administration.

Lagasse, P.F. et al. (2009). Bridge scour and stream instability
countermeasures. HEC-23, 3rd ed. Federal Highway Administration.

## `G`

```python
G = 9.81
```

## `M2_PERIOD`

```python
M2_PERIOD = 12.4206012 * 3600.0
```

## `SHAPE_FACTOR`

```python
SHAPE_FACTOR = {'circular': 1.0, 'round_nose': 1.0, 'square': 1.1, 'rectangular': 1.1, 'sharp_nose': 0.9, 'group': 1.0}
```

## `shape_factor`

```python
def shape_factor(shape: str) -> float
```

```text
HEC-18 nose shape factor K1, for the pier plan form.
```

## `alignment_factor`

```python
def alignment_factor(width: float, length: float, skew_degrees: float) -> float
```

```text
HEC-18 flow alignment factor K2::

    K2 = (cos theta + (L/a) sin theta) ** 0.65

A long base presents its width to the flow when aligned and most of its
length when it is not, so skew matters enormously for anything that is
not square in plan. This is the factor that makes a tidal estuary
awkward: a base set square to the ebb is skewed to the flood, and a
pier aligned to neither is skewed to both.

``L/a`` is capped at 12, past which HEC-18 stops claiming accuracy.
```

## `Pier`

```python
class Pier
    diameter: float = 2.0
    shape: str = 'circular'
    length: float | None = None
```

```text
The column itself, above the base.

Attributes
----------
diameter : float
    Stem width across the flow [m].
shape : str
    Plan form, keying :data:`SHAPE_FACTOR`.
length : float, optional
    Stem length along the flow [m]. Defaults to the diameter, which is
    right for a circular pier and wrong for a blade.
```

## `PierBase`

```python
class PierBase
    width: float = 6.0
    length: float = 6.0
    height: float = 2.0
    top_level: float = -1.0
    skew: float = 0.0
```

```text
The footing, pile cap or caisson the stem stands on.

Attributes
----------
width : float
    Across the flow [m].
length : float
    Along the flow [m].
height : float
    Thickness of the base [m].
top_level : float
    Level of the top of the base relative to the *initial* bed.
    Negative means buried, which is the usual design intent, and is
    also the case worth watching: a base buried half a metre is
    invisible until the scour hole finds it.
skew : float
    Angle between the base's long axis and the flow [deg]. In a
    reversing tidal flow this is the ebb alignment; the flood value is
    taken as the supplement.
```

### `PierBase.bottom_level` (property)

```python
PierBase.bottom_level(self) -> float
```

```text
Level of the underside of the base, relative to the initial bed.
```

### `PierBase.buried` (property)

```python
PierBase.buried(self) -> bool
```

```text
Whether the base starts below the bed.
```

## `equivalent_diameter`

```python
def equivalent_diameter(pier: Pier, base: PierBase | None, depth: float, scour: float=0.0, skew_degrees: float | None=None) -> dict
```

```text
Effective obstacle width seen by the flow [m].

A pier of two widths is reduced to one by weighting each element over
the depth of flow it occupies::

    D_e = [D_base h_base + D_stem (h - h_base)] / h

where ``h_base`` is how much of the base stands proud of the *scoured*
bed. That last word is the whole point. A base buried below the initial
bed contributes nothing at first, and contributes more and more as the
hole deepens, so ``D_e`` is a function of the scour it is being used to
predict. :func:`equilibrium_scour` iterates it.

Both elements also carry their own shape and alignment factors, so a
long rectangular cap skewed to the flow is correctly worse than a
round one.

Parameters
----------
scour : float
    Scour depth already developed [m], measured down from the initial
    bed. Sets how much of a buried base is exposed.

Returns
-------
dict
    ``D_e`` plus the exposed base height and the factors used.
```

## `keulegan_carpenter`

```python
def keulegan_carpenter(Um: float, period: float, diameter: float) -> float
```

```text
KC = Um T / D, on the *near-bed* orbital velocity.

Scour is a bed process, so the velocity that matters is the one at the
bed, not the one at the surface. This is the convention Sumer and
Fredsoe's relations are written in, and using a surface orbital
velocity here would overstate KC badly in deep water.
```

## `velocity_ratio`

```python
def velocity_ratio(current: float, orbital: float) -> float
```

```text
Ucw = Uc / (Uc + Um), the current's share of the near-bed flow.

Zero is a pure wave case, one is a pure current. It is the parameter
Sumer and Fredsoe's combined relation turns on, and a surprising amount
of estuarine scour sits near 0.7 to 0.9, where the current dominates but
the waves still matter.
```

## `scour_ratio_combined`

```python
def scour_ratio_combined(KC: float, Ucw: float, current_ratio: float=1.3, current_live_bed: bool | None=None) -> dict
```

```text
S/D in combined waves and current, Sumer and Fredsoe (2001)::

    S/D = 1.3 {1 - exp[-A (KC - B)]}     for KC >= B
    A   = 0.03 + (3/4) Ucw^2.6
    B   = 6 exp(-4.7 Ucw)

The two limits are worth checking, because they are what make the
relation trustworthy across the middle:

- ``Ucw = 0`` gives A = 0.03 and B = 6, which is exactly the waves-only
  relation of Sumer, Fredsoe and Christiansen (1992), including the
  threshold at KC = 6 below which the horseshoe vortex does not form.
- ``Ucw = 1`` gives B = 0.055, so the threshold vanishes, and S/D tends
  to 1.3, the steady-current value, **as KC grows**.

The steady-current floor
------------------------
That last clause is the trap, and ``current_live_bed`` is the answer to
it. KC is built on the *wave* orbital velocity, so a strong current
under small waves has a high Ucw and a low KC at the same time, and the
formula then returns almost no scour. Read literally it says a pier in
a 1.5 m/s current scours less than the same pier in still water with a
ripple on it, which is nonsense.

The resolution is that a steady current is the ``KC -> infinity`` limit
of an oscillatory flow, not the ``KC -> 0`` one. A current that can
move the bed on its own digs its own horseshoe vortex whatever the
waves are doing, and adding waves to a current does not abolish it. So
when the approach current alone is live-bed, the ratio is floored at
the steady-current value.

This floor is an addition to the published relation, not part of it.
It is flagged in the result as ``current_governs`` so it is never
silently applied.

Parameters
----------
current_live_bed : bool, optional
    Whether the steady current alone exceeds the threshold of motion.
    ``None`` disables the floor and gives the bare published relation.

Returns
-------
dict
    ``ratio`` S/D, the coefficients, and which branch governed.
```

## `depth_limitation`

```python
def depth_limitation(depth: float, diameter: float) -> float
```

```text
Shallow-water reduction on the scour depth, ``tanh(h/D)``.

A scour hole needs room to form. Where the water is shallow compared
with the obstacle the horseshoe vortex is squeezed and the hole is
smaller, which is the Breusers, Nicollet and Shen (1977) depth
limitation. Above about ``h/D = 3`` it is worth nothing (tanh 3 =
0.995) and can be ignored; below ``h/D = 1`` it takes a quarter off.

It matters here because a wide caisson base in an estuary at low water
can easily sit at ``h/D`` well under one, which is exactly where the
unlimited relations start promising holes deeper than the water.
```

## `current_shields`

```python
def current_shields(material, velocity: float, depth: float, roughness: float | None=None) -> dict
```

```text
Skin-friction Shields parameter under a depth-averaged current.

Uses a logarithmic velocity profile to get the bed shear stress,

    u* = U kappa / ln(11 h / k_s)

with ``k_s = 2.5 d50`` unless given, then ``theta = u*^2 / (g (s-1) d50)``.
The result drives the scour time scale and says whether the bed is live
or in clear water, which decides how long the hole takes to form even
though it barely changes how deep it ends up.
```

## `scour_time_scale`

```python
def scour_time_scale(material, diameter: float, depth: float, theta: float) -> dict
```

```text
How long the scour hole takes to form [s].

Sumer, Christiansen and Fredsoe (1992) give a dimensionless time scale

    T* = (1/2000) (h/D) theta^-2.2

which is made dimensional by

    T = T* D^2 / sqrt(g (s-1) d50^3)

and the hole then develops as ``S(t) = S_eq [1 - exp(-t/T)]``.

In a tidal estuary this is not a detail. The time scale for a pier a
couple of metres across is typically most of a day, while the tide
reverses every six hours, so the hole never reaches the equilibrium
depth that a steady-current calculation hands you. Ignoring that is
conservative for the pier and expensive for the client; relying on it
without checking the spring tide is neither.

Raises
------
ValueError
    If the bed is not live. The relation is a live-bed result and
    diverges as theta goes to zero.
```

## `scour_development`

```python
def scour_development(equilibrium: float, elapsed: float, time_scale: float) -> float
```

```text
Scour depth after ``elapsed`` seconds [m].

    S(t) = S_eq [1 - exp(-t / T)]

The exponential approach is the one universally observed, whatever
disagreement there is about the time scale itself.
```

## `EstuaryConditions`

```python
class EstuaryConditions
    mean_depth: float = 10.0
    tidal_amplitude: float = 2.0
    tidal_current: float = 1.0
    river_current: float = 0.3
    Hs: float = 1.0
    Tp: float = 5.0
    tidal_period: float = M2_PERIOD
    current_phase: float = 90.0
    bed: str = 'medium_sand'
    wave_follows_tide: bool = False
```

```text
Tide, river and waves at the pier.

Sign convention: positive is ebb, seaward. The river current is always
positive, the tidal current changes sign, and the two therefore add on
the ebb and oppose on the flood. That asymmetry is why estuarine scour
is an ebb problem far more often than a flood one.

Attributes
----------
mean_depth : float
    Water depth at mean tide level [m].
tidal_amplitude : float
    Half the tidal range [m].
tidal_current : float
    Amplitude of the depth-averaged tidal current [m/s].
river_current : float
    Depth-averaged river current [m/s], steady and seaward.
Hs, Tp : float
    Significant wave height and peak period at the pier [m, s].
tidal_period : float
    Defaults to M2.
current_phase : float
    Phase lead of the current over the elevation [deg]. 90 is a
    standing wave, where slack water coincides with high and low water;
    0 is a progressive wave, where the strongest currents do. Real
    estuaries sit between, and the answer moves with it, so it is an
    input rather than a buried assumption.
bed : str
    Sediment key.
wave_follows_tide : bool
    Whether the wave height is taken to scale with the water depth,
    as it does for a depth-limited estuary chop, or to stay constant.
```

### `EstuaryConditions.material` (property)

```python
EstuaryConditions.material(self)
```

### `EstuaryConditions.peak_ebb_current` (property)

```python
EstuaryConditions.peak_ebb_current(self) -> float
```

```text
The worst steady current: tide and river running together.
```

### `EstuaryConditions.peak_flood_current` (property)

```python
EstuaryConditions.peak_flood_current(self) -> float
```

```text
Tide against river, so the smaller of the two peaks.
```

## `tidal_state`

```python
def tidal_state(conditions: EstuaryConditions, phase_degrees: float) -> dict
```

```text
Depth, current and wave orbital velocity at one phase of the tide.

Returns
-------
dict
    ``depth``, ``elevation``, ``current`` (signed, positive ebb),
    ``Um`` near-bed orbital velocity, and the wave height used.
```

## `equilibrium_scour`

```python
def equilibrium_scour(pier: Pier, base: PierBase | None, depth: float, current: float, Um: float, period: float, skew_degrees: float | None=None, limit_by_depth: bool=True, bed=None, iterations: int=80, tolerance: float=1e-09) -> dict
```

```text
Equilibrium scour depth for one steady set of conditions [m].

Solves the feedback between scour depth and effective diameter. The
scour depends on the obstacle width; the obstacle width depends on how
much of the base the scour has exposed; so the two are found together
by fixed-point iteration rather than by evaluating the relation once at
the initial geometry.

Where there is no base, or the base is deep enough never to be reached,
this converges on the first pass and costs nothing.

Pass ``bed`` to enable the steady-current floor described in
:func:`scour_ratio_combined`. Without it the bare published relation is
used, which understates a current-dominated case badly.

Returns
-------
dict
    ``depth`` of scour, the converged ``D_e``, the geometry at
    convergence, and whether the iteration settled.
```

## `riprap_size`

```python
def riprap_size(velocity: float, material_density: float=2650.0, shape: str='round_nose') -> dict
```

```text
Median stone size for scour protection at a pier [m].

HEC-23 design guideline 12::

    d50 = 0.692 (K V)^2 / (2 g (s - 1))

with K = 1.5 for a round-nosed pier and 1.7 for a rectangular one. The
factor accounts for the flow accelerating around the pier: the stone
has to survive the local velocity, not the approach velocity, and the
difference is a factor of two in speed and four in stone weight.
```

## `scour_protection`

```python
def scour_protection(pier: Pier, base: PierBase | None, velocity: float, scour: float, material_density: float=2650.0) -> dict
```

```text
A rock apron sized to the pier and the flow.

Extent follows HEC-23: the apron reaches two obstacle widths from the
face, and is at least three stones thick. The width it is measured from
is the base where there is one, because that is what the flow sees once
the hole has formed.

The apron does not remove the scour, it relocates it. An edge scour
hole forms at the perimeter instead, and a rigid apron that cannot
settle into it will undermine and unravel from the edge inwards. That
is why the apron is specified as a falling apron with a launch
allowance rather than as a slab.
```

## `PierScourDesign`

```python
class PierScourDesign
    pier: Pier
    base: PierBase | None
    conditions: EstuaryConditions
    states: list[dict]
    governing: dict
    equilibrium: float
    tidal_limited: float
    time_scale: float
    protection: dict
    notes: list[str] = field(default_factory=list)
```

```text
The outcome of :func:`design_pier_scour`.
```

### `PierScourDesign.base_exposed` (property)

```python
PierScourDesign.base_exposed(self) -> bool
```

```text
Whether the governing scour hole reaches the base.
```

### `PierScourDesign.undermined` (property)

```python
PierScourDesign.undermined(self) -> bool
```

```text
Whether the hole reaches below the underside of the base.
```

### `PierScourDesign.envelope` (method)

```python
PierScourDesign.envelope(self) -> np.ndarray
```

```text
Scour depth at each phase of the tide [m].
```

### `PierScourDesign.phases` (method)

```python
PierScourDesign.phases(self) -> np.ndarray
```

## `design_pier_scour`

```python
def design_pier_scour(pier: Pier, conditions: EstuaryConditions, base: PierBase | None=None, samples: int=73, limit_by_depth: bool=True, protection_factor: float=1.0) -> PierScourDesign
```

```text
Work a tidal cycle and report the scour envelope at a pier.

Evaluates the combined wave and current scour at every phase of the
tide, with the water depth, the current and the wave orbital velocity
all moving together, and reports the deepest.

Two depths come out of it and they answer different questions.
``equilibrium`` is what the governing condition would eventually
produce if it were held indefinitely, and is the right number for
sizing scour protection and for the long-term foundation check.
``tidal_limited`` is what that condition can actually achieve in the
half cycle it lasts, and is the right number for asking what happens
during a single spring tide.

Which of the two is smaller is not obvious in advance, which is why it
is computed rather than assumed. A vigorously live bed cuts its hole in
an hour or two and reaches equilibrium well inside one half cycle; a
barely mobile bed under a big pier takes days and never gets close.
Either way ``equilibrium`` is the number to design protection on, since
the hole does not refill on the reverse flow and successive tides work
it deeper.

Parameters
----------
samples : int
    Phases to evaluate over the full cycle.
protection_factor : float
    Multiplier on the equilibrium scour used to size the apron launch
    allowance. 1.0 sizes for the predicted hole; a value above one buys
    margin against a relation whose scatter is substantial.

Returns
-------
PierScourDesign
```

## `ABUTMENT_SHAPE`

```python
ABUTMENT_SHAPE = {'vertical': 1.0, 'wing_wall': 0.82, 'spill_through': 0.55}
```

## `KU_CLEAR_WATER`

```python
KU_CLEAR_WATER = 0.025
```

## `KU_CRITICAL`

```python
KU_CRITICAL = 6.19
```

## `abutment_shape_factor`

```python
def abutment_shape_factor(shape: str) -> float
```

```text
HEC-18 abutment shape factor K1.
```

## `BridgeOpening`

```python
class BridgeOpening
    approach_width: float = 120.0
    opening_width: float = 70.0
    pier_blockage: float = 0.0
    abutment_length: float = 25.0
    abutment_shape: str = 'spill_through'
    abutment_skew: float = 90.0
    slope: float = 0.0005
    flow_fraction: float = 1.0
    abutment_depth_fraction: float = 0.4
```

```text
The waterway, and the gap the bridge leaves in it.

Contraction scour is a property of the opening rather than of any
structure in it: squeeze the same discharge through less width and the
bed has to drop until the section can carry it again. So the geometry
that matters is the width upstream against the width left between the
abutments, less whatever the piers themselves occupy.

Attributes
----------
approach_width : float
    Bottom width of the channel upstream, W1 [m].
opening_width : float
    Gross width between the abutment faces, W2 [m].
pier_blockage : float
    Total width of piers standing in the opening [m]. Subtracted from
    the gross width, because the flow does not use it.
abutment_length : float
    Length of the embankment projected normal to the flow, L' [m], at
    one end. This is what the abutment blocks, not how long the
    structure is.
abutment_shape : str
    Keys :data:`ABUTMENT_SHAPE`. Spill-through is the usual highway
    form and the most forgiving; a vertical wall is nearly twice as
    bad.
abutment_skew : float
    Angle of the embankment to the flow [deg]. 90 is square on; less
    than 90 points downstream, more points upstream.
slope : float
    Energy grade line slope of the approach [-]. Only ever used to
    classify the mode of transport, which moves the answer by a few
    per cent; see :func:`contraction_scour`.
flow_fraction : float
    Fraction of the total discharge that goes through the opening,
    Q2/Q1. One where the bridge spans the whole waterway, less where
    flow stays out on a floodplain.
abutment_depth_fraction : float
    Flow depth at the abutment as a fraction of the approach channel
    depth. Froehlich's ``ya`` is the depth where the embankment
    actually sits, out on the bank or the floodplain, and not the
    depth in the middle of the channel. It matters more than it looks:
    the equation carries a ``+ ya`` term, so feeding it a mid-channel
    depth in a deep estuary returns a hole deeper than the water.
    Set it from the surveyed cross-section. The default assumes the
    abutment stands in a little under half the channel depth.
```

### `BridgeOpening.net_opening` (property)

```python
BridgeOpening.net_opening(self) -> float
```

```text
Width actually available to the flow, W2 [m].
```

### `BridgeOpening.contraction_ratio` (property)

```python
BridgeOpening.contraction_ratio(self) -> float
```

```text
W1 / W2. One means no contraction; more means a squeeze.
```

### `BridgeOpening.contracted` (property)

```python
BridgeOpening.contracted(self) -> bool
```

## `critical_velocity`

```python
def critical_velocity(bed, depth: float) -> float
```

```text
Velocity at which the bed starts to move [m/s].

HEC-18 equation 6.1::

    Vc = 6.19 y^(1/6) D50^(1/3)      (SI)

This is the switch between the two contraction scour modes, and it is
a real switch rather than a smooth transition: below it the approach
delivers no sediment to the opening and the bed there scours until the
flow can no longer move it, above it the opening is fed from upstream
and reaches a balance instead.
```

## `transport_exponent`

```python
def transport_exponent(bed, depth: float, slope: float) -> dict
```

```text
Laursen's exponent k1, and the mode of transport behind it.

The shear velocity against the fall velocity says whether the sediment
travels along the bed or up in the water column, and Laursen's
live-bed relation carries a different exponent for each::

    V*/w < 0.50   k1 = 0.59   mostly contact load
    0.50 to 2.0   k1 = 0.64   some suspended
    V*/w > 2.0    k1 = 0.69   mostly suspended

The spread is worth keeping in perspective. k1 is an exponent on the
width ratio, so across the whole range it moves the scoured depth of a
two-to-one contraction by about seven per cent. It is not where the
uncertainty in a contraction scour estimate lives.
```

## `contraction_scour`

```python
def contraction_scour(opening: BridgeOpening, depth: float, velocity: float, bed, opening_depth: float | None=None, regime: str | None=None) -> dict
```

```text
Bed lowering across the whole opening [m].

Two modes, and which one applies is decided by whether the approach
flow is already carrying bed material.

**Live bed**, Laursen (1960), HEC-18 equation 6.2::

    y2 / y1 = (Q2/Q1)^(6/7) (W1/W2)^k1

The opening is fed from upstream, so it scours only until the enlarged
section carries the sediment that arrives. The answer depends on the
width ratio and almost nothing else.

**Clear water**, HEC-18 equation 6.4::

    y2 = [ 0.025 Q2^2 / (Dm^(2/3) W2^2) ]^(3/7)

Nothing arrives from upstream, so the opening scours until the flow in
it can no longer move the bed. Deeper, slower, and the mode that
governs a bridge on a coarse bed or in a slack tidal reach.

Parameters
----------
depth, velocity : float
    Approach flow, upstream of the contraction.
opening_depth : float, optional
    Existing depth in the opening before scour, y0. Defaults to the
    approach depth, which assumes a level bed through the bridge.
regime : str, optional
    Force ``"live"`` or ``"clear"``. Left alone, the critical velocity
    decides.

    The two modes are separate relations fitted to separate data, and
    they do not meet at the threshold: the predicted depth steps as the
    bed comes alive. Forcing both and comparing them across the switch
    is the honest way to see how big that step is for a given case
    before quoting a number from either side of it.

Returns
-------
dict
    ``depth`` of scour, the scoured flow depth ``y2``, the regime, and
    the numbers behind it.
```

## `abutment_scour`

```python
def abutment_scour(opening: BridgeOpening, depth: float, velocity: float, method: str | None=None, abutment_depth: float | None=None) -> dict
```

```text
Local scour at one abutment [m].

Two equations, chosen by how far the embankment reaches into the flow
compared with the depth.

**Froehlich (1989)**, for a short abutment, ``L'/y < 25``::

    ys / y = 2.27 K1 K2 (L'/y)^0.43 Fr^0.61 + 1

**HIRE**, for a long one::

    ys / y = 4 Fr^0.33 (K1 / 0.55) K2

Notes
-----
That trailing ``+ 1`` in Froehlich is not physics. HEC-18 added it as a
factor of safety, and it has the consequence that the equation can
never return less than one flow depth of scour, however short the
abutment or however slow the water. A spill-through abutment barely
projecting into a sluggish estuary will still be handed a metre of
scour for every metre of depth. It is reported here as
``safety_margin`` so the conservatism is visible rather than baked
silently into a foundation level.

HEC-18 replaced both of these with the NCHRP 24-20 amplification
approach in its fifth edition. These are the fourth-edition relations,
which is the edition the pier scour in this module also comes from, and
they remain the ones most practitioners will recognise.

Parameters
----------
depth : float
    Approach depth in the channel [m].
abutment_depth : float, optional
    Flow depth where the abutment actually stands [m]. Defaults to
    ``depth`` reduced by the opening's
    :attr:`~BridgeOpening.abutment_depth_fraction`, because an
    abutment sits on the bank and not in the channel. Passing the
    channel depth here is the single easiest way to get an absurd
    answer out of Froehlich.
```

## `bridge_scour_state`

```python
def bridge_scour_state(opening: BridgeOpening, depth: float, velocity: float, bed, pier: 'Pier | None'=None, base: 'PierBase | None'=None, Um: float=0.0, period: float=6.0, skew_degrees: float | None=None, limit_by_depth: bool=True) -> dict
```

```text
All three scour components for one steady set of approach conditions.

The components are computed in the order the water meets them, because
each one changes the flow the next one sees:

1. **Contraction** first, from the *approach* depth and velocity. It
   lowers the bed across the opening and so deepens the section.
2. **Local scour** second, from the flow *in the opening*. That flow is
   faster than the approach, because the same discharge is going
   through less width, and deeper, because the contraction has already
   scoured it. Using approach conditions here is the classic way to
   understate a pier.
3. **Abutment** scour alongside, from the approach flow it turns.

They are then added only where they coexist. A pier in midstream gets
contraction plus its own hole; an abutment gets contraction plus its
own. Adding all three at one point double-counts, and is a reliable
way to arrive at a foundation depth nobody can build.

Returns
-------
dict
    ``contraction``, ``pier``, ``abutment``, the flow in the opening,
    and the two totals.
```

## `BridgeScourDesign`

```python
class BridgeScourDesign
    opening: BridgeOpening
    conditions: EstuaryConditions
    pier: 'Pier | None'
    base: 'PierBase | None'
    states: list[dict]
    governing: dict
    contraction: float
    pier_local: float
    abutment: float
    total_at_pier: float
    total_at_abutment: float
    protection: dict
    notes: list[str] = field(default_factory=list)
```

```text
The outcome of :func:`design_bridge_scour`.
```

### `BridgeScourDesign.total` (property)

```python
BridgeScourDesign.total(self) -> float
```

```text
The deepest total at any location and any phase [m].
```

### `BridgeScourDesign.governing_location` (property)

```python
BridgeScourDesign.governing_location(self) -> str
```

### `BridgeScourDesign.phases` (method)

```python
BridgeScourDesign.phases(self) -> np.ndarray
```

### `BridgeScourDesign.component` (method)

```python
BridgeScourDesign.component(self, name: str) -> np.ndarray
```

```text
Envelope of one component through the cycle [m].
```

## `design_bridge_scour`

```python
def design_bridge_scour(opening: BridgeOpening, conditions: EstuaryConditions, pier: 'Pier | None'=None, base: 'PierBase | None'=None, samples: int=73, limit_by_depth: bool=True, protection_factor: float=1.0) -> BridgeScourDesign
```

```text
Total scour at a crossing, worked over the tidal cycle.

The same sweep as :func:`design_pier_scour`, carrying all three HEC-18
components rather than one. Each is enveloped over the cycle, and the
envelopes are reported separately as well as combined, because they do
not all peak at the same phase and a designer needs to see which one is
driving the number.

Returns
-------
BridgeScourDesign
```

