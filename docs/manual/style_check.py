"""
Check the manual chapters against docs/manual/STYLE.md.

The manual is an engineering reference: impersonal, declarative, free of
argument by contrast, metaphor, evaluative adjectives and reader-directed
language. This flags the patterns that specification prohibits.

    python docs/manual/style_check.py            # report
    python docs/manual/style_check.py --quiet    # counts only, exit 1 if any

Code blocks, captured program output, raw LaTeX blocks and inline code are
skipped: they quote the software, not the prose.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parent / "chapters"

#: (name, pattern, note). Patterns run case-insensitively on prose only.
RULES: list[tuple[str, str, str]] = [
    ("contrast", r"\b(rather than|instead of|as opposed to)\b",
     "state the behavior directly"),
    ("contrast", r",\s+not\s+(?:a|an|the|as|by|from|to|one|his|its|what|where|how)\b",
     "\"X, not Y\": state X"),
    ("contrast", r"\bnot\s+\w+,\s+but\b", "\"not X, but Y\": state Y"),
    ("contrast", r"\bis not (?:a|an|the)\b", "state the scope positively"),
    ("causality", r"\b(because|that is why|which is why|the reason)\b",
     "keep only technical causality"),
    # Case-sensitive: "US" in a reference is not the pronoun "us".
    ("second person", r"\b(?-i:you|your|yours|we|our|ours|us)\b",
     "use impersonal forms"),
    ("reader-directed", r"\b(note that|remember|keep in mind|as we saw|let us|"
                        r"bear in mind|do not forget)\b", "remove"),
    ("evaluative", r"\b(honest(?:ly)?|easiest|easy|hardest|trap|pitfall|lesson|"
                   r"all-rounder|benign|deliberately|of course|simply|just|"
                   r"obvious(?:ly)?|clever|elegant|nice(?:ly)?|unfortunately|"
                   r"sadly|luckily|surprisingly|absurd|nonsense|wrong-headed|"
                   r"worth (?:knowing|seeing|having|doing|it)|the point is|"
                   r"interesting(?:ly)?|crucial(?:ly)?|vital)\b", "state behavior"),
    ("metaphor", r"\b(brick|hairline|clock|cliff|ring(?:s|ing)? around|"
                 r"stands on|hand(?:s|ed)? (?:it |them |the )?(?:over|back)|"
                 r"under the hood|black box|out of the box|rule of thumb|"
                 r"back of an? envelope|in the wild|heart of|core of the story|"
                 r"tell(?:s)? the story|paints?|reads? like|feels? like)\b",
     "use literal wording"),
    ("hedging", r"\b(arguably|presumably|one might|it turns out|as it happens|"
                r"in practice, though|happily)\b", "remove"),
    ("rhetorical question", r"[^.!?]*\?(?:\s|$)", "state the answer"),
]

SKIP_BLOCK = re.compile(
    r"(```.*?```|^:::.*?^:::|\$\$.*?\$\$)", re.S | re.M)
# Image and link targets are blanked; caption and link text stays, because a
# caption is prose and is checked with the rest.
SKIP_INLINE = re.compile(r"(`[^`]*`|\$[^$\n]+\$|\]\([^)]*\)(?:\{[^}\n]*\})?)")


def prose(text: str) -> str:
    """Blank out everything that is not prose, keeping offsets."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    text = SKIP_BLOCK.sub(blank, text)
    text = SKIP_INLINE.sub(blank, text)
    # headings and table rows are labels, not prose
    text = re.sub(r"^(#+ .*|\|.*)$", blank, text, flags=re.M)
    return text


def check(path: Path) -> list[tuple[int, str, str, str]]:
    text = path.read_text(encoding="utf-8")
    clean = prose(text)
    hits = []
    for name, pattern, note in RULES:
        for m in re.finditer(pattern, clean, re.I):
            line = clean[:m.start()].count("\n") + 1
            source = text.splitlines()[line - 1].strip()
            hits.append((line, name, m.group(0).strip(), source))
    return sorted(hits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--quiet", action="store_true", help="counts only")
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()

    paths = args.files or sorted(CHAPTERS.glob("*.md"))
    total = 0
    for path in paths:
        hits = check(path)
        total += len(hits)
        if hits and not args.quiet:
            print(f"\n{path.name}")
            for line, name, found, source in hits:
                print(f"  {line:5d}  {name:18s} {found!r}")
                print(f"         {source[:100]}")
        elif hits:
            print(f"{path.name}: {len(hits)}")
    print(f"\n{total} style findings in {len(paths)} files")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
