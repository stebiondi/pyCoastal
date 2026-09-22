# The repository for AI agents {#sec:agents}

pyCoastal is written for two kinds of reader. Engineers read this manual.
AI agents, working on a design or answering a question on a user's behalf,
search the repository, and they work best from plain text, structured data,
and a clear map of where things are. The repository is laid out so that
every piece of knowledge in it has a machine-readable form next to the human
one (@tbl:agent-files).

: Human and machine-readable forms of the same knowledge. {#tbl:agent-files}

| Knowledge | For people | For agents |
|-------------------------|-------------------------------|----------------------------------------------|
| Where everything is | this manual, `README.md` | `AGENTS.md`, `llms.txt` |
| Theory and usage | `pyCoastal manual.pdf` | `docs/manual/chapters/*.md` |
| API | the source | `docs/reference/*.md`, one file per module |
| Worked examples | Part IV | `examples/*.py`, `docs/examples.md` |
| Literature | PyCoaPedia explorer | `pycoapedia.sqlite`, `pedia/topics/*.md`, `python -m pyCoastal.pedia --json` |

## Entry points

**`AGENTS.md`** at the repository root is the map an agent should read
first: what each directory holds, the conventions (units, levels, axis
order), how to run the tests and the examples, how to query PyCoaPedia, and
the rules the code follows (every relation names its source, nothing
silently extrapolates, warnings are part of the result). **`llms.txt`**
gives the same map in the compact format some tools look for.

**The manual chapters** in `docs/manual/chapters/` are Markdown with LaTeX
mathematics, one file per chapter, which is exactly the source of this PDF;
an agent can search them without parsing a PDF.

**The API reference** in `docs/reference/` is generated from the docstrings
by the manual build, one Markdown file per module with every public class,
function and constant, its signature, and its full docstring, so it cannot
drift from the code.

**The example index** `docs/examples.md` lists every script in `examples/`
with what it demonstrates and how to run it.

## Querying the literature

For literature questions an agent should use the database rather than read
Markdown pages one by one. A good pattern is search, then open, then cite:

```bash
python -m pyCoastal.pedia --json search "toe scour vertical wall" --limit 20
python -m pyCoastal.pedia --json topic scour.structures
python -m pyCoastal.pedia --json paper 2229
```

Every claim returned carries its regime and its source paper, with the DOI,
so an answer built from PyCoaPedia can state where each statement holds and
where it comes from. `pedia/SCHEMA.md` lists the tables, the controlled
vocabularies, and worked SQL queries for anything the command line does not
cover.

## Keeping it current

`python docs/manual/build_manual.py` regenerates the PDF, the API reference
and the example index; `python pedia/build_pedia.py --db <source>` refreshes
the knowledge base in all its forms. Both are deterministic, so their output
belongs in version control and a diff shows exactly what changed.
