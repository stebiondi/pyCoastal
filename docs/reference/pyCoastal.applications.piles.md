# `pyCoastal.applications.piles`

Source: [`pyCoastal/applications/piles.py`](../../pyCoastal/applications/piles.py)

Wave loads on slender piles: Morison forces, shear, moment and scour.

The load on a pile is not one number. It is a distribution up the pile that
changes through the wave cycle, and the two things a designer needs from it
(the base shear and the overturning moment at the mudline) peak at different
phases. This module computes the distribution, integrates it, and sweeps the
phase, rather than evaluating a formula at the crest and hoping.

The Morison equation splits the load on a slender member into a drag term,
in phase with the velocity, and an inertia term, in phase with the
acceleration::

    f(z) = 0.5 rho Cd D u|u|  +  rho Cm (pi D^2 / 4) du/dt

Slender means the member is small enough not to change the wave that is
loading it, conventionally D / L below about 0.2. Above that the wave
diffracts around the member and the Morison equation no longer applies; the
functions here say so rather than returning a number.

Sources
-------
Morison, J. R., O'Brien, M. P., Johnson, J. W. and Schaaf, S. A. (1950),
    "The force exerted by surface waves on piles".

Sarpkaya, T. (2010), Wave Forces on Offshore Structures. Drag and inertia
    coefficients, and their dependence on Keulegan-Carpenter number.

DNV-RP-C205 (2010), Environmental Conditions and Environmental Loads.
    Coefficient guidance for smooth and rough cylinders.

Wheeler, J. D. (1970), "Method for calculating forces produced by irregular
    waves". The stretching used to carry linear kinematics up to the
    instantaneous free surface.

Sumer, B. M., Fredsoe, J. and Christiansen, N. (1992), "Scour around
    vertical pile in waves". The scour relation used here.

Conventions
-----------
Elevation z is measured from the still water level and increases upward, so
the mudline is at z = -depth and a wave crest reaches z = +eta. Forces are
newtons, forces per unit length newtons per metre, and moments newton metres
about the mudline unless stated.

## `G`

```python
G = 9.81
```

## `RHO`

```python
RHO = 1025.0
```

## `NU`

```python
NU = 1.19e-06
```

## `wave_kinematics`

```python
def wave_kinematics(H: float, T: float, depth: float, z, phase: float=0.0, stretching: str='wheeler') -> dict
```

```text
Horizontal velocity and acceleration under a linear wave.

Parameters
----------
H : float
    Wave height [m].
T : float
    Period [s].
depth : float
    Still water depth [m].
z : array_like
    Elevations from the still water level, negative downward [m].
phase : float
    Wave phase in radians. Zero is the crest at the pile.
stretching : str
    "wheeler" maps the still-water profile onto the instantaneous water
    column, "none" evaluates linear theory as written, and "extrapolate"
    continues the still-water profile above the still water level.

    Linear theory says nothing about the water between the still water
    level and the crest, which is exactly where the load is largest.
    Extrapolating the cosh profile there overstates the velocity badly;
    Wheeler stretching is the usual fix and is the default.

Returns
-------
dict
    ``u`` and ``dudt`` at each elevation, the surface elevation ``eta``,
    the wavelength, and a mask of which elevations are in the water.
```

## `keulegan_carpenter`

```python
def keulegan_carpenter(H: float, T: float, depth: float, diameter: float, z: float=0.0) -> float
```

```text
KC = u_max T / D, at elevation ``z``.

Sets which Morison term dominates. Below about 3 the load is almost all
inertia and the drag coefficient hardly matters; above about 20 drag
governs and the inertia coefficient hardly matters. A monopile in a
design storm usually sits awkwardly between the two.
```

## `reynolds_number`

```python
def reynolds_number(H: float, T: float, depth: float, diameter: float, z: float=0.0, viscosity: float=NU) -> float
```

```text
Re = u_max D / nu, at elevation ``z``.
```

## `drag_inertia_coefficients`

```python
def drag_inertia_coefficients(KC: float, rough: bool=True) -> dict
```

