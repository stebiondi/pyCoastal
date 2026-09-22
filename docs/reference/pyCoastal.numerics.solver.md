# `pyCoastal.numerics.solver`

Source: [`pyCoastal/numerics/solver.py`](../../pyCoastal/numerics/solver.py)

High‐level Solver: ties together grid, physics, boundary conditions, and time‐integrator.

## `Solver`

```python
class Solver
```

### `Solver.run` (method)

```python
Solver.run(self, t0, t_end, callback=None)
```

```text
March from t0 to t_end.
callback(state, t) will be called after each step (for output/plotting).
```

