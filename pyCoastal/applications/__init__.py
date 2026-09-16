"""
pyCoastal.applications
----------------------
Scenario-level simulators assembled from the numerics, physics and tools
layers. Each application takes an engineering design, runs it forward, and
reports the quantities a coastal engineer actually decides on: how long a
beach fill survives, how much wave energy reaches a berth, and so on.
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
]
