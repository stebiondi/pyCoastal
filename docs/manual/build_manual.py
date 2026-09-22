"""
Build the pyCoastal manual: Markdown chapters in, a PDF out.

The hand-written chapters live in ``docs/manual/chapters``. Everything that
can drift out of step with the code is generated here instead of typed:

- the printed output of every worked example (``outputs/*.txt``, refreshed
  with ``--run-examples``);
- the input tables of the Coastal Design Bench, parsed from ``webapp/app.js``;
- the test inventory, from ``tests/``;
- the CoastalWiki part and its bibliography, from ``webapp/knowledge.json``;
- the API reference, from the package docstrings;
- the example listings, from ``examples/``.

The Markdown goes through pandoc (with pandoc-crossref for numbered figures,
tables, equations and sections) to one HTML file with MathML, and a
Chromium-family browser prints that to PDF. The table of contents gets its
page numbers from a first printing: the link targets in that PDF say which
page each heading landed on, and the second printing carries them.

Run from the repository root:

    python docs/manual/build_manual.py                 # -> pyCoastal manual.pdf
    python docs/manual/build_manual.py --run-examples  # refresh example output
    python docs/manual/build_manual.py --html-only     # stop after the HTML

Needs pandoc (on PATH, or the copy bundled with pypandoc), pandoc-crossref
(optional), Pillow, pypdf, and Microsoft Edge or Google Chrome.
"""

from __future__ import annotations

import argparse
import ast
import json
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
# Scratch space for the HTML, figures and the first printing. Kept out of the
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

#: Example listing order for Appendix B, following the chapters.
EXAMPLE_ORDER = [
    "numerics/water_drop.py", "waves2D.py", "wave2D_irregular.py", "current.py",
    "pollutant.py", "numerics/viscous_fluid.py", "numerics/2D_irr_turb.py",
    "equilibrium_shoreline.py", "design_wave.py", "breakwater_design.py",
    "seawall_section.py", "port_diffraction.py", "port_layout_comparison.py",
    "pile_wave_loads.py", "pier_scour.py", "bridge_scour.py", "backwater.py",
    "navigation_channel.py", "berth_fenders.py", "nourishment_design.py",
    "nourishment_profile.py", "storm_surge_flooding.py",
]

#: Package modules for Appendix A, in the order a reader meets them.
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
]

#: Synthesis headings, in the order a reader wants them.
SYNTHESIS_ORDER = [
    ("well_established", "Well established"),
    ("governing_physics", "Governing physics"),
    ("dimensionless_parameters", "Dimensionless parameters"),
    ("major_equations", "Major equations"),
    ("typical_methods", "Typical methods"),
    ("numerical_models", "Numerical models"),
    ("experimental_datasets", "Experimental datasets"),
    ("validated_ranges", "Validated ranges"),
    ("recent_advances", "Recent advances"),
    ("disagreements", "Disagreements"),
    ("limitations", "Limitations"),
    ("open_questions", "Open questions"),
    ("seminal_papers", "Seminal papers"),
]

CONFIDENCE = {
    "direct_finding": "direct finding",
    "literature_review_statement": "review statement",
    "inferred_relationship": "inferred",
    "proposed_hypothesis": "hypothesis",
}

NOISE = (
    "Ignoring fixed", "UserWarning", "plt.show()", "FigureCanvasAgg",
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]<>#+!|~^$@])")


def esc(text) -> str:
    """Escape free text so pandoc reads it as text and nothing else."""
    text = str(text).replace("\r", " ").replace("\n", " ").strip()
    text = _MD_SPECIAL.sub(r"\\\1", text)
    # A line starting "12. " or "- " would become a list.
    return re.sub(r"^(\d+)\.", r"\1\\.", text)


def surname(author) -> str:
    """Sort key for a first-author string such as "A. Engelstad"."""
    words = re.findall(r"[^\s.,]+", str(author or "").strip())
    return (words[-1] if words else "~").lower()


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


