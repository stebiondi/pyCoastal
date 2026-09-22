# `pyCoastal.physics.turbulence`

Source: [`pyCoastal/physics/turbulence.py`](../../pyCoastal/physics/turbulence.py)

## `SmagorinskyModel`

```python
class SmagorinskyModel
```

```text
Large-eddy eddy viscosity: ``nu_t = (C_s * Delta)**2 * |S|``
```

### `SmagorinskyModel.eddy_viscosity` (method)

```python
SmagorinskyModel.eddy_viscosity(self, u: np.ndarray, v: np.ndarray, grid=None)
```

```text
Strain-rate magnitude ``|S| = sqrt(2 S_ij S_ij)``.

x is axis 0 and y is axis 1. Pass ``grid`` so the velocity
gradients use the real cell spacing.
```

## `KEpsilonModel`

```python
class KEpsilonModel
```

```text
k–ε two‐equation closure in eddy‐viscosity form:
  ν_t = C_μ k^2/ε
  transport eqns for k and ε must be added by solver
```

### `KEpsilonModel.eddy_viscosity` (method)

```python
KEpsilonModel.eddy_viscosity(self, k: np.ndarray, eps: np.ndarray)
```

## `KOmegaModel`

```python
class KOmegaModel
```

```text
k–ω (Wilcox) two‐equation closure:
  ν_t = k/ω
```

### `KOmegaModel.eddy_viscosity` (method)

```python
KOmegaModel.eddy_viscosity(self, k: np.ndarray, ω: np.ndarray)
```

