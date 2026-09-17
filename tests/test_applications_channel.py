"""Navigation channel design: vessel, squat, clearance, width and depth."""

import math

import numpy as np
import pytest

from pyCoastal.applications.channel import (
    BANK_CLEARANCE,
    KNOT,
    MANOEUVRING_LANE,
    PASSING_DISTANCE,
    WIDTH_COMPONENTS,
    ChannelDesign,
    Vessel,
    channel_width,
    design_channel,
    squat_barrass,
    squat_icorels,
    turning_basin_diameter,
    underkeel_clearance,
    wave_response_allowance,
)


@pytest.fixture
def ship():
    return Vessel(name="Test ship", length=300.0, beam=45.0, draught=14.0,
                  block_coefficient=0.70)


@pytest.fixture
def channel(ship):
    return design_channel(ship, speed=8.0, design_water_level=1.2, Hs=1.5,
                          Tp=9.0, existing_bed=-11.0)


# ---------------------------------------------------------------------------
# Vessel
# ---------------------------------------------------------------------------


def test_displacement_follows_the_block_coefficient(ship):
    expected = 0.70 * ship.length_pp * 45.0 * 14.0
    assert ship.displaced_volume == pytest.approx(expected)
    assert ship.displacement == pytest.approx(expected * 1.025)


def test_length_between_perpendiculars_defaults_below_length_overall(ship):
    assert ship.length_pp == pytest.approx(0.96 * 300.0)


def test_vessel_rejects_impossible_dimensions():
    for bad in (dict(length=0.0), dict(beam=-1.0), dict(draught=0.0)):
        kwargs = dict(name="x", length=100.0, beam=20.0, draught=8.0)
        kwargs.update(bad)
        with pytest.raises(ValueError):
            Vessel(**kwargs)


def test_vessel_rejects_an_impossible_block_coefficient():
    with pytest.raises(ValueError):
        Vessel(name="x", length=100.0, beam=20.0, draught=8.0,
               block_coefficient=1.4)


# ---------------------------------------------------------------------------
# Squat
# ---------------------------------------------------------------------------


def test_squat_grows_faster_than_linearly_with_speed(ship):
    squats = [squat_icorels(ship, v, 17.0)["squat"] for v in (4, 6, 8, 10)]
    ratios = [b / a for a, b in zip(squats, squats[1:])]
    assert all(r > 1.0 for r in ratios)
    # Doubling the speed from 4 to 8 knots more than quadruples the squat,
    # because of the 1 / sqrt(1 - Fnh^2) term.
    assert squats[2] / squats[0] > 4.0


def test_squat_grows_as_the_water_shallows(ship):
    squats = [squat_icorels(ship, 8.0, h)["squat"] for h in (40, 25, 16, 12)]
    assert all(b > a for a, b in zip(squats, squats[1:]))
    assert squats[-1] > 3.0 * squats[0]


def test_squat_is_zero_at_rest(ship):
    assert squat_icorels(ship, 0.0, 20.0)["squat"] == pytest.approx(0.0)


def test_froude_number_uses_the_right_unit_conversion(ship):
    result = squat_icorels(ship, 10.0, 20.0)
    assert result["speed_ms"] == pytest.approx(10.0 * KNOT)
    assert result["froude"] == pytest.approx(
        10.0 * KNOT / math.sqrt(9.81 * 20.0)
    )


def test_squat_flags_speeds_beyond_the_formula(ship):
    assert squat_icorels(ship, 8.0, 20.0)["beyond_range"] is False
    fast = squat_icorels(ship, 14.0, 8.0)
    assert 0.7 <= fast["froude"] < 0.99
    assert fast["beyond_range"] is True


def test_squat_refuses_the_critical_speed(ship):
    with pytest.raises(ValueError):
        squat_icorels(ship, 40.0, 4.0)


def test_squat_validates_its_inputs(ship):
    with pytest.raises(ValueError):
        squat_icorels(ship, -1.0, 20.0)
    with pytest.raises(ValueError):
        squat_icorels(ship, 8.0, 0.0)


def test_barrass_doubles_in_a_confined_channel(ship):
    open_water = squat_barrass(ship, 8.0, 18.0, confined=False)["squat"]
    confined = squat_barrass(ship, 8.0, 18.0, confined=True)["squat"]
    assert confined == pytest.approx(2.0 * open_water)


def test_barrass_matches_its_closed_form(ship):
    assert squat_barrass(ship, 10.0, 18.0)["squat"] == pytest.approx(
        0.70 * 100.0 / 100.0
    )


def test_the_two_squat_formulae_stay_within_a_factor_of_two(ship):
    """Different derivations, but they must not disagree wildly."""
    for speed in (5.0, 8.0, 11.0):
        a = squat_icorels(ship, speed, 17.5)["squat"]
        b = squat_barrass(ship, speed, 17.5)["squat"]
        assert 0.5 < a / b < 2.0