def find_browser() -> str:
    candidates = [
        shutil.which("msedge"), shutil.which("chrome"),
        shutil.which("google-chrome"), shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    sys.exit("No Chromium-family browser found for printing the PDF.")


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
# CoastalWiki
# ---------------------------------------------------------------------------

class Wiki:
    def __init__(self, path: Path):
        self.data = json.loads(path.read_text(encoding="utf-8"))
        self.topics = self.data["topics"]
        self.papers = self.data["papers"]
        # Number papers in bibliography order: first author, then year.
        cited = set()
        for t in self.topics.values():
            for c in t.get("claims", []):
                cited.add(str(c.get("paper")))
            for e in t.get("equations", []):
                cited.add(str(e.get("paper")))
        keys = [k for k in self.papers if k in cited] or list(self.papers)
        keys.sort(key=lambda k: (surname(self.papers[k].get("a")),
                                 self.papers[k].get("y") or 0,
                                 str(self.papers[k].get("t") or "").lower()))
        self.number = {k: i + 1 for i, k in enumerate(keys)}
        self.order = keys
        self.module_of: dict[str, list[str]] = {}
        for m in self.data["modules"].values():
            for t in m["topics"]:
                self.module_of.setdefault(t, []).append(m["label"])

    def cite(self, paper) -> str:
        n = self.number.get(str(paper))
        return f"[[{n}]](#wbib-{n})" if n else ""

    def anchor(self, tid: str) -> str:
        return "wiki-" + slug(tid)

    def stats(self) -> str:
        c = self.data["corpus"]
        inc = self.data["included"]
        n_claims = sum(len(t.get("claims", [])) for t in self.topics.values())
        n_eq = sum(len(t.get("equations", [])) for t in self.topics.values())
        return (
            f"The extract was generated on {self.data['generated']}. The full "
            f"wiki holds {c['papers']:,} papers, {c['knowledge_claims']:,} "
            f"claims, {c['equations']:,} equations, {c['topics']} topics, and "
            f"{c['topic_synthesis_statements']:,} synthesis statements. The "
            f"extract shipped with the app, and reproduced here, holds "
            f"{inc['topics']} topics, {n_claims:,} claims, {n_eq} equations, "
            f"and {len(self.order):,} cited papers.")

    # -- rendering ---------------------------------------------------------

    def topic(self, tid: str, level: int) -> str:
        t = self.topics[tid]
        h = "#" * level
        parts = [f"{h} {esc(t['label'])} {{#{self.anchor(tid)}}}", ""]
        meta = [f"Topic `{tid}`"]
        if t.get("description"):
            meta.append(esc(str(t["description"]).rstrip(". ")))
        parts.append("*" + ". ".join(meta) + ".*")
        counts = (f"Papers screened: {t.get('papers', 0)}. Claims: "
                  f"{len(t.get('claims', []))}. Equations: "
                  f"{len(t.get('equations', []))}.")
        if tid in self.module_of:
            counts += (" Shown in the Coastal Design Bench beside: "
                       + ", ".join(self.module_of[tid]) + ".")
        parts += ["", counts, ""]

        syn = t.get("synthesis") or {}
        if isinstance(syn, dict) and syn:
            parts.append("::: {.synthesis}")
            seen = set()
            for key, title in SYNTHESIS_ORDER + [(k, k.replace("_", " ").capitalize())
                                                 for k in syn if k not in dict(SYNTHESIS_ORDER)]:
                if key in seen or key not in syn or not syn[key]:
                    continue
                seen.add(key)
                value = syn[key]
                if isinstance(value, (list, tuple)):
                    value = "; ".join(str(v) for v in value)
                elif isinstance(value, dict):
                    value = "; ".join(f"{k}: {v}" for k, v in value.items())
                parts.append(f"**{title}.** {esc(value)}\n")
            parts.append(":::\n")

        eqs = t.get("equations", [])
        if eqs:
            parts.append("**Equations**\n")
            for e in eqs:
                latex = str(e.get("latex", "")).strip().strip("$").strip()
                latex = latex.replace("\n", " ")
                parts.append(f"- *{esc(e.get('name', 'Equation'))}* "
                             f"{self.cite(e.get('paper'))}")
                if latex:
                    parts.append(f"\n  $${latex}$$\n")
                if e.get("regime"):
                    parts.append(f"  Regime: {esc(e['regime'])}")
                variables = e.get("variables")
                if isinstance(variables, str):
                    try:
                        variables = json.loads(variables)
                    except (ValueError, TypeError):
                        variables = {"": variables}
                if isinstance(variables, dict) and variables:
                    vs = "; ".join(f"`{k}` {esc(v)}" if k else esc(v)
                                   for k, v in variables.items())
                    parts.append(f"  Variables: {vs}")
                parts.append("")

        claims = t.get("claims", [])
        if claims:
            parts.append("**Claims**\n")
            parts.append("::: {.claims}")
            for i, c in enumerate(claims, 1):
                tag = ", ".join(x for x in (
                    CONFIDENCE.get(c.get("confidence"), c.get("confidence") or ""),
                    c.get("evidence") or "") if x)
                line = f"{i}. {esc(c.get('text', ''))}"
                if c.get("regime"):
                    line += f" *Regime: {esc(c['regime'])}*"
                if tag:
                    line += f" [{esc(tag)}]{{.tag}}"
                line += f" {self.cite(c.get('paper'))}"
                parts.append(line)
            parts.append(":::\n")
        return "\n".join(parts)

    def modules_chapter(self) -> str:
        out = ["# The knowledge base by design module {#sec:wiki-modules}", "",
               "Each design module of the Coastal Design Bench opens the "
               "wiki topics below in its Theory and sources panel. The "
               "topics themselves are reproduced in the chapters that follow.", ""]
        for key, m in self.data["modules"].items():
            out.append(f"## {esc(m['label'])}")
            out.append("")
            out.append(f"*{esc(m.get('blurb', ''))}* (module key `{key}`)")
            out.append("")
            out.append("| Topic | Papers | Claims | Equations |")
            out.append("|------------------------------------------|------|------|------|")
            for tid in m["topics"]:
                t = self.topics.get(tid)
                if not t:
                    out.append(f"| `{tid}` (not in extract) | | | |")
                    continue
                out.append(f"| [{esc(t['label'])}](#{self.anchor(tid)}) (`{tid}`) | "
                           f"{t.get('papers', 0)} | {len(t.get('claims', []))} | "
                           f"{len(t.get('equations', []))} |")
            out.append("")
        return "\n".join(out)

    def tree_chapters(self) -> str:
        roots = [tid for tid, t in self.topics.items()
                 if t.get("parent") in (None, "None", "") or int(t.get("level", 0)) == 0]
        roots.sort()
        children: dict[str, list[str]] = {}
        for tid, t in self.topics.items():
            parent = t.get("parent")
            if parent not in (None, "None", "") and tid not in roots:
                children.setdefault(parent, []).append(tid)
        for v in children.values():
            v.sort()
        out = []
        for root in roots:
            t = self.topics[root]
            out.append(f"# Wiki: {esc(t['label'])} {{#{self.anchor(root)}-ch}}")
            out.append("")
            out.append(self.topic(root, 2).replace(
                f"## {esc(t['label'])}", f"## {esc(t['label'])}: overview", 1))
            stack = [(c, 2) for c in reversed(children.get(root, []))]
            while stack:
                tid, level = stack.pop()
                out.append(self.topic(tid, min(level, 5)))
                for c in reversed(children.get(tid, [])):
                    stack.append((c, level + 1))
        return "\n\n".join(out)

    def bibliography(self) -> str:
        out = ["::: {.bibliography}"]
        for k in self.order:
            p = self.papers[k]
            n = self.number[k]
            doi = p.get("doi")
            link = f" [doi:{esc(doi)}](https://doi.org/{doi})" if doi else ""
            journal = f" *{esc(p['j'])}*." if p.get("j") else ""
            out.append(f"[{n}]{{#wbib-{n} .bibno}} {esc(p.get('a') or 'Anon.')} "
                       f"({p.get('y') or 'n.d.'}). {esc(p.get('t') or '')}."
                       f"{journal}{link}\n")
        out.append(":::")
        return "\n".join(out)


# ---------------------------------------------------------------------------
# API reference and example listings
# ---------------------------------------------------------------------------

def docblock(doc: str | None) -> str:
    if not doc:
        return ""
    return "::: {.docstring}\n" + fence(doc, "text") + "\n:::"


def api_reference() -> str:
    out = []
    for rel in API_MODULES:
        path = ROOT / rel
        tree = ast.parse(path.read_text(encoding="utf-8"))
        mod = rel[:-3].replace("/", ".")
        if mod.endswith(".__init__"):
            mod = mod[: -len(".__init__")]
        out.append(f"## `{mod}` {{.unnumbered #api-{slug(mod)}}}")
        out.append(docblock(ast.get_docstring(tree)))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                sig = f"{node.name}({ast.unparse(node.args)})"
                if node.returns is not None:
                    sig += f" -> {ast.unparse(node.returns)}"
                out.append(f"### `{node.name}` {{.unnumbered .apientry}}")
                out.append(fence("def " + sig, "python"))
                out.append(docblock(ast.get_docstring(node)))
            elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                bases = ", ".join(ast.unparse(b) for b in node.bases)
                head = f"class {node.name}" + (f"({bases})" if bases else "")
                lines = [head]
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        lines.append("    " + ast.unparse(item))
                out.append(f"### `{node.name}` {{.unnumbered .apientry}}")
                out.append(fence("\n".join(lines), "python"))
                out.append(docblock(ast.get_docstring(node)))
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                            not item.name.startswith("_")):
                        deco = [ast.unparse(d) for d in item.decorator_list]
                        kind = "property" if "property" in deco else (
                            "classmethod" if "classmethod" in deco else "method")
                        sig = f"{node.name}.{item.name}({ast.unparse(item.args)})"
                        if item.returns is not None:
                            sig += f" -> {ast.unparse(item.returns)}"
                        out.append(f"**{kind}**\n\n" + fence(sig, "python"))
                        d = ast.get_docstring(item)
                        if d:
                            out.append(docblock(d))
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [t.id for t in targets if isinstance(t, ast.Name)]
                if names and all(n.isupper() and not n.startswith("_") for n in names):
                    value = ast.unparse(node.value) if node.value is not None else ""
                    if len(value) > 1500:
                        value = value[:1500] + " ..."
                    out.append(f"### `{names[0]}` {{.unnumbered .apientry}}")
                    out.append(fence(f"{names[0]} = {value}", "python"))
        out.append("")
    return "\n\n".join(x for x in out if x)


