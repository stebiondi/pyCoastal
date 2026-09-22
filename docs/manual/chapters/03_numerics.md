# Part II. Numerical framework {.part .unnumbered}

# Grids, operators, and time integration {#sec:numerics}

Computational coastal engineering connects governing equations with the
numerical choices that approximate them. `pyCoastal.numerics` exposes those
choices one brick at a time: a grid, the finite-difference operators that
act on it, the integrators that march it in time, and the boundary
conditions that close it. Every choice is visible in the code and can be
changed one at a time.

## Grids

### `UniformGrid`

Most numerical examples use a uniform Cartesian mesh, the simplest setting
in which to illustrate discretization ideas. Two storage layouts are common:
cell-centered (unknowns at cell centers) and node-centered (unknowns at grid
intersections). pyCoastal adopts the cell-centered layout, which keeps
stencils symmetric and boundary handling simple on rectangular domains.

```python
from pyCoastal.numerics.grid import UniformGrid

grid = UniformGrid(shape=(200, 100), spacing=(2.0, 2.0), origin=(0.0, 0.0))
grid.Xc          # cell-center coordinates, a list [X, Y] built with indexing="ij"
grid.Xf          # face coordinates
grid.spacing     # (dx, dy)
grid.n_cells, grid.cell_volume
grid.boundary_indices["west"]    # flat indices of the west boundary cells
```

`UniformGrid(shape, spacing, origin=None)` works in one and two dimensions.
A three-dimensional shape raises `NotImplementedError` on construction,
because the boundary indices are built there and are defined for 1D and 2D
only. Cell centers sit at $x_i = x_0 + (i + \tfrac12)\Delta x$. In 2D the
flat index of cell $(i, j)$ is $i\,n_y + j$, so that `x` is axis 0 and `y`
is axis 1 in every array. The grid precomputes, for each side (`"west"`,
`"east"`, `"south"`, `"north"`), the flat indices of the boundary cells in
`boundary_indices` and a copy in `sponge_indices`, which the boundary
conditions of @sec:bcs use. `neumann_indices(side)` returns the pair of
boundary and first-interior indices needed to impose a gradient.

### `Mesh1D`, `Mesh2D`, and `Domain`

`pyCoastal.numerics.domain` provides simple structured meshes built from a
case file. `Mesh1D(x0, x1, nx)` stores cell centers `x` and spacing `dx`;
`Mesh2D(x0, x1, nx, y0, y1, ny)` stores 2D center arrays `x`, `y` and
spacings `dx`, `dy`. `Domain(cfg)` reads a `domain:` block with
`dimension: 1` or `2` and instantiates the right mesh; `Domain.info()`
prints a summary. Note the axis order: `Mesh2D` builds its arrays with
NumPy's default `indexing="xy"`, so they are shaped (ny, nx), the other way
round from `UniformGrid`. Mixing the two in one script is the easiest
mistake to make here.

**Indexing and memory layout.** Arrays follow NumPy C order, so the
last index is contiguous. Spacings $\Delta x$, $\Delta y$ are constant.

## Finite differences

Finite differences approximate derivatives with algebraic expressions built
from nearby grid values. On a uniform grid, a first derivative at a cell
center can be estimated by a centered difference, which samples one point
on either side to keep symmetry and second-order accuracy. Higher
derivatives and one-sided formulas follow the same idea. The approach turns
differential equations into systems of algebraic equations, which is why it
remains a common choice for structured-grid problems in fluid mechanics and
wave modeling.

### Centered operators

Centered operators combine values symmetrically around the point of
interest, which keeps the approximation free of directional bias and gives
higher accuracy for smooth solutions. For first derivatives and the
Laplacian ([@eq:central; @eq:laplacian]):

