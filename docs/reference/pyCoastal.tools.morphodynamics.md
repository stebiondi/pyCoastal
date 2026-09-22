# `pyCoastal.tools.morphodynamics`

Source: [`pyCoastal/tools/morphodynamics.py`](../../pyCoastal/tools/morphodynamics.py)

## `circle_through_points`

```python
def circle_through_points(p1, p2, p3, n=200)
```

```text
Build a circular arc passing through three non-collinear points (x, y).
Returns x, y arrays following the branch that goes through p2.
```

## `two_point_arc`

```python
def two_point_arc(p_start, p_end, sag, n=200)
```

```text
Arc through two points with a prescribed sag (positive = bulge up, negative = bulge down).
```

## `build_tombolo_arcs`

```python
def build_tombolo_arcs(Lshore: float, Gb: float, Lb1: float, Lb2: float, yb: float, x_b1: float | None=None, x_b2: float | None=None, n_pts: int=200, sag_side_factor: float=0.3) -> tuple[np.ndarray, np.ndarray, dict]
```

```text
Build a schematic shoreline (Hsu/Evans-like) using three arcs: left, central, right.
Ye = 1.204*Yi - 0.07*Gb is the retreat depth below the breakwater crest line.
```

## `accretion_metrics`

```python
def accretion_metrics(x_eq: np.ndarray, y_eq: np.ndarray, geom: dict) -> tuple[float, float]
```

```text
Compute retreat (Yi-Ye) and accretion percentage including rectangles under T1–T2 and T3–T4.
```

## `bruuns_rule`

```python
def bruuns_rule(S: float, beta: float, L: float=None, h: float=None, B: float=None) -> float
```

```text
Estimate shoreline retreat (R) using Bruun's rule.
If L, h, and B are provided: R = S*L / (h + B)
Else: R = S / tan(beta)
```

## `exner_change`

```python
def exner_change(qs_dx: float, porosity: float=0.64) -> float
```

```text
Compute bed elevation change rate (∂η/∂t) from sediment divergence based on the Exner equation.
∂η/∂t = -1/(1–n) * qs_dx
```

## `linear_slope`

```python
def linear_slope(grid, north_level: float, south_level: float) -> np.ndarray
```

```text
Create a plane beach profile that is south_level at y=0 and north_level at y=L_y.
```