def example_listings() -> str:
    out = []
    for rel in EXAMPLE_ORDER:
        path = ROOT / "examples" / rel
        if not path.exists():
            continue
        out.append(f"## `examples/{rel}` {{.unnumbered}}")
        out.append(fence(path.read_text(encoding="utf-8"), "python"))
    listed = {ROOT / "examples" / r for r in EXAMPLE_ORDER}
    for path in sorted((ROOT / "examples").rglob("*.py")):
        if path not in listed:
            rel = path.relative_to(ROOT / "examples").as_posix()
            out.append(f"## `examples/{rel}` {{.unnumbered}}")
            out.append(fence(path.read_text(encoding="utf-8"), "python"))
    out.append("## Case files in `examples/configs/` {.unnumbered}")
    for path in sorted((ROOT / "examples" / "configs").glob("*.yaml")):
        out.append(f"**`{path.name}`**\n")
        out.append(fence(path.read_text(encoding="utf-8"), "yaml"))
    return "\n\n".join(out)


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

def assemble(wiki: Wiki) -> str:
    parts = []
    for path in sorted(CHAPTERS.glob("*.md")):
        parts.append(path.read_text(encoding="utf-8"))
    text = "\n\n".join(parts)

    text = re.sub(r"<!-- output: (\w+) -->", lambda m: example_output(m.group(1)), text)
    replacements = {
        "<!-- webapp-inputs -->": webapp_inputs,
        "<!-- test-table -->": test_table,
        "<!-- wiki-stats -->": wiki.stats,
        "<!-- wiki -->": lambda: ("::: {.wiki}\n\n" + wiki.modules_chapter() + "\n\n"
                                  + wiki.tree_chapters() + "\n\n:::"),
        "<!-- wiki-bib -->": wiki.bibliography,
        "<!-- api -->": lambda: "::: {.api}\n\n" + api_reference() + "\n\n:::",
        "<!-- examples -->": lambda: "::: {.listing}\n\n" + example_listings() + "\n\n:::",
    }
    for key, fn in replacements.items():
        if key in text:
            text = text.replace(key, fn())
    return text


