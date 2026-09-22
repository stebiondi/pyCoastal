# `pyCoastal.numerics.operators`

Source: [`pyCoastal/numerics/operators.py`](../../pyCoastal/numerics/operators.py)

## `laplacian`

```python
def laplacian(field: np.ndarray, grid) -> np.ndarray
```

```text
Compute the 5-point Laplacian of `field` on a UniformGrid, using
centered finite differences and periodic (roll) indexing.

Parameters
----------
field : (nx,ny) array
  Input scalar field.
grid : UniformGrid
  The grid, provides grid.spacing = (dx, dy).

Returns
-------
lap : (nx,ny) array
  The discrete Laplacian ∂²/∂x² + ∂²/∂y².
```

## `gradient`

```python
def gradient(field, grid)
```

```text
Centered gradient ∇f → (fx, fy) on cell centers.

x is axis 0 and y is axis 1, matching UniformGrid and grad_x/grad_y.
```

## `grad_x`

```python
def grad_x(field, grid)
```

```text
∂/∂x using centered differences.
```

## `grad_y`

```python
def grad_y(field, grid)
```

```text
∂/∂y using centered differences.
```

## `upwind_x`

```python
def upwind_x(field, u, grid)
```

```text
First-order upwind in x: uses flow sign in u to pick difference.
```

## `upwind_y`

```python
def upwind_y(field, v, grid)
```

```text
First-order upwind in y.
```

## `divergence`

```python
def divergence(ux, uy, grid)
```

```text
Centered divergence ∇·u on cell centers.
```

## `curl_z`

```python
def curl_z(u, v, grid)
```

```text
∇×(u,v) in 2D gives scalar k-component: ∂v/∂x − ∂u/∂y.
```

## `biharmonic`

```python
def biharmonic(field, grid)
```

```text
Δ² field = Laplacian(Laplacian(field)).
```

## `mixed_xy`

```python
def mixed_xy(field, grid)
```

```text
∂²/∂x∂y of field (central).
```

## `advect`

```python
def advect(u, v, field, grid, scheme='upwind')
```

```text
Compute u·∇field + v·∇field using chosen scheme.
```

## `smooth3`

```python
def smooth3(field, grid)
```

```text
Simple 5-point smoothing filter (weights sum to one).
```

