"""PyCoaPedia: the shipped knowledge base and its reader."""

import json

import pytest

from pyCoastal import pedia
from pyCoastal.pedia.__main__ import main as cli


def test_database_ships_with_counts():
    s = pedia.stats()
    assert s["name"] == "PyCoaPedia"
    for key in ("topics", "claims", "equations", "papers"):
        assert int(s[key]) > 0


def test_tree_starts_at_the_top_level_branches():
    roots = pedia.children(None)
    assert roots and all(r["parent_id"] is None for r in roots)
    nodes = pedia.tree(roots[0]["id"])
    assert nodes[0]["depth"] == 0
    assert all(n["id"].startswith(roots[0]["id"]) for n in nodes)


def test_topic_carries_synthesis_claims_and_papers():
    t = pedia.topic("structures.overtopping")
    assert t["label"]
    assert "well_established" in t["synthesis"]
    assert len(t["claims"]) == t["n_claims"]
    assert "seawall" in t["modules"]


def test_unknown_topic_suggests_close_matches():
    with pytest.raises(KeyError, match="overtopping"):
        pedia.topic("overtopping")


def test_search_finds_and_filters():
    hits = pedia.search("overtopping foreshore", limit=10)
    assert hits
    claims_only = pedia.search("overtopping", kind="claim", limit=10)
    assert claims_only and all(h["kind"] == "claim" for h in claims_only)
    scoped = pedia.search("scour", topic="scour", limit=10)
    assert all(h["topic_id"] is None or h["topic_id"].startswith("scour") for h in scoped)


def test_search_survives_punctuation():
    assert isinstance(pedia.search('Rc/Hm0 "quoted" (brackets)'), list)


def test_every_claim_cites_a_paper_in_the_database():
    con = pedia.connect()
    orphans = con.execute(
        "SELECT COUNT(*) FROM claims c LEFT JOIN papers p ON p.id = c.paper_id "
        "WHERE p.id IS NULL").fetchone()[0]
    assert orphans == 0


def test_every_mapped_design_module_has_topics():
    mods = pedia.modules()
    for key in ("seawall", "structures", "channel", "piles", "surge", "port",
                "nourishment", "extremes"):
        assert pedia.for_module(key)
        assert mods[key]["topics"]


def test_paper_lookup_by_id_and_doi():
    c = pedia.claims("structures.overtopping")[0]
    p = pedia.paper(c["paper_id"])
    assert c["id"] in [x["id"] for x in p["claims"]]
    if p["doi"]:
        assert pedia.paper(doi=p["doi"].upper())["id"] == p["id"]


def test_open_copies_are_lawful_and_never_local():
    s = pedia.stats()
    assert 0 < int(s["papers_open_access"]) <= int(s["papers"])
    assert 0 < int(s["full_text_extractions"]) <= int(s["papers"])
    rows = pedia.connect().execute(
        "SELECT access, open_url, open_version, open_license FROM papers").fetchall()
    for access, url, version, license_ in rows:
        assert access in ("open", "restricted", "unavailable", "unknown")
        if url:
            assert access == "open" and url.startswith("http")
            assert license_ == "read only" or license_ == "public domain" \
                or license_.startswith("CC BY")
        else:
            assert version is None
    sources = {r[0] for r in pedia.connect().execute(
        "SELECT DISTINCT extraction_source FROM paper_extractions")}
    assert sources <= {"full_text", "abstract"}


def test_knowledge_extract_carries_open_copies():
    path = pedia.database_path().parents[2] / "webapp" / "knowledge.json"
    if not path.exists():
        pytest.skip("webapp not in this checkout")
    papers = json.loads(path.read_text(encoding="utf-8"))["papers"]
    with_copy = [p for p in papers.values() if "oa" in p]
    assert with_copy and all(p["oa"].startswith("http") and p["l"] for p in with_copy)


def test_cli_json_output(capsys):
    assert cli(["--json", "search", "overtopping", "--limit", "3"]) == 0
    hits = json.loads(capsys.readouterr().out)
    assert 0 < len(hits) <= 3
