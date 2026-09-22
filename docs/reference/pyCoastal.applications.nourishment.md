# `pyCoastal.applications.nourishment`

Source: [`pyCoastal/applications/nourishment.py`](../../pyCoastal/applications/nourishment.py)

Beach nourishment simulator.

A beach fill is a perturbation to an otherwise straight shoreline. Under
small wave angles the one-line model reduces to a diffusion equation, so the
fill spreads alongshore and the placed sand leaves the project area over
time. This module sizes that behaviour: it builds the initial planform from
a design, evolves it with the one-line model in ``pyCoastal.tools.shoreline``,
and reports volume retained, project design life, and a renourishment
schedule.

The linearized solution (Pelnard-Considere, 1956) is provided separately as
``pelnard_considere`` and is used to verify the numerical solver.

Coordinates follow the package convention: x is alongshore, y is the
cross-shore shoreline offset (positive seaward), z is elevation.

## `SECONDS_PER_YEAR`

```python
SECONDS_PER_YEAR = 365.25 * 24 * 3600.0
```

## `cerc_coefficient`

```python
def cerc_coefficient(K: float=0.39, s: float=2.65, gamma_b: float=0.78, g: float=9.81) -> float
```

```text
CERC alongshore transport coefficient in the SI form this model needs.

The CERC (SPM 1984) formula for the immersed-weight transport rate gives a
volumetric flux

    Q = K sqrt(g / gamma_b) Hb^(5/2) sin(2 alpha) / (16 (s - 1))

which is a *solid* sediment volume, excluding voids. That is the form
required here, because ``tools.shoreline.rhs_y_t`` divides by (1 - p)
itself. Supplying a bulk-volume coefficient instead double-counts porosity.

Parameters
----------
K : float
    Dimensionless CERC coefficient for the immersed-weight transport rate.
    0.39 is the SPM value for significant wave height; values near 0.2 are
    commonly back-calculated from field data.
s : float
    Sediment specific gravity [-].
gamma_b : float
    Breaker index Hb/hb [-].
g : float
    Gravitational acceleration [m/s^2].

Returns
-------
float
    Coefficient such that Q [m^3/s per m of beach] = coeff Hb^(5/2) sin(2 alpha).
```

## `KCERC_DEFAULT`

```python
KCERC_DEFAULT = cerc_coefficient()
```

## `WaveClimate`

```python
class WaveClimate
    Hb: float = 1.0
    T: float = 8.0
    alpha0: float = 0.0
    Kcerc: float = KCERC_DEFAULT
```

```text
Wave conditions driving alongshore transport.

Attributes
----------
Hb : float
    Representative breaking wave height [m].
T : float
    Representative wave period [s]. Carried for reporting; the CERC flux
    itself depends on Hb and the breaking angle.
alpha0 : float
    Breaking wave angle relative to the unperturbed shoreline [rad].
    Zero means shore-normal incidence, for which the fill diffuses
    symmetrically without migrating alongshore.
Kcerc : float
    CERC alongshore transport coefficient, in SI units such that the
    solid-volume flux Q is m^3/s. Defaults to ``cerc_coefficient()`` for
    standard sand. Note this is *not* the dimensionless CERC K.
```

## `NourishmentDesign`

```python
class NourishmentDesign
    length: float = 1000.0
    berm_width: float = 30.0
    taper: float = 100.0
    center: float | None = None
    D: float = 8.0
    B: float = 2.0
    porosity: float = 0.4
```

```text
Geometry and sediment properties of a beach fill.

The fill is placed as a berm of width ``berm_width`` (the seaward advance
of the shoreline) over a length ``length``, with linear tapers of length
``taper`` at each end.

Attributes
----------
length : float
    Alongshore length of the full-width section [m].
berm_width : float
    Shoreline advance at placement [m].
taper : float
    Alongshore length of the linear taper at each end [m].
center : float, optional
    Alongshore position of the fill centre [m]. Defaults to the centre
    of the model domain.
D : float
    Depth of closure [m]: the offshore limit of the active profile.
B : float
    Berm height above mean sea level [m].
porosity : float
    Sediment porosity [-].
```

### `NourishmentDesign.active_height` (property)

```python
NourishmentDesign.active_height(self) -> float
```

```text
Vertical extent of the active profile, D + B [m].
```

### `NourishmentDesign.placed_volume` (property)

```python
NourishmentDesign.placed_volume(self) -> float
```

```text
In-situ volume of sand placed [m^3].

Trapezoidal planform (full-width section plus two linear tapers)
multiplied by the active profile height.
```

## `longshore_diffusivity`

```python
def longshore_diffusivity(climate: WaveClimate, design: NourishmentDesign) -> float
```

