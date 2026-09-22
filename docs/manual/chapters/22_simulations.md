# Simulation examples {#sec:simulations}

Each numerical example combines one governing equation, one discretization
and one diagnostic. The scripts read their parameters from YAML files in
`examples/configs/`, so a case is repeated or swept by editing the case
file. The fields are animated with matplotlib. The scripts run from the
repository root.

```bash
python examples/numerics/water_drop.py
python examples/waves2D.py
python examples/wave2D_irregular.py
python examples/current.py
python examples/pollutant.py
python examples/numerics/viscous_fluid.py
python examples/numerics/2D_irr_turb.py
python examples/equilibrium_shoreline.py
```

## Case files

The YAML keys used by the examples are collected in @tbl:yaml. Grid keys
give cell counts and either spacings or domain lengths; physics keys the
parameters of the equation; solver keys the time step (directly or through
a CFL number) and the run length; output keys the gauge locations as grid
indices.

: YAML keys used by the numerical examples. {#tbl:yaml}

| Config | grid | physics | solver / forcing | output |
|--------|------|---------|------------------|--------|
| `water_drop.yaml` | `Nx, Ny, Lx, Ly` | `wave_speed, sigma` | `CFL, t_final` | |
| `waves2D.yaml` | `nx, ny, dx, dy` | `gravity, depth` | `amplitude, period`; `cfl, t_final` | `obs_points` |
| `waves2D_irregular.yaml` | `nx, ny, dx, dy` | `gravity, depth` | `type` (pm or jonswap), `gamma, Hs, Tp`; `dt, duration` | `gauge` |
| `current.yaml` | `nx, ny, dx, dy` | `speed` | `cfl, t_final` | `gauge` |
| `pollutant.yaml` | `Lx, Ly, Nx, Ny` | `diffusivity, U0, R` | `t_final, c0_sigma` | |
| `viscous_fluid.yaml` | `Nx, Ny, Lx, Ly` | `viscosity, background_speed, vortex_sigma` | `dt, t_final` | |
| `equilibrium_shoreline.yaml` | `Lshore, Gb, Lb1, Lb2, Yi` | | `n_points, sag_side_factor` | |

## Water drop: the 2D wave equation

**Objective.** Verify the accuracy of the Laplacian and the stability of the
time stepping on a simple hyperbolic system (@eq:simulations-1),

$$ \frac{\partial^2\eta}{\partial t^2} = c^2\nabla^2\eta. $$ {#eq:simulations-1}

A Gaussian bump of width `sigma` is released at the center of the domain
with zero Dirichlet boundaries, and the circular front should travel at
$c$. Refining the grid and the time step should converge the solution at
the expected order.

![Circular wave propagation from a central disturbance (`examples/numerics/water_drop.py`).](media/water_drop_central.png){#fig:water-drop width=70%}

## Regular waves: `waves2D.py`

A depth-averaged wave field in uniform depth, forced by a sinusoid of
amplitude `amplitude` and period `period` at the $y = 0$ boundary and
periodic in $x$. The script solves linear advection along $y$ column by
column with an upwind stencil and forward Euler, animates $\eta$, and
records the time series at the observation points. The wave speed comes
from the linear dispersion relation for the configured depth and period.

## Irregular waves: a numerical flume

**Objective.** Generate a target spectrum and manage reflections. The script
synthesizes a surface elevation record from a Pierson-Moskowitz or JONSWAP
spectrum (@sec:tools-wave), imposes it as a Dirichlet condition at the
inflow boundary, and records a gauge inside the domain, so the input and
interior spectra ($H_s$, $T_p$) can be compared. A sponge at the outflow
absorbs the outgoing waves.

![Irregular wave field at the end of the run (`examples/wave2D_irregular.py`).](media/wave2D_irregular_final.png){#fig:irregular width=70%}

## Current and pollutant: advection and diffusion

**Objective.** Observe upwind smearing and diffusive spreading. `current.py`
advects a passive field with a uniform current, $u_t + c\,u_x = 0$, with a
Dirichlet inlet on the west and a Neumann outlet on the east, and records
a gauge. `pollutant.py` solves the full advection-diffusion equation for a
Gaussian patch in a vortex flow in a shallow pond (@eq:simulations-2),

$$ \frac{\partial C}{\partial t} + u\frac{\partial C}{\partial x} + v\frac{\partial C}{\partial y} = D\nabla^2 C, $$ {#eq:simulations-2}

with upwind advection, centered diffusion (`operators.gradient` and
`operators.laplacian`), and zero-flux boundaries. For pure diffusion the
variance of the patch grows as $2Dt$, which the run can be checked against.

## Viscous fluid: velocity decay

**Objective.** Check the diffusive time scale and operator accuracy.
`viscous_fluid.py` evolves two counter-rotating vortices on a periodic
domain with central differences and forward Euler. The diffusion part can
be checked against the decaying mode (@eq:simulations-3)

$$ u(x, y, t) = U_0\sin(k_x x)\sin(k_y y)\exp\left[-\nu(k_x^2 + k_y^2)t\right]. $$ {#eq:simulations-3}

## Boundary-condition test: `2D_irr_turb.py`

A pure boundary-condition exercise on a 400 m by 400 m grid: a sinusoidal
Dirichlet wave maker on the south side, a spatially ramped sponge on the
north, a Dirichlet inflow velocity and a zero-gradient surface on the west,
zero-gradient outflow on the east, and walls for the normal velocity. No
physics is advanced; the script applies the `BoundaryManager` every step
and records a gauge, which isolates what the boundary classes do.

## Equilibrium shoreline behind detached breakwaters

`equilibrium_shoreline.py` builds a schematic equilibrium planform behind a
pair of detached breakwaters from three circular arcs (a left lateral arc,
a central salient, and a right lateral arc), following the Hsu and Evans
style of parabolic bay construction. The geometry comes from
`equilibrium_shoreline.yaml` (shoreline length, gap between breakwaters,
their lengths, and offshore distance) and the construction uses
`pyCoastal.tools.morphodynamics` (@sec:tools-morpho), which also reports
the retreat and the accretion percentage.

![Equilibrium shoreline behind two detached breakwaters (`examples/equilibrium_shoreline.py`).](media/equilibrium_shoreline.png){#fig:eq-shoreline width=80%}

## Diagnostics, verification, and validation

Numerical experiments should be accompanied by simple, repeatable checks:

- **CFL monitor.** Compute and report the Courant number each step, and
  adapt $\Delta t$ if needed.
- **Divergence.** After a projection step, $\|\nabla\cdot\mathbf u\|_2$
  should sit near the Poisson solver tolerance.
- **Energy and variance.** Monitor $\int\eta^2$ or the kinetic energy to spot
  drift or spurious reflections.
- **Convergence.** Refine $\Delta x$, $\Delta y$, and $\Delta t$ and verify
  the expected order.
- **Spectral targets.** Compare $H_s$ and $T_p$ at interior gauges with the
  input, and estimate reflection by separating incident and reflected
  waves.

Save arrays as NumPy files and figures with matplotlib; export animations as
`.gif` or `.mp4`. Store the run metadata (git hash, YAML, random seeds)
beside the outputs so a figure can be regenerated exactly.

## Extending the framework

To add physics or numerics:

1. implement a right-hand side `rhs(u, t)` and pass it to an integrator;
2. provide boundary handlers consistent with the stencils;
3. add YAML keys with sensible defaults;
4. add a small example and a docstring that states the equations, the
   variables, the numerics, and the stability limits.

## Limitations of the numerical framework

- Uniform Cartesian grids only; no curvilinear or unstructured meshes.
- Explicit time stepping, which is restrictive for stiff sources such as the
  $\varepsilon$ or $\omega$ transport.
- The turbulence closures are educational scaffolds, not production RANS or
  LES.
- No wetting and drying or moving shorelines in the 2D solvers. (The design
  applications handle shoreline change with the one-line model and flooding
  with connectivity-aware mapping; see @sec:nourishment and @sec:surge.)
