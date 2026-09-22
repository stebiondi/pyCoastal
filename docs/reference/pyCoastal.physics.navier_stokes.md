# `pyCoastal.physics.navier_stokes`

Source: [`pyCoastal/physics/navier_stokes.py`](../../pyCoastal/physics/navier_stokes.py)

## `initialize_state`

```python
def initialize_state(grid)
```

```text
Return a dict with zero u,v,p fields on the grid.
```

## `rhs`

```python
def rhs(state, t, grid, bc_mgr, ν=0.001)
```

```text
Compute convection + diffusion terms for u,v (no pressure).
Enforce velocity BCs on the resulting rhs arrays, then return them.
```

