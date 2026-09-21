"""Open channel hydraulics: normal and critical depth, backwater, afflux.

Most of this is testable against definitions rather than against data,
which is the nice thing about it. Normal depth has to reproduce Manning,
critical depth has to give a Froude number of exactly one and has to
minimise specific energy, and a profile started at normal depth has to have
no length. Those pin the solvers completely.
"""

import math

import numpy as np
import pytest

from pyCoastal.applications.river import (
    MANNING,
    PIER_SHAPE,
    Channel,
    classify_slope,
    critical_depth,
    flow_distribution,
    friction_slope,
    froude_number,
    gvf_profile,
    normal_depth,
    profile_type,
    specific_energy,
    yarnell_afflux,
)

Q = 250.0
SLOPE = 0.0008


@pytest.fixture
def channel():
    return Channel(width=30.0, side_slope=2.0, roughness="natural_clean")


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def test_a_rectangular_channel_has_no_side_slope():
    rect = Channel(width=20.0, side_slope=0.0)
    assert rect.area(3.0) == pytest.approx(60.0)
    assert rect.top_width(3.0) == pytest.approx(20.0)
    assert rect.perimeter(3.0) == pytest.approx(26.0)


def test_a_trapezoid_widens_with_depth(channel):
    assert channel.top_width(2.0) > channel.top_width(1.0) > channel.width


def test_the_area_of_a_triangle_is_half_base_times_height():
    tri = Channel(width=0.0, side_slope=2.0)
    # Top width at depth y is 4y, so the area is 2 y^2.
    assert tri.area(3.0) == pytest.approx(2.0 * 9.0)
    assert tri.top_width(3.0) == pytest.approx(12.0)


def test_the_hydraulic_radius_is_area_over_perimeter(channel):
    assert channel.hydraulic_radius(2.5) == pytest.approx(
        channel.area(2.5) / channel.perimeter(2.5))


def test_roughness_can_be_a_name_or_a_number():
    assert Channel(roughness="gravel").n == MANNING["gravel"]
    assert Channel(roughness=0.031).n == pytest.approx(0.031)


def test_the_channel_validates_itself():
    with pytest.raises(ValueError):
        Channel(width=-1.0)
    with pytest.raises(ValueError):
        Channel(side_slope=-1.0)
    with pytest.raises(ValueError):
        Channel(width=0.0, side_slope=0.0)
    with pytest.raises(ValueError):
        Channel(roughness=0.0)
    with pytest.raises(ValueError) as excinfo:
        Channel(roughness="glass")
    assert "gravel" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Normal depth
# ---------------------------------------------------------------------------


def test_normal_depth_reproduces_manning(channel):
    """The definition: Q = K sqrt(S0) at the normal depth."""
    yn = normal_depth(channel, Q, SLOPE)
    assert channel.conveyance(yn) * math.sqrt(SLOPE) == pytest.approx(Q, rel=1e-9)


def test_a_steeper_bed_runs_shallower(channel):
    assert (normal_depth(channel, Q, 0.005)
            < normal_depth(channel, Q, 0.0005))


def test_a_rougher_channel_runs_deeper():
    smooth = Channel(width=30.0, side_slope=2.0, roughness="concrete_smooth")
    rough = Channel(width=30.0, side_slope=2.0, roughness="natural_weedy")
    assert normal_depth(rough, Q, SLOPE) > normal_depth(smooth, Q, SLOPE)


def test_more_discharge_runs_deeper(channel):
    assert normal_depth(channel, 500.0, SLOPE) > normal_depth(channel, 100.0, SLOPE)


def test_normal_depth_is_undefined_without_a_falling_bed(channel):
    """Not an edge case: a ponded reach genuinely has no normal depth."""
    for slope in (0.0, -0.001):
        with pytest.raises(ValueError) as excinfo:
            normal_depth(channel, Q, slope)
        assert "uniform flow" in str(excinfo.value).lower()


def test_normal_depth_needs_a_discharge(channel):
    with pytest.raises(ValueError):
        normal_depth(channel, 0.0, SLOPE)


