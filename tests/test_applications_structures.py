"""Armour sizing and wave overtopping.

Checks are against the published forms of the relations and against the
behaviour a designer would insist on: more wave means more stone, more
freeboard means less water over the crest, rougher armour means less again.
"""
import math

import pytest

from pyCoastal.applications.structures import (
    DAMAGE_LEVELS,
    ROUGHNESS_FACTORS,
    TOLERABLE_DISCHARGE,
    DesignConditions,
    armour_layer,
    assess_overtopping,
    design_rubble_mound,
    obliquity_factor,
    overtopping_sloped,
    overtopping_vertical,
    overtopping_with_uncertainty,
    required_crest_freeboard,
    rock_armour_hudson,
    rock_armour_vandermeer,
)

G = 9.81


@pytest.fixture
def conditions():
    return DesignConditions(Hm0=4.0, Tm10=9.0, depth=12.0, storm_duration=6 * 3600.0)


# --------------------------------------------------------------------------
# Design conditions
# --------------------------------------------------------------------------

def test_peak_period_converts_with_the_standard_ratio():
    c = DesignConditions.from_peak_period(Hm0=3.0, Tp=11.0)
    assert c.Tm10 == pytest.approx(10.0)


def test_wave_count_is_duration_over_period():
    c = DesignConditions(Hm0=2.0, Tm10=8.0, storm_duration=4 * 3600.0)
    assert c.wave_count == pytest.approx(1800.0)


def test_wave_count_saturates_at_the_van_der_meer_limit():
    """Damage stops progressing near N = 7500, so the count is capped."""
    c = DesignConditions(Hm0=2.0, Tm10=8.0, storm_duration=100 * 3600.0)
    assert c.wave_count == 7500.0


def test_deep_water_wavelength_closed_form(conditions):
    assert conditions.deep_water_wavelength() == pytest.approx(
        G * 9.0**2 / (2 * math.pi)
    )


def test_breaker_parameter_closed_form(conditions):
    s0 = conditions.Hm0 / conditions.deep_water_wavelength()
    assert conditions.breaker_parameter(2.0) == pytest.approx(0.5 / math.sqrt(s0))


def test_steeper_slopes_give_a_larger_breaker_parameter(conditions):
    assert conditions.breaker_parameter(1.5) > conditions.breaker_parameter(4.0)


@pytest.mark.parametrize("kwargs", [{"Hm0": 0.0}, {"Tm10": -1.0}, {"depth": 0.0}])
def test_invalid_conditions_are_rejected(kwargs):
    base = {"Hm0": 2.0, "Tm10": 8.0, "depth": 10.0}
    with pytest.raises(ValueError):
        DesignConditions(**{**base, **kwargs})


# --------------------------------------------------------------------------
# Rock armour
# --------------------------------------------------------------------------

def test_vandermeer_plunging_matches_the_published_form(conditions):
    """Hs/(D Dn50) = 6.2 P^0.18 (S/sqrt(N))^0.2 xi^-0.5."""
    P, S, cot_a = 0.4, 2.0, 2.0
    out = rock_armour_vandermeer(conditions, cot_a, permeability=P, damage=S)
    if out["regime"] != "plunging":
        pytest.skip("this case is surging")

    N = conditions.wave_count
    xi = conditions.breaker_parameter(cot_a)
    expected = 6.2 * P**0.18 * (S / math.sqrt(N)) ** 0.2 * xi**-0.5
    assert out["stability_number"] == pytest.approx(expected)
    assert out["Dn50"] == pytest.approx(conditions.Hm0 / (1.585 * expected))


def test_vandermeer_surging_matches_the_published_form():
    """On a steep slope with long waves the surging branch governs."""
    c = DesignConditions(Hm0=2.0, Tm10=14.0, depth=20.0, storm_duration=3 * 3600.0)
    P, S, cot_a = 0.4, 2.0, 1.5
    out = rock_armour_vandermeer(c, cot_a, permeability=P, damage=S)
    assert out["regime"] == "surging"

    N = c.wave_count
    xi = c.breaker_parameter(cot_a)
    expected = 1.0 * P**-0.13 * (S / math.sqrt(N)) ** 0.2 * math.sqrt(cot_a) * xi**P
    assert out["stability_number"] == pytest.approx(expected)


