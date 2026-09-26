"""Vertical seawall design: Goda pressures, stability, scour and toe."""

import math

import pytest

from pyCoastal.applications.seawall import (
    RHO_W,
    SeawallDesign,
    bearing_pressures,
    design_seawall,
    goda_breaking_height,
    goda_pressures,
    overturning_safety,
    scour_depth_vertical_wall,
    sliding_safety,
    toe_stone_size,
)
from pyCoastal.applications.structures import DesignConditions


@pytest.fixture
def conditions():
    return DesignConditions.from_peak_period(
        Hm0=2.0, Tp=8.0, depth=3.5, storm_duration=6 * 3600.0
    )


@pytest.fixture
def wall(conditions):
    return design_seawall(
        conditions, still_water_level=2.5, seabed_level=-1.0,
        tolerable_use="trained_staff",
    )


# ---------------------------------------------------------------------------
# Goda pressures
# ---------------------------------------------------------------------------


def test_goda_pressure_head_is_a_sane_fraction_of_the_wave():
    """p1 should be of order rho g Hmax, not orders away from it."""
    res = goda_pressures(Hm0=3.0, T=10.0, depth=12.0, wall_toe_depth=12.0,
                         crest_freeboard=6.0, depth_limit=False)
    ceiling = RHO_W * 9.81 * res["Hmax"] / 1000.0
    assert 0.3 * ceiling < res["p1"] < 1.0 * ceiling


def test_goda_alpha1_tends_to_its_deep_water_floor():
    """alpha1 falls to 0.6 in deep water, where 2kh/sinh(2kh) vanishes."""
    deep = goda_pressures(Hm0=2.0, T=6.0, depth=200.0, wall_toe_depth=20.0,
                          crest_freeboard=5.0, depth_limit=False)
    assert deep["alpha1"] == pytest.approx(0.6, abs=1e-3)


def test_goda_alpha3_is_one_when_the_wall_starts_at_the_bed():
    shallow = goda_pressures(Hm0=1.5, T=8.0, depth=6.0, wall_toe_depth=1e-6,
                             crest_freeboard=4.0, depth_limit=False)
    assert shallow["alpha3"] == pytest.approx(1.0, abs=1e-5)


def test_goda_oblique_attack_reduces_the_load():
    kwargs = dict(Hm0=3.0, T=10.0, depth=10.0, wall_toe_depth=10.0,
                  crest_freeboard=5.0, depth_limit=False)
    head_on = goda_pressures(beta_degrees=0.0, **kwargs)
    oblique = goda_pressures(beta_degrees=45.0, **kwargs)
    assert oblique["F"] < head_on["F"]


def test_goda_depth_limit_caps_the_design_wave():
    limited = goda_pressures(Hm0=4.0, T=10.0, depth=4.0, wall_toe_depth=4.0,
                             crest_freeboard=4.0)
    h_b = 4.0 + 5.0 * 4.0 / 30.0
    assert limited["Hmax"] == pytest.approx(
        goda_breaking_height(10.0, h_b, 1 / 30))
    assert limited["Hmax"] < 1.8 * 4.0
    assert limited["depth_limited"] is True

    free = goda_pressures(Hm0=4.0, T=10.0, depth=4.0, wall_toe_depth=4.0,
                          crest_freeboard=4.0, depth_limit=False)
    assert free["Hmax"] == pytest.approx(1.8 * 4.0)
    assert free["depth_limited"] is False


def test_goda_force_is_bounded_by_the_pressure_box():
    """F cannot exceed p1 times the full loaded height."""
    res = goda_pressures(Hm0=2.5, T=9.0, depth=9.0, wall_toe_depth=9.0,
                         crest_freeboard=4.0, depth_limit=False)
    box = res["p1"] * (9.0 + res["hc_star"])
    assert 0.0 < res["F"] < box


def test_goda_lever_arm_lies_within_the_loaded_height():
    res = goda_pressures(Hm0=2.5, T=9.0, depth=9.0, wall_toe_depth=9.0,
                         crest_freeboard=4.0, depth_limit=False)
    assert 0.0 < res["arm"] < 9.0 + res["hc_star"]


