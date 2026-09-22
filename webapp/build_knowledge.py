"""
Distil the PyCoaPedia source database into a JSON extract the browser app can load.

Normally run through ``pedia/build_pedia.py``, which writes this extract,
the shipped SQLite database and the Markdown pages from one snapshot.

The source database is about 150 MB of SQLite, which no browser is going to open.
What the app actually needs is small: the topic tree, the curated synthesis
for each topic, the atomic claims with their regime bounds, the equations,
and enough paper metadata to cite and link. That comes to a couple of
megabytes.

The point of the extract is provenance. Every design relation in pyCoastal
names a source and states where it stops being valid. The wiki holds the
same shape of information as queryable data, with a DOI behind each piece,
so the app can put the two side by side: here is the number, and here is
what the literature says about the ground it stands on.

Run it against the source database:

    python webapp/build_knowledge.py \
        --db ../2026_CoastalWiki/data/coastalwiki.db \
        --out webapp/knowledge.json
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date
from pathlib import Path

#: pyCoastal module to wiki topics. The mapping is deliberately generous:
#: a design relation usually sits at the meeting point of several topics,
#: and an engineer looking up a crest level wants the overtopping topic and
#: the runup topic, not one of them.
MODULE_TOPICS: dict[str, dict] = {
    "extremes": {
        "label": "Design conditions",
        "blurb": "Return values and their uncertainty, from a record.",
        "topics": [
            "waves.generation.extremes",
            "uncertainty.reliability",
            "uncertainty.sources",
            "risk.probabilistic",
            "field.extreme",
        ],
    },
    "seawall": {
        "label": "Seawall design",
        "blurb": "Crest level, wave pressures, stability, scour and toe.",
        "topics": [
            "structures.seawalls",
            "structures.overtopping",
            "structures.failure",
            "scour.structures",
            "scour.protection",
            "design.criteria",
        ],
    },
    "structures": {
        "label": "Breakwater design",
        "blurb": "Rock armour stability and overtopping.",
        "topics": [
            "structures.breakwaters",
            "structures.overtopping",
            "wave_structure.transmission",
            "wave_structure.porous",
            "design.performance",
        ],
    },
    "channel": {
        "label": "Navigation channel",
        "blurb": "Depth chain, squat and channel width.",
        "topics": [
            "ports.navigation",
            "ports.sedimentation",
            "ports.mooring",
            "design.guidance",
        ],
    },
    "piles": {
        "label": "Pile wave loads",
        "blurb": "Morison drag and inertia, and pile scour.",
        "topics": [
            "wave_structure.loads",
            "wave_structure.loads.impact",
            "scour.structures",
            "scour.pipelines",
        ],
    },
    "surge": {
        "label": "Storm surge and flooding",
        "blurb": "Water level budget and inundation extent.",
        "topics": [
            "storm_surge.forcing",
            "storm_surge.forcing.wind",
            "storm_surge.forcing.pressure",
            "storm_surge.coupling.wave_setup",
            "storm_surge.compound",
            "waves.transformation.breaking.runup",
            "inundation.models",
            "inundation.uncertainty",
        ],
    },
    "port": {
        "label": "Harbour agitation",
        "blurb": "Diffraction into a harbour and berth downtime.",
        "topics": [
            "ports.agitation",
            "waves.transformation.diffraction",
            "waves.transformation.reflection",
        ],
    },
    "nourishment": {
        "label": "Beach nourishment",
        "blurb": "One-line shoreline response to a fill.",
        "topics": [
            "beaches.nourishment",
            "nearshore.longshore",
            "morphodynamics.planform",
            "beaches.change",
        ],
    },
}


def fetch(connection: sqlite3.Connection, query: str, *args) -> list[sqlite3.Row]:
    return connection.execute(query, args).fetchall()


def build(db_path: Path) -> dict:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    topics: dict[str, dict] = {}
    for row in fetch(connection, "SELECT id, parent_id, label, description, level "
                                 "FROM topics WHERE active = 1 ORDER BY id"):
        topics[row["id"]] = {
            "label": row["label"],
            "parent": row["parent_id"],
            "level": row["level"],
            "description": row["description"] or "",
            "synthesis": {},
            "claims": [],
            "equations": [],
            "papers": 0,
        }

    # The curated synthesis is the most useful thing in the corpus: thirteen
    # sections per topic, written from the papers rather than scraped.
    for row in fetch(connection,
                     "SELECT topic_id, section, statement "
                     "FROM topic_synthesis_statements ORDER BY topic_id, section"):
        topic = topics.get(row["topic_id"])
        if topic and row["statement"]:
            # A section can hold several statements; keep them all.
            previous = topic["synthesis"].get(row["section"])
            topic["synthesis"][row["section"]] = (
                f"{previous} {row['statement']}" if previous else row["statement"])

    wanted_papers: set[int] = set()

    for row in fetch(connection,
                     "SELECT topic_id, paper_id, claim_text, applicable_regime, "
                     "       confidence, evidence_type "
                     "FROM knowledge_claims ORDER BY topic_id, id"):
        topic = topics.get(row["topic_id"])
        if not topic or not row["claim_text"]:
            continue
        topic["claims"].append({
            "text": row["claim_text"],
            "regime": row["applicable_regime"] or "",
            "confidence": row["confidence"] or "",
            "evidence": row["evidence_type"] or "",
            "paper": row["paper_id"],
        })
        wanted_papers.add(row["paper_id"])

    for row in fetch(connection,
                     "SELECT topic_id, paper_id, name, expression_latex, "
                     "       applicable_regime, variable_definitions "
                     "FROM equations ORDER BY topic_id, id"):
        topic = topics.get(row["topic_id"])
        if not topic or not row["expression_latex"]:
            continue
        topic["equations"].append({
            "name": row["name"] or "",
            "latex": row["expression_latex"],
            "regime": row["applicable_regime"] or "",
            "variables": row["variable_definitions"] or "",
            "paper": row["paper_id"],
        })
        wanted_papers.add(row["paper_id"])

    for row in fetch(connection,
                     "SELECT topic_id, COUNT(*) AS n FROM paper_topics "
                     "GROUP BY topic_id"):
        topic = topics.get(row["topic_id"])
        if topic:
            topic["papers"] = row["n"]

    # Only the papers something actually points at, with the few fields a
    # citation needs. Abstracts and full texts stay in the database.
    papers: dict[str, dict] = {}
    for row in fetch(connection,
                     "SELECT id, title, publication_year, journal, doi, "
                     "       citation_count FROM papers"):
        if row["id"] not in wanted_papers:
            continue
        papers[str(row["id"])] = {
            "t": row["title"] or "",
            "y": row["publication_year"],
            "j": row["journal"] or "",
            "doi": row["doi"] or "",
            "c": row["citation_count"] or 0,
        }

    # First author, so a citation reads like a citation.
    for row in fetch(connection,
                     "SELECT pa.paper_id, a.family_name, a.display_name "
                     "FROM paper_authors pa "
                     "JOIN authors a ON a.id = pa.author_id "
                     "WHERE pa.author_order = 1"):
        entry = papers.get(str(row["paper_id"]))
        if entry:
            entry["a"] = row["family_name"] or row["display_name"] or ""

    totals = {
        name: connection.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        for name in ("papers", "knowledge_claims", "equations", "topics",
                     "topic_synthesis_statements")
    }
    connection.close()

    kept = {tid: t for tid, t in topics.items()
            if t["synthesis"] or t["claims"] or t["equations"]}
    return {
        "generated": date.today().isoformat(),
        "corpus": totals,
        "included": {
            "topics": len(kept),
            "claims": sum(len(t["claims"]) for t in kept.values()),
            "equations": sum(len(t["equations"]) for t in kept.values()),
            "papers": len(papers),
        },
        "modules": MODULE_TOPICS,
        "topics": kept,
        "papers": papers,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True,
                        help="Path to the PyCoaPedia source database (coastalwiki.db)")
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).with_name("knowledge.json"))
    args = parser.parse_args()

    if not args.db.exists():
        raise SystemExit(f"No database at {args.db}")

    extract = build(args.db)
    args.out.write_text(json.dumps(extract, separators=(",", ":"),
                                   ensure_ascii=False), encoding="utf-8")

    size = args.out.stat().st_size / 1e6
    print(f"Wrote {args.out} ({size:.2f} MB)")
    print(f"  corpus   : {extract['corpus']['papers']} papers, "
          f"{extract['corpus']['knowledge_claims']} claims, "
          f"{extract['corpus']['topics']} topics")
    print(f"  included : {extract['included']['topics']} topics, "
          f"{extract['included']['claims']} claims, "
          f"{extract['included']['equations']} equations, "
          f"{extract['included']['papers']} papers")
    missing = [t for module in MODULE_TOPICS.values() for t in module["topics"]
               if t not in extract["topics"]]
    if missing:
        print(f"  WARNING  : mapped topics absent from the corpus: {missing}")


if __name__ == "__main__":
    main()
