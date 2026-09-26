"""
Command line for PyCoaPedia.

    python -m pyCoastal.pedia stats
    python -m pyCoastal.pedia search "wave overtopping" [--kind claim] [--topic structures] [--limit 10]
    python -m pyCoastal.pedia tree [ROOT]
    python -m pyCoastal.pedia topic structures.overtopping [--claims] [--json]
    python -m pyCoastal.pedia module seawall
    python -m pyCoastal.pedia paper --doi 10.1016/...   (or an integer id)
    python -m pyCoastal.pedia sql "SELECT id, label FROM topics WHERE level = 0"

Add ``--json`` to any command for machine-readable output, which is what an
agent should ask for.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap

from . import (SECTIONS, connect, for_module, modules, paper, search, stats,
               topic, tree)


def _print(obj, as_json: bool, render) -> None:
    if as_json:
        json.dump(obj, sys.stdout, indent=1, ensure_ascii=False, default=str)
        sys.stdout.write("\n")
    else:
        render(obj)


def _wrap(text: str, indent: str = "  ") -> str:
    return textwrap.fill(" ".join(str(text).split()), width=96,
                         initial_indent=indent, subsequent_indent=indent)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="python -m pyCoastal.pedia",
                                     description="Navigate PyCoaPedia.")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats")
    s = sub.add_parser("search")
    s.add_argument("text")
    s.add_argument("--kind", choices=["topic", "synthesis", "claim", "equation", "paper"])
    s.add_argument("--topic")
    s.add_argument("--limit", type=int, default=15)
    s.add_argument("--raw", action="store_true", help="treat TEXT as an FTS5 query")
    t = sub.add_parser("tree")
    t.add_argument("root", nargs="?")
    tp = sub.add_parser("topic")
    tp.add_argument("id")
    tp.add_argument("--claims", action="store_true", help="list every claim")
    m = sub.add_parser("module")
    m.add_argument("name", nargs="?")
    p = sub.add_parser("paper")
    p.add_argument("id", nargs="?", type=int)
    p.add_argument("--doi")
    q = sub.add_parser("sql")
    q.add_argument("query")
    for sp in sub.choices.values():
        sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.cmd == "stats":
        _print(stats(), args.json, lambda d: [print(f"{k:28s} {v}") for k, v in d.items()])

    elif args.cmd == "search":
        hits = search(args.text, kind=args.kind, topic=args.topic, limit=args.limit,
                      raw=args.raw)

        def show(hits):
            for h in hits:
                print(f"[{h['kind']} {h['ref']}] {h['topic_id'] or ''}  {h['title']}")
                print(_wrap(h["snippet"]))
        _print(hits, args.json, show)

    elif args.cmd == "tree":
        nodes = tree(args.root)
        _print(nodes, args.json, lambda ns: [print(
            f"{'  ' * n['depth']}{n['label']}  [{n['id']}]  "
            f"{n['n_claims']} claims, {n['n_papers']} papers") for n in ns])

    elif args.cmd == "topic":
        t = topic(args.id)

        def show(t):
            print(f"{t['label']}  [{t['id']}]")
            print(_wrap(t["description"] or ""))
            print(f"  papers {t['n_papers']}, claims {t['n_claims']}, "
                  f"equations {t['n_equations']}; subtopics: {', '.join(t['children']) or '-'}")
            if t["modules"]:
                print(f"  pyCoastal modules: {', '.join(t['modules'])}")
            for k in SECTIONS:
                if k in t["synthesis"]:
                    print(f"\n{k.replace('_', ' ').upper()}")
                    print(_wrap(t["synthesis"][k]))
            for e in t["equations"]:
                print(f"\nEQUATION {e['name']}: {e['latex']}")
            cl = t["claims"] if args.claims else t["claims"][:8]
            if cl:
                print("\nCLAIMS" + ("" if args.claims else f" (first {len(cl)}; --claims for all)"))
                for c in cl:
                    print(_wrap(f"C{c['id']}. {c['text']} ({c['first_author']} {c['year']})"))
        _print(t, args.json, show)

    elif args.cmd == "module":
        if args.name:
            for_module(args.name)  # raises with the options on a bad name
            data = {args.name: modules()[args.name]}
        else:
            data = modules()

        def show(d):
            for key, mod in d.items():
                print(f"{key}: {mod.get('label', '')}")
                for tid in mod["topics"]:
                    print(f"  - {tid}")
        _print(data, args.json, show)

    elif args.cmd == "paper":
        pp = paper(args.id, doi=args.doi)

        def show(pp):
            print(f"{pp['first_author']} ({pp['year']}). {pp['title']}. {pp['journal']}. "
                  f"doi:{pp['doi']}")
            if pp.get("open_url"):
                print(f"Open copy ({pp['open_version'] or 'version not stated'}, "
                      f"{pp['open_license']}): {pp['open_url']}")
            if pp.get("abstract"):
                print(_wrap(pp["abstract"]))
            for k, v in pp["extraction"].items():
                print(f"\n{k.replace('_', ' ').upper()}")
                print(_wrap(v))
            print(f"\nTopics: {', '.join(pp['topics'])}")
        _print(pp, args.json, show)

    elif args.cmd == "sql":
        rows = [dict(r) for r in connect().execute(args.query).fetchall()]
        _print(rows, args.json, lambda rs: [print(r) for r in rs])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