def test_goda_low_crest_sheds_load():
    """A crest below the run-up wedge is not loaded above itself."""
    tall = goda_pressures(Hm0=3.0, T=10.0, depth=10.0, wall_toe_depth=10.0,
                          crest_freeboard=10.0, depth_limit=False)
    short = goda_pressures(Hm0=3.0, T=10.0, depth=10.0, wall_toe_depth=10.0,
                           crest_freeboard=1.0, depth_limit=False)
    assert short["F"] < tall["F"]
    assert short["hc_star"] == pytest.approx(1.0)


def test_goda_rejects_nonsense_inputs():
    for bad in (dict(Hm0=-1.0), dict(T=0.0), dict(depth=-5.0),
                dict(wall_toe_depth=0.0)):
        kwargs = dict(Hm0=2.0, T=8.0, depth=10.0, wall_toe_depth=10.0)
        kwargs.update(bad)
        with pytest.raises(ValueError):
            goda_pressures(**kwargs)


# ---------------------------------------------------------------------------
# Scour and toe
# ---------------------------------------------------------------------------


def test_scour_falls_away_in_deep_water():
    """sinh(kh) grows fast, so the standing wave stops reaching the bed."""
    depths = [4.0, 10.0, 20.0, 40.0, 80.0]
    scour = [scour_depth_vertical_wall(2.0, 9.0, h) for h in depths]
    assert all(b < a for a, b in zip(scour, scour[1:]))
    assert scour[-1] < 0.01 * scour[0]


def test_scour_is_linear_in_wave_height():
    a = scour_depth_vertical_wall(1.0, 8.0, 6.0)
    b = scour_depth_vertical_wall(3.0, 8.0, 6.0)
    assert b == pytest.approx(3.0 * a)


def test_scour_coefficient_must_be_non_negative():
    with pytest.raises(ValueError):
        scour_depth_vertical_wall(2.0, 8.0, 6.0, coefficient=-0.1)


def test_toe_stone_grows_as_the_toe_gets_shallower():
    """A toe berm near the surface takes more wave, so needs bigger rock."""
    deep_toe = toe_stone_size(3.0, toe_depth=8.0, water_depth=10.0)
    shallow_toe = toe_stone_size(3.0, toe_depth=4.0, water_depth=10.0)
    assert shallow_toe["Dn50"] > deep_toe["Dn50"]


def test_toe_range_flag_matches_the_calibration_window():
    assert toe_stone_size(2.0, 5.0, 10.0)["within_range"] is True      # 0.5
    assert toe_stone_size(2.0, 2.0, 10.0)["within_range"] is False     # 0.2
    assert toe_stone_size(2.0, 9.5, 10.0)["within_range"] is False     # 0.95


def test_toe_more_damage_allows_smaller_stone():
    tight = toe_stone_size(3.0, 6.0, 10.0, damage=0.5)
    loose = toe_stone_size(3.0, 6.0, 10.0, damage=4.0)
    assert loose["Dn50"] < tight["Dn50"]


def test_toe_mass_follows_the_cube_of_the_diameter():
    res = toe_stone_size(3.0, 6.0, 10.0)
    assert res["M50"] == pytest.approx(2650.0 * res["Dn50"] ** 3)


# ---------------------------------------------------------------------------
# Stability checks
# ---------------------------------------------------------------------------


def test_sliding_is_friction_times_net_weight_over_force():
    assert sliding_safety(100.0, 500.0, 100.0, friction=0.6) == pytest.approx(2.4)


def test_sliding_returns_zero_when_uplift_floats_the_wall():
    assert sliding_safety(100.0, 200.0, 250.0) == 0.0


def test_sliding_needs_a_real_force():
    with pytest.raises(ValueError):
        sliding_safety(0.0, 500.0, 0.0)


