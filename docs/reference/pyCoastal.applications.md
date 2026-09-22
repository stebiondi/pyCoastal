# `pyCoastal.applications`

Source: [`pyCoastal/applications/__init__.py`](../../pyCoastal/applications/__init__.py)

pyCoastal.applications
----------------------
Scenario-level design modules. Each takes an engineering design, works it
forward, and reports the quantities a coastal engineer actually decides on:
how long a beach fill survives, how much wave energy reaches a berth, how
deep a pier scours, and so on.

They are built on the ``tools`` layer (above all the linear dispersion
relation and the one-line shoreline model) and on each other: ``sediment``
supplies the bed and backfill to the scour, seawall, channel and
nourishment modules, ``structures`` supplies the design condition, and
``sections`` turns any of their results into a drawing. Where a module
marches in time it carries its own loop rather than using
``pyCoastal.numerics``, which stands on its own for the simulation
examples.