```text
Alongshore diffusivity of the linearized one-line model [m^2/s].

Linearizing Q = K Hb^(5/2) sin(2 alpha) for small angles gives

    dy/dt = eps d2y/dx2,   eps = 2 K Hb^(5/2) / ((1 - p) (D + B))

This is the same group that sets the explicit stability limit in
``pyCoastal.tools.shoreline.suggest_dt``.
```

## `initial_planform`

```python
def initial_planform(x: np.ndarray, design: NourishmentDesign) -> np.ndarray
```

```text
Shoreline offset y(x) immediately after placement [m].

A flat-topped berm over ``design.length`` with linear tapers of length
``design.taper`` at both ends.
```

## `pelnard_considere`

```python
def pelnard_considere(x: np.ndarray, t: float, design: NourishmentDesign, climate: WaveClimate) -> np.ndarray
```

```text
Analytical planform of a rectangular fill after time ``t`` [s].

Pelnard-Considere (1956) solution of the linearized one-line equation for
an initially rectangular fill of width W and length L:

    y(x,t) = (W/2) [ erf((a - x')/(2 sqrt(eps t)))
                   + erf((a + x')/(2 sqrt(eps t))) ]

with a = L/2 and x' measured from the fill centre. Tapers are not
represented: this is the reference solution used to verify the numerical
solver, not a substitute for it.
```

## `NourishmentResult`

```python
class NourishmentResult
    x: np.ndarray
    times: np.ndarray
    planforms: np.ndarray
    volume_retained: np.ndarray
    placed_volume: float
    design: NourishmentDesign
    climate: WaveClimate
```

```text
Output of a nourishment simulation.

Attributes
----------
x : np.ndarray
    Alongshore coordinate [m].
times : np.ndarray
    Output times [s].
planforms : np.ndarray
    Shoreline offset at each output time, shape (n_times, n_x) [m].
volume_retained : np.ndarray
    Volume remaining inside the project footprint at each time [m^3].
placed_volume : float
    Volume placed at construction [m^3].
```

### `NourishmentResult.times_years` (property)

```python
NourishmentResult.times_years(self) -> np.ndarray
```

### `NourishmentResult.retained_fraction` (property)

```python
NourishmentResult.retained_fraction(self) -> np.ndarray
```

```text
Fraction of the placed volume still in the project area [-].
```

### `NourishmentResult.berm_width` (property)

```python
NourishmentResult.berm_width(self) -> np.ndarray
```

```text
Shoreline offset at the fill centre through time [m].
```

### `NourishmentResult.design_life` (method)

```python
NourishmentResult.design_life(self, threshold: float=0.5) -> float
```

```text
Time until the retained fraction first falls below ``threshold`` [s].

Linearly interpolated between output times. Returns ``inf`` if the
threshold is never crossed within the simulated period.
```

## `simulate_nourishment`

```python
def simulate_nourishment(design: NourishmentDesign, climate: WaveClimate, duration: float, domain_length: float | None=None, dx: float=10.0, n_outputs: int=25, bc: str='fixed_ends', cfl: float=0.9) -> NourishmentResult
```

```text
Evolve a beach fill with the one-line model.

Parameters
----------
design, climate
    Fill geometry and driving wave conditions.
duration : float
    Simulated period [s]. Use ``years * SECONDS_PER_YEAR``.
domain_length : float, optional
    Alongshore extent of the model domain [m]. Defaults to five times the
    total fill footprint, keeping the fixed-end boundaries far enough away
    not to influence the spreading.
dx : float
    Alongshore grid spacing [m].
n_outputs : int
    Number of stored output times, including t = 0.
bc : {"fixed_ends", "zero_slope"}
    Boundary treatment, passed to ``tools.shoreline.apply_bcs``.
cfl : float
    Safety factor on the diffusive stability limit.

Returns
-------
NourishmentResult
```

## `renourishment_schedule`

```python
def renourishment_schedule(design: NourishmentDesign, climate: WaveClimate, horizon: float, threshold: float=0.5, **kwargs) -> dict
```

```text
Plan repeated renourishment over a planning horizon.

Each cycle restores the fill to its design width, so under constant wave
forcing the cycles are of equal length. Returns the interval, the number
of renourishments needed within ``horizon``, the placement times, and the
total volume required.

Parameters
----------
horizon : float
    Planning horizon [s].
threshold : float
    Retained-volume fraction that triggers renourishment.
**kwargs
    Passed through to ``simulate_nourishment``.
```

## `phi_size`

```python
def phi_size(d50: float) -> float
```

```text
Grain size on the phi scale, phi = -log2(d in mm).

Sediment statistics are done in phi because the distributions are close
to normal there and are anything but in millimetres. Note the sign:
coarser sand is a *smaller* phi.
```

## `size_from_phi`

```python
def size_from_phi(phi: float) -> float
```

