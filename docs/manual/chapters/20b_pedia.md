# Part VII. PyCoaPedia and agentic retrieval {.part .unnumbered}

# PyCoaPedia: the knowledge base {#sec:pedia}

Every design relation in pyCoastal names a source and states where it stops
being valid. PyCoaPedia holds the same shape of information for the wider
literature, as data: the peer-reviewed coastal and ocean engineering
literature distilled into a tree of topics, each with a curated synthesis,
atomic claims that carry the regime they were established in, equations with
their variables, and structured extractions of each paper, every piece
traceable to a DOI. A relation quoted outside its range is the most
expensive kind of mistake, and PyCoaPedia exists so that the range is always
one query away.

## What is in it

<!-- pedia-stats -->

The knowledge is organized around four kinds of record.

**Topics** form a tree, from 26 top-level branches (waves, structures,
scour, sediment transport, storm surge, ports, numerical modeling, and so
on) down to specific subjects such as `structures.overtopping` or
`waves.transformation.breaking.runup`. The dotted identifier is the path.

**Synthesis** is written per topic under fixed headings: what is well
established, the governing physics, the dimensionless parameters, the major
equations, typical methods, numerical models, experimental datasets,
validated ranges, recent advances, disagreements, limitations, open
questions, and the seminal papers. It is the place to start on a topic.

**Claims** are atomic findings. Each carries the regime it holds in, a
confidence class (a direct finding, a literature review statement, an
inferred relationship, or a proposed hypothesis), the kind of evidence
(field, experimental, numerical, analytical, mixed, or review), the location
in the paper, and the paper itself. Claims are linked to each other where
one supports, contradicts, extends, validates, or compares against another,
which is how disagreement in the literature becomes something that can be
queried rather than remembered.

**Papers** carry their bibliographic record and abstract, the topics they
are classified under, and a structured extraction: the research question,
the principal results, the quantitative findings, the parameter ranges, the
engineering implications, the limitations and the applicability conditions.
Parameters, numerical models, datasets and field sites used by each paper
are recorded as well.

## How it is built

PyCoaPedia is distilled from a larger research database that an ingestion
pipeline keeps growing: literature discovery through Crossref, OpenAlex and
Semantic Scholar, relevance screening, classification into the topic tree,
and extraction of claims, equations and paper summaries. That database also
holds discovery logs, raw source records and full-text bookkeeping, and is
not shipped. `pedia/build_pedia.py` takes a snapshot of it and writes three
things from one pass, so they cannot disagree (@fig:pedia-flow):

- `pyCoastal/pedia/pycoapedia.sqlite`, the distilled database with a
  full-text index, shipped inside the Python package;
- `pedia/topics/*.md`, one Markdown page per topic, with an index
  (`pedia/README.md`), a module map (`pedia/modules.md`) and the schema
  (`pedia/SCHEMA.md`);
- `webapp/knowledge.json`, the extract the PyCoaTools app and the PyCoaPedia
  explorer load.

```bash
python pedia/build_pedia.py --db ../2026_CoastalWiki/data/coastalwiki.db
```

Rerunning it after the pipeline has added papers refreshes all three, and
the tests in `tests/test_pedia.py` check the result.

```{=latex}
\begin{figure}[htbp]
\centering
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{c}
\fbox{\parbox{0.62\linewidth}{\centering Research database (discovery, screening,
classification, extraction), about 150 MB, not shipped}}\\[1mm]
$\downarrow$ \texttt{pedia/build\_pedia.py} (one snapshot, one pass)\\[1mm]
\begin{tabular}{ccc}
\fbox{\parbox{0.27\linewidth}{\centering\texttt{pycoapedia.sqlite}\\ SQL and full-text search\\ Python, CLI, agents}} &
\fbox{\parbox{0.27\linewidth}{\centering\texttt{pedia/topics/*.md}\\ one page per topic\\ GitHub, file search}} &
\fbox{\parbox{0.27\linewidth}{\centering\texttt{knowledge.json}\\ PyCoaPedia explorer\\ PyCoaTools panel}}
\end{tabular}
\end{tabular}
\caption{How PyCoaPedia is built and where each output is read.}
\label{fig:pedia-flow}
\end{figure}
```

## Navigating the knowledge

