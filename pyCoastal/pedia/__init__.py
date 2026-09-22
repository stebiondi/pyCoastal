"""
PyCoaPedia: navigate the coastal and ocean engineering literature.

PyCoaPedia is pyCoastal's knowledge base. The peer-reviewed literature is
distilled into a tree of topics, each with a curated synthesis (what is well
established, the governing physics, validated ranges, disagreements, open
questions, and so on), atomic claims that each carry the regime they were
established in and the paper they come from, equations with their variables
and regime, and per-paper extractions. Every piece is traceable to a DOI.

It ships as one SQLite file, ``pycoapedia.sqlite``, beside this module, with
a full-text index. This module is a thin, dependency-free reader over it:

    >>> from pyCoastal import pedia
    >>> pedia.stats()
    >>> for hit in pedia.search("overtopping shallow foreshore", limit=5):
    ...     print(hit["kind"], hit["title"])
    >>> t = pedia.topic("structures.overtopping")
    >>> t["synthesis"]["validated_ranges"]
    >>> pedia.claims("structures.overtopping", evidence="experimental")
    >>> pedia.for_module("seawall")          # topics behind a design module
    >>> pedia.paper(doi="10.1016/j.coastaleng.2016.07.002")

The same queries run from the shell:

    python -m pyCoastal.pedia search "wave overtopping" --limit 10
    python -m pyCoastal.pedia tree structures
    python -m pyCoastal.pedia topic structures.overtopping
    python -m pyCoastal.pedia module seawall

For anything these helpers do not cover, open the database directly with
``pedia.connect()`` (or any SQLite client); ``pedia/SCHEMA.md`` in the
repository documents every table. Set ``PYCOAPEDIA_DB`` to point at a
different build of the database.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from functools import lru_cache
from pathlib import Path

__all__ = [
    "connect", "stats", "tree", "children", "topic", "search", "claims",
    "equations", "papers", "paper", "for_module", "modules", "related_claims",
    "SECTIONS",
]

#: Synthesis sections, in reading order.
SECTIONS = (
    "well_established", "governing_physics", "dimensionless_parameters",
    "major_equations", "typical_methods", "numerical_models",
    "experimental_datasets", "validated_ranges", "recent_advances",
    "disagreements", "limitations", "open_questions", "seminal_papers",
)

_DEFAULT = Path(__file__).with_name("pycoapedia.sqlite")


def database_path() -> Path:
    """Where the database is read from: ``PYCOAPEDIA_DB``, else the packaged copy."""
    return Path(os.environ.get("PYCOAPEDIA_DB", _DEFAULT))


@lru_cache(maxsize=None)
def _connection(path: str) -> sqlite3.Connection:
    if not Path(path).exists():
        raise FileNotFoundError(
            f"PyCoaPedia database not found at {path}. Build it with "
            "`python pedia/build_pedia.py --db <source.db>` or set PYCOAPEDIA_DB.")
    con = sqlite3.connect(f"file:{Path(path).as_posix()}?mode=ro", uri=True,
                          check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def connect() -> sqlite3.Connection:
    """A read-only connection to the database, rows as ``sqlite3.Row``."""
    return _connection(str(database_path()))


def _rows(sql: str, *args) -> list[dict]:
    return [dict(r) for r in connect().execute(sql, args).fetchall()]


def stats() -> dict:
    """Build date and counts."""
    return {r["key"]: r["value"] for r in _rows("SELECT key, value FROM metadata")}


# ---------------------------------------------------------------------------
# The topic tree
# ---------------------------------------------------------------------------

def children(topic_id: str | None = None) -> list[dict]:
    """Direct subtopics of ``topic_id``, or the top-level branches when None."""
    if topic_id is None:
        return _rows("SELECT * FROM topics WHERE parent_id IS NULL ORDER BY id")
    return _rows("SELECT * FROM topics WHERE parent_id = ? ORDER BY id", topic_id)


def tree(root: str | None = None) -> list[dict]:
    """The subtree under ``root`` (the whole tree when None), depth first.

    Each entry carries ``depth`` relative to the root, so printing
    ``"  " * depth + label`` draws the tree.
    """
    out: list[dict] = []

    def walk(node: dict, depth: int) -> None:
        out.append({**node, "depth": depth})
        for child in children(node["id"]):
            walk(child, depth + 1)

    starts = children(None) if root is None else _rows(
        "SELECT * FROM topics WHERE id = ?", root)
    if root is not None and not starts:
        raise KeyError(f"No topic {root!r}")
    for node in starts:
        walk(node, 0)
    return out


def topic(topic_id: str) -> dict:
    """Everything about one topic: synthesis, claims, equations, key papers."""
    rows = _rows("SELECT * FROM topics WHERE id = ?", topic_id)
    if not rows:
        close = _rows("SELECT id FROM topics WHERE id LIKE ? LIMIT 8", f"%{topic_id}%")
        hint = f" Did you mean: {', '.join(r['id'] for r in close)}?" if close else ""
        raise KeyError(f"No topic {topic_id!r}.{hint}")
    t = rows[0]
    synthesis: dict[str, str] = {}
    for r in _rows("SELECT section, statement FROM synthesis WHERE topic_id = ?", topic_id):
        synthesis[r["section"]] = (synthesis.get(r["section"], "") + " " + r["statement"]).strip()
    t["synthesis"] = {k: synthesis[k] for k in SECTIONS if k in synthesis} | {
        k: v for k, v in synthesis.items() if k not in SECTIONS}
    t["children"] = [c["id"] for c in children(topic_id)]
    t["claims"] = claims(topic_id)
    t["equations"] = equations(topic_id)
    t["papers"] = papers(topic_id, limit=25)
    t["modules"] = [r["module"] for r in _rows(
        "SELECT module FROM module_topics WHERE topic_id = ?", topic_id)]
    return t


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def _fts_query(text: str) -> str:
    """Turn free text into an FTS5 query: every word must appear, any order."""
    words = re.findall(r"[\w\-]+", text, flags=re.UNICODE)
    return " ".join(f'"{w}"' for w in words if len(w) > 1) or '""'


def search(text: str, kind: str | None = None, topic: str | None = None,
           limit: int = 20, raw: bool = False) -> list[dict]:
    """Full-text search over topics, synthesis, claims, equations and papers.

    Parameters
    ----------
    text : str
        Free text. Every word has to match (stemmed, so "overtopping"
        finds "overtopped"). Pass ``raw=True`` to give an FTS5 query
        instead, with OR, NEAR, quotes and prefixes (``scour*``).
    kind : str, optional
        Restrict to "topic", "synthesis", "claim", "equation" or "paper".
    topic : str, optional
        Restrict to a topic and everything under it.
    limit : int
        Number of hits, best first.

    Returns
    -------
    list of dict
        ``kind``, ``ref`` (the id to look up), ``topic_id``, ``title`` and a
        highlighted ``snippet``.
    """
    sql = ("SELECT kind, ref, topic_id, title, "
           "snippet(search, 4, '[', ']', ' ... ', 24) AS snippet, rank "
           "FROM search WHERE search MATCH ?")
    args: list = [text if raw else _fts_query(text)]
    if kind:
        sql += " AND kind = ?"
        args.append(kind)
    if topic:
        sql += " AND (topic_id = ? OR topic_id LIKE ?)"
        args += [topic, f"{topic}.%"]
    sql += " ORDER BY rank LIMIT ?"
    args.append(limit)
    return _rows(sql, *args)


# ---------------------------------------------------------------------------
# Claims, equations, papers
# ---------------------------------------------------------------------------

def claims(topic_id: str | None = None, evidence: str | None = None,
           confidence: str | None = None, contains: str | None = None,
           subtopics: bool = False, limit: int | None = None) -> list[dict]:
    """Claims, filtered, each with its citation.

    ``evidence`` is one of field, experimental, numerical, analytical,
    mixed or review; ``confidence`` one of direct_finding,
    literature_review_statement, inferred_relationship or
    proposed_hypothesis. ``subtopics=True`` includes the topics below.
    """
    sql = ("SELECT c.*, p.first_author, p.year, p.doi, p.title AS paper_title "
           "FROM claims c LEFT JOIN papers p ON p.id = c.paper_id WHERE 1=1")
    args: list = []
    if topic_id:
        if subtopics:
            sql += " AND (c.topic_id = ? OR c.topic_id LIKE ?)"
            args += [topic_id, f"{topic_id}.%"]
        else:
            sql += " AND c.topic_id = ?"
            args.append(topic_id)
    if evidence:
        sql += " AND c.evidence_type = ?"
        args.append(evidence)
    if confidence:
        sql += " AND c.confidence = ?"
        args.append(confidence)
    if contains:
        sql += " AND c.text LIKE ?"
        args.append(f"%{contains}%")
    sql += " ORDER BY c.topic_id, c.id"
    if limit:
        sql += " LIMIT ?"
        args.append(limit)
    return _rows(sql, *args)


def related_claims(claim_id: int) -> list[dict]:
    """Claims linked to this one: supports, contradicts, extends, validates, ..."""
    return _rows(
        "SELECT r.relationship, r.rationale, c.id, c.topic_id, c.text, "
        "       CASE WHEN r.source_claim_id = ? THEN 'out' ELSE 'in' END AS direction "
        "FROM claim_relationships r JOIN claims c "
        "  ON c.id = CASE WHEN r.source_claim_id = ? THEN r.target_claim_id "
        "                 ELSE r.source_claim_id END "
        "WHERE r.source_claim_id = ? OR r.target_claim_id = ?",
        claim_id, claim_id, claim_id, claim_id)


def equations(topic_id: str | None = None) -> list[dict]:
    """Equations, with variables decoded to a dict, and their source."""
    sql = ("SELECT e.*, p.first_author, p.year, p.doi FROM equations e "
           "LEFT JOIN papers p ON p.id = e.paper_id")
    rows = _rows(sql + " WHERE e.topic_id = ?", topic_id) if topic_id else _rows(sql)
    for r in rows:
        try:
            r["variables"] = json.loads(r["variables"]) if r["variables"] else {}
        except (ValueError, TypeError):
            pass
    return rows


def papers(topic_id: str, limit: int | None = 50) -> list[dict]:
    """Papers classified under a topic, topic-specific ones first, then by citations."""
    sql = ("SELECT p.id, p.doi, p.title, p.first_author, p.authors, p.year, p.journal, "
           "p.citation_count, pt.role FROM paper_topics pt JOIN papers p "
           "ON p.id = pt.paper_id WHERE pt.topic_id = ? "
           "ORDER BY (pt.role = 'specific') DESC, coalesce(p.citation_count, 0) DESC")
    if limit:
        return _rows(sql + " LIMIT ?", topic_id, limit)
    return _rows(sql, topic_id)


def paper(paper_id: int | None = None, doi: str | None = None) -> dict:
    """One paper with its abstract, extraction, topics and claims."""
    if paper_id is None and doi is None:
        raise ValueError("Give paper_id or doi.")
    rows = (_rows("SELECT * FROM papers WHERE id = ?", paper_id) if paper_id is not None
            else _rows("SELECT * FROM papers WHERE lower(doi) = lower(?)", doi))
    if not rows:
        raise KeyError(f"No paper {paper_id or doi!r}")
    p = rows[0]
    ext = _rows("SELECT * FROM paper_extractions WHERE paper_id = ?", p["id"])
    p["extraction"] = {k: v for k, v in ext[0].items() if v and k != "paper_id"} if ext else {}
    p["topics"] = [r["topic_id"] for r in _rows(
        "SELECT topic_id FROM paper_topics WHERE paper_id = ?", p["id"])]
    p["claims"] = _rows("SELECT id, topic_id, text, regime FROM claims WHERE paper_id = ?",
                        p["id"])
    return p


# ---------------------------------------------------------------------------
# pyCoastal design modules
# ---------------------------------------------------------------------------

def modules() -> dict[str, dict]:
    """Design modules and the topics mapped to each."""
    out: dict[str, dict] = {}
    for r in _rows("SELECT * FROM module_topics ORDER BY module, position"):
        m = out.setdefault(r["module"], {"label": r["module_label"],
                                         "blurb": r["module_blurb"], "topics": []})
        m["topics"].append(r["topic_id"])
    return out


def for_module(module: str) -> list[dict]:
    """The topics behind a pyCoastal design module, e.g. "seawall" or "channel"."""
    rows = _rows("SELECT t.* FROM module_topics m JOIN topics t ON t.id = m.topic_id "
                 "WHERE m.module = ? ORDER BY m.position", module)
    if not rows:
        raise KeyError(f"No module {module!r}. Options: {sorted(modules())}")
    return rows
