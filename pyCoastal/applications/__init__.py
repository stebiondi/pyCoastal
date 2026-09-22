"""
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
"""

from .nourishment import (
    KCERC_DEFAULT,
    NourishmentDesign,
    NourishmentResult,
    WaveClimate,
    cerc_coefficient,
    longshore_diffusivity,
    pelnard_considere,
    initial_planform,
    simulate_nourishment,
    renourishment_schedule,
)

from .port import (
    Breakwater,
    IncidentWave,
    PortLayout,
    PortResult,
    harbour_layout,
    measure_reflection,
    simulate_port,
)

from .structures import (
    DesignConditions,
    BreakwaterDesign,
    design_rubble_mound,
    overtopping_sloped,
    overtopping_vertical,
    required_crest_freeboard,
    rock_armour_hudson,
    rock_armour_vandermeer,
)

from .surge import (
    StormConditions,
    barometric_setup,
    bathtub_flood,
    inundation_limit,
    isolated_low_ground,
    total_water_level,
    wind_setup,
    wind_setup_profile,
)

__all__ = [
    "KCERC_DEFAULT",
    "NourishmentDesign",
    "NourishmentResult",
    "WaveClimate",
    "cerc_coefficient",
    "longshore_diffusivity",
    "pelnard_considere",
    "initial_planform",
    "simulate_nourishment",
    "renourishment_schedule",
    # port
    "Breakwater",
    "IncidentWave",
    "PortLayout",
    "PortResult",
    "harbour_layout",
    "measure_reflection",
    "simulate_port",
    # structures
    "DesignConditions",
    "BreakwaterDesign",
    "design_rubble_mound",
    "overtopping_sloped",
    "overtopping_vertical",
    "required_crest_freeboard",
    "rock_armour_hudson",
    "rock_armour_vandermeer",
    # surge
    "StormConditions",
    "barometric_setup",
    "bathtub_flood",
    "inundation_limit",
    "isolated_low_ground",
    "total_water_level",
    "wind_setup",
    "wind_setup_profile",
]
