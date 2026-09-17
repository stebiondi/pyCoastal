API Reference
=============

Applications
------------

Scenario-level modules. Each one takes an engineering design and reports
the quantities a project turns on, with every relation traced to a source.

.. autosummary::
   :toctree: generated
   :recursive:

   pyCoastal.applications.extremes
   pyCoastal.applications.nourishment
   pyCoastal.applications.port
   pyCoastal.applications.structures
   pyCoastal.applications.seawall
   pyCoastal.applications.channel
   pyCoastal.applications.piles
   pyCoastal.applications.surge

Drawings
--------

Primitives for issuing a design as a dimensioned drawing, and the section
generators built on them.

.. autosummary::
   :toctree: generated
   :recursive:

   pyCoastal.drafting
   pyCoastal.applications.sections
   pyCoastal.plotting

Tools
-----

Single-purpose engineering relations used by the applications.

.. autosummary::
   :toctree: generated
   :recursive:

   pyCoastal.tools.wave
   pyCoastal.tools.structural
   pyCoastal.tools.sediment_transport
   pyCoastal.tools.morphodynamics
   pyCoastal.tools.shoreline

Numerics and physics
--------------------

The solver layer the phase-resolved models are built on.

.. autosummary::
   :toctree: generated
   :recursive:

   pyCoastal.numerics.grid
   pyCoastal.numerics.operators
   pyCoastal.numerics.boundary
   pyCoastal.numerics.time_intg
   pyCoastal.physics.shallow_water
   pyCoastal.physics.navier_stokes
   pyCoastal.physics.turbulence
   pyCoastal.io