```text
Grain size in metres from a phi value.
```

## `dean_scale`

```python
def dean_scale(material, viscosity: float=NU) -> float
```

```text
Profile scale parameter A [m^(1/3)] from the fall velocity.

    A = 0.067 w^0.44,  w in cm/s

Kriebel, Kraus and Larson (1991). Tying A to the fall velocity rather
than reading it off a grain-size table means it comes from the same
Soulsby relation the rest of the package uses, so a sediment cannot have
one settling velocity for scour and another for its profile.

Checks against Dean's own table: fine sand at 0.19 mm gives 0.094 and
medium sand at 0.38 mm gives 0.141, against tabulated values of about
0.10 and 0.14.
```

## `equilibrium_profile`

```python
def equilibrium_profile(A: float, y)
```

```text
Depth h = A y^(2/3) at distance y offshore [m].
```

## `profile_width`

```python
def profile_width(A: float, depth: float) -> float
```

```text
Distance offshore to a given depth on an equilibrium profile [m].
```

## `fill_volume_for_advance`

```python
def fill_volume_for_advance(A_native: float, A_fill: float, advance: float, berm_height: float, closure_depth: float) -> dict
```

```text
Fill volume per metre of beach for a given shoreline advance.

The integration runs over *depth*, not distance, because the active
profile is bounded by the closure contour and not by a line at some
fixed chainage. At each depth the fill has pushed the profile seaward by

    offset(h) = advance + (h / A_fill)^(3/2) - (h / A_native)^(3/2)

and the volume is that offset integrated from the waterline down to
closure, plus the dry berm::

    V = B a + a h_L + 0.4 h_L^(5/2) (A_f^-3/2 - A_n^-3/2)

where h_L is the closure depth, or the depth at which the two profiles
meet if the fill is coarse enough to intersect first.

Returns
-------
dict
    The ``volume`` [m3 per m], the depth and distance at which the
    profiles meet, and whether they meet at all.

Notes
-----
For equal grain sizes every term but the first two vanishes and this is
exactly V = (B + h*) a, the formula everyone starts from. That is not an
approximation here, it is the same expression with A_fill = A_native.
```

## `critical_volume`

```python
def critical_volume(A_native: float, A_fill: float, berm_height: float, closure_depth: float) -> float
```

```text
Volume per metre below which a fine fill gives no dry beach at all.

Fill finer than the native sand lies flatter. The first cubic metres go
into flattening the underwater profile, and only once that is paid for
does the waterline move. Below this volume the placement is an offshore
terrace, which is a legitimate design but not the one that was sold.

Zero for fill as coarse as the native sand or coarser.
```

## `shoreline_advance`

```python
def shoreline_advance(A_native: float, A_fill: float, volume: float, berm_height: float, closure_depth: float, tolerance: float=0.0001) -> dict
```

```text
Dry beach gained for a given fill volume, and how the profile behaves.

Parameters
----------
volume : float
    Placed volume per metre of beach [m3/m].

Returns
-------
dict
    ``advance`` [m], the profile ``kind`` (intersecting, non-intersecting
    or submerged), and the critical volume where that matters.

Notes
-----
Solved by bisection on the volume, which is monotonic in the advance.
An analytic inverse exists for each case separately; one solver that
cannot pick the wrong branch is worth more than three formulae.
```

## `profile_overfill_factor`

```python
def profile_overfill_factor(native, borrow, berm_height: float, closure_depth: float, advance: float=30.0) -> dict
```

```text
How much more borrow material is needed for the same dry beach.

The ratio of the volume needed using the borrow material to the volume
needed using sand identical to the native, for the same shoreline
advance.

Returns
-------
dict
    The ``factor``, both volumes, and the two profile scales.

Notes
-----
This is a profile-based factor and is not the same quantity as James's
(1975) textural overfill ratio R_A, which comes off a chart built from
the phi mean and sorting of both distributions and accounts for the
fines winnowing out. Both answer "how much extra do I buy"; they do it
from different evidence, and neither replaces the other. Use
:func:`grain_compatibility` for the textural side.
```

## `grain_compatibility`

```python
def grain_compatibility(native, borrow) -> dict
```

```text
Compare a borrow source with the native beach, on the phi scale.

Returns
-------
dict
    ``delta`` = (phi_borrow - phi_native) / sigma_native, the mean shift
    in native standard deviations, negative when the borrow is coarser;
    ``sorting_ratio`` = sigma_borrow / sigma_native; and a ``verdict``.

Notes
-----
The verdict follows the rule every nourishment text states and no chart
is needed for: borrow that is coarser and no more poorly sorted than the
native sand is well suited, and borrow that is finer is not, in
proportion to how much finer. James's (1975) chart puts numbers on the
second case; this says which case you are in and how far.
```