# ---------------------------------------------------------------------------
# Critical depth
# ---------------------------------------------------------------------------


def test_critical_depth_gives_a_froude_number_of_one(channel):
    yc = critical_depth(channel, Q)
    assert froude_number(channel, Q, yc) == pytest.approx(1.0, abs=1e-9)


def test_critical_depth_minimises_specific_energy(channel):
    yc = critical_depth(channel, Q)
    at = specific_energy(channel, Q, yc)
    for factor in (0.8, 0.9, 0.95, 1.05, 1.1, 1.3):
        assert specific_energy(channel, Q, yc * factor) > at


def test_critical_depth_does_not_care_about_slope_or_roughness():
    """It is a property of the section and the discharge alone."""
    smooth = Channel(width=30.0, side_slope=2.0, roughness="concrete_smooth")
    rough = Channel(width=30.0, side_slope=2.0, roughness="natural_weedy")
    assert critical_depth(smooth, Q) == pytest.approx(critical_depth(rough, Q))


def test_the_rectangular_critical_depth_has_a_closed_form():
    """yc = (q^2/g)^(1/3) for a rectangle, which is worth checking against."""
    rect = Channel(width=20.0, side_slope=0.0)
    q = Q / 20.0
    assert critical_depth(rect, Q) == pytest.approx((q**2 / 9.81) ** (1 / 3),
                                                    rel=1e-8)


def test_flow_is_subcritical_above_and_supercritical_below(channel):
    yc = critical_depth(channel, Q)
    assert froude_number(channel, Q, yc * 1.5) < 1.0
    assert froude_number(channel, Q, yc * 0.7) > 1.0


def test_froude_and_energy_need_a_positive_depth(channel):
    with pytest.raises(ValueError):
        froude_number(channel, Q, 0.0)
    with pytest.raises(ValueError):
        specific_energy(channel, Q, 0.0)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def test_a_gentle_bed_is_mild_and_a_steep_one_steep(channel):
    assert classify_slope(channel, Q, 0.0008)["kind"] == "mild"
    assert classify_slope(channel, Q, 0.02)["kind"] == "steep"


def test_flat_and_adverse_beds_have_no_normal_depth(channel):
    for slope, kind in ((0.0, "horizontal"), (-0.001, "adverse")):
        got = classify_slope(channel, Q, slope)
        assert got["kind"] == kind
        assert got["normal"] is None
        assert got["critical"] > 0


def test_the_same_reach_can_change_class_with_discharge(channel):
    """Critical and normal depth move at different rates with Q."""
    kinds = {classify_slope(channel, q, 0.006)["kind"]
             for q in (5.0, 50.0, 500.0, 5000.0)}
    assert len(kinds) > 1


def test_the_mild_profiles_are_named_correctly(channel):
    got = classify_slope(channel, Q, SLOPE)
    yn, yc = got["normal"], got["critical"]
    assert profile_type(yn * 1.5, got) == "M1"
    assert profile_type(0.5 * (yn + yc), got) == "M2"
    assert profile_type(yc * 0.6, got) == "M3"


def test_the_steep_profiles_are_named_correctly(channel):
    got = classify_slope(channel, Q, 0.02)
    yn, yc = got["normal"], got["critical"]
    assert profile_type(yc * 1.5, got) == "S1"
    assert profile_type(0.5 * (yn + yc), got) == "S2"
    assert profile_type(yn * 0.6, got) == "S3"


def test_horizontal_and_adverse_reaches_have_only_zones_two_and_three(channel):
    for slope, letter in ((0.0, "H"), (-0.001, "A")):
        got = classify_slope(channel, Q, slope)
        yc = got["critical"]
        assert profile_type(yc * 1.5, got) == f"{letter}2"
        assert profile_type(yc * 0.6, got) == f"{letter}3"


def test_profile_naming_needs_a_positive_depth(channel):
    got = classify_slope(channel, Q, SLOPE)
    with pytest.raises(ValueError):
        profile_type(0.0, got)


