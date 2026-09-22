# Installation and first steps {#sec:install}

## Requirements

pyCoastal needs Python 3.10 or newer. The runtime dependencies are kept to
two, so the design modules install anywhere:

- `numpy >= 1.21` for arrays, gradients, and linear algebra;
- `PyYAML >= 5.4` for YAML case files.

Everything else is optional and imported lazily, only by the functions that
need it (@tbl:extras).

: Optional dependency groups declared in `pyproject.toml`. {#tbl:extras}

| Extra | Installs | Needed for |
|-------|----------|-----------|
| `sparse` | `scipy >= 1.7` | sparse direct solver in `physics.poisson` |
| `vtk` | `vtk >= 9.0` | `io.write_vtk` |
| `plots` | `matplotlib >= 3.4` | `drafting`, `applications.sections`, `plotting`, and the examples |
| `dev` | `pytest`, `scipy`, `matplotlib` | running the test suite |
| `docs` | `sphinx`, `sphinx-rtd-theme` | the Sphinx API pages in `docs/` |

## Installing

From PyPI:

```bash
pip install pyCoastal
pip install "pyCoastal[plots]"      # with drawings and plotting
```

From a clone, in editable mode, which is the right choice for development
and for running the examples:

```bash
git clone https://github.com/stebiondi/pyCoastal.git
cd pyCoastal
python -m venv .venv
source .venv/bin/activate           # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Check the installation and run the tests:

```bash
python -c "import pyCoastal; print(pyCoastal.__version__)"
python -m pytest tests/
```

Continuous integration runs the same suite on Ubuntu and Windows under
Python 3.10, 3.11, and 3.13 on every push to `main` and on every pull
request (`.github/workflows/tests.yml`). A separate workflow builds and
publishes the distribution to PyPI (`.github/workflows/publish.yml`).

## Repository layout

```text
pyCoastal/
├── pyCoastal/               the package
│   ├── numerics/            grids, operators, time integrators, BCs, solver
│   ├── physics/             shallow water, Navier-Stokes, Poisson, turbulence
│   ├── tools/               standalone formulae: waves, sediment, structures,
│   │                        one-line shoreline, morphodynamics
│   ├── applications/        design modules (extremes, structures, seawall,
│   │                        port, piles, scour, river, channel, berthing,
│   │                        nourishment, surge, sediment, sections)
│   ├── drafting.py          drawing primitives, sheets, title blocks, DXF
│   ├── plotting.py          color maps and helpers for the examples
│   ├── config.py, io.py     case-file reading and VTK output
├── examples/                worked examples and their YAML configs
├── tests/                   the pytest suite
├── webapp/                  Coastal Design Bench (browser app)
├── media/                   figures, animations, drawing sheets, DXF files
├── docs/                    Sphinx sources and this manual (docs/manual)
├── paper/                   JOSS-style paper
└── pyCoastal manual.pdf     this manual
```

## Conventions

The same conventions hold in every module. Where a module departs from them
its docstring says so.

**Coordinates.** `x` and `y` span the horizontal plane and `z` is elevation,
positive upward. In every 2D array `x` is axis 0 and `y` is axis 1, matching
`UniformGrid`, which builds its coordinates with `indexing="ij"` and
flattens as `i*ny + j`. In cross-shore work `x` is the chainage and in
alongshore work (the one-line model) `x` is alongshore and `y` is the
cross-shore shoreline offset, positive seaward.

**Units.** SI throughout: meters, seconds, kilograms, newtons. Forces on
walls and walls' weights are kN per meter run; overtopping discharges are
liters per second per meter (l/s/m), the unit of the tolerability tables;
ship speeds are in knots where the formula is written in knots and every
such function says so. Grain sizes are meters, not millimeters. Angles are
degrees where a geotechnical or navigational input is conventionally stated
in degrees, and radians in wave-direction and slope-angle arguments of the
low-level tools; each function states which.

**Levels.** Levels are meters relative to chart datum (m CD) and increase
upward. Depths and draughts are positive numbers. Pier scour drawings use
the initial bed as datum, because every dimension there is a depth below it.

**Wave parameters.** Design wave heights are spectral significant heights
$H_{m0}$ at the toe of the structure. EurOtop relations use the spectral
period $T_{m-1,0}$; if only the peak period is known,
`DesignConditions.from_peak_period` converts with $T_{m-1,0} = T_p/1.1$.
Goda's pressure method is written around the significant period, so the
seawall module passes $T_p$ to it.

**Slopes.** Slopes are given as $\cot\alpha$, the horizontal run per unit
rise, because that is how they appear on drawings.

## Quick start

A seawall from a design condition to a drawing sheet, in eight lines:

```python
from pyCoastal.applications.structures import DesignConditions
from pyCoastal.applications.seawall import design_seawall
from pyCoastal.applications.sections import seawall_sheet

conditions = DesignConditions.from_peak_period(Hm0=2.8, Tp=9.5, depth=8.5)
wall = design_seawall(conditions, still_water_level=2.9, seabed_level=-5.6,
                      tolerable_use="trained_staff")
print(wall.summary())
sheet = seawall_sheet(wall, project="Bayfront promenade protection", size="A3")
sheet.save("seawall.png")     # 600 dpi, at a true scale stated on the sheet
sheet.to_dxf("seawall.dxf")   # the geometry on named layers, for CAD
```

The printed summary is the design report, in the order an engineer checks
it (crest, founding level, base, wave force, safety factors, bearing). The
full worked example is in @sec:seawall.

Every example in `examples/` runs from the repository root:

```bash
python examples/seawall_section.py
python examples/breakwater_design.py
python examples/design_wave.py
```

and writes its figures to `media/`. Appendix B lists the full source of
each one.

## Reading case files

The numerical examples read their parameters from YAML files in
`examples/configs/`. Two helpers parse case files into dictionaries:

- `pyCoastal.config.load_config(path)` reads `.yaml`/`.yml` (PyYAML),
  `.json`, and `.ini`/`.cfg` files;
- `pyCoastal.io.read_data(path)` does the same for any path-like object,
  and `pyCoastal.io.write_vtk(grid, filename)` writes a VTK grid object to
  a legacy `.vtk` file (needs the `vtk` extra).

`pyCoastal.numerics.domain.Domain(cfg)` builds a `Mesh1D` or `Mesh2D` from a
`domain:` block with `dimension`, `x0`, `x1`, `nx` (and `y0`, `y1`, `ny` in
2D).