def test_regime_switches_at_the_critical_breaker_parameter(conditions):
    out = rock_armour_vandermeer(conditions, 2.0)
    if out["xi"] < out["xi_cr"]:
        assert out["regime"] == "plunging"
    else:
        assert out["regime"] == "surging"


def test_stone_size_grows_with_wave_height_but_sub_linearly():
    """In the plunging branch Dn50 goes as Hm0^0.75, not Hm0.

    Dn50 is proportional to Hm0 * xi^0.5 and xi itself falls as Hm0^-0.5 at
    fixed period, so doubling the design wave needs about 2^0.75 = 1.68 times
    the stone, not twice. Worth pinning: assuming linear scaling oversizes.
    """
    small = DesignConditions(Hm0=3.0, Tm10=9.0, storm_duration=6 * 3600.0)
    large = DesignConditions(Hm0=6.0, Tm10=9.0, storm_duration=6 * 3600.0)
    a = rock_armour_vandermeer(small, 2.0)
    b = rock_armour_vandermeer(large, 2.0)
    assert a["regime"] == b["regime"] == "plunging"
    assert b["Dn50"] / a["Dn50"] == pytest.approx(2**0.75, rel=0.05)


def test_stone_size_increases_with_wave_height_across_regimes():
    sizes = [
        rock_armour_vandermeer(
            DesignConditions(Hm0=H, Tm10=9.0, storm_duration=6 * 3600.0), 2.0
        )["Dn50"]
        for H in (2.0, 3.0, 4.0, 6.0)
    ]
    assert all(a < b for a, b in zip(sizes, sizes[1:]))


def test_allowing_more_damage_permits_smaller_stone(conditions):
    start = rock_armour_vandermeer(conditions, 2.0, damage=DAMAGE_LEVELS["start_of_damage"])
    failure = rock_armour_vandermeer(conditions, 2.0, damage=DAMAGE_LEVELS["failure_1_in_2"])
    assert failure["Dn50"] < start["Dn50"]


def test_a_longer_storm_needs_bigger_stone():
    short = DesignConditions(Hm0=3.0, Tm10=9.0, storm_duration=1 * 3600.0)
    long = DesignConditions(Hm0=3.0, Tm10=9.0, storm_duration=12 * 3600.0)
    assert (
        rock_armour_vandermeer(long, 2.0)["Dn50"]
        > rock_armour_vandermeer(short, 2.0)["Dn50"]
    )


def test_a_permeable_core_permits_smaller_stone(conditions):
    """Permeability lets run-up dissipate inside the mound."""
    impermeable = rock_armour_vandermeer(conditions, 2.0, permeability=0.1)
    permeable = rock_armour_vandermeer(conditions, 2.0, permeability=0.5)
    assert permeable["Dn50"] < impermeable["Dn50"]


def test_safety_factor_increases_the_stone_size(conditions):
    plain = rock_armour_vandermeer(conditions, 2.0, safety_factor=1.0)
    safe = rock_armour_vandermeer(conditions, 2.0, safety_factor=1.3)
    assert safe["Dn50"] > plain["Dn50"]


def test_mass_follows_the_cube_of_the_diameter(conditions):
    out = rock_armour_vandermeer(conditions, 2.0)
    assert out["M50"] == pytest.approx(2650.0 * out["Dn50"] ** 3)


def test_hudson_matches_its_published_form(conditions):
    out = rock_armour_hudson(conditions, cot_alpha=2.0, Kd=4.0)
    expected = (4.0 * 2.0) ** (1 / 3) / 1.27
    assert out["stability_number"] == pytest.approx(expected)


def test_hudson_and_vandermeer_agree_to_within_a_factor(conditions):
    """Different formulations, but they must land in the same ballpark."""
    vdm = rock_armour_vandermeer(conditions, 2.0)["Dn50"]
    hud = rock_armour_hudson(conditions, 2.0)["Dn50"]
    assert 0.6 < hud / vdm < 1.7


def test_gentler_slopes_need_smaller_stone_under_hudson(conditions):
    """Hudson's cot(alpha) enters the stability number directly."""
    steep = rock_armour_hudson(conditions, cot_alpha=1.5)["Dn50"]
    gentle = rock_armour_hudson(conditions, cot_alpha=4.0)["Dn50"]
    assert gentle < steep


@pytest.mark.parametrize(
    "kwargs",
    [{"cot_alpha": 0.0}, {"permeability": 0.0}, {"permeability": 0.9},
     {"damage": 0.0}, {"safety_factor": 0.0}],
)
def test_invalid_armour_inputs_are_rejected(conditions, kwargs):
    base = {"cot_alpha": 2.0}
    with pytest.raises(ValueError):
        rock_armour_vandermeer(conditions, **{**base, **kwargs})