The same knowledge can be reached five ways, and they suit different
readers. A typical workflow runs from the design question to the evidence:
start from the pyCoastal module you are using, read the synthesis of its
topics (above all the validated ranges and the disagreements), then drill
into the claims whose regime matches the case, and from a claim to its paper
and the paper's quantitative findings.

### In the browser: the PyCoaPedia explorer

`webapp/pedia.html` is a standalone page that loads the same extract as
PyCoaTools. The topic tree is on the left with the number of claims on each
branch; a search box searches topics, synthesis, claims and equations at
once; and chips filter everything to the topics behind one pyCoastal design
module. A topic page shows its breadcrumb and subtopics, the synthesis under
its headings, the equations (typeset when KaTeX is reachable), and the
claims, filterable by kind of evidence, each linking to its paper by DOI.
Topic and claim views have their own URLs, so a finding can be shared as a
link. From PyCoaTools, the PyCoaPedia button in the masthead and the Theory
and sources panel beside each design lead to the same pages.

### From Python

`pyCoastal.pedia` is a small read-only interface to the database, with no
dependencies beyond the standard library:

```python
from pyCoastal import pedia

pedia.stats()                                   # build date and counts
pedia.tree("scour")                             # a branch of the topic tree
hits = pedia.search("overtopping shallow foreshore", limit=10)
t = pedia.topic("structures.overtopping")       # synthesis, claims, equations
t["synthesis"]["validated_ranges"]
pedia.claims("structures.overtopping", evidence="experimental")
pedia.related_claims(410)                       # supports, contradicts, ...
pedia.for_module("seawall")                     # topics behind a design module
pedia.paper(doi="10.1016/j.coastaleng.2016.07.002")
```

`search` runs on an FTS5 index with Porter stemming, so every word must
appear but "overtopping" also finds "overtopped"; `kind=` restricts it to
topics, synthesis, claims, equations or papers, `topic=` to one branch, and
`raw=True` accepts the full FTS5 syntax (`OR`, `NEAR`, prefixes). For
anything else, `pedia.connect()` returns a read-only connection to the
database, and the environment variable `PYCOAPEDIA_DB` points the module at
another build.

### From the shell

```bash
python -m pyCoastal.pedia stats
python -m pyCoastal.pedia search "wave overtopping" --kind claim --limit 10
python -m pyCoastal.pedia tree structures
python -m pyCoastal.pedia topic structures.overtopping --claims
python -m pyCoastal.pedia module seawall
python -m pyCoastal.pedia paper --doi 10.1016/j.coastaleng.2016.07.002
python -m pyCoastal.pedia sql "SELECT id, label FROM topics WHERE level = 0"
```

Every command accepts `--json` for machine-readable output.

### In SQL

The database is an ordinary SQLite file, so any client or language can query
it. `pedia/SCHEMA.md` documents every table and its controlled vocabularies,
with worked queries; two of them show the idea:

```sql
-- the validated ranges behind a pyCoastal design module
SELECT m.topic_id, s.statement
FROM module_topics m JOIN synthesis s ON s.topic_id = m.topic_id
WHERE m.module = 'seawall' AND s.section = 'validated_ranges';

-- where the literature disagrees
SELECT a.text, b.text, r.rationale
FROM claim_relationships r
JOIN claims a ON a.id = r.source_claim_id
JOIN claims b ON b.id = r.target_claim_id
WHERE r.relationship = 'contradicts';
```

### As Markdown

`pedia/README.md` draws the whole topic tree with links, `pedia/modules.md`
lists the topics behind each design module, and each page in `pedia/topics/`
holds one topic: breadcrumb, subtopics, synthesis, equations in LaTeX,
claims with their regime and citation, and the most relevant papers. The
pages read on GitHub and suit tools that search files.

## The design modules and their topics

Each design module of pyCoastal, and of PyCoaTools, is mapped to the topics
whose literature bears on it (@tbl:pedia-modules). The mapping is
deliberately generous, because a design relation sits where several topics
meet: an engineer setting a crest level wants the overtopping topic and the
runup topic, not one of them.

<!-- pedia-modules -->

## Coverage and its limits

Coverage is uneven by design: PyCoaPedia records what has been screened,
not what exists. A topic with few claims is a topic that has not yet been
read closely, not one where nothing is known, and the paper counts say how
much of each branch has been screened. Claims are extracted from papers and
checked, but a claim is only as good as the regime attached to it, and it is
the regime that should be read first.