# ---------------------------------------------------------------------------
# Wave response
# ---------------------------------------------------------------------------


def test_wave_allowance_is_the_stated_fraction():
    assert wave_response_allowance(2.0, 0.5)["allowance"] == pytest.approx(1.0)


def test_wave_allowance_reports_resonance_risk(ship):
    # A 14 s wave is about 306 m long, close to the 300 m vessel.
    near = wave_response_allowance(2.0, 0.5, period=14.0, vessel=ship)
    assert near["near_resonant"] is True
    far = wave_response_allowance(2.0, 0.5, period=5.0, vessel=ship)
    assert far["near_resonant"] is False


def test_wave_allowance_rejects_an_indefensible_factor():
    with pytest.raises(ValueError):
        wave_response_allowance(2.0, factor=3.0)


def test_wave_allowance_rejects_a_negative_height():
    with pytest.raises(ValueError):
        wave_response_allowance(-1.0)


# ---------------------------------------------------------------------------
# Underkeel clearance
# ---------------------------------------------------------------------------


def test_clearance_sums_its_parts(ship):
    result = underkeel_clearance(ship, squat=0.4, wave_allowance=0.8)
    assert result["gross"] == pytest.approx(sum(result["components"].values()))
    assert result["required_depth"] == pytest.approx(14.0 + result["gross"])


def test_clearance_rejects_a_negative_allowance(ship):
    with pytest.raises(ValueError):
        underkeel_clearance(ship, squat=0.4, wave_allowance=-0.1)


def test_clearance_components_are_all_reported(ship):
    result = underkeel_clearance(ship, 0.4, 0.8)
    for name in ("squat", "wave response", "net clearance",
                 "dredging tolerance", "survey tolerance", "siltation"):
        assert name in result["components"]


# ---------------------------------------------------------------------------
# Width
# ---------------------------------------------------------------------------


def test_width_is_built_from_beams(ship):
    result = channel_width(ship, manoeuvrability="moderate", section="outer")
    assert result["width"] == pytest.approx(
        result["width_in_beams"] * ship.beam
    )


def test_width_basic_lane_matches_the_table(ship):
    result = channel_width(ship, manoeuvrability="poor",
                           conditions={k: min(v, key=lambda x: v[x][0])
                                       for k, v in WIDTH_COMPONENTS.items()})
    assert result["components"]["basic manoeuvring lane"] == pytest.approx(
        MANOEUVRING_LANE["poor"] * ship.beam
    )


def test_two_way_channel_is_wider_than_one_way(ship):
    one = channel_width(ship, two_way=False)["width"]
    two = channel_width(ship, two_way=True)["width"]
    assert two > 2.0 * one - 2.0 * BANK_CLEARANCE["sloping_channel_edges"]["moderate"] * ship.beam


def test_two_way_adds_a_passing_distance(ship):
    result = channel_width(ship, two_way=True, speed_class="fast")
    assert result["components"]["passing distance"] == pytest.approx(
        PASSING_DISTANCE["fast"] * ship.beam
    )
    assert result["lanes"] == 2


def test_worse_conditions_give_a_wider_channel(ship):
    calm = channel_width(ship, conditions={"crosswind": "mild",
                                           "crosscurrent": "negligible"})
    rough = channel_width(ship, conditions={"crosswind": "severe",
                                            "crosscurrent": "strong"})
    assert rough["width"] > calm["width"]


def test_unspecified_conditions_are_reported_as_assumed(ship):
    result = channel_width(ship, conditions={"crosswind": "severe"})
    assert result["assumed"]
    assert not any(a.startswith("crosswind") for a in result["assumed"])
    assert any(a.startswith("crosscurrent") for a in result["assumed"])


def test_width_rejects_unknown_classes(ship):
    with pytest.raises(ValueError):
        channel_width(ship, manoeuvrability="excellent")
    with pytest.raises(ValueError):
        channel_width(ship, section="middle")
    with pytest.raises(ValueError):
        channel_width(ship, conditions={"crosswind": "hurricane"})
    with pytest.raises(ValueError):
        channel_width(ship, speed_class="supersonic")
    with pytest.raises(ValueError):
        channel_width(ship, bank="marshmallow")


def test_width_tables_are_self_consistent():
    """Every class must give an (outer, inner) pair of non-negative widths."""
    for name, classes in WIDTH_COMPONENTS.items():
        for key, value in classes.items():
            assert len(value) == 2, f"{name}/{key}"
            assert all(v >= 0 for v in value), f"{name}/{key}"


# ---------------------------------------------------------------------------
# The whole design
# ---------------------------------------------------------------------------


