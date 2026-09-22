# `pyCoastal.numerics.boundary`

Source: [`pyCoastal/numerics/boundary.py`](../../pyCoastal/numerics/boundary.py)

pycoastal.boundary
------------------
Boundary‐condition classes for pyCoastal solvers.  
Defines Dirichlet, Neumann, Wall (no‐flow), and Sponge (damping) BCs.

Each BC must implement `apply(fields, grid, t)` where:
  - fields: dict of solution arrays, e.g. {"eta": η_array, "q": q_array, ...}
  - grid:   an object providing boundary indices, e.g. grid.boundary_indices["west"]
  - t:      current simulation time (s)

## `BoundaryCondition`

```python
class BoundaryCondition
```

```text
Abstract base class for all boundary conditions.
```

### `BoundaryCondition.apply` (method)

```python
BoundaryCondition.apply(self, fields: Mapping[str, np.ndarray], grid, t: float)
```

```text
Apply this BC to the given fields at time t.
```

## `DirichletBC`

```python
class DirichletBC(BoundaryCondition)
```

```text
Enforce a prescribed value at a boundary (ghost cell or face).
```

### `DirichletBC.apply` (method)

```python
DirichletBC.apply(self, fields, grid, t)
```

## `NeumannBC`

```python
class NeumannBC(BoundaryCondition)
```

```text
Zero‐gradient (or specified) Neumann BC: copy interior value to boundary.
```

### `NeumannBC.apply` (method)

```python
NeumannBC.apply(self, fields, grid, t)
```

## `WallBC`

```python
class WallBC(BoundaryCondition)
```

```text
No‐flow wall: set normal velocity (or flux) to zero.
```

### `WallBC.apply` (method)

```python
WallBC.apply(self, fields, grid, t)
```

## `SpongeBC`

```python
class SpongeBC(BoundaryCondition)
```

```text
Damping (sponge) layer: relax solution toward reference (often zero).
```

### `SpongeBC.apply` (method)

```python
SpongeBC.apply(self, fields, grid, t)
```

## `BoundaryManager`

```python
class BoundaryManager
```

```text
Holds and applies a list of boundary conditions each timestep.
```

### `BoundaryManager.add` (method)

```python
BoundaryManager.add(self, bc: BoundaryCondition)
```

### `BoundaryManager.apply_all` (method)

```python
BoundaryManager.apply_all(self, fields: Mapping[str, np.ndarray], grid, t: float)
```

```text
Apply every registered BC to the solution fields at time t.

Args:
    fields: dict of field arrays (modified in place)
    grid: solution grid, with boundary_indices, sponge_indices, etc.
    t: current time
```