def test_overturning_uses_the_two_thirds_uplift_arm():
    # Restoring 1000, uplift 30 over a 6 m base removes 30*4 = 120.
    fos = overturning_safety(F=100.0, arm=2.0, restoring_moment=1000.0,
                             uplift=30.0, base_width=6.0)
    assert fos == pytest.approx((1000.0 - 120.0) / 200.0)


def test_overturning_returns_zero_when_uplift_wins():
    assert overturning_safety(10.0, 1.0, 100.0, uplift=100.0,
                              base_width=3.0) == 0.0


def test_bearing_resultant_at_the_centre_is_uniform():
    res = bearing_pressures(normal=600.0, base_width=6.0, net_moment=1800.0)
    assert res["e"] == pytest.approx(0.0)
    assert res["p_max"] == pytest.approx(100.0)
    assert res["p_min"] == pytest.approx(100.0)
    assert res["middle_third"] is True


def test_bearing_at_the_middle_third_edge_puts_p_min_at_zero():
    # e = B/6 exactly: the classic no-tension limit.
    width = 6.0
    normal = 600.0
    x_res = 0.5 * width - width / 6.0
    res = bearing_pressures(normal, width, net_moment=normal * x_res)
    assert res["middle_third"] is True
    assert res["p_min"] == pytest.approx(0.0, abs=1e-9)
    assert res["p_max"] == pytest.approx(2.0 * normal / width)


def test_bearing_outside_the_middle_third_uses_the_no_tension_wedge():
    width = 6.0
    normal = 600.0
    x_res = 1.0                       # well outside the middle third
    res = bearing_pressures(normal, width, net_moment=normal * x_res)
    assert res["middle_third"] is False
    assert res["p_max"] == pytest.approx(2.0 * normal / (3.0 * x_res))


def test_bearing_needs_a_positive_width():
    with pytest.raises(ValueError):
        bearing_pressures(100.0, 0.0, 50.0)


# ---------------------------------------------------------------------------
# The whole design
# ---------------------------------------------------------------------------


def test_design_meets_every_target_it_was_given(wall):
    assert wall.sliding_FoS >= 1.2
    assert wall.overturning_FoS >= 1.5
    assert wall.bearing["middle_third"] is True


def test_design_crest_delivers_the_tolerable_discharge(wall):
    # The crest is set on the upper bound, so the upper bound is what must
    # meet the 1 l/s/m limit for trained staff.
    assert wall.q_upper == pytest.approx(1.0, rel=0.02)
    assert wall.q_mean < wall.q_upper


def test_design_levels_are_ordered(wall):
    assert wall.founding_level < wall.seabed_level < wall.still_water_level
    assert wall.still_water_level < wall.promenade_level < wall.crest_level


def test_design_embedment_is_bracketed(conditions):
    tiny_scour = design_seawall(
        conditions, 2.5, -1.0, scour_coefficient=0.0, minimum_embedment=1.5
    )
    assert tiny_scour.embedment == pytest.approx(1.5)

    huge_scour = design_seawall(
        conditions, 2.5, -1.0, scour_coefficient=5.0, maximum_embedment=2.5
    )
    assert huge_scour.embedment == pytest.approx(2.5)
    assert any("embedment limit" in w for w in huge_scour.warnings)


def test_design_a_stricter_limit_lifts_the_crest(conditions):
    lax = design_seawall(conditions, 2.5, -1.0, tolerable_use="trained_staff")
    strict = design_seawall(conditions, 2.5, -1.0,
                            tolerable_use="pedestrians_unaware")
    assert strict.crest_level > lax.crest_level


def test_design_a_bigger_wave_needs_a_wider_base():
    small = DesignConditions.from_peak_period(Hm0=2.0, Tp=9.0, depth=8.5)
    big = DesignConditions.from_peak_period(Hm0=3.5, Tp=9.0, depth=8.5)
    assert (design_seawall(big, 2.5, -1.0).base_width
            > design_seawall(small, 2.5, -1.0).base_width)


