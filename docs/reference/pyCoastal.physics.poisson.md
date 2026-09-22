# `pyCoastal.physics.poisson`

Source: [`pyCoastal/physics/poisson.py`](../../pyCoastal/physics/poisson.py)

## `apply_dirichlet_bc`

```python
def apply_dirichlet_bc(phi, bc_mask, bc_values)
```

```text
Enforce Dirichlet BC on phi array in place.

bc_mask   : boolean array of same shape as phi; True where BC applies
bc_values : array same shape as phi; the prescribed phi values
```

## `build_laplacian`

```python
def build_laplacian(nx, ny, dx, dy)
```

```text
Build 2D Laplacian operator with Dirichlet zero BC on a regular grid.
Returns a scipy CSR sparse matrix of shape (nx*ny, nx*ny).
```

## `solve_direct`

```python
def solve_direct(rhs, dx, dy, bc_mask=None, bc_values=None)
```

```text
Solve ∇²φ = rhs with Dirichlet BC via a sparse direct solver (requires SciPy).
- rhs : 2D array of shape (ny, nx)
- dx, dy : grid spacing
- bc_mask, bc_values : optional masks/values for Dirichlet φ
Returns φ as 2D array.
```

## `solve_jacobi`

```python
def solve_jacobi(rhs, dx, dy, bc_mask=None, bc_values=None, tol=1e-06, maxiter=5000)
```

```text
Simple Jacobi iteration for ∇²φ = rhs with optional Dirichlet BC.
Returns φ after convergence or maxiter.
```

## `solve_poisson`

```python
def solve_poisson(rhs, dx, dy, bc_mask=None, bc_values=None, method='auto', **kwargs)
```

```text
Poisson solver interface.
  rhs        : 2D array of RHS values
  dx, dy     : grid spacing
  bc_mask    : bool array where Dirichlet BC applies
  bc_values  : array of same shape with prescribed φ values
  method     : 'direct', 'jacobi', or 'auto'
  **kwargs   : passed to the chosen solver (tol, maxiter, etc.)
```

