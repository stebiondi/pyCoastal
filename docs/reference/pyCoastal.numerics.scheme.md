# `pyCoastal.numerics.scheme`

Source: [`pyCoastal/numerics/scheme.py`](../../pyCoastal/numerics/scheme.py)

Time‐integration and spatial discretization schemes.

## `TimeIntegrator`

```python
class TimeIntegrator
```

```text
Base class for explicit time integrators (e.g. Euler, RK2, RK3).
```

### `TimeIntegrator.step` (method)

```python
TimeIntegrator.step(self, state, rhs, t, **kwargs)
```

```text
Advance 'state' one time step.
state : dict of numpy arrays (e.g. { "u":…, "h":…, … })
rhs   : function(state, t, **kwargs) → dict of tendencies
t     : current time
returns (new_state, new_time)
```

## `EulerIntegrator`

```python
class EulerIntegrator(TimeIntegrator)
```

### `EulerIntegrator.step` (method)

```python
EulerIntegrator.step(self, state, rhs, t, **kwargs)
```

## `SSPRK2Integrator`

```python
class SSPRK2Integrator(TimeIntegrator)
```

### `SSPRK2Integrator.step` (method)

```python
SSPRK2Integrator.step(self, state, rhs, t, **kwargs)
```

## `central_difference`

```python
def central_difference(phi, spacing, axis)
```

```text
Second‐order central difference in 'axis'.
```

## `upwind`

```python
def upwind(phi, vel, spacing, axis)
```

```text
First‐order upwind scheme for advection term vel·∇phi.
vel: array of the same shape giving velocity component in 'axis'.
```