TITLE_PAGE = """
<section class="titlepage">
<img class="logo" src="media/pycoastal-logo.png" alt="pyCoastal">
<h1 class="title">pyCoastal</h1>
<p class="subtitle">A Python toolbox for coastal, port and ocean engineering</p>
<p class="edition">User manual and reference, version {version}</p>
<p class="author">Stefano Biondi<br>University of Florida</p>
<p class="date">{date}</p>
</section>
"""


def package_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    return m.group(1) if m else "dev"


def build_toc(html_body: str, pages: dict[str, int] | None) -> str:
    """Table of contents from the numbered headings pandoc produced."""
    entries = []
    for m in re.finditer(r'<(h[12])([^>]*)>(.*?)</\1>', html_body, re.S):
        tag, attrs, inner = m.groups()
        idm = re.search(r'id="([^"]+)"', attrs)
        if not idm:
            continue
        hid = idm.group(1)
        cls = re.search(r'class="([^"]*)"', attrs)
        classes = cls.group(1).split() if cls else []
        if "apientry" in classes:
            continue
        if tag == "h2" and hid.startswith("wiki-"):
            continue
        text = re.sub(r"<[^>]+>", "", inner).strip()
        level = "part" if "part" in classes else tag
        page = pages.get(hid, 0) if pages else 0
        entries.append((level, hid, text, page))
    rows = []
    for level, hid, text, page in entries:
        num = str(page) if page else "000"
        rows.append(f'<li class="toc-{level}"><a href="#{hid}"><span class="t">'
                    f'{text}</span><span class="dots"></span><span class="p">{num}</span></a></li>')
    return ('<nav class="toc" id="contents"><h1 class="unnumbered toc-title">'
            'Contents</h1><ul>' + "\n".join(rows) + "</ul></nav>")


