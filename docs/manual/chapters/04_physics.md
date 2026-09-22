# Governing equations and closures {#sec:physics}

`pyCoastal.physics` holds the governing equations as building blocks: flux
functions and source terms that a solver assembles into a right-hand side,
a pressure-projection step, Poisson solvers, and eddy-viscosity closures.

## Shallow water equations

The shallow water equations describe a fluid layer whose horizontal scales
are much larger than its depth. They track the total depth and the
depth-averaged velocity, with the pressure hydrostatic. They capture wave
propagation, flooding and draining, and large-scale currents:

$$ \frac{\partial h}{\partial t} + \frac{\partial (hu)}{\partial x} + \frac{\partial (hv)}{\partial y} = 0, $$ {#eq:swe-mass}

$$ \frac{\partial (hu)}{\partial t} + \frac{\partial}{\partial x}\left(hu^2 + \tfrac12 g h^2\right) + \frac{\partial (huv)}{\partial y} = S_x, $$ {#eq:swe-x}

$$ \frac{\partial (hv)}{\partial t} + \frac{\partial (huv)}{\partial x} + \frac{\partial}{\partial y}\left(hv^2 + \tfrac12 g h^2\right) = S_y. $$ {#eq:swe-y}

Here $h$ is the total depth, $u$ and $v$ the depth-averaged velocities, and
$S_x$, $S_y$ collect bed slope, bottom friction, and Coriolis. When adding
sources, preserve the lake-at-rest balance.

`ShallowWater2D(g=9.81)` provides `fluxes(h, hu, hv)`, which returns the
three flux pairs $(F_h, G_h)$, $(F_{hu}, G_{hu})$, $(F_{hv}, G_{hv})$, and
`source_bed_slope(h, zb, grid=None)`, which returns
$S_x = -g h\,\partial z_b/\partial x$ and $S_y = -g h\,\partial z_b/\partial y$.
Pass the grid so the derivatives use the real spacing; without it the
spacing is taken as one.

## Incompressible Navier-Stokes

For incompressible viscous flow a popular explicit strategy is Chorin's
projection (fractional step) method: predict the velocity with advection
and diffusion, solve a Poisson equation for the pressure that removes the
divergence, then correct:

$$ \tilde{\mathbf u} = \mathbf u^n + \Delta t\left(N(\mathbf u^n) + \nu\nabla^2\mathbf u^n\right), $$ {#eq:ns-predict}

$$ \nabla^2 p^{n+1} = \frac{1}{\Delta t}\nabla\cdot\tilde{\mathbf u}, $$ {#eq:ns-poisson}

$$ \mathbf u^{n+1} = \tilde{\mathbf u} - \Delta t\,\nabla p^{n+1}, $$ {#eq:ns-correct}

with $\mathbf u = (u, v)$, $p$ the kinematic pressure, and $\nu$ the
viscosity. `pyCoastal.physics.navier_stokes` provides
`initialize_state(grid)`, which returns zero `u`, `v`, `p` fields, and
`rhs(state, t, grid, bc_mgr, ν=0.001)`, which returns the convection and
diffusion tendencies for `u` and `v` (the predictor of @eq:ns-predict),
with the velocity boundary conditions enforced on the result.

## Poisson solver

A Poisson solver computes a field whose Laplacian matches a given source.
It appears in the pressure projection, in potential flow, and in diffusion
steady states:

$$ \nabla^2\phi = b \text{ in } \Omega,\qquad \phi|_{\Gamma_D} = \phi_D,\qquad
\left.\frac{\partial\phi}{\partial n}\right|_{\Gamma_N} = g_N, $$

with the compatibility condition $\int_\Omega b\,\mathrm{d}\Omega +
\int_{\Gamma_N} g_N\,\mathrm{d}\Gamma = 0$ for a pure Neumann problem. The
five-point Laplacian of @eq:laplacian gives a sparse linear system. The
Jacobi iteration, with $h = \Delta x = \Delta y$, reads

$$ \phi^{(k+1)}_{i,j} = \tfrac14\left(\phi^{(k)}_{i+1,j} + \phi^{(k)}_{i-1,j} + \phi^{(k)}_{i,j+1} + \phi^{(k)}_{i,j-1} - h^2 b_{i,j}\right), $$

stopping when $\|b - A\phi^{(k)}\|_2 / \|b\|_2 < \varepsilon$.

`pyCoastal.physics.poisson` offers:

- `build_laplacian(nx, ny, dx, dy)`, the sparse CSR operator with zero
  Dirichlet boundaries (needs SciPy);
- `solve_direct(rhs, dx, dy, bc_mask=None, bc_values=None)`, a sparse direct
  solve;
- `solve_jacobi(rhs, dx, dy, bc_mask=None, bc_values=None, tol=1e-6,
  maxiter=5000)`;
- `solve_poisson(rhs, dx, dy, ..., method="auto")`, which picks the direct
  solver when SciPy is available and Jacobi otherwise;
- `apply_dirichlet_bc(phi, bc_mask, bc_values)`, which imposes Dirichlet
  values in place.

## Turbulence closures

When the grid cannot resolve all scales, eddy-viscosity closures emulate the
transport by unresolved motions. The closures here are educational
scaffolds: production RANS or LES needs careful calibration and near-wall
treatment.

**Smagorinsky (LES).** The eddy viscosity is proportional to the local strain
rate and the filter width:

$$ \nu_t = (C_s\Delta)^2|S|,\qquad |S| = \sqrt{2S_{ij}S_{ij}},\qquad S_{ij} = \tfrac12\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right), $$

with $C_s \approx$ 0.1 to 0.2. `SmagorinskyModel(Cs=0.17, filter_width=1.0)`
computes `eddy_viscosity(u, v, grid)`.

**$k$-$\varepsilon$ (RANS).** Two transport equations for the turbulent
kinetic energy $k$ and its dissipation $\varepsilon$, with
$\nu_t = C_\mu k^2/\varepsilon$:

$$ \partial_t k + U_j\partial_{x_j}k = P - \varepsilon + \partial_{x_j}\left[\left(\nu + \frac{\nu_t}{\sigma_k}\right)\partial_{x_j}k\right], $$

$$ \partial_t\varepsilon + U_j\partial_{x_j}\varepsilon = C_{\varepsilon1}\frac{\varepsilon}{k}P - C_{\varepsilon2}\frac{\varepsilon^2}{k} + \partial_{x_j}\left[\left(\nu + \frac{\nu_t}{\sigma_\varepsilon}\right)\partial_{x_j}\varepsilon\right], $$

with $P = 2\nu_t S_{ij}S_{ij}$. `KEpsilonModel(Cmu=0.09, sigma_k=1.0,
sigma_e=1.3, C1=1.44, C2=1.92)` returns the eddy viscosity from `k` and
`eps`; the transport equations belong to the solver.

**$k$-$\omega$ (RANS).** Pairs $k$ with the specific dissipation
$\omega = \varepsilon/k$, which behaves better near walls, with
$\nu_t = k/\omega$:

$$ \partial_t k + U_j\partial_{x_j}k = P - \beta^* k\omega + \partial_{x_j}\left[(\nu + \sigma_k^*\nu_t)\partial_{x_j}k\right], $$

$$ \partial_t\omega + U_j\partial_{x_j}\omega = \alpha\frac{\omega}{k}P - \beta\omega^2 + \partial_{x_j}\left[(\nu + \sigma_\omega\nu_t)\partial_{x_j}\omega\right]. $$

`KOmegaModel(sigma_k=2.0, sigma_ω=2.0, beta_star=0.09, beta=0.075,
gamma=0.52)` returns `k / ω` from `eddy_viscosity(k, ω)`.
