# Part I. Getting started {.part .unnumbered}

# Introduction {#sec:intro}

Coastal zones concentrate population, infrastructure and ecosystems in
energetic, time-varying environments. Waves, tides, surges and currents
interact with the shoreline and drive erosion, flooding, sediment transport
and loads on structures. Quantifying these processes supports navigation,
coastal protection, habitat conservation and climate adaptation.

pyCoastal is a Python toolbox for coastal, port and ocean engineering. It
contains two independent layers in one code base.

1. **A numerical framework**: uniform grids, finite-difference operators,
   explicit time integrators, boundary-condition classes, Poisson solvers,
   and governing-equation components (shallow water, incompressible
   Navier-Stokes, eddy-viscosity closures). Each numerical component is
   exposed and can be replaced.
2. **A design chain**: scenario-level applications that take an engineering
   design and return project quantities. These include the 100-year wave
   with its confidence band, armor stone size, crest level, seawall base
   width, scour depth over a tidal cycle, dredge level, fender size, flood
   extent, and the corresponding drawing sheet.

## The design chain

pyCoastal is organized in the sequence a coastal scheme is designed
(@tbl:chain). Each step passes a structured object to the subsequent
module. This maintains consistency between calculations and drawings.

: The design chain and the modules that implement each step. {#tbl:chain}

| Step | Module | Output |
|------------|-------------------------------------|------------------------------------|
| Design condition | `applications.extremes` | 100-year wave or water level, with a confidence band |
| Bed and soil | `applications.sediment` | grain mobility, fall velocity, earth pressure |
| Nearshore | `applications.port` | phase-resolved diffraction into a harbor, berth agitation |
| Structure | `applications.structures`, `applications.seawall` | armor size, crest level, stability checks |
| Loads | `applications.piles`, `applications.berthing` | Morison loads through the wave cycle, berthing energy and fenders |
| Scour | `applications.scour`, `applications.river` | contraction, pier and abutment scour over the tidal cycle; the flow split that supplies it |
| Navigation | `applications.channel` | dredge level, channel width, dredge volume |
| Coastline | `applications.nourishment`, `applications.surge` | fill life and profile, water level budget and a connected flood map |
| Deliverable | `drafting`, `applications.sections` | dimensioned drawing sheet and DXF |

## Implementation rules

Three rules apply throughout the package.

**Source attribution.** Module docstrings list the sources implemented (Van
der Meer 1988, EurOtop 2018, Goda 2010, PIANC 2014, HEC-18, among others).
Each function records the equation it implements.

**Range reporting.** Where a relation has a documented range of validity,
the function computes outside that range and reports the condition through
a `warnings` list, a flag such as `within_range`, `impulsive` or
`screening_only`, or an entry in the returned dictionary.

**Assumption reporting.** Unspecified channel-width components are assigned
the least restrictive class and reported as assumed. The `+1` safety term in
Froehlich's abutment equation is returned separately as `safety_margin`. The
steady-current floor applied to the Sumer and Fredsoe scour relation is
flagged as `current_governs`.

## Terminology

The following terms are used in Part VII. A *field* is a variable defined
over the domain, such as water depth, velocity or pressure. A *grid*
divides the domain into cells holding those variables; pyCoastal stores
values at cell centers. A *stencil* is the pattern of neighboring cells used
to approximate a derivative by finite differences; these approximations form
the spatial *operators*. A *time integrator* advances the discretized
solution using a right-hand side containing fluxes, advection, diffusion,
pressure gradients and sources. *Boundary conditions* define the solution at
the domain edges.

In Parts III and IV, a *design condition* is the wave and water level used
to size a structure, a *design object* (for example `SeawallDesign` or
`ChannelDesign`) is the dimensioned result returned by a design function,
and a *sheet* is a drawing at a stated scale with border, title block and
specification notes.

## Manual organization

- **Part I**: installation, repository layout, conventions, quick start.
- **Part II**: the standalone engineering formulae in `pyCoastal.tools`,
  used by the design modules.
- **Part III**: one chapter per design application, in the order of the
  design chain.
- **Part IV**: the drafting layer, sections, sheets and DXF export.
- **Part V**: PyCoaTools, the browser implementation of the design modules.
- **Part VI**: PyCoaPedia, its interfaces, and the repository layout for AI
  agents.
- **Part VII**: the numerical framework, the governing equations, and the
  simulation examples. The design modules have no dependency on this layer.
- **Part VIII**: the test suite and the verification of the browser engine
  against the Python implementation.
- **Appendices**: list of symbols and engineering references.