def test_armour_layer_geometry():
    out = armour_layer(Dn50=1.5, n_layers=2, layer_coefficient=1.0, porosity=0.37)
    assert out["thickness"] == pytest.approx(3.0)
    assert out["stones_per_m2"] == pytest.approx(2 * 0.63 / 1.5**2)
    assert out["mass_per_m2"] == pytest.approx(out["stones_per_m2"] * 2650 * 1.5**3)


def test_armour_layer_rejects_impossible_porosity():
    with pytest.raises(ValueError):
        armour_layer(Dn50=1.0, porosity=1.0)


# --------------------------------------------------------------------------
# Overtopping
# --------------------------------------------------------------------------

def test_overtopping_falls_steeply_with_freeboard(conditions):
    q = [
        overtopping_sloped(conditions, Rc, 2.0, gamma_f=0.4)["q"]
        for Rc in (2.0, 4.0, 6.0, 8.0)
    ]
    assert all(a > b for a, b in zip(q, q[1:]))
    assert q[0] > 100 * q[-1]


def test_overtopping_takes_the_lesser_of_the_two_branches(conditions):
    """EurOtop caps the breaking expression with the non-breaking maximum."""
    out = overtopping_sloped(conditions, 4.0, 2.0)
    Hm0 = conditions.Hm0
    xi = conditions.breaker_parameter(2.0)
    breaking = (0.023 / math.sqrt(0.5)) * xi * math.exp(-((2.7 * 4.0 / (xi * Hm0)) ** 1.3))
    non_breaking = 0.09 * math.exp(-((1.5 * 4.0 / Hm0) ** 1.3))
    assert out["q_dimensionless"] == pytest.approx(min(breaking, non_breaking))


def test_rough_armour_reduces_overtopping(conditions):
    smooth = overtopping_sloped(conditions, 4.0, 2.0, gamma_f=1.0)["q"]
    rough = overtopping_sloped(conditions, 4.0, 2.0, gamma_f=0.4)["q"]
    assert rough < smooth


def test_oblique_attack_reduces_overtopping(conditions):
    head_on = overtopping_sloped(conditions, 4.0, 2.0, gamma_beta=1.0)["q"]
    oblique = overtopping_sloped(
        conditions, 4.0, 2.0, gamma_beta=obliquity_factor(45.0)
    )["q"]
    assert oblique < head_on


def test_obliquity_factor_matches_its_formula():
    assert obliquity_factor(0.0) == pytest.approx(1.0)
    assert obliquity_factor(45.0) == pytest.approx(1 - 0.0063 * 45)
    # Beyond 80 degrees the factor is held constant.
    assert obliquity_factor(120.0) == pytest.approx(obliquity_factor(80.0))


def test_bigger_waves_overtop_more(conditions):
    calm = DesignConditions(Hm0=2.0, Tm10=9.0, depth=12.0)
    storm = DesignConditions(Hm0=5.0, Tm10=9.0, depth=12.0)
    assert (
        overtopping_sloped(storm, 4.0, 2.0)["q"]
        > overtopping_sloped(calm, 4.0, 2.0)["q"]
    )


def test_zero_or_negative_freeboard_is_refused(conditions):
    with pytest.raises(ValueError, match="positive freeboard"):
        overtopping_sloped(conditions, 0.0, 2.0)
    with pytest.raises(ValueError, match="positive freeboard"):
        overtopping_sloped(conditions, -1.0, 2.0)


@pytest.mark.parametrize("gamma", [0.0, 1.2])
def test_out_of_range_reduction_factors_are_refused(conditions, gamma):
    with pytest.raises(ValueError):
        overtopping_sloped(conditions, 4.0, 2.0, gamma_f=gamma)


def test_vertical_wall_matches_its_published_form(conditions):
    out = overtopping_vertical(conditions, 4.0)
    expected = 0.047 * math.exp(-((2.35 * 4.0 / conditions.Hm0) ** 1.3))
    assert out["q_dimensionless"] == pytest.approx(expected)


