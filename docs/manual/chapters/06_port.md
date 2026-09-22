# Harbor agitation and port layout {#sec:port}

*Module:* `pyCoastal.applications.port`. *Examples:*
`examples/port_diffraction.py`, `examples/port_layout_comparison.py`.

Phase-resolved wave propagation into a harbor, reported as the wave
energy that reaches the berths. Breakwaters are rasterized onto the grid as
reflecting walls with a settable absorption, waves enter from a soft source
line, and the open boundaries are damped by sponge layers so that outgoing
and reflected energy leaves the domain instead of ringing around it.

## The solver

The model integrates the second-order wave equation in flux form (@eq:port-wave),

$$ \frac{\partial^2\eta}{\partial t^2} = \nabla\cdot\left(c^2\nabla\eta\right), $$ {#eq:port-wave}

with zero flux on every face touching a breakwater cell, by an explicit
leapfrog step at a Courant number of 0.35. The celerity comes from the
linear dispersion relation (@eq:dispersion) at the local depth and the run
period, so the wavelength is correct in intermediate water rather than the
shallow-water $\sqrt{gh}$. The model is therefore accurate for the single
frequency it is run at. It is not a spectral model and does not represent
breaking, wave-current interaction, refraction over a varying bed, or
nonlinear transfers.

Harbor performance is the disturbance coefficient (@eq:port-1)

$$ K_d = \frac{H_\mathrm{local}}{H_\mathrm{reference}}, $$ {#eq:port-1}

with the reference height measured at a probe in open water outside the
harbor, which makes the result independent of how the source is calibrated.
Against a semi-infinite breakwater the solver gives a deep quiet shadow,
$K_d$ near 0.5 on the geometric shadow boundary, and Fresnel fringes in the
illuminated field.

## Geometry

`Breakwater(points, width=20.0, name="breakwater", absorption=0.0)` is a
polyline of a given thickness; cells within `width/2` of the centerline
become land. `absorption` is a damping collar in the water next to the
structure, a model knob rather than the reflection coefficient itself.
`measure_reflection(absorption, period, depth)` fires a normally incident
wave at a full-width wall and infers
$K_r = (H_\mathrm{max} - H_\mathrm{min})/(H_\mathrm{max} + H_\mathrm{min})$
from the standing-wave envelope (@tbl:absorption). The mapping is not
monotonic: past about 0.75 the collar becomes an impedance step and
reflects again. Use 0.3 to 0.4 for a rubble mound ($K_r$ near 0.4) and 0 for
a vertical caisson.

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
- `offset_entrance_layout` (`"offset_entrance"`): overlapping arms making a
  dog-leg entrance, so waves must diffract twice;
- `hooked_breakwater_layout` (`"hooked"`): a main breakwater with a
  shore-parallel hook, so the entrance faces along the coast;
- `detached_breakwater_layout` (`"detached_screen"`): two arms with a
  detached screen off the gap;
- `marina_layout` (`"marina"`): an outer harbor protecting an inner basin
  through an offset second opening.

**Wave direction.** `IncidentWave(height=1.5, period=8.0, direction=0.0)`
supports an oblique direction, but a phased source line only lights a
parallelogram of the domain (`illuminated_mask`), and `simulate_port` warns
when a structure falls outside it. The accurate way to study direction is to
turn the harbor into the waves with `rotate_layout(layout, degrees)` and
drive it shore-normal, since only the relative angle matters.

**Absorption matters.** Left fully reflecting, a detached screen forms a
pocket with the arms that rings, and basin agitation goes up. For a 150 m
gap with 280 m arms at $T = 9$ s, mean basin $K_d$ went from 0.35 to 0.51
with a reflecting screen, and from 0.20 to 0.04 once the structures were
armored.

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
`wave_height`, and the `reference_height`. The default duration lets the
wave cross the domain twice plus the ramp and analysis windows; the sponge
defaults to 1.5 wavelengths.

## Worked examples

`examples/port_diffraction.py` drives a 9 s swell at 25 degrees into a
two-arm harbor (by rotating the layout), writes an animation of the
instantaneous surface, and reports $K_d$ at four berths:

<!-- output: port_diffraction -->

![Disturbance coefficient in the harbor. The north berth sits in the diffracted field from the entrance and exceeds the 0.5 m limit.](media/port_disturbance.png){#fig:port-disturbance width=85%}

`examples/port_layout_comparison.py` runs all five layouts under the same
design wave and ranks them by basin agitation:

<!-- output: port_layout_comparison -->

![The five built-in layouts under the same design wave.](media/port_layouts.png){#fig:port-layouts}
