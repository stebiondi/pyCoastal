"""
Build the pyCoastal manual: Markdown chapters in, a PDF out.

The hand-written chapters live in ``docs/manual/chapters``. Everything that
can drift out of step with the code is generated here instead of typed:

- the printed output of every worked example (``outputs/*.txt``, refreshed
  with ``--run-examples``);
- the input tables of PyCoaTools, parsed from ``webapp/app.js``;
- the test inventory, from ``tests/``;
- the PyCoaPedia figures and module table, from the shipped database.

The Markdown goes through pandoc (with pandoc-crossref for numbered figures,
tables, equations and sections) to LaTeX, set in the style of the first
edition: the article class in Computer Modern, with the wave on the cover.
Tectonic (or latexmk with xelatex) typesets it.

The same run writes the Markdown that agents read instead of the PDF: the
API reference in ``docs/reference/`` (one file per module, from the
docstrings) and the example index ``docs/examples.md``.

Run from the repository root:

    python docs/manual/build_manual.py                 # -> pyCoastal manual.pdf
    python docs/manual/build_manual.py --run-examples  # refresh example output
    python docs/manual/build_manual.py --tex-only      # stop after the LaTeX

Needs pandoc (on PATH, or the copy bundled with pypandoc), pandoc-crossref
(optional), Pillow, pypdf, and Tectonic or a TeX distribution with xelatex.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHAPTERS = HERE / "chapters"
OUTPUTS = HERE / "outputs"
# Scratch space for the LaTeX, figures and intermediate files. Kept out of the
# repository (and out of any synced folder) because it is large and disposable.
BUILD = Path(tempfile.gettempdir()) / "pycoastal_manual_build"
PDF_OUT = ROOT / "pyCoastal manual.pdf"

#: Engineering examples whose printed output the manual quotes.
ENGINEERING_EXAMPLES = [
    "design_wave", "breakwater_design", "seawall_section", "port_diffraction",
    "port_layout_comparison", "pile_wave_loads", "pier_scour", "bridge_scour",
    "backwater", "navigation_channel", "berth_fenders", "nourishment_design",
    "nourishment_profile", "storm_surge_flooding",
]

#: Example order in docs/examples.md, following the chapters.
EXAMPLE_ORDER = [
    "numerics/water_drop.py", "waves2D.py", "wave2D_irregular.py", "current.py",
    "pollutant.py", "numerics/viscous_fluid.py", "numerics/2D_irr_turb.py",
    "equilibrium_shoreline.py", "design_wave.py", "breakwater_design.py",
    "seawall_section.py", "port_diffraction.py", "port_layout_comparison.py",
    "pile_wave_loads.py", "pier_scour.py", "bridge_scour.py", "backwater.py",
    "navigation_channel.py", "berth_fenders.py", "nourishment_design.py",
    "nourishment_profile.py", "storm_surge_flooding.py",
]

#: Package modules for docs/reference, in the order a reader meets them.
API_MODULES = [
    "pyCoastal/__init__.py", "pyCoastal/config.py", "pyCoastal/io.py",
    "pyCoastal/numerics/grid.py", "pyCoastal/numerics/domain.py",
    "pyCoastal/numerics/operators.py", "pyCoastal/numerics/scheme.py",
    "pyCoastal/numerics/time_intg.py", "pyCoastal/numerics/boundary.py",
    "pyCoastal/numerics/solver.py",
    "pyCoastal/physics/shallow_water.py", "pyCoastal/physics/navier_stokes.py",
    "pyCoastal/physics/poisson.py", "pyCoastal/physics/turbulence.py",
    "pyCoastal/tools/wave.py", "pyCoastal/tools/sediment_transport.py",
    "pyCoastal/tools/structural.py", "pyCoastal/tools/shoreline.py",
    "pyCoastal/tools/morphodynamics.py",
    "pyCoastal/applications/__init__.py",
    "pyCoastal/applications/extremes.py", "pyCoastal/applications/sediment.py",
    "pyCoastal/applications/structures.py", "pyCoastal/applications/seawall.py",
    "pyCoastal/applications/port.py", "pyCoastal/applications/piles.py",
    "pyCoastal/applications/scour.py", "pyCoastal/applications/river.py",
    "pyCoastal/applications/channel.py", "pyCoastal/applications/berthing.py",
    "pyCoastal/applications/nourishment.py", "pyCoastal/applications/surge.py",
    "pyCoastal/applications/sections.py",
    "pyCoastal/drafting.py", "pyCoastal/plotting.py",
    "pyCoastal/pedia/__init__.py",
]

NOISE = (
    "Ignoring fixed", "UserWarning", "plt.show()", "FigureCanvasAgg",
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]<>#+!|~^$@])")
_SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")
_SUPERSCRIPT_RUN = re.compile("[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+")


def esc(text) -> str:
    """Escape free text so pandoc reads it as text and nothing else."""
    text = str(text).replace("\r", " ").replace("\n", " ").strip()
    text = _MD_SPECIAL.sub(r"\\\1", text)
    # Unicode superscripts (m s⁻¹) become real ones: the text face has no
    # superscript minus.
    text = _SUPERSCRIPT_RUN.sub(
        lambda m: "^" + m.group(0).translate(_SUPERSCRIPT) + "^", text)
    # A line starting "12. " or "- " would become a list.
    return re.sub(r"^(\d+)\.", r"\1\\.", text)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fence(body: str, lang: str = "") -> str:
    ticks = "```"
    while ticks in body:
        ticks += "`"
    return f"{ticks}{lang}\n{body.rstrip()}\n{ticks}"


def find_pandoc() -> str:
    exe = shutil.which("pandoc")
    if exe:
        return exe
    try:
        import pypandoc  # noqa: F401
        path = Path(pypandoc.__file__).parent / "files" / (
            "pandoc.exe" if os.name == "nt" else "pandoc")
        if path.exists():
            return str(path)
    except ImportError:
        pass
    sys.exit("pandoc not found: install it or `pip install pypandoc_binary`.")


def find_crossref() -> str | None:
    exe = shutil.which("pandoc-crossref")
    if exe:
        return exe
    appdata = os.environ.get("APPDATA")
    if appdata:
        path = Path(appdata) / "pandoc" / "filters" / "pandoc-crossref.exe"
        if path.exists():
            return str(path)
    return None


# ---------------------------------------------------------------------------
# Example output
# ---------------------------------------------------------------------------

def run_examples() -> None:
    """Run each engineering example in a scratch copy and keep its output.

    A scratch copy, because the examples write their figures into
    ``media/`` and the manual should not rewrite committed artwork.
    """
    OUTPUTS.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name in ("pyCoastal", "examples", "media"):
            shutil.copytree(ROOT / name, tmp / name)
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8",
                   PYTHONPATH=str(tmp))
        for name in ENGINEERING_EXAMPLES:
            print(f"  running {name}")
            proc = subprocess.run(
                [sys.executable, f"examples/{name}.py"], cwd=tmp, env=env,
                capture_output=True, text=True, encoding="utf-8")
            if proc.returncode:
                print(proc.stderr)
                sys.exit(f"examples/{name}.py failed")
            (OUTPUTS / f"{name}.txt").write_text(proc.stdout, encoding="utf-8")


def example_output(name: str) -> str:
    path = OUTPUTS / f"{name}.txt"
    if not path.exists():
        sys.exit(f"No captured output for {name}; run with --run-examples.")
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not any(n in ln for n in NOISE)]
    body = "\n".join(lines).strip()
    return (f"::: {{.output}}\n**Output of `examples/{name}.py`**\n\n"
            f"{fence(body, 'text')}\n:::")


# ---------------------------------------------------------------------------
# Coastal Design Bench inputs
# ---------------------------------------------------------------------------

def webapp_inputs() -> str:
    src = (ROOT / "webapp" / "app.js").read_text(encoding="utf-8")
    start = src.index("var MODULES = {")
    body = src[start:]
    blocks = list(re.finditer(r"\n  (\w+): \{\n    label: \"([^\"]+)\",\n"
                              r"    note: \"([^\"]+)\"", body))
    out = []
    for i, m in enumerate(blocks):
        key, label, note = m.groups()
        end = blocks[i + 1].start() if i + 1 < len(blocks) else len(body)
        chunk = body[m.end():end]
        chunk = chunk[:chunk.index("run: function")] if "run: function" in chunk else chunk
        rows = []
        for obj in re.finditer(r"\{\s*key:(.*?)\}", chunk, re.S):
            text = "key:" + obj.group(1)

            def field(name, text=text):
                mm = re.search(name + r":\s*(\"[^\"]*\"|\[[^\]]*\]|[-\w.]+)", text)
                return mm.group(1).strip('"') if mm else ""

            kind = field("type") or "slider"
            if kind == "select":
                opts = re.findall(r"\"([^\"]+)\"", field("options"))
                rng = ", ".join(f"`{o}`" for o in opts)
            elif kind == "toggle":
                rng = "on / off"
            else:
                rng = f"{field('min')} to {field('max')}, step {field('step')}"
            unit = field("unit")
            rows.append(f"| `{field('key')}` | {esc(field('label'))} | "
                        f"{esc(unit) if unit else '-'} | {kind} | {rng} | "
                        f"`{field('value')}` |")
        out.append(f"### {esc(label)} {{.unnumbered}}\n\n*{esc(note)}* "
                   f"(module key `{key}`)\n\n"
                   "| Input | Label | Unit | Control | Range or options | Default |\n"
                   "|-------|-------|------|---------|------------------|---------|\n"
                   + "\n".join(rows))
    return "\n\n".join(out)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_table() -> str:
    rows, total = [], 0
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        count = sum(
            1 for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and n.name.startswith("test_"))
        total += count
        doc = ast.get_docstring(tree) or ""
        first = doc.strip().split("\n\n")[0].replace("\n", " ") if doc else ""
        rows.append(f"| `{path.name}` | {count} | {esc(first)} |")
    return (f"The suite holds {total} test functions in {len(rows)} files "
            "(parametrized tests expand to more cases when run).\n\n"
            ": Test files and what they cover. {#tbl:tests}\n\n"
            "| File | Tests | Scope |\n|----------------------------|------|------------------------------------|\n" + "\n".join(rows))


# ---------------------------------------------------------------------------
# PyCoaPedia, read from the shipped database
# ---------------------------------------------------------------------------

def pedia_connection():
    import sqlite3
    path = ROOT / "pyCoastal" / "pedia" / "pycoapedia.sqlite"
    if not path.exists():
        sys.exit(f"No PyCoaPedia database at {path}; run pedia/build_pedia.py first.")
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def pedia_stats() -> str:
    con = pedia_connection()
    m = {r["key"]: r["value"] for r in con.execute("SELECT key, value FROM metadata")}
    roots = con.execute("SELECT COUNT(*) FROM topics WHERE parent_id IS NULL").fetchone()[0]
    links = con.execute("SELECT COUNT(*) FROM claim_relationships").fetchone()[0]
    extracted = con.execute("SELECT COUNT(*) FROM paper_extractions").fetchone()[0]
    return (f"The build shipped with this version of pyCoastal was generated on "
            f"{m['generated']}. It holds {int(m['topics'])} topics in {roots} "
            f"top-level branches, {int(m['claims']):,} claims linked by "
            f"{links:,} claim-to-claim relationships, {int(m['equations'])} "
            f"equations, and {int(m['papers']):,} papers, {extracted:,} of them "
            f"with a structured extraction, drawn from "
            f"{int(m['papers_screened_in_source']):,} papers screened.")


def pedia_modules() -> str:
    con = pedia_connection()
    rows = [": Design modules and their PyCoaPedia topics. {#tbl:pedia-modules}", "",
            "| Module | Topics |", "|------------------|------------------------------------------------------|"]
    mods: dict[str, list] = {}
    labels = {}
    for r in con.execute("SELECT m.module, m.module_label, t.label, t.id FROM module_topics m "
                         "JOIN topics t ON t.id = m.topic_id ORDER BY m.module, m.position"):
        mods.setdefault(r["module"], []).append(f"{esc(r['label'])} (`{r['id']}`)")
        labels[r["module"]] = r["module_label"]
    for key, topics in mods.items():
        rows.append(f"| {esc(labels[key])} (`{key}`) | " + "; ".join(topics) + " |")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Markdown for agents: the API reference and the example index
# ---------------------------------------------------------------------------

REFERENCE = ROOT / "docs" / "reference"
EXAMPLES_MD = ROOT / "docs" / "examples.md"


def module_name(rel: str) -> str:
    """Dotted module name for a source path, e.g. pyCoastal.applications.scour."""
    mod = rel[:-3].replace("/", ".")
    return mod[: -len(".__init__")] if mod.endswith(".__init__") else mod


def module_reference(rel: str) -> tuple[str, str]:
    """One module's public API as Markdown: (module name, text)."""
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
    mod = module_name(rel)
    out = [f"# `{mod}`", "", f"Source: [`{rel}`](../../{rel})", ""]
    doc = ast.get_docstring(tree)
    if doc:
        out += [doc, ""]
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            sig = f"{node.name}({ast.unparse(node.args)})"
            if node.returns is not None:
                sig += f" -> {ast.unparse(node.returns)}"
            out += [f"## `{node.name}`", "", fence("def " + sig, "python"), ""]
            if ast.get_docstring(node):
                out += [fence(ast.get_docstring(node), "text"), ""]
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            bases = ", ".join(ast.unparse(b) for b in node.bases)
            head = [f"class {node.name}" + (f"({bases})" if bases else "")]
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    head.append("    " + ast.unparse(item))
            out += [f"## `{node.name}`", "", fence("\n".join(head), "python"), ""]
            if ast.get_docstring(node):
                out += [fence(ast.get_docstring(node), "text"), ""]
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                    deco = [ast.unparse(d) for d in item.decorator_list]
                    kind = "property" if "property" in deco else (
                        "classmethod" if "classmethod" in deco else "method")
                    sig = f"{node.name}.{item.name}({ast.unparse(item.args)})"
                    if item.returns is not None:
                        sig += f" -> {ast.unparse(item.returns)}"
                    out += [f"### `{node.name}.{item.name}` ({kind})", "", fence(sig, "python"), ""]
                    if ast.get_docstring(item):
                        out += [fence(ast.get_docstring(item), "text"), ""]
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            if names and all(n.isupper() and not n.startswith("_") for n in names):
                value = ast.unparse(node.value) if node.value is not None else ""
                if len(value) > 2000:
                    value = value[:2000] + " ..."
                out += [f"## `{names[0]}`", "", fence(f"{names[0]} = {value}", "python"), ""]
    return mod, "\n".join(out)


