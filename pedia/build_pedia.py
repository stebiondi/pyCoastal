"""
Build PyCoaPedia from the source knowledge database.

PyCoaPedia is pyCoastal's knowledge base: the peer-reviewed coastal and
ocean engineering literature distilled into topics, curated synthesis,
atomic claims with the regime each holds in, equations, and per-paper
extractions, every piece traceable to a DOI. It is built from a larger
research database (hundreds of megabytes, with discovery logs, raw source
records and full-text bookkeeping) that is not shipped. This script keeps
what a reader or an agent needs and writes it three ways, from one pass,
so the three can never disagree:

``pyCoastal/pedia/pycoapedia.sqlite``
    The distilled database, shipped inside the package, with a full-text
    index over topics, synthesis, claims, equations and papers. Read it
    with ``pyCoastal.pedia`` or any SQLite client.
``pedia/topics/*.md``, ``pedia/README.md``, ``pedia/modules.md``
    One Markdown page per topic, with an index, for browsing on GitHub and
    for retrieval by file search.
``webapp/knowledge.json``
    The extract the PyCoaTools browser app loads.

The source database is copied to a temporary file before it is read,
because it is usually being written by the ingestion pipeline at the same
time.

    python pedia/build_pedia.py --db ../2026_CoastalWiki/data/coastalwiki.db
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DB_OUT = ROOT / "pyCoastal" / "pedia" / "pycoapedia.sqlite"
MD_DIR = HERE / "topics"
JSON_OUT = ROOT / "webapp" / "knowledge.json"

sys.path.insert(0, str(ROOT / "webapp"))
from build_knowledge import (  # noqa: E402
    MODULE_TOPICS, access_routes, build as build_extract)

SECTIONS = [
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

SCHEMA = """
CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE topics (
    id TEXT PRIMARY KEY,          -- dotted path, e.g. structures.overtopping
    parent_id TEXT,               -- NULL for the 26 top-level branches
    label TEXT NOT NULL,
    description TEXT,
    level INTEGER,                -- depth in the tree, 0 at the top
    n_papers INTEGER DEFAULT 0,
    n_claims INTEGER DEFAULT 0,
    n_equations INTEGER DEFAULT 0
);

CREATE TABLE synthesis (
    topic_id TEXT NOT NULL REFERENCES topics(id),
    section TEXT NOT NULL,        -- well_established, validated_ranges, ...
    statement TEXT NOT NULL
);

CREATE TABLE papers (
    id INTEGER PRIMARY KEY,
    doi TEXT,
    title TEXT,
    authors TEXT,                 -- "Family, Family, Family" in author order
    first_author TEXT,
    year INTEGER,
    journal TEXT,
    abstract TEXT,
    citation_count INTEGER,
    access TEXT,                  -- open, restricted, unavailable or unknown
    open_url TEXT,                -- best lawful open copy, when access = open
    open_version TEXT,            -- version_of_record, accepted_manuscript, ...
    open_license TEXT             -- CC BY, CC BY-NC-ND, public domain, read only
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY,
    topic_id TEXT REFERENCES topics(id),
    paper_id INTEGER REFERENCES papers(id),
    text TEXT NOT NULL,
    regime TEXT,                  -- where the finding holds
    evidence_type TEXT,           -- field, experimental, numerical, ...
    evidence_summary TEXT,
    confidence TEXT,              -- direct_finding, literature_review_statement, ...
    source_locator TEXT           -- section, figure or table in the paper
);

CREATE TABLE claim_relationships (
    source_claim_id INTEGER REFERENCES claims(id),
    target_claim_id INTEGER REFERENCES claims(id),
    relationship TEXT,            -- supports, contradicts, extends, validates, ...
    rationale TEXT
);

