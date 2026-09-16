"""
pyCoastal: A modular coastal‐process modeling framework.

Subpackages
-----------
config   Input‐file parsing (YAML/JSON/INI)
domain   Mesh & geometry definitions (1D/2D/3D)
numerics Numerical infrastructure (grids, schemes, solvers)
physics  Governing equations & closures
tools    Standalone formulae & utilities
boundary Boundary‐condition classes
io       I/O for VTK, CSV, NetCDF, etc.

Coordinate convention
---------------------
x and y span the horizontal plane and z is elevation, positive upward.
In every 2D array x is axis 0 and y is axis 1, matching UniformGrid, which
builds its coordinates with ``indexing="ij"`` and flattens as ``i*ny + j``.
"""

from importlib.metadata import PackageNotFoundError, version as _version

try:
    __version__ = _version("pyCoastal")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0.0.0.dev0"

# expose the two I/O entrypoints:
from .io import read_data, write_vtk
