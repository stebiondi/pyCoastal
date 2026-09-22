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

From a clone, in editable mode, for development and for running the
examples:

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
├── pyCoastal/pedia/         PyCoaPedia reader and its SQLite database
├── pedia/                   PyCoaPedia as Markdown, its schema, and the builder
├── webapp/                  PyCoaTools and the PyCoaPedia explorer (browser)
├── media/                   figures, animations, drawing sheets, DXF files
├── docs/                    this manual (docs/manual), the API reference
│                            (docs/reference) and the example index
├── AGENTS.md, llms.txt      the repository map for AI agents
├── paper/                   JOSS-style paper
└── pyCoastal manual.pdf     this manual
```

## Conventions

The following conventions apply in every module. Departures are recorded in
the docstring of the module concerned.

**Coordinates.** `x` and `y` span the horizontal plane and `z` is elevation,
positive upward. In 2D arrays `x` is axis 0 and `y` is axis 1, matching
`UniformGrid`, which builds its coordinates with `indexing="ij"` and
flattens as `i*ny + j`. In cross-shore work `x` is the chainage, and in
alongshore work (the one-line model) `x` is alongshore and `y` is the
cross-shore shoreline offset, positive seaward.

The design applications and the operators follow that axis order. Two older
pieces of the numerical framework do not, and this manual says so where they
appear: `numerics.domain.Mesh2D` builds its coordinate arrays with NumPy's
default `indexing="xy"`, so they are shaped (ny, nx), and the solvers in
`physics.poisson` take their right-hand side in that same (ny, nx) form.

**Units.** SI throughout: meters, seconds, kilograms, newtons. Wall forces
and wall weights are kN per meter run. Overtopping discharge is liters per
second per meter (l/s/m), the unit of the tolerability tables. Ship speeds
are knots in the functions whose source formula is written in knots. Grain
sizes are meters. Geotechnical and navigational angles are degrees;
wave-direction and slope-angle arguments of the low-level tools are radians.
Each function states the unit it takes.

**Levels.** Levels are meters relative to chart datum (m CD) and increase
upward. Depths and draughts are positive. Pier scour drawings use the
initial bed as datum; dimensions on those drawings are depths below it.

**Wave parameters.** Design wave heights are spectral significant heights
$H_{m0}$ at the structure toe. EurOtop relations take the spectral period
$T_{m-1,0}$. `DesignConditions.from_peak_period` converts a peak period with
$T_{m-1,0} = T_p/1.1$. Goda's pressure method is formulated on the
significant period; the seawall module passes $T_p$ to it.

**Slopes.** Slope input: $\cot\alpha$, defined as horizontal run per unit
rise. This convention is used in the generated drawings.

## Quick start

A seawall from a design condition to a drawing sheet:

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

The printed summary is the design report: crest level, founding level, base
dimensions, wave force, safety factors and bearing pressures. The full
worked example is in @sec:seawall.

Every example in `examples/` runs from the repository root:

```bash
python examples/seawall_section.py
python examples/breakwater_design.py
python examples/design_wave.py
```

and writes its figures to `media/`. `docs/examples.md` lists them all.

## Reading case files

The numerical examples read their parameters from YAML files in
`examples/configs/`. Two helpers parse case files into dictionaries:

- `pyCoastal.config.load_config(path)` reads `.yaml`/`.yml` (PyYAML),
  `.json`, and `.ini`/`.cfg` files;
- `pyCoastal.io.read_data(path)` does the same for any path-like object,
  and `pyCoastal.io.write_vtk(grid, filename)` writes a VTK grid object to
  a legacy `.vtk` file (needs the `vtk` extra).

These are used by the simulation examples of @sec:simulations.
`pyCoastal.numerics.domain.Domain(cfg)` builds a `Mesh1D` or `Mesh2D` from a
`domain:` block with `dimension`, `x0`, `x1`, `nx` (and `y0`, `y1`, `ny` in
2D).