CREATE TABLE equations (
    id INTEGER PRIMARY KEY,
    topic_id TEXT REFERENCES topics(id),
    paper_id INTEGER REFERENCES papers(id),
    name TEXT,
    latex TEXT,
    equation_type TEXT,
    variables TEXT,               -- JSON object, symbol -> meaning
    regime TEXT
);

CREATE TABLE paper_topics (
    paper_id INTEGER REFERENCES papers(id),
    topic_id TEXT REFERENCES topics(id),
    role TEXT,                    -- specific, related, primary_session, ...
    confidence REAL
);

CREATE TABLE paper_extractions (
    paper_id INTEGER PRIMARY KEY REFERENCES papers(id),
    research_question TEXT, problem_addressed TEXT, physical_mechanisms TEXT,
    numerical_methods TEXT, laboratory_configuration TEXT,
    boundary_conditions TEXT, parameter_ranges TEXT, principal_results TEXT,
    quantitative_findings TEXT, observed_relationships TEXT,
    empirical_relationships TEXT, analytical_formulations TEXT,
    engineering_implications TEXT, limitations TEXT,
    applicability_conditions TEXT, contradictions TEXT,
    unresolved_questions TEXT, future_research TEXT,
    extraction_source TEXT        -- full_text or abstract
);

CREATE TABLE parameters (
    id INTEGER PRIMARY KEY, paper_id INTEGER REFERENCES papers(id),
    name TEXT, symbol TEXT, dimensionless INTEGER, definition TEXT, units TEXT,
    minimum_value REAL, maximum_value REAL, value_text TEXT, role TEXT
);

CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, version TEXT,
                     model_family TEXT, governing_framework TEXT, url TEXT);
CREATE TABLE paper_models (paper_id INTEGER, model_id INTEGER, usage_role TEXT,
                           configuration TEXT);
CREATE TABLE datasets (id INTEGER PRIMARY KEY, name TEXT, description TEXT,
                       persistent_id TEXT, url TEXT);
CREATE TABLE paper_datasets (paper_id INTEGER, dataset_id INTEGER, usage_role TEXT);
CREATE TABLE field_sites (id INTEGER PRIMARY KEY, name TEXT, country TEXT,
                          latitude REAL, longitude REAL, environment TEXT,
                          description TEXT);
CREATE TABLE paper_field_sites (paper_id INTEGER, field_site_id INTEGER,
                                usage_role TEXT);

-- pyCoastal design modules and the topics that bear on each.
CREATE TABLE module_topics (
    module TEXT NOT NULL,         -- extremes, seawall, structures, ...
    module_label TEXT,
    module_blurb TEXT,
    topic_id TEXT REFERENCES topics(id),
    position INTEGER
);

-- One row per searchable thing. kind is topic, synthesis, claim, equation
-- or paper; ref is the id in that table (the topic id for topic and
-- synthesis rows).
CREATE VIRTUAL TABLE search USING fts5(
    kind UNINDEXED, ref UNINDEXED, topic_id UNINDEXED, title, body,
    tokenize = 'porter unicode61'
);

