# `pyCoastal.io`

Source: [`pyCoastal/io.py`](../../pyCoastal/io.py)

## `read_data`

```python
def read_data(path: 'str | os.PathLike') -> dict
```

```text
Read a YAML, JSON or INI file and return a python dict.

Accepts a Path as well as a string, so a caller can resolve the file
relative to its own location rather than to the shell's directory.
```

## `write_vtk`

```python
def write_vtk(grid, filename: str)
```

```text
Write a vtkUnstructuredGrid (or similar) to a .vtk file.
```