def test_vertical_wall_flags_impulsive_conditions():
    """Shallow water over the toe drives the wall into the impulsive regime."""
    deep = DesignConditions(Hm0=2.0, Tm10=8.0, depth=20.0)
    shallow = DesignConditions(Hm0=3.0, Tm10=12.0, depth=3.0)
    assert not overtopping_vertical(deep, 3.0)["impulsive"]
    assert overtopping_vertical(shallow, 3.0)["impulsive"]


def test_uncertainty_band_brackets_the_mean(conditions):
    q = overtopping_sloped(conditions, 4.0, 2.0)
    band = overtopping_with_uncertainty(q, factor=3.0)
    assert band["q_lower"] < band["q_mean"] < band["q_upper"]
    assert band["q_upper"] == pytest.approx(9 * band["q_lower"])


def test_uncertainty_factor_below_one_is_refused(conditions):
    q = overtopping_sloped(conditions, 4.0, 2.0)
    with pytest.raises(ValueError):
        overtopping_with_uncertainty(q, factor=0.5)


# --------------------------------------------------------------------------
# Inversion and assessment
# --------------------------------------------------------------------------

@pytest.mark.parametrize("q_target", [0.1, 1.0, 10.0])
def test_required_freeboard_round_trips(conditions, q_target):
    Rc = required_crest_freeboard(conditions, q_target, 2.0, gamma_f=0.4)
    achieved = overtopping_sloped(conditions, Rc, 2.0, gamma_f=0.4)["q"]
    assert achieved == pytest.approx(q_target, rel=0.02)


def test_a_stricter_limit_needs_a_higher_crest(conditions):
    lenient = required_crest_freeboard(conditions, 10.0, 2.0)
    strict = required_crest_freeboard(conditions, 0.1, 2.0)
    assert strict > lenient


def test_required_freeboard_works_for_a_vertical_wall(conditions):
    Rc = required_crest_freeboard(conditions, 1.0, 2.0, vertical=True)
    assert overtopping_vertical(conditions, Rc)["q"] == pytest.approx(1.0, rel=0.02)


def test_required_freeboard_rejects_a_nonpositive_target(conditions):
    with pytest.raises(ValueError):
        required_crest_freeboard(conditions, 0.0, 2.0)


def test_assessment_sorts_from_strictest_to_most_permissive():
    limits = [info["limit"] for info in assess_overtopping(0.5).values()]
    assert limits == sorted(limits)


def test_assessment_marks_the_right_uses_as_acceptable():
    out = assess_overtopping(0.5)
    assert not out["pedestrians_unaware"]["acceptable"]   # limit 0.03
    assert out["trained_staff"]["acceptable"]             # limit 1.0
    assert out["vehicles_low_speed"]["acceptable"]        # limit 10


def test_every_tolerable_limit_is_positive_and_described():
    for limit, description in TOLERABLE_DISCHARGE.values():
        assert limit > 0
        assert description


# --------------------------------------------------------------------------
# Whole section
# --------------------------------------------------------------------------

def test_design_meets_the_limit_on_the_upper_bound_not_the_mean(conditions):
    """Designing to the mean would be exceeded about half the time."""
    design = design_rubble_mound(conditions, cot_alpha=2.0, tolerable_use="trained_staff")
    limit = TOLERABLE_DISCHARGE["trained_staff"][0]
    assert design.q_upper == pytest.approx(limit, rel=0.05)
    assert design.q_mean < limit


def test_a_stricter_use_raises_the_crest(conditions):
    staff = design_rubble_mound(conditions, tolerable_use="trained_staff")
    strollers = design_rubble_mound(conditions, tolerable_use="pedestrians_unaware")
    assert strollers.crest_freeboard > staff.crest_freeboard


def test_armour_choice_changes_the_crest_but_not_the_stone(conditions):
    """Roughness enters overtopping only; stability sizes the rock."""
    rock = design_rubble_mound(conditions, armour="rock_two_layer_permeable")
    smooth = design_rubble_mound(conditions, armour="smooth_concrete")
    assert smooth.crest_freeboard > rock.crest_freeboard
    assert smooth.Dn50 == pytest.approx(rock.Dn50)


def test_design_summary_reports_the_governing_numbers(conditions):
    text = design_rubble_mound(conditions).summary()
    for expected in ("Design condition", "Armour", "Crest freeboard", "Overtopping"):
        assert expected in text


def test_unknown_armour_or_use_is_refused(conditions):
    with pytest.raises(ValueError, match="Unknown armour"):
        design_rubble_mound(conditions, armour="marshmallow")
    with pytest.raises(ValueError, match="Unknown use"):
        design_rubble_mound(conditions, tolerable_use="hovercraft")


