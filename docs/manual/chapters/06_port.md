# Harbor agitation and port layout {#sec:port}

*Module:* `pyCoastal.applications.port`. *Examples:*
`examples/port_diffraction.py`, `examples/port_layout_comparison.py`.

The module computes phase-resolved wave propagation into a harbor and
reports the wave energy at the berths. Breakwaters are rasterized onto the
grid as reflecting walls with a configurable absorption. Waves are
introduced at a soft source line. The open boundaries carry sponge layers
that damp outgoing and reflected energy.

## The solver

The model integrates the second-order wave equation in flux form (@eq:port-wave),

$$ \frac{\partial^2\eta}{\partial t^2} = \nabla\cdot\left(c^2\nabla\eta\right), $$ {#eq:port-wave}

with zero flux on every face adjacent to a breakwater cell, using an
explicit leapfrog step at a Courant number of 0.35. The celerity is taken
from the linear dispersion relation (@eq:dispersion) at the local depth and
the run period, which gives the correct wavelength in intermediate water.
The solution applies to the single frequency of the run. The model excludes
spectral content, breaking, wave-current interaction, refraction over a
varying bed and nonlinear transfers.

Harbor performance is the disturbance coefficient (@eq:port-1)

$$ K_d = \frac{H_\mathrm{local}}{H_\mathrm{reference}}, $$ {#eq:port-1}

where the reference height is measured at a probe in open water outside the
harbor. This normalization removes the dependence on source calibration.
For a semi-infinite breakwater the solver returns $K_d$ near 0.5 on the
geometric shadow boundary and Fresnel fringes in the illuminated field.

## Geometry

`Breakwater(points, width=20.0, name="breakwater", absorption=0.0)` defines
a polyline of given thickness; cells within `width/2` of the centerline are
set to land. `absorption` applies a damping collar in the water adjacent to
the structure. It is a model parameter; the resulting reflection
coefficient is obtained from `measure_reflection`.
`measure_reflection(absorption, period, depth)` propagates a normally
incident wave onto a full-width wall and evaluates
$K_r = (H_\mathrm{max} - H_\mathrm{min})/(H_\mathrm{max} + H_\mathrm{min})$
from the standing-wave envelope (@tbl:absorption). The mapping is
non-monotonic: above about 0.75 the collar acts as an impedance step and
reflection increases. Values of 0.3 to 0.4 correspond to a rubble mound
($K_r$ near 0.4); 0 corresponds to a vertical caisson.

: Reflection coefficient against the absorption setting. {#tbl:absorption}

| absorption | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
|------------|------|------|------|------|------|
| $K_r$ | 0.95 | 0.48 | 0.22 | 0.19 | 0.25 |

`PortLayout(Lx=1200, Ly=900, dx=4.0, depth=10.0, breakwaters=[])` holds the
domain, grid spacing, constant depth, and structures. Five layouts are built
in (`LAYOUTS`):

- `harbour_layout` (`"two_arm"`): two shore-normal arms with a gap
  entrance, and optionally a back wall (drop `"east"` from the sponge sides
  so the quay reflects);
- `offset_entrance_layout` (`"offset_entrance"`): overlapping arms forming a
  dog-leg entrance, which requires two diffractions to reach the basin;
- `hooked_breakwater_layout` (`"hooked"`): a main breakwater with a
  shore-parallel hook, with the entrance oriented along the coast;
- `detached_breakwater_layout` (`"detached_screen"`): two arms with a
  detached screen off the gap;
- `marina_layout` (`"marina"`): an outer harbor protecting an inner basin
  through an offset second opening.

**Wave direction.** `IncidentWave(height=1.5, period=8.0, direction=0.0)`
accepts an oblique direction. A phased source line illuminates only a
parallelogram of the domain (`illuminated_mask`), and `simulate_port` issues
a warning when a structure lies outside that region. Oblique cases are
therefore run by rotating the layout with `rotate_layout(layout, degrees)`
and driving it shore-normal; the solution depends on the relative angle
only.

**Absorption setting.** With a fully reflecting detached screen, the screen
and the arms form a resonant pocket and basin agitation increases. For a
150 m gap with 280 m arms at $T = 9$ s, mean basin $K_d$ is 0.35 without the
screen, 0.51 with a reflecting screen, and 0.04 with the same screen and
arms at an absorption of 0.35.

## Running a simulation

```python
import numpy as np
from pyCoastal.applications.port import IncidentWave, harbour_layout, simulate_port

layout = harbour_layout(gap=130, arm_length=300, back_wall=True, absorption=0.35)
wave = IncidentWave(height=1.5, period=9.0, direction=np.deg2rad(0))

result = simulate_port(layout, wave, sponge_sides=("west", "north", "south"))

result.disturbance_coefficient          # Kd over the whole basin
result.probe((1120, 450))               # Kd at one point
result.berth_report({"quay": (1120, 450)})
result.operable_fraction({"quay": (1120, 450)}, limit=0.5)
```

`simulate_port(layout, wave, duration=None, cfl=0.35, sponge_thickness=None,
sponge_strength=2.0, sponge_sides=..., source_x=None, ramp_periods=3.0,
analysis_periods=6.0, n_snapshots=120, store_from=None,
reference_point=None)` returns a `PortResult` with the coordinate axes,
stored surface `snapshots`, the `land` mask, the analysis-window
`wave_height` and the `reference_height`. The default duration covers two
domain crossings plus the ramp and analysis windows. The default sponge
thickness is 1.5 wavelengths.

## Worked examples

`examples/port_diffraction.py` propagates a 9 s swell at 25 degrees into a
two-arm harbor by rotating the layout, writes an animation of the
instantaneous surface, and reports $K_d$ at four berths:

<!-- output: port_diffraction -->

![Disturbance coefficient in the harbor. The north berth lies in the diffracted field from the entrance and exceeds the 0.5 m operational limit.](media/port_disturbance.png){#fig:port-disturbance width=85%}

`examples/port_layout_comparison.py` runs all five layouts under the same
design wave and ranks them by basin agitation:

<!-- output: port_layout_comparison -->

![The five built-in layouts under the same design wave, each panel labeled with its layout and mean basin $K_d$.](media/port_layouts.png){#fig:port-layouts}
