# `pyCoastal.tools.shoreline`

Source: [`pyCoastal/tools/shoreline.py`](../../pyCoastal/tools/shoreline.py)

## `OneLineParams`

```python
class OneLineParams
```

```text
Parameters for the one-line shoreline change model:
  D      active profile depth [m]
  p      porosity [-]
  Kcerc  alongshore transport coefficient [SI units so that Q is m^3/s]
  Hfree  offshore or structure-free breaking height field H_b,free(x) [m] or scalar
  alpha0 incident breaking angle relative to local shoreline, before feedback [rad] or array over x
  Kt     transmission factor field in [0,1] or scalar
  beta0  incident wave direction azimuth [rad], measured from +x axis pointing alongshore
  morfac morphological acceleration factor for faster adjustment
```

## `make_grid`

```python
def make_grid(Lx: float=1000.0, dx: float=5.0) -> tuple[np.ndarray, np.ndarray]
```

```text
Alongshore grid x and initial shoreline position y(x,0).
y is the cross-shore offset at MSL. y0=0 means straight shoreline.
```

## `breakwaters_geometry`

```python
def breakwaters_geometry(x: np.ndarray, tips: list[float] | tuple[float, ...], y_tip: float=150.0, crest_freeboard: float=2.0) -> dict
```

```text
Geometry for N detached rubble-mound breakwaters.
  tips    iterable of alongshore tip positions [m]
  y_tip   offshore distance of the tips from initial shoreline [m]
Returns dictionary with arrays over x.
```

## `kd_diffraction_field`

```python
def kd_diffraction_field(x: np.ndarray, geom: dict, beta0: float) -> np.ndarray
```

```text
Simple linear-diffraction shadow factor Kd(x) in [0,1].
Approximates each breakwater tip as a semi-infinite barrier.
Kd = 0.5*(1 + cos(theta)) clamped, where theta is the diffraction angle between
incident direction and the ray from the tip to the shoreline point (x,0).
Combined shadow from both tips taken as min over the two tips.
```

## `field_or_scalar_to_array`

```python
def field_or_scalar_to_array(val: float | ArrayLike, x: np.ndarray) -> np.ndarray
```

```text
Broadcast scalar to 1D array if needed, otherwise validate shape.
```

## `compute_flux_Qls`

```python
def compute_flux_Qls(x: np.ndarray, y: np.ndarray, pars: OneLineParams, kd: np.ndarray, Hfree: np.ndarray, Kt: np.ndarray, alpha0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]
```

```text
Q_ls = Kcerc * H_b^(5/2) * sin(2*alpha_b)
alpha_b = alpha0 - y_x  (small angle approximation, radians)
H_b = kd * Kt * Hfree
```

## `rhs_y_t`

```python
def rhs_y_t(x: np.ndarray, y: np.ndarray, pars: OneLineParams, kd: np.ndarray, Hfree: np.ndarray, Kt: np.ndarray, alpha0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```

```text
y_t = - 1/((1-p) D) * dQls/dx
```

## `suggest_dt`

```python
def suggest_dt(x: np.ndarray, pars: OneLineParams, Hb: np.ndarray) -> float
```

```text
Stability guidance for explicit scheme from linearized diffusion term:
  G = 2 Kcerc H_b^(5/2) / ((1-p) D)
  dt <= 0.45 * dx^2 / max(G)
```

## `apply_bcs`

```python
def apply_bcs(y: np.ndarray, bc: str='fixed_ends', yL: float=0.0, yR: float=0.0) -> np.ndarray
```

```text
Boundary conditions on y.
  fixed_ends: y(0)=yL, y(L)=yR
  zero_slope: y_x=0 at ends
```

## `run_one_line_model`

```python
def run_one_line_model() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict, OneLineParams, dict]
```

```text
Convenience runner with default 2-breakwater setup (backward-compatible).
Returns x, y_final, kd, hist, pars, geom.
```