CREATE INDEX claims_topic ON claims(topic_id);
CREATE INDEX claims_paper ON claims(paper_id);
CREATE INDEX equations_topic ON equations(topic_id);
CREATE INDEX synthesis_topic ON synthesis(topic_id);
CREATE INDEX paper_topics_topic ON paper_topics(topic_id);
CREATE INDEX paper_topics_paper ON paper_topics(paper_id);
CREATE INDEX papers_doi ON papers(doi);
"""


def snapshot(db: Path) -> Path:
    tmp = Path(tempfile.gettempdir()) / "pycoapedia_source_snapshot.db"
    shutil.copyfile(db, tmp)
    return tmp


def build_sqlite(src: sqlite3.Connection, out: Path) -> dict:
    if out.exists():
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)
    dst = sqlite3.connect(out)
    dst.executescript(SCHEMA)
    q = lambda sql, *a: src.execute(sql, a).fetchall()  # noqa: E731

    topics = q("SELECT id, parent_id, label, description, level FROM topics "
               "WHERE active = 1 ORDER BY id")
    topic_ids = {t[0] for t in topics}
    dst.executemany("INSERT INTO topics (id, parent_id, label, description, level) "
                    "VALUES (?,?,?,?,?)", topics)

    dst.executemany(
        "INSERT INTO synthesis VALUES (?,?,?)",
        [r for r in q("SELECT topic_id, section, statement FROM topic_synthesis_statements "
                      "WHERE statement IS NOT NULL AND statement <> '' "
                      "ORDER BY topic_id, section, id") if r[0] in topic_ids])

    claims = [r for r in q(
        "SELECT id, topic_id, paper_id, claim_text, applicable_regime, evidence_type, "
        "evidence_summary, confidence, source_locator FROM knowledge_claims "
        "WHERE claim_text IS NOT NULL AND claim_text <> '' ORDER BY topic_id, id")
        if r[1] in topic_ids]
    dst.executemany("INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?)", claims)
    claim_ids = {c[0] for c in claims}
    dst.executemany(
        "INSERT INTO claim_relationships VALUES (?,?,?,?)",
        [r for r in q("SELECT source_claim_id, target_claim_id, relationship, rationale "
                      "FROM claim_relationships")
         if r[0] in claim_ids and r[1] in claim_ids])

    equations = [r for r in q(
        "SELECT id, topic_id, paper_id, name, expression_latex, equation_type, "
        "variable_definitions, applicable_regime FROM equations "
        "WHERE expression_latex IS NOT NULL ORDER BY topic_id, id") if r[1] in topic_ids]
    dst.executemany("INSERT INTO equations VALUES (?,?,?,?,?,?,?,?)", equations)

    paper_topics = [r for r in q("SELECT paper_id, topic_id, role, confidence FROM paper_topics")
                    if r[1] in topic_ids]
    dst.executemany("INSERT INTO paper_topics VALUES (?,?,?,?)", paper_topics)

    # Every paper something points at, and every paper screened as relevant.
    wanted = ({c[2] for c in claims} | {e[2] for e in equations}
              | {p[0] for p in paper_topics}
              | {r[0] for r in q("SELECT id FROM papers WHERE relevance_status = 'included'")})
    authors: dict[int, list[str]] = {}
    for pid, fam, disp in q("SELECT pa.paper_id, a.family_name, a.display_name "
                            "FROM paper_authors pa JOIN authors a ON a.id = pa.author_id "
                            "ORDER BY pa.paper_id, pa.author_order"):
        authors.setdefault(pid, []).append(fam or disp or "")
    access = access_routes(src)
    rows = []
    for r in q("SELECT id, doi, title, publication_year, journal, abstract, citation_count "
               "FROM papers"):
        if r[0] not in wanted:
            continue
        names = [n for n in authors.get(r[0], []) if n]
        rows.append((r[0], r[1], r[2], ", ".join(names), names[0] if names else None,
                     r[3], r[4], r[5], r[6], *access.get(r[0], ("unknown", None, None, None))))
    dst.executemany("INSERT INTO papers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)

    cols = [c[1] for c in dst.execute("PRAGMA table_info(paper_extractions)")]
    dst.executemany(
        f"INSERT INTO paper_extractions VALUES ({','.join('?' * len(cols))})",
        [r for r in q(f"SELECT {', '.join(cols)} FROM paper_extractions") if r[0] in wanted])

    for table, cols_ in (
        ("parameters", "id, paper_id, name, symbol, dimensionless, definition, units, "
                       "minimum_value, maximum_value, value_text, role"),
        ("models", "id, name, version, model_family, governing_framework, url"),
        ("paper_models", "paper_id, model_id, usage_role, configuration"),
        ("datasets", "id, name, description, persistent_id, url"),
        ("paper_datasets", "paper_id, dataset_id, usage_role"),
        ("field_sites", "id, name, country, latitude, longitude, environment, description"),
        ("paper_field_sites", "paper_id, field_site_id, usage_role"),
    ):
        data = q(f"SELECT {cols_} FROM {table}")
        n = len(cols_.split(","))
        dst.executemany(f"INSERT INTO {table} VALUES ({','.join('?' * n)})", data)

    for key, m in MODULE_TOPICS.items():
        dst.executemany("INSERT INTO module_topics VALUES (?,?,?,?,?)",
                        [(key, m["label"], m["blurb"], t, i)
                         for i, t in enumerate(m["topics"]) if t in topic_ids])

    dst.execute("""UPDATE topics SET
        n_papers = (SELECT COUNT(*) FROM paper_topics p WHERE p.topic_id = topics.id),
        n_claims = (SELECT COUNT(*) FROM claims c WHERE c.topic_id = topics.id),
        n_equations = (SELECT COUNT(*) FROM equations e WHERE e.topic_id = topics.id)""")

    # Full-text index.
    ins = "INSERT INTO search (kind, ref, topic_id, title, body) VALUES (?,?,?,?,?)"
    dst.executemany(ins, [("topic", t[0], t[0], t[2], t[3] or "") for t in topics])
    dst.executemany(ins, [("synthesis", r[0], r[0], r[1], r[2]) for r in dst.execute(
        "SELECT topic_id, section, statement FROM synthesis").fetchall()])
    dst.executemany(ins, [("claim", c[0], c[1], c[4] or "", c[3]) for c in claims])
    dst.executemany(ins, [("equation", e[0], e[1], e[3] or "",
                           f"{e[7] or ''} {e[4] or ''}") for e in equations])
    primary = {}
    for pid, tid, *_ in paper_topics:
        primary.setdefault(pid, tid)
    ext = dict(dst.execute("SELECT paper_id, coalesce(principal_results,'') || ' ' || "
                           "coalesce(engineering_implications,'') FROM paper_extractions"))
    dst.executemany(ins, [("paper", p[0], primary.get(p[0]), p[2] or "",
                           f"{p[7] or ''} {ext.get(p[0], '')}") for p in rows])

    today = date.today().isoformat()
    meta = {
        "name": "PyCoaPedia",
        "generated": today,
        "topics": str(len(topics)),
        "claims": str(len(claims)),
        "equations": str(len(equations)),
        "papers": str(len(rows)),
        "papers_screened_in_source": str(q("SELECT COUNT(*) FROM papers")[0][0]),
        "papers_open_access": str(sum(1 for r in rows if r[10])),
        "full_text_extractions": str(dst.execute(
            "SELECT COUNT(*) FROM paper_extractions "
            "WHERE extraction_source = 'full_text'").fetchone()[0]),
    }
    dst.executemany("INSERT INTO metadata VALUES (?,?)", meta.items())
    dst.commit()
    dst.execute("VACUUM")
    dst.close()
    return meta


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def cite(p: sqlite3.Row | None) -> str:
    if p is None:
        return ""
    who = p["first_author"] or "Anon."
    yr = p["year"] or "n.d."
    doi = p["doi"]
    return f"({who} {yr}, [doi:{doi}](https://doi.org/{doi}))" if doi else f"({who} {yr})"


VERSION_LABEL = {"version_of_record": "published version",
                 "accepted_manuscript": "accepted manuscript",
                 "submitted_manuscript": "submitted manuscript",
                 "preprint": "preprint"}


def open_copy(p: sqlite3.Row | None) -> str:
    if p is None or not p["open_url"]:
        return ""
    ver = VERSION_LABEL.get(p["open_version"], "open copy")
    return f" [{ver}, {p['open_license']}]({p['open_url']})"


def one_line(text) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def build_markdown(db: Path, meta: dict) -> None:
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    papers = {r["id"]: r for r in con.execute("SELECT * FROM papers")}
    topics = {r["id"]: r for r in con.execute("SELECT * FROM topics ORDER BY id")}
    children: dict[str | None, list[str]] = {}
    for tid, t in topics.items():
        children.setdefault(t["parent_id"], []).append(tid)
    modules_of: dict[str, list[str]] = {}
    for r in con.execute("SELECT module_label, topic_id FROM module_topics"):
        modules_of.setdefault(r["topic_id"], []).append(r["module_label"])

    if MD_DIR.exists():
        shutil.rmtree(MD_DIR)
    MD_DIR.mkdir(parents=True)

    for tid, t in topics.items():
        lines = [f"# {t['label']}", "",
                 f"`{tid}` | {one_line(t['description'])}", ""]
        crumbs = []
        parent = t["parent_id"]
        while parent:
            crumbs.insert(0, f"[{topics[parent]['label']}]({parent}.md)")
            parent = topics[parent]["parent_id"]
        if crumbs:
            lines += ["Parent: " + " > ".join(crumbs), ""]
        kids = children.get(tid, [])
        if kids:
            lines += ["Subtopics: " + ", ".join(f"[{topics[k]['label']}]({k}.md)" for k in kids), ""]
        lines += [f"Papers: {t['n_papers']}. Claims: {t['n_claims']}. "
                  f"Equations: {t['n_equations']}.", ""]
        if tid in modules_of:
            lines += ["Used by pyCoastal design modules: " + ", ".join(modules_of[tid]) + ".", ""]

        syn: dict[str, list[str]] = {}
        for r in con.execute("SELECT section, statement FROM synthesis WHERE topic_id=?", (tid,)):
            syn.setdefault(r["section"], []).append(one_line(r["statement"]))
        if syn:
            lines += ["## Synthesis", ""]
            for key, title in SECTIONS + [(k, k.replace("_", " ").capitalize())
                                          for k in syn if k not in dict(SECTIONS)]:
                if key in syn:
                    lines += [f"**{title}.** " + " ".join(syn.pop(key)), ""]

        eqs = con.execute("SELECT * FROM equations WHERE topic_id=?", (tid,)).fetchall()
        if eqs:
            lines += ["## Equations", ""]
            for e in eqs:
                lines += [f"### {one_line(e['name']) or 'Equation'}", "",
                          "$$", one_line(e["latex"]), "$$", ""]
                if e["regime"]:
                    lines += [f"Regime: {one_line(e['regime'])}", ""]
                try:
                    var = json.loads(e["variables"]) if e["variables"] else {}
                except ValueError:
                    var = {"": e["variables"]}
                if isinstance(var, dict) and var:
                    lines += ["Variables: " + "; ".join(
                        f"`{k}` {one_line(v)}" if k else one_line(v) for k, v in var.items()), ""]
                lines += [f"Source: {cite(papers.get(e['paper_id']))}", ""]

        claims = con.execute("SELECT * FROM claims WHERE topic_id=?", (tid,)).fetchall()
        if claims:
            lines += ["## Claims", ""]
            for c in claims:
                tag = ", ".join(x for x in (c["confidence"], c["evidence_type"]) if x)
                line = f"- **C{c['id']}.** {one_line(c['text'])}"
                if c["regime"]:
                    line += f" *Regime: {one_line(c['regime'])}.*"
                if tag:
                    line += f" [{tag}]"
                line += f" {cite(papers.get(c['paper_id']))}"
                lines.append(line)
            lines.append("")

        key_papers = con.execute(
            "SELECT p.* FROM paper_topics pt JOIN papers p ON p.id = pt.paper_id "
            "WHERE pt.topic_id=? ORDER BY (pt.role='specific') DESC, "
            "coalesce(p.citation_count,0) DESC LIMIT 25", (tid,)).fetchall()
        if key_papers:
            lines += ["## Papers", ""]
            for p in key_papers:
                doi = f" [doi:{p['doi']}](https://doi.org/{p['doi']})" if p["doi"] else ""
                lines.append(f"- {p['first_author'] or 'Anon.'} ({p['year'] or 'n.d.'}). "
                             f"{one_line(p['title'])}. *{one_line(p['journal'])}*."
                             f"{doi}{open_copy(p)}")
            if t["n_papers"] > len(key_papers):
                lines.append(f"- ... and {t['n_papers'] - len(key_papers)} more in "
                             "`pycoapedia.sqlite` (table `paper_topics`).")
            lines.append("")
        (MD_DIR / f"{tid}.md").write_text("\n".join(lines), encoding="utf-8")

    # Index: the tree.
    idx = ["# PyCoaPedia", "",
           "The pyCoastal knowledge base: peer-reviewed coastal and ocean engineering "
           "distilled into topics, synthesis, claims with their regimes, and equations, "
           "every piece traceable to a DOI.", "",
           f"Generated {meta['generated']}: {meta['topics']} topics, {meta['claims']} claims, "
           f"{meta['equations']} equations, {meta['papers']} papers. "
           f"{meta['papers_open_access']} papers link to a lawful open copy, and "
           f"{meta['full_text_extractions']} extractions were made from the full text "
           "(the rest from the abstract).", "",
           "- Browse the topic tree below, or [by pyCoastal design module](modules.md).",
           "- Query it: [`SCHEMA.md`](SCHEMA.md) describes the SQLite database "
           "(`pyCoastal/pedia/pycoapedia.sqlite`) and its full-text index.",
           "- From Python: `from pyCoastal import pedia; pedia.search('overtopping')`.",
           "- From the shell: `python -m pyCoastal.pedia search \"wave overtopping\"`.",
           "", "## Topic tree", ""]

    def walk(tid: str, depth: int) -> None:
        t = topics[tid]
        idx.append(f"{'  ' * depth}- [{t['label']}](topics/{tid}.md) `{tid}` "
                   f"({t['n_claims']} claims, {t['n_papers']} papers)")
        for k in children.get(tid, []):
            walk(k, depth + 1)

    for root in children.get(None, []):
        walk(root, 0)
    (HERE / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

    mods = ["# PyCoaPedia by pyCoastal design module", "",
            "Each design module of pyCoastal (and of the PyCoaTools browser app) is "
            "mapped to the topics whose literature bears on it.", ""]
    for key, m in MODULE_TOPICS.items():
        mods += [f"## {m['label']} (`{key}`)", "", m["blurb"], ""]
        for t in m["topics"]:
            if t in topics:
                mods.append(f"- [{topics[t]['label']}](topics/{t}.md) `{t}`")
        mods.append("")
    (HERE / "modules.md").write_text("\n".join(mods), encoding="utf-8")
    con.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--db", type=Path, required=True,
                        help="the source knowledge database (coastalwiki.db)")
    args = parser.parse_args()
    if not args.db.exists():
        raise SystemExit(f"No database at {args.db}")

    src_path = snapshot(args.db)
    src = sqlite3.connect(src_path)
    meta = build_sqlite(src, DB_OUT)
    src.close()
    print(f"Wrote {DB_OUT.relative_to(ROOT)} ({DB_OUT.stat().st_size / 1e6:.1f} MB): "
          f"{meta['topics']} topics, {meta['claims']} claims, "
          f"{meta['equations']} equations, {meta['papers']} papers")

    build_markdown(DB_OUT, meta)
    print(f"Wrote {len(list(MD_DIR.glob('*.md')))} topic pages in "
          f"{MD_DIR.relative_to(ROOT)}")

    extract = build_extract(src_path)
    JSON_OUT.write_text(json.dumps(extract, separators=(",", ":"), ensure_ascii=False),
                        encoding="utf-8")
    print(f"Wrote {JSON_OUT.relative_to(ROOT)} ({JSON_OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
