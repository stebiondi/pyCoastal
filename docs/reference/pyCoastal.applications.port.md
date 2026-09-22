# `pyCoastal.applications.port`

Source: [`pyCoastal/applications/port.py`](../../pyCoastal/applications/port.py)

Port layout simulator.

Propagates a phase-resolved wave field into a harbour and reports how much
wave energy reaches the berths. Breakwaters are rasterized onto the grid as
reflecting walls, waves enter from a soft source line, and the open
boundaries are damped by sponge layers so outgoing and reflected energy
leaves the domain instead of ringing around it.

The solver integrates the second-order wave equation

    d2 eta / dt2 = div( c^2 grad eta )

in flux form, with zero flux on every face touching a breakwater cell. The
celerity c is taken from the linear dispersion relation at the local depth
and the chosen wave period, using ``pyCoastal.tools.wave.dispersion``, so the
wavelength is correct in intermediate water rather than the shallow-water
approximation sqrt(g h). The model is therefore accurate for the single
frequency it is run at; it is not a broad-banded spectral model, and it does
not represent breaking, wave-current interaction, or nonlinear transfers.

Harbour performance is reported as the disturbance coefficient

    Kd = H_local / H_reference

with H_reference measured at a probe in open water outside the harbour. That
normalisation makes the result independent of how the source is calibrated.

Coordinates follow the package convention: x and y span the horizontal
plane with x on axis 0, z is elevation.

## `G`

```python
G = 9.81
```

## `Breakwater`

```python
class Breakwater
    points: list[tuple[float, float]]
    width: float = 20.0
    name: str = 'breakwater'
    absorption: float = 0.0
```

```text
A breakwater as a polyline of a given thickness.

Attributes
----------
points : sequence of (x, y)
    Vertices of the centreline [m]. Two points give a straight arm;
    more give a bent or dog-leg structure.
width : float
    Structure thickness [m]. Cells within ``width / 2`` of the
    centreline become land.
name : str
    Label used in reports and plots.
absorption : float
    Energy absorption of the seaward face, 0 for a fully reflecting
    vertical wall and 1 for a perfect absorber. A rubble-mound armour
    slope is roughly 0.5 to 0.8. Implemented as a damping collar in the
    water next to the structure, so this is a model knob and not the
    reflection coefficient itself. Measured Kr for a normally incident
    wave, from ``measure_reflection``:

        absorption  0.00  0.25  0.50  0.75  1.00
        Kr          0.95  0.48  0.22  0.19  0.25

    The mapping is not monotonic: past about 0.75 the collar is damped so
    strongly that it becomes an impedance step and starts reflecting
    again. Use roughly 0.3 to 0.4 for a rubble mound (Kr near 0.4), and
    leave it at 0 for a vertical caisson.
```

### `Breakwater.distance_field` (method)

```python
Breakwater.distance_field(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray
```

```text
Distance from every grid point to this structure's centreline [m].
```

## `PortLayout`

```python
class PortLayout
    Lx: float = 1200.0
    Ly: float = 900.0
    dx: float = 4.0
    depth: float = 10.0
    breakwaters: list[Breakwater] = field(default_factory=list)
```

```text
Harbour geometry and bathymetry.

Attributes
----------
Lx, Ly : float
    Domain extent [m].
dx : float
    Grid spacing [m], used in both directions.
depth : float
    Still-water depth [m]. Constant depth only; refraction over a
    varying bed is out of scope for this solver.
breakwaters : list of Breakwater
    Structures rasterized as reflecting walls.
```

### `PortLayout.shape` (property)

```python
PortLayout.shape(self) -> tuple[int, int]
```

### `PortLayout.coordinates` (method)

```python
PortLayout.coordinates(self) -> tuple[np.ndarray, np.ndarray]
```

```text
1D coordinate arrays (x, y) [m].
```

### `PortLayout.meshgrid` (method)

```python
PortLayout.meshgrid(self) -> tuple[np.ndarray, np.ndarray]
```

```text
2D coordinate arrays with x on axis 0.
```

### `PortLayout.land_mask` (method)

```python
PortLayout.land_mask(self) -> np.ndarray
```

```text
Boolean array, True where a breakwater occupies the cell.
```

## `harbour_layout`

```python
def harbour_layout(Lx: float=1200.0, Ly: float=900.0, dx: float=4.0, depth: float=10.0, gap: float=120.0, arm_length: float=330.0, width: float=24.0, back_wall: bool=True, absorption: float=0.0) -> PortLayout
```

```text
A conventional two-arm harbour with a gap entrance.

Two shore-normal breakwaters project from the downwave (east) side of the
domain, leaving an opening of width ``gap`` centred on the domain. With
``back_wall`` the basin is closed by a quay along the landward edge, so
energy entering the harbour has to leave through the gap again. Handy as
a starting point and as the geometry used in the tests. ``absorption``
is applied to every structure; see ``Breakwater.absorption``.

When using a back wall, drop "east" from ``simulate_port(sponge_sides=...)``
so the quay reflects instead of being absorbed.
```

