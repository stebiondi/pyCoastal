# `pyCoastal.numerics.grid`

Source: [`pyCoastal/numerics/grid.py`](../../pyCoastal/numerics/grid.py)

Basic Cartesian grid for 1D/2D/3D domains, now with boundary‐index support
for Dirichlet/Neumann/Sponge BCs.

## `UniformGrid`

```python
class UniformGrid
```

### `UniformGrid.neumann_indices` (method)

```python
UniformGrid.neumann_indices(self, side: str)
```

### `UniformGrid.n_cells` (property)

```python
UniformGrid.n_cells(self)
```

### `UniformGrid.cell_volume` (property)

```python
UniformGrid.cell_volume(self)
```

### `UniformGrid.cell_indices` (method)

```python
UniformGrid.cell_indices(self)
```

