# `pyCoastal.numerics.domain`

Source: [`pyCoastal/numerics/domain.py`](../../pyCoastal/numerics/domain.py)

Domain and mesh definitions for pyCoastal.
Provides 1D and 2D structured grid classes.

## `Mesh1D`

```python
class Mesh1D
```

```text
Simple 1D mesh.
Attributes
----------
x : np.ndarray
    Cell center coordinates.
dx : float
    Uniform grid spacing.
```

## `Mesh2D`

```python
class Mesh2D
```

```text
Rectangular 2D mesh.
Attributes
----------
x, y : np.ndarray
    2D arrays of cell‐center coordinates.
dx, dy : float
    Uniform spacings in x and y.
```

## `Domain`

```python
class Domain
```

```text
High‐level domain object. Reads geometry from config
and instantiates the appropriate mesh.
```

### `Domain.info` (method)

```python
Domain.info(self)
```

```text
Print a summary of the domain.
```

