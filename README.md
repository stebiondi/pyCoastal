<p align="center">
  <img src="media/pyCoastal_logo.png" width="400">
</p>

A Python toolbox for coastal, port and ocean engineering. A wave record
becomes a design condition, the design condition sizes a structure, and the
structure comes out as a dimensioned drawing with its quantities and notes.
Every relation names its source and states its range of validity.

<p align="center">
  <img src="media/seawall_sheet.png" alt="Seawall drawing sheet" width="800">
</p>

## Install

```bash
pip install pyCoastal            # PyPI
pip install -e ".[dev]"          # from a clone, with tests and plotting
```

## Quick start

```python
from pyCoastal.applications.structures import DesignConditions
from pyCoastal.applications.seawall import design_seawall
from pyCoastal.applications.sections import seawall_sheet

conditions = DesignConditions.from_peak_period(Hm0=2.8, Tp=9.5, depth=8.5)
wall = design_seawall(conditions, still_water_level=2.9, seabed_level=-5.6)
print(wall.summary())
seawall_sheet(wall, size="A3").save("seawall.png")
```

## What is inside

| Area | Modules |
|------|---------|
| Design conditions | `applications.extremes` (POT, annual maxima, bootstrap bands) |
| Structures | `applications.structures`, `seawall`, `piles`, `berthing` |
| Scour | `applications.scour` (pier, contraction, abutment over a tidal cycle) |
| Ports and rivers | `applications.port`, `channel`, `river` |
| Coastline | `applications.nourishment`, `surge`, `sediment` |
| Drawings | `drafting`, `applications.sections` (drawing sheets and DXF) |
| Numerics | `numerics`, `physics`, `tools` (grids, operators, SWE, NS, waves) |

Worked examples live in `examples/`, and `webapp/` holds the Coastal Design
Bench, a browser version of the design modules with the CoastalWiki
literature extract.

## Documentation

The full manual, covering theory, every module, every example and the
CoastalWiki knowledge base, is [`pyCoastal manual.pdf`](pyCoastal%20manual.pdf).
It is built from `docs/manual/` with `python docs/manual/build_manual.py`.

## Citation

> Biondi, S. (2025). *pyCoastal: a Python package for Coastal Engineering*,
> v0.2.0. https://github.com/stebiondi/pyCoastal

MIT License. Copyright (c) 2025 Stefano Biondi.
