# `pyCoastal.physics.shallow_water`

Source: [`pyCoastal/physics/shallow_water.py`](../../pyCoastal/physics/shallow_water.py)

## `ShallowWater2D`

```python
class ShallowWater2D
```

```text
2D nonlinear shallow water equations:
  ∂h/∂t + ∂(h u)/∂x + ∂(h v)/∂y = 0
  ∂(h u)/∂t + ∂(h u^2 + ½ g h^2)/∂x + ∂(h u v)/∂y = Sx
  ∂(h v)/∂t + ∂(h u v)/∂x + ∂(h v^2 + ½ g h^2)/∂y = Sy
```

### `ShallowWater2D.fluxes` (method)

```python
ShallowWater2D.fluxes(self, h: np.ndarray, hu: np.ndarray, hv: np.ndarray)
```

```text
Compute the three flux‐pairs (in x and y) for the SWEs.
Returns (Fh, Gh), (Fhu, Ghu), (Fhv, Ghv)
```

### `ShallowWater2D.source_bed_slope` (method)

```python
ShallowWater2D.source_bed_slope(self, h: np.ndarray, zb: np.ndarray, grid=None)
```

```text
Return bed‐slope source terms Sx, Sy for momentum:
  Sx = - g h ∂zb/∂x,  Sy = - g h ∂zb/∂y

x is axis 0 and y is axis 1. Pass ``grid`` (a UniformGrid) so the
derivatives use the real cell spacing; without it the spacing is
taken as unity, which is only correct on a unit mesh.
```

