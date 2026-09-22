# `pyCoastal.tools.wave`

Source: [`pyCoastal/tools/wave.py`](../../pyCoastal/tools/wave.py)

## `dispersion`

```python
def dispersion(T: float, h: float, g: float=9.81, tol: float=1e-12) -> float
```

```text
Solve the linear dispersion relation for the wavelength L.

Solves omega^2 = g k tanh(k h) by Newton-Raphson, starting from the
explicit Fenton & McKee (1990) approximation. This converges in a handful
of iterations across the full range from deep water to the shallow-water
limit.

Args:
    T (float): Wave period (s)
    h (float): Water depth (m)
    g (float, optional): Gravity acceleration (m/s^2). Default: 9.81.
    tol (float, optional): Relative convergence tolerance on k.

Returns:
    float: Wavelength L (m)

Raises:
    ValueError: If T or h is not strictly positive.
```

## `wave_number`

```python
def wave_number(T: float, h: float) -> float
```

```text
Compute wave number k = 2π / L.

Args:
    T (float): Period (s)
    h (float): Depth (m)

Returns:
    float: Wave number k (rad/m)
```

## `surf_similarity`

```python
def surf_similarity(alpha: float, H: float, T: float) -> float
```

```text
Compute the Iribarren (surf similarity) number ξ.

ξ = tan(alpha) / sqrt(H / L0), where L0 = g*T²/(2π)

Args:
    alpha (float): Slope angle (radians)
    H (float): Wave height (m)
    T (float): Wave period (s)

Returns:
    float: Iribarren number ξ
```

## `breaker_type`

```python
def breaker_type(alpha: float, H: float, T: float) -> str
```

```text
Determine wave breaking type based on Iribarren number.

Classifications:
- ξ < 0.4     : Spilling breaker
- 0.4 ≤ ξ ≤ 2 : Plunging breaker
- ξ > 2       : Collapsing/surging breaker

Args:
    alpha (float): Slope angle (rad)
    H (float): Wave height (m)
    T (float): Wave period (s)

Returns:
    str: 'Spilling', 'Plunging', or 'Surging' (collapsing)
```

## `ursell_number`

```python
def ursell_number(H: float, T: float, h: float) -> tuple
```

```text
Calculate Ursell number U = H*L²/h³ and provide interpretation.

Args:
    H (float): Wave height (m)
    T (float): Period (s)
    h (float): Depth (m)

Returns:
    (float, str): Ursell number U and interpretation.
```

## `wave_setup`

```python
def wave_setup(Hb: float, gamma: float=0.8) -> float
```

```text
Estimate mean water level increase at shoreline due to wave setup.
η = (5/16) * γ * Hb
```

## `generate_irregular_wave`

```python
def generate_irregular_wave(Hs: float, Tp: float, duration: float, dt: float, spectrum: str='pm', gamma: float=3.3) -> tuple[np.ndarray, np.ndarray]
```

```text
Generate one realization of an irregular wave time-series η(t).

Args:
  Hs        : significant wave height [m]
  Tp        : peak period               [s]
  duration  : total record length       [s]
  dt        : time step                 [s]
  spectrum  : 'pm' or 'jonswap'
  gamma     : peak enhancement factor (JONSWAP only)

Returns:
  t   : time array of length N = ceil(duration/dt)
  eta : η(t) time-series
```

