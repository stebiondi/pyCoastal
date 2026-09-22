# Part I. Getting started {.part .unnumbered}

# Introduction {#sec:intro}

Coastal zones concentrate people, infrastructure, and ecosystems in
environments that are energetic and constantly changing. Waves, tides,
surges, and currents interact with complex shorelines to drive erosion,
flooding, sediment transport, and loads on structures. Anticipating these
processes is essential for safe navigation, coastal protection, habitat
conservation, and climate adaptation.

pyCoastal is a Python toolbox for coastal, port, and ocean engineering. It
has two faces that share one code base:

1. **A numerical framework** of uniform grids, finite-difference operators,
   explicit time integrators, boundary handlers, Poisson solvers, and
   physics building blocks (shallow water, incompressible Navier-Stokes,
   eddy-viscosity closures). It favors clarity over ultimate efficiency so
   that students and practitioners can see and modify every numerical
   brick.
2. **A design chain** of scenario-level applications that take an
   engineering design and report the quantities a project actually turns
   on: a 100-year wave with its confidence band, an armor stone size and a
   crest level, a seawall base width, a scour depth over a tidal cycle, a
   dredge level, a fender size, a flood extent, and the drawing sheet that
   carries all of it.

## The design chain

A real coastal scheme runs as a chain, and pyCoastal is organized the same
way (@tbl:chain). Each step hands its result to the next as an object, not
as a number you retype, so a drawing cannot drift out of step with the
calculation behind it.

: The design chain and the modules that implement each step. {#tbl:chain}

| Step | Module | What it gives you |
|------|--------|-------------------|
| Design condition | `applications.extremes` | 100-year wave or water level, with a confidence band |
| Bed and soil | `applications.sediment` | grain mobility, fall velocity, earth pressure |
| Nearshore | `applications.port` | phase-resolved diffraction into a harbor, berth agitation |
| Structure | `applications.structures`, `applications.seawall` | armor size, crest level, stability checks |
| Loads | `applications.piles`, `applications.berthing` | Morison loads through the wave cycle, berthing energy and fenders |
| Scour | `applications.scour`, `applications.river` | contraction, pier and abutment scour over the tidal cycle; the flow split that feeds it |
| Navigation | `applications.channel` | dredge level, channel width, dredge volume |
| Coastline | `applications.nourishment`, `applications.surge` | fill life and profile, water level budget and a connected flood map |
| Deliverable | `drafting`, `applications.sections` | a dimensioned drawing sheet and a DXF |

## Principles

Three rules run through the whole package, and they explain most of the
design decisions you will meet in the later chapters.

**Every relation names its source.** Module docstrings list their sources
(Van der Meer 1988, EurOtop 2018, Goda 2010, PIANC 2014, HEC-18, and so
on), and each function says which equation it implements.

**Nothing silently extrapolates.** Where a formula has a documented range of
validity, the functions compute outside it if asked, because engineering
judgement outside a range is the engineer's call, but they say so through a
`warnings` list, a flag such as `within_range`, `impulsive`, or
`screening_only`, or a note in the returned dictionary.

**Assumptions are reported, not buried.** Width components of a channel that
you did not specify are taken at their most benign class and reported as
assumed. The `+1` safety term in Froehlich's abutment equation is reported
as a separate `safety_margin`. The steady-current floor added to the Sumer
and Fredsoe scour relation is flagged as `current_governs`. A reviewer
should always be able to see which assumption to argue with.

## Before the math

A few terms recur throughout the numerical parts of this manual. A *field*
is any variable defined over the domain, such as water depth, velocity, or
pressure. A *grid* divides the domain into cells where these variables are
stored; in pyCoastal the values live at cell centers. A *stencil* is the
small pattern of neighboring cells used to approximate derivatives through
finite differences, and these approximations form the spatial *operators*.
Once the spatial terms are discretized, a *time integrator* updates the
solution step by step, using a right-hand side that gathers fluxes,
advection, diffusion, pressure gradients, and sources. *Boundary conditions*
specify what happens at the domain edges.

On the design side, a *design condition* is the wave and water level a
structure is sized against, a *design object* (for example `SeawallDesign`
or `ChannelDesign`) is the fully dimensioned result of a design function,
and a *sheet* is a drawing at a true, stated scale with a border, a title
block, and specification notes.

## How this manual is organized

- **Part I** covers installation, the repository layout, conventions, and a
  quick start.
- **Part II** describes the numerical framework and the governing equations,
  with the simulation examples that exercise them.
- **Part III** documents the standalone engineering formulae in
  `pyCoastal.tools`.
- **Part IV** has one chapter per design application.
- **Part V** covers the drafting layer: sections, sheets, and DXF export.
- **Part VI** describes the Coastal Design Bench browser app.
- **Part VII** describes the test suite and the verification of the browser
  engine against the Python.
- **Part VIII** reproduces the CoastalWiki knowledge base shipped with the
  app.
- **Appendices** give the complete API reference, the full source of every
  example, a list of symbols, and the reference lists.
