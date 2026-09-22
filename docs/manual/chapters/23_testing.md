# Part VIII. Quality assurance {.part .unnumbered}

# The test suite {#sec:testing}

A design code that nobody checks is a liability, so pyCoastal carries a test
suite that grew with every module. It runs with

```bash
python -m pytest tests/
```

and in continuous integration on Ubuntu and Windows under Python 3.10, 3.11,
and 3.13 on every push to `main` and every pull request.

## What the tests check

The tests are not only regression checks. Most of them pin a result to an
independent reference, and the kinds of check recur across modules:

- **Published values and limits.** The Van der Meer plunging and surging
  branches against the published forms; the Sumer and Fredsoe relation collapsing to the
  waves-only form at $U_{cw} = 0$ and to $S/D = 1.3$ in pure current; the
  toe scour recovering Xie at $K_r = 1$; Dean's profile scale against his
  table.
- **Analytical solutions.** The one-line solver against Pelnard-Considere;
  the port solver against the semi-infinite breakwater shadow; the fill
  volume and critical volume for matched sand; normal depth against
  Manning's equation.
- **Physical consistency.** Monotonic responses (more overtopping at lower
  crest, deeper scour at higher velocity), conservation (volume in the
  nourishment model), and conventions (axis order, units, sign of levels).
- **Honest failure.** Functions that must refuse (cohesive beds in scour,
  normal depth on an adverse slope, non-positive freeboard in the
  overtopping relations) raise, and functions that must warn outside their
  range do so.
- **Drawings.** Sheets reject unknown paper sizes and report their fitted
  scale, and DXF export round-trips one line per edge with every layer
  queued.

## Tests by file

<!-- test-table -->

## The browser engine

The JavaScript engine of PyCoaTools is checked against the
Python by `webapp/verify_engine.py` on the reference cases of
`webapp/make_vectors.py`, and the page repeats the comparison on load
(@sec:webapp). `webapp/verify_app.py` executes every module of the page
once. These verifiers are not yet wired into continuous integration and are
run by hand before publishing the app.