def test_every_roughness_factor_is_in_range():
    for name, value in ROUGHNESS_FACTORS.items():
        assert 0.0 < value <= 1.0, name


# ---------------------------------------------------------------------------
# Toe scour
# ---------------------------------------------------------------------------


def test_reflection_rises_with_surf_similarity():
    from pyCoastal.applications.structures import reflection_coefficient

    values = [reflection_coefficient(2.0, xi) for xi in (1.0, 2.0, 4.0, 8.0)]
    assert all(b > a for a, b in zip(values, values[1:]))
    assert all(0.0 < v <= 1.0 for v in values)


def test_permeable_slope_reflects_less_than_smooth():
    from pyCoastal.applications.structures import reflection_coefficient

    rough = reflection_coefficient(2.0, 3.0, permeable=True)
    smooth = reflection_coefficient(2.0, 3.0, permeable=False)
    assert rough < smooth


def test_toe_scour_at_a_vertical_wall_recovers_xie():
    """Reflection of one must reproduce the vertical-wall relation exactly."""
    from pyCoastal.applications.seawall import scour_depth_vertical_wall
    from pyCoastal.applications.structures import toe_scour

    result = toe_scour("fine_sand", 3.0, 12.0, 15.0, reflection=1.0)
    assert result["unlimited_depth"] == pytest.approx(
        scour_depth_vertical_wall(3.0, 12.0, 15.0)
    )


def test_toe_scour_scales_with_reflection():
    from pyCoastal.applications.structures import toe_scour

    full = toe_scour("fine_sand", 3.0, 12.0, 15.0, reflection=1.0)
    half = toe_scour("fine_sand", 3.0, 12.0, 15.0, reflection=0.5)
    assert half["unlimited_depth"] == pytest.approx(
        0.5 * full["unlimited_depth"])


def test_toe_scour_decays_with_depth():
    from pyCoastal.applications.structures import toe_scour

    depths = [8.0, 15.0, 25.0, 40.0]
    scour = [toe_scour("fine_sand", 3.0, 12.0, h)["unlimited_depth"]
             for h in depths]
    assert all(b < a for a, b in zip(scour, scour[1:]))


def test_toe_scour_is_not_computed_for_a_cohesive_bed():
    from pyCoastal.applications.structures import toe_scour

    result = toe_scour("soft_clay", 3.0, 12.0, 15.0)
    assert result["depth"] == 0.0
    assert result["applies"] is False


def test_toe_scour_is_reduced_on_an_immobile_bed():
    """A clear-water bed does not scour to the live-bed depth."""
    from pyCoastal.applications.structures import toe_scour

    result = toe_scour("coarse_gravel", 0.4, 6.0, 30.0)
    assert result["mobility"]["mobile"] is False
    assert result["depth"] == pytest.approx(0.5 * result["unlimited_depth"])


def test_toe_scour_validates_its_reflection():
    from pyCoastal.applications.structures import toe_scour

    with pytest.raises(ValueError):
        toe_scour("fine_sand", 3.0, 12.0, 15.0, reflection=1.5)


def test_breakwater_toe_scour_is_smaller_for_a_flatter_mound():
    """A flatter slope reflects less and therefore scours its toe less."""
    from pyCoastal.applications.structures import breakwater_toe_scour

    conditions = DesignConditions.from_peak_period(Hm0=4.0, Tp=11.0, depth=12.0)
    steep = design_rubble_mound(conditions, cot_alpha=1.5)
    flat = design_rubble_mound(conditions, cot_alpha=3.5)
    assert (breakwater_toe_scour(flat, 12.0)["depth"]
            < breakwater_toe_scour(steep, 12.0)["depth"])


def test_breakwater_toe_scour_is_below_the_vertical_wall_value():
    from pyCoastal.applications.seawall import scour_depth_vertical_wall
    from pyCoastal.applications.structures import breakwater_toe_scour

    conditions = DesignConditions.from_peak_period(Hm0=4.0, Tp=11.0, depth=12.0)
    mound = design_rubble_mound(conditions, cot_alpha=2.0)
    scour = breakwater_toe_scour(mound, 12.0)
    wall = scour_depth_vertical_wall(4.0, conditions.Tm10, 12.0)
    assert scour["depth"] < wall
    assert scour["apron_width"] >= 2.0