def pandoc_html(markdown: str, pandoc: str, crossref: str | None) -> str:
    src = BUILD / "manual.md"
    src.write_text(markdown, encoding="utf-8")
    out = BUILD / "body.html"
    cmd = [pandoc, str(src), "-f", "markdown",
           "-t", "html5", "--mathml", "--number-sections",
           "--wrap=none", "-o", str(out)]
    if crossref:
        cmd[2:2] = ["--filter", crossref,
                    "-M", "chapters=true", "-M", "chaptersDepth=1",
                    "-M", "sectionsDepth=3",
                    "-M", "linkReferences=true", "-M", "nameInLink=true",
                    "-M", "figPrefix=Figure", "-M", "tblPrefix=Table",
                    "-M", "eqnPrefix=Equation", "-M", "secPrefix=Section",
                    "-M", "autoSectionLabels=false"]
    print("  pandoc ...")
    proc = subprocess.run(cmd, cwd=BUILD, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode:
        print(proc.stderr)
        sys.exit("pandoc failed")
    noise = [ln for ln in proc.stderr.splitlines() if ln.strip()]
    if noise:
        print(f"  pandoc: {len(noise)} warnings, first few:")
        for ln in noise[:8]:
            print("   ", ln[:200])
    return out.read_text(encoding="utf-8")


def page_html(body: str, toc: str) -> str:
    css = (HERE / "manual.css").read_text(encoding="utf-8")
    from datetime import date
    title = TITLE_PAGE.format(version=package_version(),
                              date=date.today().strftime("%B %Y"))
    return (f"<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>pyCoastal manual</title><style>{css}</style></head>"
            f"<body>{title}{toc}<main>{body}</main></body></html>")


def print_pdf(browser: str, html_path: Path, pdf_path: Path) -> None:
    user_dir = Path(tempfile.mkdtemp(prefix="pycoastal-manual-"))
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--generate-pdf-document-outline",
           f"--user-data-dir={user_dir}", "--virtual-time-budget=60000",
           f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
    print(f"  printing {pdf_path.name} ...")
    if pdf_path.exists():
        pdf_path.unlink()
    subprocess.run(cmd, capture_output=True, timeout=1800)
    if not pdf_path.exists():
        sys.exit("The browser did not write a PDF.")


def heading_pages(pdf_path: Path, ids: list[str]) -> dict[str, int]:
    """Page of each TOC target, read from the link annotations of the TOC."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    page_index = {p.indirect_reference.idnum: i for i, p in enumerate(reader.pages)}
    found: dict[str, int] = {}
    order = iter(ids)
    # The TOC links appear in document order, one per entry.
    for page in reader.pages[:60]:
        for annot in page.get("/Annots") or []:
            a = annot.get_object()
            if a.get("/Subtype") != "/Link":
                continue
            dest = None
            if "/Dest" in a:
                dest = a["/Dest"]
            elif "/A" in a and a["/A"].get("/S") == "/GoTo":
                dest = a["/A"].get("/D")
            if dest is None:
                continue
            if isinstance(dest, str) or hasattr(dest, "startswith"):
                try:
                    dest = reader.named_destinations[str(dest)]
                    target = dest.page
                except KeyError:
                    continue
            else:
                target = dest[0]
            try:
                idx = page_index[target.idnum] if hasattr(target, "idnum") else page_index[target.indirect_reference.idnum]
            except (KeyError, AttributeError):
                continue
            try:
                hid = next(order)
            except StopIteration:
                return found
            found[hid] = idx + 1
    return found


def compact(pdf_path: Path) -> None:
    """Pack the browser's PDF into object streams, if PyMuPDF is available.

    Chromium writes a tagged PDF with every structure element as its own
    uncompressed object, which is a third of the file. Object streams and a
    garbage pass take that back without touching the outline or the links.
    """
    try:
        import fitz
    except ImportError:
        print("  PyMuPDF not installed; leaving the PDF uncompacted")
        return
    print("  compacting ...")
    tmp = pdf_path.with_suffix(".tmp.pdf")
    with fitz.open(str(pdf_path)) as doc:
        doc.save(str(tmp), garbage=3, deflate=True, use_objstms=1)
    tmp.replace(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--run-examples", action="store_true",
                        help="rerun the engineering examples and refresh their output")
    parser.add_argument("--html-only", action="store_true",
                        help="write build/manual.html and stop")
    parser.add_argument("--out", type=Path, default=PDF_OUT)
    args = parser.parse_args()
    args.out = args.out.resolve()

    BUILD.mkdir(exist_ok=True)
    if args.run_examples:
        print("Running examples")
        run_examples()

    print("Assembling")
    wiki = Wiki(ROOT / "webapp" / "knowledge.json")
    markdown = assemble(wiki)
    markdown = prepare_images(markdown)
    # The title page logo.
    from PIL import Image
    with Image.open(ROOT / "media" / "pyCoastal_logo.png") as im:
        im.convert("RGBA").save(BUILD / "media" / "pycoastal-logo.png")

    body = pandoc_html(markdown, find_pandoc(), find_crossref())
    toc = build_toc(body, None)
    html_path = BUILD / "manual.html"
    html_path.write_text(page_html(body, toc), encoding="utf-8")
    print(f"  wrote {html_path}")
    if args.html_only:
        return

    browser = find_browser()
    first = BUILD / "pass1.pdf"
    print_pdf(browser, html_path, first)
    ids = re.findall(r'<li class="toc-[^"]+"><a href="#([^"]+)"', toc)
    pages = heading_pages(first, ids)
    print(f"  located {len(pages)} of {len(ids)} contents entries")
    html_path.write_text(page_html(body, build_toc(body, pages)), encoding="utf-8")
    print_pdf(browser, html_path, args.out)
    compact(args.out)
    from pypdf import PdfReader
    n = len(PdfReader(str(args.out)).pages)
    size = args.out.stat().st_size / 1e6
    print(f"Wrote {args.out.name}: {n} pages, {size:.1f} MB")


if __name__ == "__main__":
    main()
