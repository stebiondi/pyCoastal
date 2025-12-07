# pycoastal/tools/__init__.py

"""
pycoastal.tools
---------------
Collection of standalone coastal‐engineering formulae and utilities.
All functions here accept fully configurable parameters (no hidden hard-coded values).
Users configure defaults (or override) via their case input file.
"""

from .wave import (
    dispersion,
    wave_number,
    surf_similarity,
    breaker_type,
    ursell_number,
    wave_setup,
    generate_irregular_wave,
)
from .morphodynamics import (
    bruuns_rule,
    exner_change,
    linear_slope,
    circle_through_points,
    two_point_arc,
    build_tombolo_arcs,
    accretion_metrics,
)
from .shoreline import (
    OneLineParams,
    make_grid,
    breakwaters_geometry,
    kd_diffraction_field,
    field_or_scalar_to_array,
    compute_flux_Qls,
    rhs_y_t,
    suggest_dt,
    apply_bcs,
    run_one_line_model,
)
from .structural import (
    hudson_dn50,
    vandermeer_dn50,
    hunt_runup,
    stockdon_runup,
    goda_wave_force,
    iribarren_stability,
)
from .sediment_transport import (
    shields_parameter,
    van_rijn_bedload,
    van_rijn_suspended,
    bijker_bedload,
    cerc_transport,
    bagnold_sediment,
    izbash_current,
    einstein_bedload,
)

__all__ = [
    # wave.py
    "dispersion",
    "wave_number",
    "surf_similarity",
    "breaker_type",
    "ursell_number",
    "wave_setup",
    "generate_irregular_wave",
    # morphodynamics.py
    "bruuns_rule",
    "exner_change",
    "linear_slope",
    "circle_through_points",
    "two_point_arc",
    "build_tombolo_arcs",
    "accretion_metrics",
    # shoreline.py
    "OneLineParams",
    "make_grid",
    "breakwaters_geometry",
    "kd_diffraction_field",
    "field_or_scalar_to_array",
    "compute_flux_Qls",
    "rhs_y_t",
    "suggest_dt",
    "apply_bcs",
    "run_one_line_model",
    # structural.py
    "hudson_dn50",
    "vandermeer_dn50",
    "hunt_runup",
    "stockdon_runup",
    "goda_wave_force",
    "iribarren_stability",
    # sediment_transport.py
    "shields_parameter",
    "van_rijn_bedload",
    "van_rijn_suspended",
    "bijker_bedload",
    "cerc_transport",
    "bagnold_sediment",
    "izbash_current",
    "einstein_bedload",
]