$$
\left.\frac{\partial f}{\partial x}\right|_{i,j} \approx \frac{f_{i+1,j}-f_{i-1,j}}{2\Delta x},
\qquad
\left.\frac{\partial f}{\partial y}\right|_{i,j} \approx \frac{f_{i,j+1}-f_{i,j-1}}{2\Delta y},
$$ {#eq:central}

$$
\nabla^2 f\big|_{i,j} \approx \frac{f_{i+1,j}-2f_{i,j}+f_{i-1,j}}{\Delta x^2}
+ \frac{f_{i,j+1}-2f_{i,j}+f_{i,j-1}}{\Delta y^2}.
$$ {#eq:laplacian}

### Upwind differences for advection

For an advection term with velocity $u$ the solution at a point is
determined by what arrives from upstream, so the stencil is taken from the
upstream side (@eq:upwind):

$$
\left.\frac{\partial f}{\partial x}\right|_{i} \approx
\begin{cases}
\dfrac{f_i - f_{i-1}}{\Delta x}, & u > 0,\\[2mm]
\dfrac{f_{i+1} - f_i}{\Delta x}, & u < 0.
\end{cases}
$$ {#eq:upwind}

The one-sided stencil introduces numerical diffusion but is stable for
hyperbolic problems and prevents non-physical oscillations.

### The operator library

`pyCoastal.numerics.operators` implements these stencils on a
`UniformGrid` (@tbl:operators). The operators use periodic (roll) indexing,
so boundary values must be imposed afterwards by the boundary conditions.

: Operators in `pyCoastal.numerics.operators`. {#tbl:operators}

| Function | Operation |
|----------|-----------|
| `laplacian(field, grid)` | 5-point Laplacian, @eq:laplacian |
| `gradient(field, grid)` | centered gradient, returns `(fx, fy)` |
| `grad_x`, `grad_y` | centered first derivatives |
| `upwind_x(field, u, grid)`, `upwind_y(field, v, grid)` | first-order upwind derivatives |
| `divergence(ux, uy, grid)` | centered $\nabla\cdot\mathbf{u}$ |
| `curl_z(u, v, grid)` | $\partial v/\partial x - \partial u/\partial y$ |
| `biharmonic(field, grid)` | $\nabla^4 f$ as the Laplacian of the Laplacian |
| `mixed_xy(field, grid)` | $\partial^2 f/\partial x\,\partial y$ |
| `advect(u, v, field, grid, scheme="upwind")` | $u\,\partial_x f + v\,\partial_y f$ |
| `smooth3(field, grid)` | 5-point smoothing filter, weights summing to one |

`pyCoastal.numerics.scheme` adds axis-generic versions,
`central_difference(phi, spacing, axis)` and
`upwind(phi, vel, spacing, axis)`.

## Time integration

Once space is discretized, the semi-discrete variable $u(t)$ evolves under a
right-hand side that gathers fluxes and sources, $\mathrm{d}u/\mathrm{d}t =
\mathrm{RHS}(u, t)$. Explicit schemes compute the new state from
information at the current level only, which makes them simple to apply and
to check. The choice of integrator controls stability, accuracy, and how
fast information moves through the grid.

**Forward Euler** (first order) treats the rate as constant over the step (@eq:numerics-1):

$$ u^{n+1} = u^n + \Delta t\,\mathrm{RHS}(u^n). $$ {#eq:numerics-1}

**Heun / RK2** (second order) averages the slopes at the start and the end of
the step (@eq:numerics-2):

$$ k_1 = \mathrm{RHS}(u^n,t),\quad k_2 = \mathrm{RHS}(u^n + \Delta t\,k_1, t+\Delta t),\quad
u^{n+1} = u^n + \tfrac{\Delta t}{2}(k_1 + k_2). $$ {#eq:numerics-2}

**Classical RK4** (fourth order) is @eq:numerics-3:

$$ u^{n+1} = u^n + \tfrac{\Delta t}{6}\,(k_1 + 2k_2 + 2k_3 + k_4). $$ {#eq:numerics-3}

**SSP RK3** (third order, strong stability preserving) blends each stage with
the earlier state, which keeps monotonicity for advection-dominated problems
under a CFL limit (@eq:ssprk3):

$$
\begin{aligned}
u^{(1)} &= u^n + \Delta t\,\mathrm{RHS}(u^n),\\
u^{(2)} &= \tfrac34 u^n + \tfrac14\left[u^{(1)} + \Delta t\,\mathrm{RHS}(u^{(1)})\right],\\
u^{n+1} &= \tfrac13 u^n + \tfrac23\left[u^{(2)} + \Delta t\,\mathrm{RHS}(u^{(2)})\right].
\end{aligned}
$$ {#eq:ssprk3}

SSP RK3 is the recommended all-rounder for wave and transport demonstrations.

**Adams-Bashforth 2** (second order, multistep) reuses the previous
right-hand side, and needs one starting step from another method (@eq:numerics-4):

$$ u^{n+1} = u^n + \tfrac{\Delta t}{2}\left(3\,\mathrm{RHS}(u^n) - \mathrm{RHS}(u^{n-1})\right). $$ {#eq:numerics-4}

These live in `pyCoastal.numerics.time_intg` as array functions,
`euler_step(u, t, dt, rhs)`, `rk2_step`, `rk4_step`, `rk3_ssp_step`, and
`ab2_step(u, u_prev, t, dt, rhs)`, where `rhs(u, t)` returns an array of the
same shape as `u`.

For multi-field states, `pyCoastal.numerics.scheme` provides integrator
classes that act on a dictionary of arrays:
`EulerIntegrator(dt)` and `SSPRK2Integrator(dt)` (Shu-Osher second-order
TVD), both with `step(state, rhs, t, **kwargs)` returning
`(new_state, new_time)`, where `rhs(state, t, **kwargs)` returns a
dictionary of tendencies.

### The `Solver` driver

`pyCoastal.numerics.solver.Solver(grid, physics, bc, integrator=None)`
sketches the loop: `Solver.run(t0, t_end, callback=None)` applies the
boundary conditions, takes one step through the integrator, and calls
`callback(state, t)` after each. It expects a `physics` object with
`initialize_state(grid)`, `rhs(state, t, grid=..., bc=...)` and a `dt`, and
a `bc` object with `apply(state, t)`.

It is a scaffold rather than the way this package is driven, and two things
have to be adapted before it runs. `BoundaryManager` exposes
`apply_all(fields, grid, t)`, not `apply(state, t)`, so it has to be wrapped;
and `physics.navier_stokes.rhs` takes `bc_mgr`, not the `bc` keyword the
solver passes. Every example in `examples/` writes its own time loop
instead, which is also the clearer way to see what a scheme does, and the
design applications that march in time (the port solver of @sec:port, the
one-line model of @sec:tools-oneline) carry their own loops.

### Stability

The CFL condition states that information carried by advection cannot move
farther than one cell per step. For an advective speed $c$ (@eq:cfl):

$$ \mathrm{CFL} = \max\left(\frac{c\,\Delta t}{\Delta x}, \frac{c\,\Delta t}{\Delta y}\right) < 1. $$ {#eq:cfl}

Diffusion imposes its own, often more severe, limit (@eq:diffusive):

$$ \Delta t \le \frac{1}{2\nu}\left(\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}\right)^{-1}. $$ {#eq:diffusive}

The time step must satisfy both. The design applications apply the same
rule internally: the port solver steps at a Courant number of 0.35 by
default, and the one-line shoreline model at 0.9 of its diffusive limit
(`tools.shoreline.suggest_dt`).

## Boundary conditions {#sec:bcs}

Boundary conditions close the discrete system. They fix a value, prescribe
a gradient, let waves or flow enter or leave, or enforce a wall, and they
control how signals reflect and how energy enters or exits the domain.

### Ghost-cell formulas

For a cell-centered scheme the classical formulas at $x = 0$ are:

- **Dirichlet** (value), $q|_\Gamma = q_D(x,t)$: $q_0 = 2 q_b - q_1$ with
  $q_b = q_D$.
- **Neumann** (gradient), $\partial q/\partial n|_\Gamma = g_N$:
  $q_0 = q_1 - \Delta x\, g_N$.
- **Solid wall**: $u_n = 0$, mirroring the normal component
  antisymmetrically; free slip mirrors the tangential velocity
  symmetrically, no slip antisymmetrically.
- **Sponge layer** (wave absorption): a damping zone relaxes the solution
  toward a reference state (@eq:sponge),

$$ \frac{\partial q}{\partial t} = -\sigma(x)\,[q - q_\mathrm{ref}], \qquad
\sigma(s) = \sigma_\mathrm{max}\sin^2\!\left(\frac{\pi s}{2}\right),\quad s = \frac{x - x_0}{L_\mathrm{sp}}\in[0,1]. $$ {#eq:sponge}

A sponge of $L_\mathrm{sp} \approx$ 1 to 3 wavelengths with
$\sigma_\mathrm{max} \sim \kappa c / L_\mathrm{sp}$, $\kappa \approx$ 3 to 6,
absorbs well; monitor reflections with gauges inside the domain.

### The boundary classes

`pyCoastal.numerics.boundary` implements boundary conditions that act
directly on the boundary cells, using the flat indices precomputed by the
grid. Every class takes a side name and a list of field keys and implements
`apply(fields, grid, t)`:

- `DirichletBC(location, var_names, value)`, where `value` is a number or
  a function of time;
- `NeumannBC(location, var_names, gradient=0.0)`, which copies the interior
  value plus `gradient * dx` onto the boundary;
- `WallBC(location, var_names)`, which sets the named fields (normally the
  normal velocity or flux) to zero;
- `SpongeBC(location, var_names, damping)`, which multiplies the boundary
  strip by a constant factor or by `damping(t, k)` evaluated per flat index
  `k`, so a spatial ramp can be built from the index;
- `BoundaryManager(bcs=())` holds a list of conditions; `add(bc)` registers
  one and `apply_all(fields, grid, t)` applies them all, in order, at time
  `t`.

```python
import numpy as np
from pyCoastal.numerics.grid import UniformGrid
from pyCoastal.numerics.boundary import (
    DirichletBC, NeumannBC, WallBC, SpongeBC, BoundaryManager,
)

grid = UniformGrid(shape=(200, 200), spacing=(2.0, 2.0))
fields = {"eta": np.zeros(grid.shape), "u": np.zeros(grid.shape),
          "v": np.zeros(grid.shape)}

bcs = BoundaryManager()
bcs.add(DirichletBC("south", ["eta"], lambda t: 0.5 * np.sin(2 * np.pi * t / 3.0)))
bcs.add(DirichletBC("west", ["u"], value=0.2))          # inflow
bcs.add(NeumannBC("east", ["u", "eta", "v"]))           # zero-gradient outflow
bcs.add(WallBC("north", ["v"]))                          # no normal flow
bcs.add(SpongeBC("north", ["eta"], damping=0.9))         # damp the strip
bcs.apply_all(fields, grid, t=0.0)
```

The complete version of this demonstration is
`examples/numerics/2D_irr_turb.py`.
