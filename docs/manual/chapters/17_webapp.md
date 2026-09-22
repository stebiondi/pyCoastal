# Part V. PyCoaTools {.part .unnumbered}

# The browser app {#sec:webapp}

*Directory:* `webapp/`.

PyCoaTools is a static web page that runs the pyCoastal design
modules in the browser, draws the result as a sheet, writes the design
report, and puts next to it what the peer-reviewed literature says about the
ground the relations stand on. Its tagline is the whole idea: size a
structure with the pyCoastal relations, then read what the literature says
about the ground they stand on.

## How it works

A browser has no Python, so `webapp/engine.js` carries a JavaScript
transliteration of the design modules, function for function: where the
Python bisects, the JavaScript bisects; where the Python iterates on the base
width, so does the JavaScript. Units follow the Python. A second
implementation of a design code is worth having only if somebody checks it,
so:

- `make_vectors.py` dumps reference cases straight out of pyCoastal into
  `vectors.json`, deliberately including awkward ones (the surging armor
  branch, an impulsive wall, a depth-limited Goda wave, drag- and
  inertia-dominated piles, a resultant outside the middle third);
- `verify_engine.py` runs `engine.js` in QuickJS against those cases and
  fails on any disagreement beyond floating-point noise;
- the page re-runs the same comparison on load and shows the result as a
  chip in the masthead, so the user sees it too.

`app.js` defines the modules, their inputs, the run functions, the report,
and the checks; `draw.js` draws each module's sheet as SVG; and
`index.html` is the application frame: a fixed masthead, an input panel, the
drawing, the design report, and the Theory and sources panel, each scrolling
on its own. Above 1560 px the report sits beside the drawing in its own pane.
The page uses the fonts the desktop already has (Segoe UI and Consolas) and
fetches no web font, so the first frame is correct.

## Modules and inputs

The app has six modules. Each input is a slider with a range, a select, or a
toggle, and the defaults follow the worked examples of Part III.

<!-- webapp-inputs -->

![Seawall module sheet as rendered by `draw.js`.](media/webapp/seawall.png){#fig:web-seawall width=85%}

![Channel module sheet.](media/webapp/channel.png){#fig:web-channel width=85%}

![Monopile module sheet.](media/webapp/monopile.png){#fig:web-monopile width=85%}

![Nourishment module, planform view.](media/webapp/nourishment_planform.png){#fig:web-nourishment width=85%}

![Return values module.](media/webapp/extremes.png){#fig:web-extremes width=85%}

## Theory and sources

The Theory and sources panel reads `knowledge.json`, the extract of
PyCoaPedia that `pedia/build_pedia.py` writes. The source database is about
150 MB of SQLite, which no browser will open; the app needs the topic tree,
the curated synthesis for each topic, the atomic claims with their regime
bounds, the equations, and enough paper metadata to cite and link, which
comes to under 2 MB. Each design module is mapped to the PyCoaPedia topics that
bear on it (the mapping is deliberately generous, because a design relation
sits where several topics meet), and the panel shows each topic's synthesis,
claims, and equations with a DOI behind every piece. Coverage is uneven by
design: PyCoaPedia records what has been screened, not what exists. The
PyCoaPedia button in the masthead opens the full explorer, described with
the rest of the knowledge base in @sec:pedia.

## Verification and review tools

- `verify_app.py` loads the page's own scripts into QuickJS behind a stub
  DOM, so the module definitions, run functions, report and check builders,
  and in-page verification all execute at least once before publishing. It
  catches the things that break a static page: a typo in a function name, an
  input key that no run function reads, a check that throws on the defaults.
- `render_preview.py` runs `draw.js` in QuickJS behind a DOM stub that
  serializes to real SVG, then rasterizes it, because a script that runs can
  still draw nothing (a sheet that paints its background last passes every
  check and shows a blank page). Output goes to `media/webapp/`.
- `rasterise.py` draws the app's SVG with matplotlib, since the SVG is
  deliberately narrow (paths of M, L, H, V, Z plus rects, circles, and
  text). It is a review tool: is the thing on the page, in the right place,
  in the right order.

```bash
pip install quickjs svglib
python webapp/make_vectors.py --out webapp/vectors.json
python webapp/verify_engine.py
python webapp/verify_app.py
python webapp/render_preview.py --out media/webapp
```

To use the app locally, serve the folder (`python -m http.server` inside
`webapp/`) and open `index.html`; the page loads `knowledge.json` and
`vectors.json` with `fetch`, which needs a server rather than a file URL.