## `offset_entrance_layout`

```python
def offset_entrance_layout(Lx: float=1400.0, Ly: float=900.0, dx: float=4.0, depth: float=10.0, gap: float=130.0, overlap: float=140.0, separation: float=180.0, arm_length: float=300.0, width: float=24.0, back_wall: bool=True, absorption: float=0.0) -> PortLayout
```

```text
Overlapping arms, so no straight path leads into the basin.

The two arms sit at different x and overlap in y, turning the entrance
into a dog-leg. Waves have to diffract twice to reach the basin, which is
the usual way to quieten a harbour without narrowing the navigable
opening.

Parameters
----------
overlap : float
    Alongshore distance over which the two arms shadow each other [m].
separation : float
    Distance between the two arms in x [m], setting the length of the
    entrance channel.
```

## `hooked_breakwater_layout`

```python
def hooked_breakwater_layout(Lx: float=1400.0, Ly: float=900.0, dx: float=4.0, depth: float=10.0, gap: float=150.0, hook_length: float=220.0, arm_length: float=340.0, width: float=24.0, back_wall: bool=True, absorption: float=0.0) -> PortLayout
```

```text
A long main breakwater with a shore-parallel hook, plus a lee arm.

The hook turns back across the approach so the entrance faces along the
coast rather than into the incoming waves. Common where the design wave
arrives consistently from one sector.

Parameters
----------
hook_length : float
    Length of the returning limb at the head of the main arm [m].
```

## `detached_breakwater_layout`

```python
def detached_breakwater_layout(Lx: float=1400.0, Ly: float=900.0, dx: float=4.0, depth: float=10.0, gap: float=150.0, screen_length: float=300.0, standoff: float=200.0, arm_length: float=280.0, width: float=24.0, back_wall: bool=True, absorption: float=0.0) -> PortLayout
```

```text
Two arms with a detached screen standing off the entrance.

The screen intercepts waves heading straight for the gap while leaving
navigable water either side of it. Used where an entrance cannot be
narrowed or offset.

Give the screen some ``absorption``. Left fully reflecting it forms a
pocket with the arms that rings, and basin agitation goes up rather than
down. For a 150 m gap with 280 m arms at T = 9 s, mean basin Kd went from
0.35 to 0.51 with a reflecting screen, and from 0.20 to 0.04 once the
structures were armoured. The effect worsens as ``standoff`` grows.

Parameters
----------
screen_length : float
    Alongshore length of the detached breakwater [m].
standoff : float
    Distance seaward of the arms at which the screen sits [m].
```

## `marina_layout`

```python
def marina_layout(Lx: float=1400.0, Ly: float=900.0, dx: float=4.0, depth: float=10.0, outer_gap: float=160.0, inner_gap: float=90.0, inner_offset: float=220.0, basin_separation: float=240.0, arm_length: float=300.0, width: float=24.0, back_wall: bool=True, absorption: float=0.0) -> PortLayout
```

```text
An outer harbour protecting an inner basin through a second opening.

The inner entrance is offset alongshore from the outer one, so energy
entering the outer harbour does not run straight into the marina. This is
the arrangement that keeps small-craft berths workable.

Parameters
----------
inner_offset : float
    Alongshore offset between the outer and inner entrances [m].
basin_separation : float
    Distance in x between the outer arms and the inner basin wall [m].
```

## `rotate_layout`

```python
def rotate_layout(layout: PortLayout, degrees: float, about: tuple[float, float] | None=None) -> PortLayout
```

```text
Rotate every structure in a layout by ``degrees`` (counter-clockwise).

Only the relative angle between the waves and the harbour matters, so
rotating the layout and driving it shore-normal is equivalent to leaving
it fixed and sending an oblique wave, without the lit-parallelogram limit
of an oblique source. This is the accurate way to study wave direction.

Structures are rotated about ``about``, defaulting to the domain centre.
Points may leave the domain; that is fine, since anything outside is
simply not rasterized.
```

## `illuminated_mask`

```python
def illuminated_mask(layout: PortLayout, wave: IncidentWave, source_x: float) -> np.ndarray
```

```text
Cells that the oblique source line actually reaches.

A source at ``x = source_x`` spanning the full domain height launches rays
at the wave angle, so the field at (x, y) originates from
``y - (x - source_x) tan(theta)``. Where that lies outside the source line
the cell never receives the incident wave.
```

## `LAYOUTS`

```python
LAYOUTS = {'two_arm': harbour_layout, 'offset_entrance': offset_entrance_layout, 'hooked': hooked_breakwater_layout, 'detached_screen': detached_breakwater_layout, 'marina': marina_layout}
```

## `IncidentWave`

```python
class IncidentWave
    height: float = 1.5
    period: float = 8.0
    direction: float = 0.0
```

