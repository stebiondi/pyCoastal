# Preface {.unnumbered}

pyCoastal began as a teaching and research package for numerical modeling,
fluid dynamics and hydraulics. Numerical models follow recurrent structural
patterns across modeling frameworks. Configured and validated, they
reproduce measured behavior and allow the analysis of conditions that cannot
be observed directly.

The first edition of this manual documented the numerical framework. The
package now also implements a design chain: a wave record yields a design
condition, the design condition sizes a structure, and the structure is
issued as a dimensioned drawing with quantities and specification notes.
Each relation records its source and its range of validity, and reports
application outside that range. PyCoaTools provides the design modules in a
browser and presents each result together with the supporting literature
held in PyCoaPedia, the knowledge base of coastal and ocean engineering
publications distributed with the package.

This manual covers both. Part I describes installation and conventions.
Part II documents the standalone engineering formulae. Part III documents
the design applications, one chapter per module, in the order of the design
chain, each with formulation, interface, a worked example reproducing the
program output, and stated limitations. Part IV covers drawings and
deliverables. Part V documents PyCoaTools. Part VI documents PyCoaPedia,
its construction, and its interfaces for browser, Python, command line and
SQL access, together with the repository layout for AI agents. Part VII
documents the numerical framework: grids, operators, time integration,
boundary conditions, governing equations, and the simulation examples.
Part VIII documents the test suite.

Stefano Biondi