def test_design_oblique_attack_needs_less_wall(conditions):
    head_on = design_seawall(conditions, 2.5, -1.0, beta_degrees=0.0)
    oblique = design_seawall(conditions, 2.5, -1.0, beta_degrees=45.0)
    assert oblique.base_width <= head_on.base_width


def test_design_gives_up_rather_than_growing_forever():
    """A gravity wall is the wrong form for some sites, and should say so."""
    brutal = DesignConditions.from_peak_period(Hm0=9.0, Tp=15.0, depth=25.0)
    result = design_seawall(brutal, 3.0, -22.0, max_base_width=8.0)
    assert result.base_width <= 8.0 + 1e-9
    assert any("gravity wall is the wrong form" in w for w in result.warnings)


def test_design_flags_impulsive_conditions():
    """Shallow water at a vertical wall is impulsive, and must be called out."""
    shallow = DesignConditions.from_peak_period(Hm0=2.2, Tp=9.0, depth=3.6)
    result = design_seawall(shallow, 2.9, -0.7)
    assert result.impulsive is True
    assert any("impulsive" in w for w in result.warnings)


def test_design_rejects_a_water_level_below_the_bed(conditions):
    with pytest.raises(ValueError):
        design_seawall(conditions, still_water_level=-6.0, seabed_level=-5.6)


def test_design_rejects_an_unknown_use(conditions):
    with pytest.raises(ValueError) as excinfo:
        design_seawall(conditions, 2.5, -1.0, tolerable_use="hovercraft")
    assert "trained_staff" in str(excinfo.value)


def test_design_rejects_a_zero_step(conditions):
    with pytest.raises(ValueError):
        design_seawall(conditions, 2.5, -1.0, step=0.0)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def test_quantities_add_up(wall):
    q = wall.quantities()
    assert q["concrete_total_m3_per_m"] == pytest.approx(
        q["concrete_base_m3_per_m"] + q["concrete_stem_m3_per_m"]
    )
    assert q["excavation_m3_per_m"] == pytest.approx(
        wall.base_width * wall.embedment
    )


def test_quantities_concrete_mass_matches_its_volume(wall):
    q = wall.quantities()
    assert q["concrete_mass_t_per_m"] == pytest.approx(
        q["concrete_total_m3_per_m"] * 2.4
    )


def test_heel_width_is_the_base_less_the_stem(wall):
    assert wall.heel_width == pytest.approx(wall.base_width - wall.stem_thickness)


def test_summary_mentions_every_check(wall):
    text = wall.summary()
    for phrase in ("Crest level", "Backfill", "Earth pressure",
                   "Load case 1", "Load case 2", "Governing case",
                   "bearing", "Stem", "Toe protection", "Overtopping", "Concrete"):
        assert phrase in text


# ---------------------------------------------------------------------------
# The backfill
# ---------------------------------------------------------------------------


def test_saturated_backfill_needs_a_wider_base(conditions):
    """A blocked drain is a structural problem, not a maintenance one.

    "Drained" can only mean down to still water: the sea feeds the fill, so
    a deeper water table is clamped there, with a warning.
    """
    drained = design_seawall(conditions, 2.5, -1.0, backfill="medium_sand",
                             water_table=30.0)
    saturated = design_seawall(conditions, 2.5, -1.0, backfill="medium_sand",
                               water_table=0.0)
    assert drained.back_water_level == pytest.approx(2.5)
    assert any("below the still water level" in w for w in drained.warnings)
    assert saturated.base_width > 1.3 * drained.base_width
    assert saturated.earth_driving["total"] > 1.2 * drained.earth_driving["total"]


def test_stronger_backfill_needs_a_narrower_base(conditions):
    weak = design_seawall(conditions, 2.5, -1.0, backfill="fine_sand")
    strong = design_seawall(conditions, 2.5, -1.0, backfill="fine_gravel")
    assert strong.base_width < weak.base_width


def test_drawdown_governs_a_saturated_backfill(conditions):
    wall = design_seawall(conditions, 2.5, -1.0, backfill="medium_sand",
                          water_table=0.0)
    assert wall.governing_case == "drawdown"
    assert any("drawdown case governs" in w for w in wall.warnings)