```text
Monochromatic incident wave.

Attributes
----------
height : float
    Incident wave height H [m].
period : float
    Wave period [s].
direction : float
    Propagation direction [rad], measured from the +x axis. Zero sends
    the wave straight up-domain toward the harbour entrance.
```

### `IncidentWave.amplitude` (property)

```python
IncidentWave.amplitude(self) -> float
```

### `IncidentWave.omega` (property)

```python
IncidentWave.omega(self) -> float
```

### `IncidentWave.wavelength` (method)

```python
IncidentWave.wavelength(self, depth: float) -> float
```

```text
Wavelength at the given depth [m], from the dispersion relation.
```

### `IncidentWave.celerity` (method)

```python
IncidentWave.celerity(self, depth: float) -> float
```

```text
Phase celerity at the given depth [m/s].
```

## `PortResult`

```python
class PortResult
    x: np.ndarray
    y: np.ndarray
    times: np.ndarray
    snapshots: np.ndarray
    land: np.ndarray
    wave_height: np.ndarray
    reference_height: float
    layout: PortLayout
    wave: IncidentWave
```

```text
Output of a port simulation.

Attributes
----------
x, y : np.ndarray
    Coordinate axes [m].
times : np.ndarray
    Times of the stored snapshots [s].
snapshots : np.ndarray
    Surface elevation, shape (n_times, nx, ny) [m].
land : np.ndarray
    Breakwater mask, shape (nx, ny).
wave_height : np.ndarray
    Wave height over the analysis window, shape (nx, ny) [m].
reference_height : float
    Wave height at the reference probe in open water [m].
layout, wave
    The inputs the run came from.
```

### `PortResult.disturbance_coefficient` (property)

```python
PortResult.disturbance_coefficient(self) -> np.ndarray
```

```text
Kd = H_local / H_reference, masked to water cells.
```

### `PortResult.probe` (method)

```python
PortResult.probe(self, point: tuple[float, float]) -> float
```

```text
Disturbance coefficient at a point [m, m].
```

### `PortResult.berth_report` (method)

```python
PortResult.berth_report(self, berths: dict[str, tuple[float, float]]) -> dict[str, dict]
```

```text
Wave height and Kd at each named berth.
```

### `PortResult.operable_fraction` (method)

```python
PortResult.operable_fraction(self, berths: dict[str, tuple[float, float]], limit: float) -> dict[str, bool]
```

```text
Whether each berth stays below an operational wave-height limit [m].
```

## `VALID_SIDES`

```python
VALID_SIDES = ('west', 'east', 'south', 'north')
```

## `simulate_port`

```python
def simulate_port(layout: PortLayout, wave: IncidentWave, duration: float | None=None, cfl: float=0.35, sponge_thickness: float | None=None, sponge_strength: float=2.0, sponge_sides: tuple[str, ...]=VALID_SIDES, source_x: float | None=None, ramp_periods: float=3.0, analysis_periods: float=6.0, n_snapshots: int=120, store_from: float | None=None, reference_point: tuple[float, float] | None=None) -> PortResult
```

```text
Propagate a phase-resolved wave field into the harbour.

Parameters
----------
layout, wave
    Harbour geometry and incident wave.
duration : float, optional
    Simulated time [s]. Defaults to enough for the wave to cross the
    domain twice plus the ramp and analysis windows.
cfl : float
    Courant number for the explicit leapfrog step.
sponge_thickness : float, optional
    Width of the absorbing margin [m]. Defaults to 1.5 wavelengths.
sponge_strength : float
    Peak damping rate in the sponge [1/s].
sponge_sides : tuple of str
    Which domain edges absorb. Drop a side to make it reflect, for
    instance the landward edge behind a harbour basin.
source_x : float, optional
    x position of the wave-maker line [m]. Defaults to just inside the
    west sponge.
ramp_periods : float
    Number of periods over which the source amplitude ramps up, to avoid
    a start-up shock.
analysis_periods : float
    Length of the window at the end of the run used to measure wave
    height, in wave periods.
n_snapshots : int
    Number of stored surface snapshots, spread over the stored window.
store_from : float, optional
    Time from which to start storing snapshots [s]. Defaults to the
    beginning of the analysis window, so the movie shows the developed
    field. Pass 0.0 to record the whole run including start-up.
reference_point : (float, float), optional
    Probe used to define the incident height. Defaults to a point in
    open water upwave of the harbour entrance.

Returns
-------
PortResult
```

## `measure_reflection`

```python
def measure_reflection(absorption: float, period: float=8.0, depth: float=10.0, dx: float=5.0, sponge_strength: float=2.0) -> float
```

```text
Reflection coefficient achieved by a given ``absorption`` setting.

Fires a normally incident wave at a full-width wall and infers Kr from
the standing-wave ratio in front of it,

    Kr = (Hmax - Hmin) / (Hmax + Hmin)

which is the usual laboratory estimate. Useful for picking an
``absorption`` value that matches a measured or specified Kr.
```