```text
Indicative Cd and Cm, with the regime named.

Post-critical Reynolds number values from DNV-RP-C205: a rough cylinder,
which is what any pile becomes once marine growth establishes, takes
Cd = 1.05, and a clean one Cd = 0.65. The inertia coefficient falls from
the potential-flow value of 2.0 as KC rises and the wake starts to
interfere with the next half cycle.

Returns
-------
dict
    ``Cd``, ``Cm`` and the dominant ``regime``. These are starting
    values for a concept design. A real design takes them from the
    governing code for the actual roughness, KC and Re, and a real
    fatigue assessment does not use a single pair at all.
```

## `morison_load_profile`

```python
def morison_load_profile(diameter: float, u, dudt, Cd: float=1.05, Cm: float=2.0, rho: float=RHO) -> dict
```

```text
Inline force per unit length, split into its two terms [N/m].
```

## `integrate_load`

```python
def integrate_load(z, load, mudline: float) -> dict
```

```text
Total force and mudline moment from a load profile.

Trapezoidal in z, which is what the profile is sampled on. The moment
arm is measured from the mudline, so the result is the overturning
moment the foundation has to carry.
```

## `PileLoad`

```python
class PileLoad
    diameter: float
    H: float
    T: float
    depth: float
    phase: float
    z: np.ndarray
    drag: np.ndarray
    inertia: np.ndarray
    total: np.ndarray
    force: float
    moment: float
    arm: float
    eta: float
    Cd: float
    Cm: float
    KC: float
    regime: str
    diffraction_ratio: float
    warnings: list[str] = field(default_factory=list)
```

```text
Wave load on a pile at one phase, or at the worst phase.
```

### `PileLoad.inertia_fraction` (property)

```python
PileLoad.inertia_fraction(self) -> float
```

```text
Share of the total force carried by the inertia term.
```

### `PileLoad.summary` (method)

```python
PileLoad.summary(self) -> str
```

## `morison_pile_load`

```python
def morison_pile_load(diameter: float, H: float, T: float, depth: float, phase: float=0.0, Cd: float | None=None, Cm: float | None=None, points: int=400, stretching: str='wheeler', rough: bool=True, air_gap: float=0.0) -> PileLoad
```

```text
Morison load on a vertical pile at one wave phase.

Parameters
----------
points : int
    Samples up the pile. The load is concentrated near the surface, so
    a coarse grid loses the peak; 400 is ample for a monopile.
air_gap : float
    Elevation above the still water level to sample to. The profile is
    zero above the instantaneous surface, so this only matters for
    plotting the dry part of the pile.
Cd, Cm : float, optional
    Taken from :func:`drag_inertia_coefficients` when not given.
```

## `phase_sweep`

```python
def phase_sweep(diameter: float, H: float, T: float, depth: float, phases: int=181, **kwargs) -> dict
```

```text
Force and moment through the wave cycle, and where each peaks.

The base shear and the overturning moment do not peak at the same
phase, because the drag term peaks under the crest while the inertia
term peaks a quarter cycle earlier, and the two have different lever
arms. Designing on the crest phase alone can miss the worst moment.
```

## `scour_depth_pile`

```python
def scour_depth_pile(diameter: float, KC: float, current_only: bool=False, live_bed: bool=True, bed=None, Hs: float | None=None, T: float | None=None, depth: float | None=None) -> dict
```

```text
Equilibrium scour depth at a vertical pile [m].

Sumer, Fredsoe and Christiansen (1992), for waves::

    S / D = 1.3 [1 - exp(-0.03 (KC - 6))]      for KC > 6

with no scour below KC = 6, where the horseshoe vortex does not form.
Under a steady current the same authors give S / D = 1.3 with a standard
deviation of 0.7, which is the ``current_only`` branch and also the
limit the wave relation tends to.

Notes
-----
This is the equilibrium depth under a sustained condition, not the depth
after one storm, and it is a live-bed result. In clear water the
equilibrium is similar but takes far longer to develop. Scour protection
is designed on the equilibrium depth; the pile itself is often checked
for both, since a scoured pile is a longer cantilever and a softer one.
```

## `design_monopile`

```python
def design_monopile(diameter: float, H: float, T: float, depth: float, rough: bool=True, stretching: str='wheeler', phases: int=181, bed=None) -> dict
```

```text
Worst-phase load, scour, and the numbers a foundation designer wants.

Sweeps the phase for the worst moment rather than assuming the crest,
returns the load at that phase, and adds the scour depth and the
resulting increase in cantilever length.
```