def test_both_load_cases_meet_their_targets(conditions):
    wall = design_seawall(conditions, 2.5, -1.0, backfill="medium_sand",
                          target_sliding=1.2, target_overturning=1.5)
    assert wall.sliding_FoS >= 1.2
    assert wall.overturning_FoS >= 1.5
    assert wall.drawdown["sliding_FoS"] >= 1.2
    assert wall.drawdown["overturning_FoS"] >= 1.5


def test_pore_water_dominates_a_saturated_backfill(conditions):
    wall = design_seawall(conditions, 2.5, -1.0, water_table=0.0)
    assert wall.earth_driving["water_fraction"] > 0.6
    assert any("Pore water is" in w for w in wall.warnings)


def test_surcharge_pushes_harder(conditions):
    bare = design_seawall(conditions, 2.5, -1.0, surcharge=0.0)
    loaded = design_seawall(conditions, 2.5, -1.0, surcharge=50.0)
    assert loaded.earth_driving["total"] > bare.earth_driving["total"]
    assert loaded.base_width >= bare.base_width


def test_driving_uses_at_rest_and_resisting_uses_active(conditions):
    """The asymmetry is deliberate: it is conservative in both directions."""
    wall = design_seawall(conditions, 2.5, -1.0)
    assert wall.earth_driving["kind"] == "at_rest"
    assert wall.earth_resisting["kind"] == "active"
    assert wall.earth_driving["total"] > wall.earth_resisting["total"]


def test_earth_pressure_can_be_left_out_of_the_resisting_side(conditions):
    credited = design_seawall(conditions, 2.5, -1.0, credit_earth_pressure=True)
    ignored = design_seawall(conditions, 2.5, -1.0, credit_earth_pressure=False)
    assert ignored.earth_resisting["total"] == 0.0
    assert credited.earth_resisting["total"] > 0.0


def test_cohesive_backfill_is_flagged(conditions):
    wall = design_seawall(conditions, 2.5, -1.0, backfill="stiff_clay")
    assert any("cohesive" in w for w in wall.warnings)


def test_retained_height_runs_from_the_promenade_to_the_founding_level(wall):
    assert wall.retained_height == pytest.approx(
        wall.promenade_level - wall.founding_level)


def test_summary_surfaces_warnings():
    shallow = DesignConditions.from_peak_period(Hm0=2.2, Tp=9.0, depth=3.6)
    result = design_seawall(shallow, 2.9, -0.7)
    assert "Warnings" in result.summary()


# ---------------------------------------------------------------------------
# Free body, bearing, stem and toe (the 2026-09 corrections)
# ---------------------------------------------------------------------------


def _independent_drawdown(d):
    """Drawdown sliding and overturning from first principles.

    Total weights; hydrostatic pressure on the face from the trough, on the
    back plane from the backfill water table, and a linear uplift between
    the two. Written apart from the design code so the two can disagree.
    """
    from pyCoastal.applications.seawall import GAMMA_C, GAMMA_W

    B, tb, s = d.base_width, d.base_thickness, d.stem_thickness
    zf, zc, zp = d.founding_level, d.crest_level, d.promenade_level
    zt = zf + tb
    zw = d.back_water_level
    fill = d.backfill
    wet = min(max(zw - zt, 0.0), zp - zt)
    dry = (zp - zt) - wet
    parts = [(GAMMA_C * B * tb, B / 2),
             (GAMMA_C * s * (zc - zt), s / 2),
             ((fill.dry_unit_weight * dry + fill.saturated_unit_weight * wet)
              * (B - s), (s + B) / 2)]
    W = sum(w for w, _ in parts)
    hf = d.drawdown["trough_level"] - zf
    hb = zw - zf
    U = 0.5 * GAMMA_W * (hf + hb) * B
    xU = B * (hf + 2 * hb) / (3 * (hf + hb))
    front = 0.5 * GAMMA_W * hf**2
    H = d.earth_driving["total"] - front
    slide = 0.6 * (W - U) / H
    over = ((sum(w * x for w, x in parts) + front * hf / 3)
            / (d.earth_driving["moment"] + U * xU))
    return slide, over


