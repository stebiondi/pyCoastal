# Part VIII. The CoastalWiki knowledge base {.part .unnumbered}

# About the knowledge base {#sec:wiki}

Every design relation in pyCoastal names a source and states where it stops
being valid. CoastalWiki holds the same shape of information as queryable
data: a provenance-first corpus of peer-reviewed coastal engineering, in
which every claim carries the regime it was established in and a DOI behind
it, because a relation quoted outside its range is the most expensive kind
of mistake. The Coastal Design Bench (Part VI) ships an extract of the wiki
and shows it beside each design; this part of the manual reproduces that
extract in full.

## What an entry contains

The wiki is organized as a topic tree (for example `structures`,
`structures.overtopping`, `structures.overtopping.*`). Each topic carries:

- a **synthesis**: curated statements under fixed headings (what is well
  established, the governing physics, the dimensionless parameters, the
  major equations, typical methods, numerical models, experimental datasets,
  validated ranges, recent advances, disagreements, limitations, open
  questions, and the seminal papers);
- **claims**: atomic findings, each with the regime it holds in, a
  confidence class (direct finding, literature review statement, inferred
  relationship, or proposed hypothesis), the kind of evidence (field,
  experimental, numerical, analytical, mixed, or review), and the paper it
  comes from;
- **equations**: named relations in LaTeX with their variables and regime;
- a count of the **papers** screened for the topic.

Citations in the following chapters are given as [number], pointing to the
wiki bibliography in Appendix E, where each entry carries its DOI.

## Coverage

<!-- wiki-stats -->

Coverage is uneven by design: the wiki records what has been screened, not
what exists. A topic with few claims is a topic that has not yet been read
closely, not one where nothing is known.

## How the chapters are arranged

The next chapter follows the Coastal Design Bench: for each design module it
lists the topics the app shows beside that module. The chapters after it
reproduce every topic of the tree, grouped by top-level branch, with its
synthesis, equations, and claims. Topics mapped to a design module are
reproduced once, in the tree, and cross-referenced from the module chapter.

<!-- wiki -->
