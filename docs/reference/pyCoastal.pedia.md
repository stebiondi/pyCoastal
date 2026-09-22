# `pyCoastal.pedia`

Source: [`pyCoastal/pedia/__init__.py`](../../pyCoastal/pedia/__init__.py)

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

## `SECTIONS`

```python
SECTIONS = ('well_established', 'governing_physics', 'dimensionless_parameters', 'major_equations', 'typical_methods', 'numerical_models', 'experimental_datasets', 'validated_ranges', 'recent_advances', 'disagreements', 'limitations', 'open_questions', 'seminal_papers')
```

## `database_path`

```python
def database_path() -> Path
```

```text
Where the database is read from: ``PYCOAPEDIA_DB``, else the packaged copy.
```

## `connect`

```python
def connect() -> sqlite3.Connection
```

```text
A read-only connection to the database, rows as ``sqlite3.Row``.
```

## `stats`

```python
def stats() -> dict
```

```text
Build date and counts.
```

## `children`

```python
def children(topic_id: str | None=None) -> list[dict]
```

```text
Direct subtopics of ``topic_id``, or the top-level branches when None.
```

## `tree`

```python
def tree(root: str | None=None) -> list[dict]
```

```text
The subtree under ``root`` (the whole tree when None), depth first.

Each entry carries ``depth`` relative to the root, so printing
``"  " * depth + label`` draws the tree.
```

## `topic`

```python
def topic(topic_id: str) -> dict
```

```text
Everything about one topic: synthesis, claims, equations, key papers.
```

## `search`

```python
def search(text: str, kind: str | None=None, topic: str | None=None, limit: int=20, raw: bool=False) -> list[dict]
```

```text
Full-text search over topics, synthesis, claims, equations and papers.

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
```

## `claims`

```python
def claims(topic_id: str | None=None, evidence: str | None=None, confidence: str | None=None, contains: str | None=None, subtopics: bool=False, limit: int | None=None) -> list[dict]
```

```text
Claims, filtered, each with its citation.

``evidence`` is one of field, experimental, numerical, analytical,
mixed or review; ``confidence`` one of direct_finding,
literature_review_statement, inferred_relationship or
proposed_hypothesis. ``subtopics=True`` includes the topics below.
```

## `related_claims`

```python
def related_claims(claim_id: int) -> list[dict]
```

```text
Claims linked to this one: supports, contradicts, extends, validates, ...
```

## `equations`

```python
def equations(topic_id: str | None=None) -> list[dict]
```

```text
Equations, with variables decoded to a dict, and their source.
```

## `papers`

```python
def papers(topic_id: str, limit: int | None=50) -> list[dict]
```

```text
Papers classified under a topic, topic-specific ones first, then by citations.
```

## `paper`

```python
def paper(paper_id: int | None=None, doi: str | None=None) -> dict
```

```text
One paper with its abstract, extraction, topics and claims.
```

## `modules`

```python
def modules() -> dict[str, dict]
```

```text
Design modules and the topics mapped to each.
```

## `for_module`

```python
def for_module(module: str) -> list[dict]
```

```text
The topics behind a pyCoastal design module, e.g. "seawall" or "channel".
```