# ---------------------------------------------------------------------------
# Backwater
# ---------------------------------------------------------------------------


def test_a_control_at_normal_depth_has_no_profile(channel):
    """Uniform flow: nothing to integrate."""
    yn = normal_depth(channel, Q, SLOPE)
    got = gvf_profile(channel, Q, SLOPE, control_depth=yn)
    assert got.reach == pytest.approx(0.0)
    assert "uniform" in " ".join(got.notes)


def test_a_bridge_on_a_mild_reach_makes_an_m1(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = gvf_profile(channel, Q, SLOPE, control_depth=yn + 1.2)
    assert got.profile == "M1"
    assert got.reach > 0
    assert got.depth[0] > got.depth[-1]        # falling towards normal


def test_the_profile_approaches_normal_depth_but_never_reaches_it(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = gvf_profile(channel, Q, SLOPE, control_depth=yn + 1.2, approach=0.99)
    assert got.depth[-1] > yn
    assert got.depth[-1] == pytest.approx(yn + 0.01 * 1.2, rel=1e-6)


def test_the_extent_depends_entirely_on_the_convention(channel):
    """An asymptotic curve has no end, so the quoted reach is a choice."""
    yn = normal_depth(channel, Q, SLOPE)
    reaches = [gvf_profile(channel, Q, SLOPE, yn + 1.2, approach=a).reach
               for a in (0.90, 0.95, 0.99, 0.999)]
    assert all(b > a for a, b in zip(reaches, reaches[1:]))
    assert reaches[-1] > 2.0 * reaches[0]
    assert "convention" in " ".join(
        gvf_profile(channel, Q, SLOPE, yn + 1.2).notes)


def test_a_bigger_obstruction_backs_water_up_further(channel):
    yn = normal_depth(channel, Q, SLOPE)
    small = gvf_profile(channel, Q, SLOPE, yn + 0.4).reach
    large = gvf_profile(channel, Q, SLOPE, yn + 2.0).reach
    assert large > small


def test_the_water_surface_rises_upstream(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = gvf_profile(channel, Q, SLOPE, yn + 1.2)
    surface = got.water_surface
    assert surface[-1] > surface[0]
    assert np.all(np.diff(got.bed_level) >= 0)


def test_depths_can_be_interpolated_along_the_reach(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = gvf_profile(channel, Q, SLOPE, yn + 1.2)
    assert got.depth_at(0.0) == pytest.approx(got.depth[0])
    middle = got.depth_at(0.5 * got.reach)
    assert got.depth[-1] < middle < got.depth[0]


def test_a_horizontal_reach_integrates_towards_critical(channel):
    yc = critical_depth(channel, Q)
    got = gvf_profile(channel, Q, 0.0, control_depth=yc * 2.0)
    assert got.profile == "H2"
    assert "No normal depth" in " ".join(got.notes)


def test_the_profile_validates_its_inputs(channel):
    yn = normal_depth(channel, Q, SLOPE)
    with pytest.raises(ValueError):
        gvf_profile(channel, Q, SLOPE, 0.0)
    with pytest.raises(ValueError):
        gvf_profile(channel, Q, SLOPE, yn + 1.0, steps=1)
    with pytest.raises(ValueError):
        gvf_profile(channel, Q, SLOPE, yn + 1.0, approach=1.0)


def test_the_friction_slope_equals_the_bed_slope_at_normal_depth(channel):
    """The definition of uniform flow, from the other direction."""
    yn = normal_depth(channel, Q, SLOPE)
    assert friction_slope(channel, Q, yn) == pytest.approx(SLOPE, rel=1e-9)


# ---------------------------------------------------------------------------
# Afflux
# ---------------------------------------------------------------------------


def test_no_piers_means_no_afflux(channel):
    yn = normal_depth(channel, Q, SLOPE)
    assert yarnell_afflux(channel, Q, yn, 0.0)["afflux"] == pytest.approx(0.0)


def test_afflux_grows_faster_than_the_blockage(channel):
    """The a^4 term: doubling the pier area more than doubles the rise."""
    yn = normal_depth(channel, Q, SLOPE)
    small = yarnell_afflux(channel, Q, yn, 0.2)["afflux"]
    large = yarnell_afflux(channel, Q, yn, 0.4)["afflux"]
    assert large / small > 2.0


def test_a_blunter_pier_causes_more_afflux(channel):
    yn = normal_depth(channel, Q, SLOPE)
    shaped = yarnell_afflux(channel, Q, yn, 0.15, "semicircular_nose")["afflux"]
    square = yarnell_afflux(channel, Q, yn, 0.15, "square_nose")["afflux"]
    assert square > shaped
    assert PIER_SHAPE["square_nose"] > PIER_SHAPE["semicircular_nose"]


def test_the_upstream_depth_is_the_downstream_plus_the_afflux(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = yarnell_afflux(channel, Q, yn, 0.2)
    assert got["upstream_depth"] == pytest.approx(yn + got["afflux"])


def test_outside_yarnells_range_it_says_so(channel):
    yn = normal_depth(channel, Q, SLOPE)
    assert yarnell_afflux(channel, Q, yn, 0.2)["in_range"] is True
    heavy = yarnell_afflux(channel, Q, yn, 0.7)
    assert heavy["in_range"] is False
    assert "momentum" in heavy["note"]


def test_afflux_validates_its_inputs(channel):
    yn = normal_depth(channel, Q, SLOPE)
    with pytest.raises(ValueError):
        yarnell_afflux(channel, Q, yn, 1.0)
    with pytest.raises(ValueError):
        yarnell_afflux(channel, Q, yn, -0.1)
    with pytest.raises(ValueError):
        yarnell_afflux(channel, Q, yn, 0.2, shape="pointy")


# ---------------------------------------------------------------------------
# Flow distribution
# ---------------------------------------------------------------------------


def test_a_bridge_spanning_everything_carries_everything(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = flow_distribution(channel, yn, SLOPE)
    assert got["main_fraction"] == pytest.approx(1.0)


def test_the_shares_add_to_one(channel):
    yn = normal_depth(channel, Q, SLOPE)
    plain = Channel(width=120.0, side_slope=3.0, roughness="floodplain_trees")
    got = flow_distribution(channel, yn, SLOPE, [(plain, 1.2), (plain, 1.0)])
    assert sum(got["shares"].values()) == pytest.approx(1.0)
    assert len(got["shares"]) == 3


def test_a_rough_floodplain_carries_far_less_than_its_width(channel):
    """The reason this is computed rather than guessed."""
    yn = normal_depth(channel, Q, SLOPE)
    plain = Channel(width=120.0, side_slope=3.0, roughness="floodplain_trees")
    got = flow_distribution(channel, yn, SLOPE, [(plain, 1.2)])
    width_share = channel.top_width(yn) / (channel.top_width(yn)
                                           + plain.top_width(1.2))
    assert got["main_fraction"] > 2.0 * width_share


def test_a_smoother_floodplain_takes_more(channel):
    yn = normal_depth(channel, Q, SLOPE)
    trees = Channel(width=120.0, side_slope=3.0, roughness="floodplain_trees")
    grass = Channel(width=120.0, side_slope=3.0, roughness="floodplain_pasture")
    wooded = flow_distribution(channel, yn, SLOPE, [(trees, 1.2)])
    mown = flow_distribution(channel, yn, SLOPE, [(grass, 1.2)])
    assert mown["main_fraction"] < wooded["main_fraction"]


def test_the_total_discharge_follows_from_the_conveyance(channel):
    yn = normal_depth(channel, Q, SLOPE)
    got = flow_distribution(channel, yn, SLOPE)
    assert got["discharge"] == pytest.approx(Q, rel=1e-9)


def test_distribution_validates_its_inputs(channel):
    with pytest.raises(ValueError):
        flow_distribution(channel, 0.0, SLOPE)
    with pytest.raises(ValueError):
        flow_distribution(channel, 2.0, 0.0)