def test_design_depth_is_self_consistent(channel):
    """The squat used must be the squat at the depth that was solved for."""
    recomputed = squat_icorels(channel.vessel, channel.speed,
                               channel.required_depth)
    assert recomputed["squat"] == pytest.approx(channel.squat["squat"], rel=1e-3)


def test_design_dredge_level_follows_the_water_level(channel):
    assert channel.dredge_level == pytest.approx(
        channel.design_water_level - channel.required_depth
    )


def test_design_depth_exceeds_the_draught(channel):
    assert channel.required_depth > channel.vessel.draught


def test_faster_vessel_needs_a_deeper_channel(ship):
    slow = design_channel(ship, 5.0, 1.2, Hs=1.5)
    fast = design_channel(ship, 11.0, 1.2, Hs=1.5)
    assert fast.required_depth > slow.required_depth


def test_bigger_waves_need_a_deeper_channel(ship):
    calm = design_channel(ship, 8.0, 1.2, Hs=0.5)
    rough = design_channel(ship, 8.0, 1.2, Hs=3.0)
    assert (rough.required_depth - calm.required_depth
            == pytest.approx(0.5 * 2.5, abs=0.05))


def test_top_width_opens_out_with_the_side_slopes(channel):
    rise = channel.existing_bed - channel.dredge_level
    assert channel.top_width == pytest.approx(
        channel.width + 2.0 * channel.side_slope * rise
    )


def test_top_width_equals_bed_width_without_an_existing_bed(ship):
    design = design_channel(ship, 8.0, 1.2, Hs=1.5, existing_bed=None)
    assert design.top_width == pytest.approx(design.width)


def test_dredge_volume_matches_the_trapezoid(channel):
    rise = channel.existing_bed - channel.dredge_level
    area = channel.width * rise + channel.side_slope * rise**2
    assert channel.dredge_volume(500.0) == pytest.approx(area * 500.0)


def test_dredge_volume_needs_an_existing_bed(ship):
    design = design_channel(ship, 8.0, 1.2, Hs=1.5)
    with pytest.raises(RuntimeError):
        design.dredge_volume(1000.0)


def test_design_warns_when_the_bed_is_already_deep_enough(ship):
    design = design_channel(ship, 8.0, 1.2, Hs=1.5, existing_bed=-40.0)
    assert any("already below" in w for w in design.warnings)


def test_design_starts_subcritical_even_for_a_fast_shallow_vessel():
    """The first iterate must not trip the critical-speed guard."""
    shallow = Vessel(name="Fast ferry", length=90.0, beam=16.0, draught=3.0,
                     block_coefficient=0.55)
    design = design_channel(shallow, speed=10.0, design_water_level=0.0,
                            Hs=0.5, net_clearance=0.3)
    assert design.required_depth > shallow.draught
    assert design.squat["froude"] < 0.95


def test_design_refuses_a_speed_the_channel_cannot_carry():
    """A shallow-draught vessel driven hard runs into her own critical speed."""
    shallow = Vessel(name="Fast ferry", length=90.0, beam=16.0, draught=3.0,
                     block_coefficient=0.55)
    with pytest.raises(ValueError) as excinfo:
        design_channel(shallow, speed=16.0, design_water_level=0.0, Hs=0.5,
                       net_clearance=0.3)
    message = str(excinfo.value)
    assert "critical speed" in message
    assert "knots" in message


def test_design_warns_at_an_unusable_speed(ship):
    shallow = Vessel(name="Shallow draught", length=90.0, beam=16.0,
                     draught=3.0, block_coefficient=0.7)
    design = design_channel(shallow, speed=10.0, design_water_level=0.0,
                            Hs=0.5, net_clearance=0.3, siltation_allowance=0.0,
                            dredging_tolerance=0.1, survey_tolerance=0.1,
                            water_level_allowance=0.1)
    assert any("Froude" in w for w in design.warnings)


def test_design_warns_near_wave_resonance(ship):
    design = design_channel(ship, 8.0, 1.2, Hs=2.0, Tp=14.0)
    assert any("worst case for vertical motion" in w for w in design.warnings)


def test_design_rejects_a_negative_speed(ship):
    with pytest.raises(ValueError):
        design_channel(ship, -2.0, 1.2)


def test_summary_covers_both_chains(channel):
    text = channel.summary()
    for phrase in ("Depth chain", "static draught", "required depth",
                   "Dredge level", "Channel width", "Volume"):
        assert phrase in text


def test_turning_basin_scales_with_vessel_length(ship):
    assisted = turning_basin_diameter(ship, assisted=True)
    unassisted = turning_basin_diameter(ship, assisted=False)
    current = turning_basin_diameter(ship, assisted=True, current=True)
    assert assisted["diameter"] == pytest.approx(1.5 * ship.length)
    assert unassisted["diameter"] > assisted["diameter"]
    assert current["diameter"] > assisted["diameter"]
