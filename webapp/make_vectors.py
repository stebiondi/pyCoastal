"""
Dump reference cases from pyCoastal for the JavaScript engine to be checked against.

The browser app runs a JavaScript transliteration of the design modules,
because a browser has no Python. A second implementation of a design code is
worth having only if somebody checks it, so this writes out what pyCoastal
actually returns for a spread of cases, and `verify_engine.py` runs the
JavaScript against the same cases. The app repeats the check on load and
reports the result on screen.

The cases deliberately include awkward ones: the surging armour branch, an
impulsive wall, a depth-limited Goda wave, a pile that is drag dominated and
one that is inertia dominated, and a resultant outside the middle third.

    python webapp/make_vectors.py --out webapp/vectors.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from pyCoastal.applications.nourishment import (
    SECONDS_PER_YEAR,
    NourishmentDesign,
    WaveClimate,
    longshore_diffusivity,
    pelnard_considere,
)
from pyCoastal.applications.sections import _plan_years, plan_margin, spreading_half_life
from pyCoastal.applications.channel import (
    Vessel,
    channel_width,
    design_channel,
    squat_barrass,
    squat_icorels,
    underkeel_clearance,
)
from pyCoastal.applications.extremes import (
    fit_gpd,
    gev_return_value,
    gpd_return_value,
    l_moments,
)
from pyCoastal.applications.piles import (
    bed_keulegan_carpenter,
    design_monopile,
    drag_inertia_coefficients,
    stream_function_wave,
    keulegan_carpenter,
    morison_pile_load,
    scour_depth_pile,
)
from pyCoastal.applications.seawall import (
    bearing_pressures,
    design_seawall,
    goda_breaking_height,
    goda_pressures,
    scour_depth_vertical_wall,
    stem_section,
    toe_stone_size,
    toe_stone_tanimoto,
)
from pyCoastal.applications.nourishment import (
    critical_volume,
    dean_scale,
    fill_volume_for_advance,
    grain_compatibility,
    phi_size,
    profile_overfill_factor,
    profile_width,
    shoreline_advance,
)
from pyCoastal.applications.sediment import (
    bed_mobility,
    critical_shields,
    dimensionless_grain_size,
    earth_pressure_coefficient,
    fall_velocity,
    lateral_earth_force,
    sediment,
    wave_shields,
)
from pyCoastal.applications.structures import (
    DesignConditions,
    breakwater_toe_scour,
    concrete_armour,
    crown_wall,
    pedersen_crown_loads,
    mound_foundation,
    roundhead,
    roundhead_kd_ratio,
    design_rubble_mound,
    overtopping_sloped,
    overtopping_vertical,
    reflection_coefficient,
    rock_armour_vandermeer,
    toe_scour,
)
from pyCoastal.tools.wave import dispersion

CASES: list[dict] = []


def finite(value):
    """Non-finite values as markers, so the file stays valid JSON.

    ``json.dumps`` writes ``Infinity`` for a Python inf, which JSON.parse
    rejects outright: the browser would fail to load the vectors and the
    verification badge would quietly vanish. An infinite factor of safety is
    a real and useful answer, so it is carried across as a string that both
    checkers understand rather than clipped to a large number.
    """
    if isinstance(value, float):
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        if math.isnan(value):
            return "nan"
    return value


def case(name: str, call: dict, expect: dict) -> None:
    CASES.append({"name": name, "call": call,
                  "expect": {k: finite(v) for k, v in expect.items()}})


def build() -> dict:
    # -- dispersion --------------------------------------------------------
    for T, h in ((8.0, 5.0), (12.0, 30.0), (6.0, 200.0), (14.0, 3.0)):
        case(f"dispersion T={T} h={h}",
             {"fn": "dispersion", "args": [T, h]},
             {"value": dispersion(T, h)})

    # -- armour, both branches --------------------------------------------
    for label, (Hm0, Tp, depth, cot) in {
        "plunging": (4.0, 11.0, 12.0, 2.0),
        "surging": (2.0, 16.0, 20.0, 4.0),
    }.items():
        c = DesignConditions.from_peak_period(Hm0=Hm0, Tp=Tp, depth=depth)
        got = rock_armour_vandermeer(c, cot)
        case(f"vandermeer {label}",
             {"fn": "rockArmourVanDerMeer",
              "conditions": [Hm0, Tp, depth, 6 * 3600.0], "args": [cot]},
             {"Dn50": got["Dn50"], "M50": got["M50"], "xi": got["xi"],
              "xi_cr": got["xi_cr"], "regime": got["regime"]})

    # -- overtopping, both branches and the vertical form -----------------
    c = DesignConditions.from_peak_period(Hm0=3.0, Tp=9.0, depth=10.0)
    for Rc, cot in ((2.0, 2.0), (6.0, 2.0), (3.0, 4.0)):
        got = overtopping_sloped(c, Rc, cot, gamma_f=0.4)
        case(f"overtopping sloped Rc={Rc} cot={cot}",
             {"fn": "overtoppingSloped", "conditions": [3.0, 9.0, 10.0, 6 * 3600.0],
              "args": [Rc, cot, 0.4]},
             {"q": got["q"], "governing": got["governing"]})
    for Rc in (2.0, 5.0):
        got = overtopping_vertical(c, Rc)
        case(f"overtopping vertical Rc={Rc}",
             {"fn": "overtoppingVertical", "conditions": [3.0, 9.0, 10.0, 6 * 3600.0],
              "args": [Rc]},
             {"q": got["q"], "h_star": got["h_star"],
              "impulsive": got["impulsive"]})

    # -- whole rubble mound ------------------------------------------------
    for cot in (1.5, 2.0, 3.0):
        c = DesignConditions.from_peak_period(Hm0=4.0, Tp=11.0, depth=12.0)
        got = design_rubble_mound(c, cot_alpha=cot)
        case(f"design_rubble_mound cot={cot}",
             {"fn": "designRubbleMound", "conditions": [4.0, 11.0, 12.0, 6 * 3600.0],
              "args": [{"cot_alpha": cot}]},
             {"Dn50": got.Dn50, "M50": got.M50,
              "crest_freeboard": got.crest_freeboard,
              "q_mean": got.q_mean, "regime": got.regime,
              "layer_thickness": got.layer["thickness"]})

    # -- concrete units and the crown wall ---------------------------------
    c = DesignConditions.from_peak_period(Hm0=4.0, Tp=11.0, depth=12.0)
    for unit, cot in (("cubes_two_layer_random", 1.5), ("tetrapod", 1.5),
                      ("accropode", 1.33), ("xbloc", 1.5), ("dolos", 2.0)):
        got = concrete_armour(c, unit, cot)
        case(f"concrete armour {unit}",
             {"fn": "concreteArmour", "conditions": [4.0, 11.0, 12.0, 6 * 3600.0],
              "args": [unit, cot]},
             {"Dn50": got["Dn50"], "M50": got["M50"],
              "stability_number": got["stability_number"]})
    for armour, cot in (("accropode", 1.5), ("tetrapod", 1.5),
                        ("rock_two_layer_permeable", 2.0)):
        got = design_rubble_mound(c, cot_alpha=cot, armour=armour)
        case(f"design_rubble_mound {armour}",
             {"fn": "designRubbleMound", "conditions": [4.0, 11.0, 12.0, 6 * 3600.0],
              "args": [{"cot_alpha": cot, "armour": armour}]},
             {"Dn50": got.Dn50, "M50": got.M50, "crest_freeboard": got.crest_freeboard,
              "layer_thickness": got.layer["thickness"],
              "underlayer_Dn50": got.underlayer_Dn50})
        cw = crown_wall(got, 0.0)
        case(f"crown wall {armour}",
             {"fn": "crownWall", "conditions": [4.0, 11.0, 12.0, 6 * 3600.0],
              "design_first": True,
              "args": [{"cot_alpha": cot, "armour": armour}, 0.0]},
             {"deck_width": cw["deck_width"], "sliding_FoS": cw["sliding_FoS"],
              "overturning_FoS": cw["overturning_FoS"], "crown_Fh": cw["loads"]["Fh"],
              "berm_width": cw["berm_width"]})
    got = pedersen_crown_loads(c, 2.0, 4.0, 5.0, 2.0, 1.5)
    case("pedersen crown loads",
         {"fn": "pedersenCrownLoads", "conditions": [4.0, 11.0, 12.0, 6 * 3600.0],
          "args": [2.0, 4.0, 5.0, 2.0, 1.5]},
         {"Fh": got["Fh"], "M": got["M"], "pb": got["pb"], "Ru": got["Ru"],
          "y_eff": got["y_eff"]})

    # -- Goda, including the depth-limited branch --------------------------
    for label, kwargs in {
        "deep": dict(Hm0=3.0, T=10.0, depth=12.0, wall_toe_depth=12.0,
                     crest_freeboard=6.0, depth_limit=False),
        "depth limited": dict(Hm0=4.0, T=10.0, depth=4.0, wall_toe_depth=4.0,
                              crest_freeboard=4.0, depth_limit=True),
        "oblique": dict(Hm0=3.0, T=10.0, depth=10.0, wall_toe_depth=10.0,
                        crest_freeboard=5.0, beta_degrees=40.0,
                        depth_limit=False),
    }.items():
        got = goda_pressures(**kwargs)
        case(f"goda {label}",
             {"fn": "godaPressures", "args": [kwargs]},
             {"p1": got["p1"], "p3": got["p3"], "pu": got["pu"],
              "F": got["F"], "arm": got["arm"], "Hmax": got["Hmax"],
              "alpha1": got["alpha1"], "alpha3": got["alpha3"]})

    # -- scour and toe -----------------------------------------------------
    for Hm0, T, h in ((2.0, 9.0, 4.0), (3.0, 12.0, 15.0)):
        case(f"scour wall Hm0={Hm0} h={h}",
             {"fn": "scourDepthVerticalWall", "args": [Hm0, T, h]},
             {"value": scour_depth_vertical_wall(Hm0, T, h)})
    for T, h, B in ((10.0, 6.0, 8.0), (8.0, 3.0, 2.0), (12.0, 9.0, 20.0)):
        got = toe_stone_tanimoto(3.0, T, h, B)
        case(f"tanimoto T={T} h={h} B={B}",
             {"fn": "toeStoneTanimoto", "args": [3.0, T, h, B]},
             {"Dn50": got["Dn50"], "stability_number": got["stability_number"],
              "kappa": got["kappa"]})
    case("goda breaking height",
         {"fn": "godaBreakingHeight", "args": [10.0, 4.67, 1 / 30]},
         {"value": goda_breaking_height(10.0, 4.67, 1 / 30)})
    for M, V in ((1200.0, 350.0), (6000.0, 1500.0), (50.0, 900.0)):
        got = stem_section(M, V)
        case(f"stem section M={M} V={V}",
             {"fn": "stemSection", "args": [M, V]},
             {"thickness": got["thickness"], "d_bending": got["d_bending"],
              "d_shear": got["d_shear"]})
    got = toe_stone_size(3.0, 6.0, 10.0)
    case("toe stone",
         {"fn": "toeStoneSize", "args": [3.0, 6.0, 10.0]},
         {"Dn50": got["Dn50"], "stability_number": got["stability_number"],
          "within_range": got["within_range"]})

    # -- bearing, inside and outside the middle third ----------------------
    for label, (normal, width, moment) in {
        "central": (600.0, 6.0, 1800.0),
        "middle third edge": (600.0, 6.0, 600.0 * 2.0),
        "outside": (600.0, 6.0, 600.0 * 1.0),
    }.items():
        got = bearing_pressures(normal, width, moment)
        case(f"bearing {label}",
             {"fn": "bearingPressures", "args": [normal, width, moment]},
             {"p_max": got["p_max"], "p_min": got["p_min"], "e": got["e"],
              "middle_third": got["middle_third"]})

    # -- whole seawall, including an impulsive case ------------------------
    for label, (Hm0, Tp, depth, swl, bed, use, extra) in {
        "promenade": (2.0, 8.0, 3.5, 2.5, -1.0, "trained_staff", {}),
        "drained": (2.0, 8.0, 3.5, 2.5, -1.0, "trained_staff",
                    {"water_table": 2.0}),
        "impulsive": (2.2, 9.0, 3.6, 2.9, -0.7, "pedestrians_aware", {}),
        "tall": (2.8, 9.5, 8.5, 2.9, -5.6, "trained_staff", {}),
        "strict gravel": (1.5, 7.0, 2.5, 2.0, -0.5, "pedestrians_unaware",
                          {"backfill": "fine_gravel", "allowable_bearing": 200.0}),
    }.items():
        c = DesignConditions.from_peak_period(Hm0=Hm0, Tp=Tp, depth=depth)
        got = design_seawall(c, swl, bed, tolerable_use=use, **extra)
        case(f"design_seawall {label}",
             {"fn": "designSeawall", "conditions": [Hm0, Tp, depth, 6 * 3600.0],
              "args": [swl, bed, dict({"tolerable_use": use}, **extra)]},
             {"crest_level": got.crest_level, "base_width": got.base_width,
              "founding_level": got.founding_level,
              "stem_thickness": got.stem_thickness,
              "base_thickness": got.base_thickness,
              "sliding_FoS": got.sliding_FoS,
              "overturning_FoS": got.overturning_FoS,
              "drawdown_sliding": got.drawdown["sliding_FoS"],
              "drawdown_overturning": got.drawdown["overturning_FoS"],
              "drawdown_p_max": got.drawdown["bearing"]["p_max"],
              "bearing_p_max": got.bearing["p_max"],
              "stem_moment": got.stem["moment"],
              "wave_force": got.wave_force,
              "toe_Dn50": got.toe_Dn50,
              "impulsive": got.impulsive,
              "concrete": got.quantities()["concrete_total_m3_per_m"]})

    # -- channel -----------------------------------------------------------
    ship = Vessel(name="Test", length=336.0, beam=48.2, draught=14.5,
                  block_coefficient=0.68)
    ship_js = ["Test", 336.0, 48.2, 14.5, 0.68]
    for speed in (6.0, 8.0, 11.0):
        got = squat_icorels(ship, speed, 17.5)
        case(f"squat icorels {speed} kn",
             {"fn": "squatIcorels", "vessel": ship_js, "args": [speed, 17.5]},
             {"squat": got["squat"], "froude": got["froude"],
              "beyond_range": got["beyond_range"]})
    got = squat_barrass(ship, 9.0, 17.5)
    case("squat barrass",
         {"fn": "squatBarrass", "vessel": ship_js, "args": [9.0, 17.5]},
         {"squat": got["squat"]})

    conditions = {"crosswind": "moderate", "crosscurrent": "low",
                  "waves": "moderate", "depth_of_waterway": "shallow"}
    for two_way in (False, True):
        got = channel_width(ship, two_way=two_way, conditions=conditions)
        case(f"channel_width two_way={two_way}",
             {"fn": "channelWidth", "vessel": ship_js,
              "args": [{"two_way": two_way, "conditions": conditions}]},
             {"width": got["width"], "lanes": got["lanes"],
              "assumed": len(got["assumed"])})

    got = underkeel_clearance(ship, 0.4, 0.9)
    case("underkeel clearance",
         {"fn": "underkeelClearance", "vessel": ship_js, "args": [0.4, 0.9, {}]},
         {"gross": got["gross"], "required_depth": got["required_depth"]})

    for label, kwargs in {
        "container": dict(speed=8.0, design_water_level=1.2, Hs=1.8, Tp=9.0,
                          net_clearance=0.8, existing_bed=-11.5),
        "calm": dict(speed=6.0, design_water_level=0.5, Hs=0.4),
    }.items():
        got = design_channel(ship, **kwargs, conditions=conditions, two_way=True)
        expect = {"dredge_level": got.dredge_level,
                  "required_depth": got.required_depth,
                  "width": got.width, "squat": got.squat["squat"]}
        if got.existing_bed is not None:
            expect["volume_per_km"] = got.dredge_volume(1000.0)
        js_kwargs = dict(kwargs)
        speed = js_kwargs.pop("speed")
        level = js_kwargs.pop("design_water_level")
        js_kwargs.update({"conditions": conditions, "two_way": True})
        case(f"design_channel {label}",
             {"fn": "designChannel", "vessel": ship_js,
              "args": [speed, level, js_kwargs]}, expect)

    # -- piles -------------------------------------------------------------
    for diameter in (0.8, 4.0, 8.0):
        KC = keulegan_carpenter(12.0, 13.0, 30.0, diameter)
        coefficients = drag_inertia_coefficients(KC)
        case(f"KC D={diameter}",
             {"fn": "keuleganCarpenter", "args": [12.0, 13.0, 30.0, diameter]},
             {"value": KC})
        case(f"coefficients D={diameter}",
             {"fn": "dragInertiaCoefficients", "args": [KC]},
             {"Cd": coefficients["Cd"], "Cm": coefficients["Cm"],
              "regime": coefficients["regime"]})

    for phase in (0.0, math.pi / 4, math.pi / 2):
        got = morison_pile_load(8.0, 12.0, 13.0, 30.0, phase=phase, points=400)
        case(f"morison phase={phase:.3f}",
             {"fn": "morisonPileLoad", "args": [8.0, 12.0, 13.0, 30.0,
                                                {"phase": phase, "points": 400}]},
             {"force": got.force, "moment": got.moment, "arm": got.arm,
              "inertia_fraction": got.inertia_fraction})

    for diameter in (0.8, 8.0):
        got = design_monopile(diameter, 12.0, 13.0, 30.0, phases=73)
        case(f"design_monopile D={diameter}",
             {"fn": "designMonopile", "args": [diameter, 12.0, 13.0, 30.0,
                                               {"phases": 73}]},
             {"max_moment": got["sweep"]["max_moment"],
              "max_force": got["sweep"]["max_force"],
              "phase_of_max_moment": got["sweep"]["phase_of_max_moment"],
              "crest_underestimate": got["crest_underestimate"],
              "scour": got["scour"]["depth"]})

    for KC in (4.0, 12.0, 60.0):
        got = scour_depth_pile(5.0, KC)
        case(f"pile scour KC={KC}",
             {"fn": "scourDepthPile", "args": [5.0, KC]},
             {"depth": got["depth"], "ratio": got["ratio"]})
    for KC, Ucw in ((3.0, 0.4), (8.0, 0.2), (2.0, 0.7)):
        got = scour_depth_pile(5.0, KC, current_ratio=Ucw)
        case(f"pile scour KC={KC} Ucw={Ucw}",
             {"fn": "scourDepthPile",
              "args": [5.0, KC, False, True, None, None, None, None, Ucw]},
             {"depth": got["depth"], "ratio": got["ratio"]})
    got = bed_keulegan_carpenter(6.45, 13.0, 30.0, 8.0)
    case("bed KC",
         {"fn": "bedKeuleganCarpenter", "args": [6.45, 13.0, 30.0, 8.0]},
         {"Um": got["Um"], "KC": got["KC"]})
    for H, T, h in ((12.0, 13.0, 30.0), (3.0, 8.0, 6.0), (1.0, 10.0, 40.0)):
        w = stream_function_wave(H, T, h)
        case(f"stream function H={H} T={T} h={h}",
             {"fn": "streamFunctionWave", "args": [H, T, h]},
             {"converged": w.converged, "crest": w.crest, "trough": w.trough,
              "wavelength": w.wavelength, "celerity": w.celerity})
    for phase in (0.0, 1.0):
        got = morison_pile_load(8.0, 12.0, 13.0, 30.0, phase=phase, points=200,
                                theory="linear")
        case(f"morison linear phase={phase}",
             {"fn": "morisonPileLoad", "args": [8.0, 12.0, 13.0, 30.0,
                                                {"phase": phase, "points": 200,
                                                 "theory": "linear"}]},
             {"force": got.force, "moment": got.moment})
    got = design_monopile(6.0, 10.0, 12.0, 25.0, phases=37, current=1.2,
                          bed="medium_sand")
    case("design_monopile with current",
         {"fn": "designMonopile", "args": [6.0, 10.0, 12.0, 25.0,
                                           {"phases": 37, "current": 1.2,
                                            "bed": "medium_sand"}]},
         {"max_moment": got["sweep"]["max_moment"],
          "max_force": got["sweep"]["max_force"],
          "scour": got["scour"]["depth"], "theory": got["load"].theory})

    # -- beach nourishment -------------------------------------------------
    for key in ("very_fine_sand", "fine_sand", "medium_sand", "coarse_sand",
                "fine_gravel"):
        case(f"dean scale {key}",
             {"fn": "deanScale", "args": [key]},
             {"value": dean_scale(key)})
        case(f"phi {key}",
             {"fn": "phiSize", "args": [sediment(key).d50]},
             {"value": phi_size(sediment(key).d50)})

    native = dean_scale("medium_sand")
    for key in ("very_fine_sand", "fine_sand", "medium_sand", "coarse_sand",
                "fine_gravel"):
        fill = dean_scale(key)
        for volume in (120.0, 250.0, 900.0):
            got = shoreline_advance(native, fill, volume, 2.0, 6.0)
            case(f"shoreline advance {key} V={volume}",
                 {"fn": "shorelineAdvance",
                  "args": [native, fill, volume, 2.0, 6.0]},
                 {"advance": got["advance"], "kind": got["kind"],
                  "critical_volume": got["critical_volume"]})
        case(f"critical volume {key}",
             {"fn": "criticalVolume", "args": [native, fill, 2.0, 6.0]},
             {"value": critical_volume(native, fill, 2.0, 6.0)})
        got = grain_compatibility("medium_sand", key)
        case(f"grain compatibility {key}",
             {"fn": "grainCompatibility", "args": ["medium_sand", key]},
             {"delta": got["delta"], "sorting_ratio": got["sorting_ratio"],
              "coarser": got["coarser"], "verdict": got["verdict"]})
        got = profile_overfill_factor("medium_sand", key, 2.0, 6.0, advance=40.0)
        case(f"overfill factor {key}",
             {"fn": "profileOverfillFactor",
              "args": ["medium_sand", key, 2.0, 6.0, 40.0]},
             {"factor": got["factor"], "borrow_volume": got["borrow_volume"],
              "native_volume": got["native_volume"]})

    for advance in (0.0, 15.0, 80.0):
        got = fill_volume_for_advance(native, dean_scale("coarse_sand"),
                                      advance, 2.0, 6.0)
        case(f"fill volume a={advance}",
             {"fn": "fillVolumeForAdvance",
              "args": [native, dean_scale("coarse_sand"), advance, 2.0, 6.0]},
             {"volume": got["volume"], "limit_depth": got["limit_depth"],
              "intersects": got["intersects"]})

    case("profile width",
         {"fn": "profileWidth", "args": [0.141, 6.0]},
         {"value": profile_width(0.141, 6.0)})

    # -- extremes ----------------------------------------------------------
    sample = [2.61, 3.04, 2.55, 4.12, 3.38, 2.90, 5.01, 3.71, 2.68, 3.15,
              4.44, 2.77, 3.92, 3.29, 2.83, 6.02, 3.55, 2.71, 4.80, 3.07]
    lam = l_moments(sample, 4)
    case("l_moments",
         {"fn": "lMoments", "args": [sample, 4]},
         {"l1": lam[0], "l2": lam[1], "l3": lam[2], "l4": lam[3]})

    excesses = [round(v - 2.5, 6) for v in sample]
    scale, shape = fit_gpd(excesses)
    case("fit_gpd",
         {"fn": "fitGpd", "args": [excesses]},
         {"scale": scale, "shape": shape})

    for T in (10.0, 100.0):
        case(f"gpd return {T}",
             {"fn": "gpdReturnValue", "args": [2.5, scale, shape, 6.0, T]},
             {"value": float(gpd_return_value(2.5, scale, shape, 6.0, T))})
        case(f"gev return {T}",
             {"fn": "gevReturnValue", "args": [3.4, 0.58, -0.06, T]},
             {"value": float(gev_return_value(3.4, 0.58, -0.06, T))})
    case("gpd return, zero shape",
         {"fn": "gpdReturnValue", "args": [3.0, 1.5, 0.0, 5.0, 100.0]},
         {"value": float(gpd_return_value(3.0, 1.5, 0.0, 5.0, 100.0))})

    # -- sediment ----------------------------------------------------------
    for key in ("silt", "fine_sand", "medium_sand", "coarse_sand", "fine_gravel"):
        case(f"grain size {key}",
             {"fn": "dimensionlessGrainSize", "args": [key]},
             {"value": dimensionless_grain_size(key)})
        case(f"critical shields {key}",
             {"fn": "criticalShields", "args": [key]},
             {"value": critical_shields(key)})
        case(f"fall velocity {key}",
             {"fn": "fallVelocity", "args": [key]},
             {"value": fall_velocity(key)})

    for kind in ("active", "at_rest", "passive"):
        for phi in (28.0, 33.0, 40.0):
            case(f"K {kind} phi={phi}",
                 {"fn": "earthPressureCoefficient", "args": [phi, kind]},
                 {"value": earth_pressure_coefficient(phi, kind)})
    case("K active with wall friction",
         {"fn": "earthPressureCoefficient", "args": [33.0, "active", 22.0]},
         {"value": earth_pressure_coefficient(33.0, "active", wall_friction=22.0)})
    case("K active with backslope",
         {"fn": "earthPressureCoefficient", "args": [33.0, "active", 0.0, 15.0]},
         {"value": earth_pressure_coefficient(33.0, "active", backslope=15.0)})

    for label, (key, height, table, load, kind) in {
        "saturated": ("medium_sand", 10.0, 0.0, 0.0, "active"),
        "drained": ("medium_sand", 10.0, 10.0, 0.0, "active"),
        "surcharged": ("coarse_sand", 7.0, 2.0, 25.0, "at_rest"),
        "cohesive": ("stiff_clay", 6.0, 6.0, 0.0, "active"),
    }.items():
        got = lateral_earth_force(key, height, table, load, kind=kind)
        case(f"earth force {label}",
             {"fn": "lateralEarthForce",
              "args": [key, height, table, load, kind]},
             {"soil": got["soil"], "water": got["water"], "total": got["total"],
              "arm": got["arm"], "K": got["K"],
              "water_fraction": got["water_fraction"]})

    for key in ("fine_sand", "coarse_gravel"):
        got = wave_shields(key, 1.5, 8.0, 10.0)
        case(f"wave shields {key}",
             {"fn": "waveShields", "args": [key, 1.5, 8.0, 10.0]},
             {"shields": got["shields"],
              "critical_shields": got["critical_shields"],
              "mobility": got["mobility"], "mobile": got["mobile"]})
        case(f"side slope {key}",
             {"fn": "dredgedSideSlope", "args": [key]},
             {"cot_beta": __import__(
                 "pyCoastal.applications.channel", fromlist=["x"]
             ).dredged_side_slope(key)["cot_beta"]})

    for cot, xi in ((2.0, 3.0), (3.5, 1.8)):
        case(f"reflection cot={cot} xi={xi}",
             {"fn": "reflectionCoefficient", "args": [cot, xi]},
             {"value": reflection_coefficient(cot, xi)})

    for key, Kr in (("fine_sand", 1.0), ("medium_sand", 0.35),
                    ("coarse_gravel", 0.5), ("soft_clay", 0.4)):
        got = toe_scour(key, 3.0, 12.0, 15.0, reflection=Kr)
        case(f"toe scour {key} Kr={Kr}",
             {"fn": "toeScour", "args": [key, 3.0, 12.0, 15.0, Kr]},
             {"depth": got["depth"], "unlimited_depth": got["unlimited_depth"],
              "applies": got["applies"]})

    # -- what the mound stands on ------------------------------------------
    for cot, armour, key in ((1.5, "tetrapod", "fine_sand"),
                             (2.0, "rock_two_layer_permeable", "medium_sand"),
                             (3.0, "rock_two_layer_permeable", "coarse_gravel")):
        c = DesignConditions.from_peak_period(Hm0=5.42, Tp=9.2, depth=10.0)
        mound = design_rubble_mound(c, cot_alpha=cot, armour=armour)
        got = mound_foundation(mound, 10.0, bed=key)
        case(f"mound foundation cot={cot} {key}",
             {"fn": "moundFoundation", "conditions": [5.42, 9.2, 10.0, 6 * 3600.0],
              "args": [{"cot_alpha": cot, "armour": armour}, 10.0, {"bed": key}],
              "design_first": True},
             {"toe_Dn50": got["toe_Dn50"], "toe_M50": got["toe_M50"],
              "toe_width": got["toe_width"],
              "toe_thickness": got["toe_thickness"],
              "bedding_thickness": got["bedding_thickness"],
              "bedding_extension": got["bedding_extension"]})
        block = crown_wall(mound, 0.0)
        case(f"crown wall cot={cot}",
             {"fn": "crownWall", "conditions": [5.42, 9.2, 10.0, 6 * 3600.0],
              "args": [{"cot_alpha": cot, "armour": armour}, 0.0],
              "design_first": True},
             {"base_level": block["base_level"],
              "deck_level": block["deck_level"],
              "parapet_top": block["parapet_top"],
              "total_width": block["total_width"],
              "concrete_m3_per_m": block["concrete_m3_per_m"]})

    # -- the roundhead -----------------------------------------------------
    for armour in ("rock_two_layer_permeable", "cubes_two_layer_random",
                   "tetrapod", "dolos"):
        for cot in (1.5, 2.0, 2.5, 3.0, 4.0):
            case(f"roundhead KD ratio {armour} cot={cot}",
                 {"fn": "roundheadKdRatio", "args": [armour, cot]},
                 {"value": roundhead_kd_ratio(armour, cot)})

    for cot, armour, ratio in ((1.5, "tetrapod", None), (2.0, "rock_two_layer_permeable", None),
                               (1.5, "tetrapod", 0.8), (3.0, "dolos", 0.5)):
        c = DesignConditions.from_peak_period(Hm0=5.42, Tp=9.2, depth=10.0)
        trunk = design_rubble_mound(c, cot_alpha=cot, armour=armour)
        got = roundhead(trunk, kd_ratio=ratio)
        case(f"roundhead {armour} cot={cot} r={ratio}",
             {"fn": "roundhead", "conditions": [5.42, 9.2, 10.0, 6 * 3600.0],
              "args": [{"cot_alpha": cot, "armour": armour}, ratio],
              "design_first": True},
             {"Dn50": got.Dn50, "M50": got.M50, "kd_ratio": got.kd_ratio,
              "crest_freeboard": got.crest_freeboard,
              "layer_thickness": got.layer["thickness"],
              "section": got.section})

    # -- the whole seawall, with the backfill in play ----------------------
    for label, (fill, table) in {
        "saturated sand": ("medium_sand", 0.0),
        "drained sand": ("medium_sand", 30.0),
        "gravel": ("fine_gravel", 0.0),
    }.items():
        c = DesignConditions.from_peak_period(Hm0=2.8, Tp=9.5, depth=8.5)
        got = design_seawall(c, 2.9, -5.6, tolerable_use="trained_staff",
                             backfill=fill, water_table=table)
        case(f"design_seawall backfill {label}",
             {"fn": "designSeawall", "conditions": [2.8, 9.5, 8.5, 6 * 3600.0],
              "args": [2.9, -5.6, {"tolerable_use": "trained_staff",
                                   "backfill": fill, "water_table": table}]},
             {"base_width": got.base_width,
              "crest_level": got.crest_level,
              "governing_case": got.governing_case,
              "earth_total": got.earth_driving["total"],
              "earth_arm": got.earth_driving["arm"],
              "drawdown_sliding": got.drawdown["sliding_FoS"],
              "drawdown_net": got.drawdown["net_force"]})

    # -- the planform: erf, diffusivity and the half-life ------------------
    import math as _math

    for z in (0.0, 0.25, 0.8, 1.5, 2.5, 4.0, -1.1):
        case(f"erf z={z}", {"fn": "erf", "args": [z]},
             {"value": _math.erf(z)})

    for length, width, Hb, D, B in (
        (1500.0, 40.0, 1.2, 6.0, 2.0),
        (800.0, 25.0, 0.6, 4.0, 1.5),
        (3000.0, 60.0, 2.1, 10.0, 3.0),
    ):
        design = NourishmentDesign(length=length, berm_width=width,
                                   taper=0.1 * length, D=D, B=B)
        climate = WaveClimate(Hb=Hb, T=8.0, alpha0=0.0)
        years = _plan_years(design, climate)
        tag = f"L={length} W={width} Hb={Hb}"
        call = {"fn": "planformEvolution",
                "fill": [length, width, 0.1 * length, D, B],
                "climate": [Hb, 8.0, 0.0],
                "args": [years]}
        centre = pelnard_considere(
            np.array([0.0]), years[-1] * SECONDS_PER_YEAR, design, climate)
        case(f"planform {tag}", call,
             {"diffusivity": longshore_diffusivity(climate, design),
              "half_life": spreading_half_life(design, climate) / SECONDS_PER_YEAR,
              "margin": plan_margin(design, climate, years),
              "centre_last": float(centre[0]),
              "spread": _math.sqrt(longshore_diffusivity(climate, design)
                                   * years[-1] * SECONDS_PER_YEAR)})

    return {"generated_from": "pyCoastal", "count": len(CASES), "cases": CASES}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).with_name("vectors.json"))
    args = parser.parse_args()
    data = build()
    # allow_nan=False turns a stray infinity into a loud failure here rather
    # than a silent one in the browser.
    args.out.write_text(json.dumps(data, indent=1, allow_nan=False),
                        encoding="utf-8")
    print(f"Wrote {args.out} with {data['count']} reference cases "
          f"({args.out.stat().st_size / 1024:.0f} kB)")


if __name__ == "__main__":
    main()