@pytest.mark.parametrize("table", [0.0, 1.0, 3.0])
def test_drawdown_matches_an_independent_free_body(conditions, table):
    d = design_seawall(conditions, 2.5, -1.0, tolerable_use="trained_staff",
                       water_table=table)
    slide, over = _independent_drawdown(d)
    assert d.drawdown["sliding_FoS"] == pytest.approx(slide, rel=1e-6)
    assert d.drawdown["overturning_FoS"] == pytest.approx(over, rel=1e-6)


def test_both_cases_keep_the_resultant_in_the_middle_third(wall):
    assert wall.bearing["middle_third"]
    assert wall.drawdown["bearing"]["middle_third"]


def test_bearing_limit_is_met_in_both_cases(wall):
    assert wall.bearing["p_max"] <= wall.allowable_bearing + 1e-6
    assert wall.drawdown["bearing"]["p_max"] <= wall.allowable_bearing + 1e-6


def test_a_lower_allowable_bearing_needs_a_wider_base(conditions):
    loose = design_seawall(conditions, 2.5, -1.0, allowable_bearing=None)
    tight = design_seawall(conditions, 2.5, -1.0, allowable_bearing=120.0)
    assert tight.base_width > loose.base_width


def test_the_water_table_is_never_taken_below_still_water(conditions):
    d = design_seawall(conditions, 2.5, -1.0, water_table=50.0)
    assert d.back_water_level == pytest.approx(2.5)


def test_the_stem_carries_its_design_moment(wall):
    from pyCoastal.applications.seawall import stem_section

    need = stem_section(wall.stem["moment"], wall.stem["shear"])
    assert wall.stem_thickness >= need["thickness"] - 1e-9
    assert wall.base_thickness >= wall.stem_thickness


def test_stem_section_bending_follows_the_lever_arm_rule():
    from pyCoastal.applications.seawall import stem_section

    res = stem_section(1000.0, 0.0)
    fyd = 500.0 / 1.15
    d = math.sqrt(1000.0e3 / (0.9 * 0.01 * fyd * 1e6))
    assert res["d_bending"] == pytest.approx(d)
    assert res["thickness"] >= d + 0.1


def test_a_tall_wall_is_flagged_as_the_wrong_form():
    c = DesignConditions.from_peak_period(Hm0=2.8, Tp=9.5, depth=8.5)
    d = design_seawall(c, 2.9, -5.6, tolerable_use="trained_staff")
    assert any("cantilever L-wall" in w for w in d.warnings)


def test_tanimoto_matches_its_published_form():
    from pyCoastal.applications.seawall import toe_stone_tanimoto
    from pyCoastal.tools.wave import dispersion

    Hs, T, h, B = 3.0, 10.0, 6.0, 8.0
    got = toe_stone_tanimoto(Hs, T, h, B)
    L = dispersion(T, h)
    k1 = (4 * math.pi * h / L) / math.sinh(4 * math.pi * h / L)
    k2 = math.sin(2 * math.pi * B / L) ** 2
    kap = k1 * k2
    Ns = max(1.8, 1.3 * (1 - kap) / kap ** (1 / 3) * h / Hs
             + 1.8 * math.exp(-1.5 * (1 - kap) ** 2 / kap ** (1 / 3) * h / Hs))
    assert got["stability_number"] == pytest.approx(Ns)
    assert got["Dn50"] == pytest.approx(Hs / (1.585 * Ns))


def test_tanimoto_stone_grows_as_the_berm_rises():
    from pyCoastal.applications.seawall import toe_stone_tanimoto

    deep = toe_stone_tanimoto(3.0, 10.0, 8.0, 8.0)
    shallow = toe_stone_tanimoto(3.0, 10.0, 3.0, 8.0)
    assert shallow["Dn50"] > deep["Dn50"]