def write_reference() -> None:
    # Overwrite in place and remove only stale pages: deleting the folder
    # fails whenever a sync client or an editor holds it open.
    REFERENCE.mkdir(parents=True, exist_ok=True)
    expected = {(module_name(rel) + ".md") for rel in API_MODULES} | {"README.md"}
    for stale in REFERENCE.glob("*.md"):
        if stale.name not in expected:
            stale.unlink()
    index = ["# pyCoastal API reference", "",
             "Generated from the docstrings by `docs/manual/build_manual.py`; "
             "do not edit by hand. One file per module.", ""]
    for rel in API_MODULES:
        mod, text = module_reference(rel)
        name = mod + ".md"
        (REFERENCE / name).write_text(text + "\n", encoding="utf-8")
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
        first = (ast.get_docstring(tree) or "").strip().split("\n")[0]
        index.append(f"- [`{mod}`]({name}): {first}")
    (REFERENCE / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def write_example_index() -> None:
    out = ["# pyCoastal examples", "",
           "Every script runs from the repository root (`python examples/<name>.py`). "
           "The engineering examples print a design report and write figures to "
           "`media/`; their captured output is in `docs/manual/outputs/`. The "
           "numerical examples animate on screen and read `examples/configs/*.yaml`.", ""]
    listed = [ROOT / "examples" / r for r in EXAMPLE_ORDER]
    rest = [p for p in sorted((ROOT / "examples").rglob("*.py")) if p not in listed]
    for path in listed + rest:
        if not path.exists():
            continue
        rel = path.relative_to(ROOT).as_posix()
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
        paras = [p for p in doc.strip().split("\n\n") if not p.strip().startswith(("Run from", "python "))]
        summary = " ".join(" ".join(paras[:2]).split()) if paras else "(no description)"
        out.append(f"## [`{rel}`](../{rel})")
        out.append("")
        out.append(summary)
        output = OUTPUTS / f"{path.stem}.txt"
        if output.exists() and path.stem in ENGINEERING_EXAMPLES:
            out.append("")
            out.append(f"Captured output: [`docs/manual/outputs/{output.name}`](manual/outputs/{output.name})")
        out.append("")
    EXAMPLES_MD.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def prepare_images(markdown: str, max_width: int = 1900) -> str:
    """Copy each referenced figure into the build, scaled for print."""
    from PIL import Image

    target = BUILD / "media"
    target.mkdir(parents=True, exist_ok=True)

    def repl(match):
        rel = match.group(2)
        src = ROOT / rel
        if not src.exists():
            print(f"  missing figure {rel}")
            return match.group(0)
        # JPEG at high quality: a sheet at 1900 px is print resolution for
        # a 170 mm column, and a PNG of it is five times the size.
        dst = target / (slug(rel.rsplit(".", 1)[0]) + ".jpg")
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            with Image.open(src) as im:
                im.seek(0)
                im = im.convert("RGBA")
                flat = Image.new("RGB", im.size, (255, 255, 255))
                flat.paste(im, mask=im.split()[3])
                if flat.width > max_width:
                    h = round(flat.height * max_width / flat.width)
                    flat = flat.resize((max_width, h), Image.LANCZOS)
                flat.save(dst, quality=86, optimize=True)
        return f"{match.group(1)}media/{dst.name})"

    return re.sub(r"(!\[[^\]]*\]\()(media/[^)\s]+)\)", repl, markdown)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def latex(code: str) -> str:
    """A raw LaTeX block for pandoc."""
    return "```{=latex}\n" + code.strip() + "\n```"


def assemble() -> str:
    parts = []
    for path in sorted(CHAPTERS.glob("*.md")):
        parts.append(path.read_text(encoding="utf-8"))
    text = "\n\n".join(parts)

    # Parts become LaTeX \part, each on a fresh page.
    text = re.sub(
        r"^# Part [IVXLC]+\. (.+?) \{\.part \.unnumbered\}\s*$",
        lambda m: latex("\\part{" + m.group(1) + "}"),
        text, flags=re.M)

    text = re.sub(r"<!-- output: (\w+) -->", lambda m: example_output(m.group(1)), text)
    replacements = {
        "<!-- webapp-inputs -->": webapp_inputs,
        "<!-- test-table -->": test_table,
        "<!-- pedia-stats -->": pedia_stats,
        "<!-- pedia-modules -->": pedia_modules,
    }
    for key, fn in replacements.items():
        if key in text:
            text = text.replace(key, fn())
    leftover = re.findall(r"<!-- [\w-]+(?::[^>]*)? -->", text)
    if leftover:
        sys.exit(f"Unfilled placeholders: {leftover}")
    return text


def package_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    return m.group(1) if m else "dev"


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------

#: Preamble additions. The look is the first edition's: the standard article
#: class in Computer Modern, 11 pt on A4. Computer Modern Unicode is used
#: for text rather than Latin Modern because the text quotes authors and
#: symbols (Fredsoe with its slashed o, Greek letters, inequality signs)
#: that Latin Modern does not carry.
HEADER = r"""
\usepackage{fontspec}
\setmainfont{cmunrm}[Extension=.otf, BoldFont=cmunbx, ItalicFont=cmunti,
  BoldItalicFont=cmunbi]
\setsansfont{cmunss}[Extension=.otf, BoldFont=cmunsx, ItalicFont=cmunsi,
  BoldItalicFont=cmunso]
\setmonofont{cmuntt}[Extension=.otf, BoldFont=cmuntb, ItalicFont=cmunit,
  BoldItalicFont=cmuntx, HyphenChar=None]
% Computer Modern has no arrows or mathematical operators in its text faces,
% and the docstrings quoted in the appendices use them (the partial, nabla,
% approximately and proportional signs). XeTeX switches to Latin Modern Math
% for exactly those characters and back again, in running text and code.
\newfontfamily\mathglyphs{latinmodern-math.otf}
\XeTeXinterchartokenstate=1
\newXeTeXintercharclass\MathGlyphClass
\makeatletter
\count@="2190
\loop\XeTeXcharclass\count@=\MathGlyphClass
  \ifnum\count@<"22FF\advance\count@ 1\repeat
\makeatother
\XeTeXcharclass"2032=\MathGlyphClass
\XeTeXcharclass"2070=\MathGlyphClass
\XeTeXcharclass"2074=\MathGlyphClass
\XeTeXcharclass"207A=\MathGlyphClass
\XeTeXcharclass"207B=\MathGlyphClass
\XeTeXinterchartoks 0 \MathGlyphClass = {\begingroup\mathglyphs}
\XeTeXinterchartoks 4095 \MathGlyphClass = {\begingroup\mathglyphs}
\XeTeXinterchartoks \MathGlyphClass 0 = {\endgroup}
\XeTeXinterchartoks \MathGlyphClass 4095 = {\endgroup}
\usepackage{multicol}
\usepackage{xcolor}
\usepackage{fvextra}
\fvset{breaklines=true, breakanywhere=true, fontsize=\footnotesize}
\RecustomVerbatimEnvironment{verbatim}{Verbatim}{}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{3}
% A live contents: every entry (title and page number) jumps to its page,
% internal links are coloured so they read as links, the bookmark panel
% opens with the outline numbered, and every page number in the footer
% jumps back to the contents.
\definecolor{linkblue}{rgb}{0.05,0.25,0.50}
\AtBeginDocument{\hypersetup{colorlinks=true, linkcolor=linkblue,
  citecolor=linkblue, urlcolor=linkblue, linktoc=all,
  bookmarksnumbered=true, bookmarksopen=true, bookmarksopenlevel=1,
  pdfpagemode=UseOutlines, pdfstartview=FitH,
  pdftitle={pyCoastal: a Python Tool for Coastal Engineering},
  pdfauthor={Stefano Biondi}}}
\let\oldtableofcontents\tableofcontents
\renewcommand{\tableofcontents}{\hypertarget{contents}{}%
  \pdfbookmark[1]{Contents}{contents-bookmark}\oldtableofcontents\clearpage}
\usepackage{fancyhdr}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\hyperlink{contents}{\thepage}}
\fancypagestyle{plain}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}%
  \fancyfoot[C]{\hyperlink{contents}{\thepage}}}
\pagestyle{fancy}
\usepackage{etoolbox}
\pretocmd{\part}{\clearpage}{}{}
\setlength{\emergencystretch}{3em}
\sloppy
\widowpenalty=10000
\clubpenalty=10000
"""

TITLE_PAGE = r"""
\begin{titlepage}
\centering
\vspace*{0.4cm}
{\LARGE\bfseries pyCoastal: a Python Tool for Coastal Engineering\par}
\vspace{0.9cm}
{\large Stefano Biondi\par}
\vspace{0.1cm}
{\large University of Florida\par}
\vspace{0.8cm}
{\normalsize User manual and reference, version @VERSION@\par}
\vspace{0.1cm}
{\normalsize @DATE@\par}
\vfill
\includegraphics[width=\linewidth]{media/manual-cover.jpg}
\vfill
\vspace*{2cm}
\end{titlepage}
"""


def find_tectonic() -> list[str]:
    exe = shutil.which("tectonic")
    if exe:
        return [exe]
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "tectonic" / "tectonic.exe"
    if local.exists():
        return [str(local)]
    if shutil.which("latexmk") and shutil.which("xelatex"):
        return ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error"]
    sys.exit("No LaTeX engine found: install Tectonic (https://tectonic-typesetting.github.io) "
             "or TeX Live with latexmk and xelatex.")


def run_tex(engine: list[str], tex: Path) -> subprocess.CompletedProcess:
    cmd = engine + [tex.name]
    if Path(engine[0]).stem == "tectonic":
        cmd = engine + ["--keep-logs", "--chatter", "minimal", tex.name]
    return subprocess.run(cmd, cwd=tex.parent, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def write_crossref_metadata() -> Path:
    """Singular and plural prefixes, so a group of references reads "Equations 5-7"."""
    path = BUILD / "crossref.yaml"
    path.write_text(
        "figPrefix: [Figure, Figures]\n"
        "tblPrefix: [Table, Tables]\n"
        "eqnPrefix: [Equation, Equations]\n"
        "secPrefix: [Section, Sections]\n"
        "rangeDelim: \"--\"\n", encoding="utf-8")
    return path


def pandoc_latex(markdown: str, pandoc: str, crossref: str | None) -> Path:
    src = BUILD / "manual.md"
    src.write_text(markdown, encoding="utf-8")
    (BUILD / "header.tex").write_text(HEADER, encoding="utf-8")
    from datetime import date
    title = (TITLE_PAGE.replace("@VERSION@", package_version())
             .replace("@DATE@", date.today().strftime("%B %Y")))
    (BUILD / "titlepage.tex").write_text(title, encoding="utf-8")
    out = BUILD / "manual.tex"
    cmd = [pandoc, str(src), "-f", "markdown", "-t", "latex", "-s",
           "--highlight-style=monochrome", "--number-sections", "--toc", "--toc-depth=2",
           "-V", "documentclass=article", "-V", "classoption=11pt",
           "-V", "papersize=a4", "-V", "geometry:margin=2.5cm",
           # Without these the template sets hidelinks, and the contents and
           # cross-references work but look like plain text.
           "-V", "colorlinks=true", "-V", "linkcolor=linkblue",
           "-V", "toccolor=linkblue", "-V", "urlcolor=linkblue",
           "-V", "citecolor=linkblue",
           "--include-in-header", str(BUILD / "header.tex"),
           "--include-before-body", str(BUILD / "titlepage.tex"),
           "--lua-filter", str(HERE / "breakable_code.lua"),
           "-o", str(out)]
    if crossref:
        cmd[2:2] = ["--filter", crossref,
                    "-M", "linkReferences=true", "-M", "nameInLink=true",
                    "--metadata-file", str(write_crossref_metadata()),
                    "-M", "autoSectionLabels=false"]
    print("  pandoc ...")
    proc = subprocess.run(cmd, cwd=BUILD, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode:
        print(proc.stderr)
        sys.exit("pandoc failed")
    return out


def style_findings() -> int:
    """Count departures from docs/manual/STYLE.md in the chapters."""
    sys.path.insert(0, str(HERE))
    import style_check

    return sum(len(style_check.check(p)) for p in sorted(CHAPTERS.glob("*.md")))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--run-examples", action="store_true",
                        help="rerun the engineering examples and refresh their output")
    parser.add_argument("--tex-only", action="store_true",
                        help="write the LaTeX source and stop")
    parser.add_argument("--out", type=Path, default=PDF_OUT)
    args = parser.parse_args()
    args.out = args.out.resolve()

    BUILD.mkdir(exist_ok=True)
    if args.run_examples:
        print("Running examples")
        run_examples()

    findings = style_findings()
    if findings:
        print(f"  style: {findings} findings, run docs/manual/style_check.py")

    print("Writing the API reference and the example index")
    write_reference()
    write_example_index()

    engine = find_tectonic()
    print("Assembling")
    markdown = prepare_images(assemble())
    from PIL import Image
    with Image.open(ROOT / "media" / "manual_cover.jpeg") as im:
        im.convert("RGB").save(BUILD / "media" / "manual-cover.jpg", quality=95)

    tex = pandoc_latex(markdown, find_pandoc(), find_crossref())
    print(f"  wrote {tex}")
    if args.tex_only:
        return

    print("  typesetting (several passes) ...")
    proc = run_tex(engine, tex)
    log = tex.with_suffix(".log")
    if proc.returncode or not tex.with_suffix(".pdf").exists():
        print((proc.stderr or proc.stdout)[-4000:])
        sys.exit(f"LaTeX failed; see {log}")
    if log.exists():
        missing = set(re.findall(r"Missing character: There is no (\S+)",
                                 log.read_text(encoding="utf-8", errors="replace")))
        if missing:
            print('  missing glyphs: ' + ' '.join(ascii(c) for c in sorted(missing)))
    shutil.copyfile(tex.with_suffix(".pdf"), args.out)
    from pypdf import PdfReader
    n = len(PdfReader(str(args.out)).pages)
    size = args.out.stat().st_size / 1e6
    print(f"Wrote {args.out.name}: {n} pages, {size:.1f} MB")


if __name__ == "__main__":
    main()
