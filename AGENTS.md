# AGENTS.md: a map of pyCoastal for AI agents

pyCoastal is a Python toolbox for coastal, port and ocean engineering: a
design chain (design condition, structure, loads, scour, navigation,
coastline, drawing) on top of a small numerical framework, plus PyCoaPedia,
a knowledge base of the peer-reviewed coastal and ocean engineering
literature. `pyCoastal manual.pdf` is the human-readable form; the same
content is available here as plain text or structured data. Start from this
file.

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

Query the database and request JSON output.

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

Every claim carries `regime` (the conditions in which it holds),
`evidence_type`, `confidence`, and a paper with a DOI. An answer taken from
PyCoaPedia states the regime and cites the DOI. Coverage follows the
screening process: a low claim count indicates limited screening of that
topic.

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
  outside their validity range and report the condition through `warnings`,
  `notes` and flags such as `within_range`, `impulsive`, `screening_only`
  and `current_governs`. These fields are part of the result.
- Design functions return design objects (`SeawallDesign`, `ChannelDesign`
  and others) with `summary()`. The drawing functions in
  `applications.sections` take those objects as input.

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

## Writing style for documentation

The manual and the docstrings are an engineering software reference.
`docs/manual/STYLE.md` is the specification and `docs/manual/style_check.py`
enforces it. In short: state implementation, assumptions, limitations and
causal dependencies directly, in an impersonal technical style, with short
declarative sentences.

Avoid rhetorical contrasts of the form "X, not Y", "not because X, but
because Y", "rather than" and "instead of" where a direct statement is
possible. Avoid metaphors, idioms, rhetorical explanation, reader-directed
language ("you", "note that") and evaluative adjectives ("honest",
"easiest", "the lesson"). State scope instead of what a routine is not:
"cohesive beds are not supported", not "cohesive beds are refused rather
than guessed at". Do not explain why a statement is true unless the reason
is technically necessary. Each section follows: definition, formulation,
implementation, inputs and outputs, limitations.

American English, no em-dashes. Name the source of every relation and state
its validity range. Keep the Python and `webapp/engine.js` in step: a change
to a design function requires the same change in the JavaScript and a fresh
`make_vectors.py` run.
