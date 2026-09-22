# AGENTS.md: a map of pyCoastal for AI agents

pyCoastal is a Python toolbox for coastal, port and ocean engineering: a
design chain (design condition, structure, loads, scour, navigation,
coastline, drawing) on top of a small numerical framework, plus PyCoaPedia,
a knowledge base of the peer-reviewed coastal and ocean engineering
literature. Humans read `pyCoastal manual.pdf`; everything in it also exists
here as plain text or data. Start from this file.

## Where things are

| Need | Look in |
|------|---------|
| Theory, equations, usage, worked examples | `docs/manual/chapters/*.md` (the source of the PDF, Markdown with LaTeX math) |
| API: every public class, function, constant | `docs/reference/<module>.md`, index in `docs/reference/README.md` |
| Example scripts and what each shows | `docs/examples.md`, scripts in `examples/`, captured output in `docs/manual/outputs/` |
| Source code | `pyCoastal/` (`applications/` design modules, `numerics/`, `physics/`, `tools/`, `drafting.py`) |
| Tests (what the code is verified against) | `tests/test_*.py` |
| Literature: topics, synthesis, claims, equations, papers | `pyCoastal/pedia/pycoapedia.sqlite`, read with `python -m pyCoastal.pedia` or SQL; Markdown in `pedia/topics/`; schema in `pedia/SCHEMA.md` |
| Browser apps | `webapp/index.html` (PyCoaTools, design modules), `webapp/pedia.html` (PyCoaPedia explorer) |

## Querying PyCoaPedia

Prefer the database over reading pages one by one. Ask for JSON.

```bash
python -m pyCoastal.pedia --json search "toe scour vertical wall" --limit 20
python -m pyCoastal.pedia --json search "overtopping" --kind claim --topic structures
python -m pyCoastal.pedia --json topic structures.overtopping     # synthesis, claims, equations, papers
python -m pyCoastal.pedia --json module seawall                   # topics behind a design module
python -m pyCoastal.pedia --json paper 2229                       # abstract, extraction, claims
python -m pyCoastal.pedia --json sql "SELECT id, label, n_claims FROM topics WHERE parent_id IS NULL"
```

Or in Python: `from pyCoastal import pedia` then `pedia.search(...)`,
`pedia.topic(...)`, `pedia.claims(topic, evidence=..., confidence=...)`,
`pedia.related_claims(id)`, `pedia.paper(doi=...)`, `pedia.for_module(...)`.

Every claim carries `regime` (where it holds), `evidence_type`,
`confidence`, and a paper with a DOI. When answering from PyCoaPedia, state
the regime and cite the DOI. Coverage is uneven: few claims on a topic means
it has not been screened closely, not that nothing is known.

## Conventions the code follows

- SI units. Wall forces in kN per meter run; overtopping in l/s/m; ship
  speeds in knots only where a formula is written in knots (the docstring
  says so). Grain sizes in meters.
- Levels in meters to chart datum, positive up. Depths and draughts positive.
- 2D arrays: x on axis 0, y on axis 1 (`indexing="ij"`).
- Design wave height is spectral `Hm0` at the toe; EurOtop uses `Tm-1,0`
  (`DesignConditions.from_peak_period` converts `Tp / 1.1`).
- Slopes as `cot_alpha` (horizontal per unit rise).
- Every relation names its source in the docstring. Functions compute
  outside their validity range but say so: read `warnings`, `notes`, and flags
  such as `within_range`, `impulsive`, `screening_only`, `current_governs`.
  These are part of the result, not noise.
- Design functions return design objects (`SeawallDesign`, `ChannelDesign`,
  ...) with `summary()`; drawing functions in `applications.sections` take
  those objects, never loose numbers.

## Running things

```bash
pip install -e ".[dev]"            # numpy, PyYAML, plus pytest, scipy, matplotlib
python -m pytest tests/            # the suite; must stay green
python examples/seawall_section.py # any example, from the repository root
```

## Regenerating derived files (never edit them by hand)

| Files | Command |
|-------|---------|
| `pyCoastal manual.pdf`, `docs/reference/`, `docs/examples.md` | `python docs/manual/build_manual.py` (needs pandoc and Tectonic or xelatex) |
| `docs/manual/outputs/*.txt` | `python docs/manual/build_manual.py --run-examples` |
| `pyCoastal/pedia/pycoapedia.sqlite`, `pedia/topics/`, `pedia/README.md`, `pedia/modules.md`, `webapp/knowledge.json` | `python pedia/build_pedia.py --db <source research database>` |
| `webapp/vectors.json` | `python webapp/make_vectors.py`, then `python webapp/verify_engine.py` |

## Writing style for changes

American English, no em-dashes, plain technical prose. Name the source of
every relation and state its range. Keep the Python and `webapp/engine.js`
in step: a change to a design function needs the same change in the
JavaScript and a fresh `make_vectors.py` run.
