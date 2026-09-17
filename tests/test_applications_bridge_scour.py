"""Contraction and abutment scour: the other two thirds of HEC-18.

Pier scour is covered in test_applications_scour.py. These are the two
components that come from the waterway rather than from the structure, and
the arithmetic that combines all three without double counting.

Several of these tests exist because of specific traps: a live-bed relation
that does not depend on velocity, a safety factor that can be most of the
answer, and an abutment equation that returns a hole deeper than the river
if it is handed the wrong depth.
"""

import math

import numpy as np
import pytest

from pyCoastal.applications.scour import (
    ABUTMENT_SHAPE,
    BridgeOpening,
    EstuaryConditions,
    Pier,
    PierBase,
    abutment_scour,
    abutment_shape_factor,
    bridge_scour_state,
    contraction_scour,
    critical_velocity,
    design_bridge_scour,
    transport_exponent,
)
from pyCoastal.applications.sediment import Sediment


@pytest.fixture
def opening():
    return BridgeOpening(approach_width=140.0, opening_width=80.0,
                         pier_blockage=5.0, abutment_length=22.0,
                         abutment_shape="spill_through", slope=4e-4)


@pytest.fixture
def estuary():
    return EstuaryConditions(mean_depth=9.0, tidal_amplitude=2.2,
                             tidal_current=1.1, river_current=0.4,
                             Hs=1.2, Tp=5.5, bed="medium_sand",
                             current_phase=75.0)


@pytest.fixture
def pier():
    return Pier(diameter=2.5)


# ---------------------------------------------------------------------------
# The opening
# ---------------------------------------------------------------------------


def test_piers_come_off_the_opening_width(opening):
    assert opening.net_opening == pytest.approx(75.0)
    assert opening.contraction_ratio == pytest.approx(140.0 / 75.0)
    assert opening.contracted is True


def test_a_full_width_crossing_is_not_contracted():
    got = BridgeOpening(approach_width=100.0, opening_width=100.0)
    assert got.contraction_ratio == pytest.approx(1.0)
    assert got.contracted is False


def test_the_opening_validates_itself():
    with pytest.raises(ValueError):
        BridgeOpening(approach_width=0.0)
    with pytest.raises(ValueError):
        BridgeOpening(opening_width=0.0)
    with pytest.raises(ValueError):
        BridgeOpening(opening_width=10.0, pier_blockage=10.0)
    with pytest.raises(ValueError):
        BridgeOpening(abutment_skew=0.0)
    with pytest.raises(ValueError):
        BridgeOpening(flow_fraction=1.5)
    with pytest.raises(ValueError):
        BridgeOpening(abutment_depth_fraction=0.0)
    with pytest.raises(ValueError):
        BridgeOpening(abutment_shape="castellated")


# ---------------------------------------------------------------------------
# Critical velocity and the mode of transport
# ---------------------------------------------------------------------------


def test_critical_velocity_rises_with_grain_size():
    speeds = [critical_velocity(Sediment("t", d50=d), 3.0)
              for d in (1e-4, 3e-4, 1e-3, 1e-2)]
    assert all(b > a for a, b in zip(speeds, speeds[1:]))


def test_critical_velocity_rises_slowly_with_depth():
    """The sixth root: four times the depth is a quarter more velocity."""
    shallow = critical_velocity("medium_sand", 2.0)
    deep = critical_velocity("medium_sand", 32.0)
    assert deep / shallow == pytest.approx(2.0 ** (4.0 / 6.0), rel=1e-9)


def test_critical_velocity_is_plausible_for_sand():
    """Fine sand in a few metres moves somewhere near half a metre a second."""
    assert 0.3 < critical_velocity("fine_sand", 3.0) < 0.8


def test_critical_velocity_refuses_a_cohesive_bed():
    with pytest.raises(ValueError):
        critical_velocity("soft_clay", 3.0)


def test_the_transport_exponent_takes_its_three_values():
    seen = set()
    for slope in (1e-6, 1e-4, 5e-3, 5e-2):
        seen.add(transport_exponent("fine_sand", 4.0, slope)["k1"])
    assert seen.issubset({0.59, 0.64, 0.69})
    assert len(seen) >= 2


def test_the_transport_exponent_rises_with_shear():
    calm = transport_exponent("fine_sand", 4.0, 1e-6)
    brisk = transport_exponent("fine_sand", 4.0, 5e-2)
    assert brisk["ratio"] > calm["ratio"]
    assert brisk["k1"] >= calm["k1"]
    assert "suspended" in brisk["mode"]


# ---------------------------------------------------------------------------
# Contraction scour
# ---------------------------------------------------------------------------


def test_no_contraction_gives_no_scour():
    """The identity the whole relation has to satisfy."""
    flat = BridgeOpening(approach_width=100.0, opening_width=100.0)
    got = contraction_scour(flat, 4.0, 1.2, "medium_sand")
    assert got["y2"] == pytest.approx(4.0)
    assert got["depth"] == pytest.approx(0.0, abs=1e-12)


def test_scour_grows_with_the_squeeze():
    depths = []
    for w2 in (100.0, 80.0, 60.0, 40.0):
        got = contraction_scour(
            BridgeOpening(approach_width=100.0, opening_width=w2),
            4.0, 1.2, "medium_sand")
        depths.append(got["depth"])
    assert all(b > a for a, b in zip(depths, depths[1:]))


def test_live_bed_scour_does_not_depend_on_velocity():
    """Laursen's relation is a sediment balance, not a velocity one.

    Above the threshold the opening is fed from upstream, and it scours
    only until it can pass what arrives. Faster water brings more sediment
    as well as carrying more, and the two cancel. This surprises people,
    so it is pinned here.
    """
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    depths = [contraction_scour(opening, 4.0, v, "medium_sand")["depth"]
              for v in (0.8, 1.5, 3.0)]
    assert all(d["regime"] == "live" for d in
               [contraction_scour(opening, 4.0, v, "medium_sand")
                for v in (0.8, 1.5, 3.0)])
    assert depths[0] == pytest.approx(depths[1])
    assert depths[1] == pytest.approx(depths[2])


def test_the_regime_switches_at_the_critical_velocity():
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    Vc = critical_velocity("medium_sand", 4.0)
    assert contraction_scour(opening, 4.0, 0.9 * Vc, "medium_sand")["regime"] == "clear"
    assert contraction_scour(opening, 4.0, 1.1 * Vc, "medium_sand")["regime"] == "live"


def test_clear_water_scour_grows_with_velocity():
    """Unlike live bed: with nothing arriving, faster water digs deeper."""
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    depths = [contraction_scour(opening, 4.0, v, "coarse_sand",
                                regime="clear")["depth"]
              for v in (0.3, 0.5, 0.8)]
    assert all(b > a for a, b in zip(depths, depths[1:]))


def test_clear_water_is_the_deeper_mode_at_the_same_flow():
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    live = contraction_scour(opening, 4.0, 1.2, "medium_sand", regime="live")
    clear = contraction_scour(opening, 4.0, 1.2, "medium_sand", regime="clear")
    assert clear["depth"] > live["depth"]


def test_a_coarser_bed_scours_less_in_clear_water():
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    fine = contraction_scour(opening, 4.0, 0.5, "fine_sand", regime="clear")
    coarse = contraction_scour(opening, 4.0, 0.5, "coarse_sand", regime="clear")
    assert coarse["depth"] < fine["depth"]


def test_still_water_scours_nothing():
    opening = BridgeOpening(approach_width=100.0, opening_width=60.0)
    assert contraction_scour(opening, 4.0, 0.0, "medium_sand")["depth"] == 0.0


def test_less_flow_through_the_opening_means_less_scour():
    tight = BridgeOpening(approach_width=100.0, opening_width=60.0,
                          flow_fraction=1.0)
    leaky = BridgeOpening(approach_width=100.0, opening_width=60.0,
                          flow_fraction=0.6)
    assert (contraction_scour(leaky, 4.0, 1.2, "medium_sand")["depth"]
            < contraction_scour(tight, 4.0, 1.2, "medium_sand")["depth"])


def test_an_already_scoured_opening_needs_less(opening):
    level = contraction_scour(opening, 5.0, 1.2, "medium_sand")
    dredged = contraction_scour(opening, 5.0, 1.2, "medium_sand",
                                opening_depth=8.0)
    assert dredged["depth"] < level["depth"]
    assert dredged["y2"] == pytest.approx(level["y2"])


def test_contraction_scour_validates_itself(opening):
    with pytest.raises(ValueError):
        contraction_scour(opening, 0.0, 1.0, "medium_sand")
    with pytest.raises(ValueError):
        contraction_scour(opening, 4.0, 1.0, "soft_clay")
    with pytest.raises(ValueError):
        contraction_scour(opening, 4.0, 1.0, "medium_sand", regime="mixed")
    with pytest.raises(ValueError):
        contraction_scour(opening, 4.0, 1.0, "medium_sand", opening_depth=0.0)


# ---------------------------------------------------------------------------
# Abutment scour
# ---------------------------------------------------------------------------


def test_shape_factors_match_hec18():
    assert abutment_shape_factor("vertical") == 1.00
    assert abutment_shape_factor("wing_wall") == 0.82
    assert abutment_shape_factor("spill_through") == 0.55
    assert set(ABUTMENT_SHAPE) == {"vertical", "wing_wall", "spill_through"}


def test_an_unknown_abutment_shape_names_the_options():
    with pytest.raises(ValueError) as excinfo:
        abutment_shape_factor("battered")
    assert "spill_through" in str(excinfo.value)


def test_a_blunter_abutment_scours_more(opening):
    depths = []
    for shape in ("spill_through", "wing_wall", "vertical"):
        got = abutment_scour(
            BridgeOpening(abutment_length=22.0, abutment_shape=shape),
            6.0, 1.2)
        depths.append(got["depth"])
    assert all(b > a for a, b in zip(depths, depths[1:]))


def test_no_embankment_means_no_abutment_scour():
    got = abutment_scour(BridgeOpening(abutment_length=0.0), 6.0, 1.2)
    assert got["depth"] == 0.0
    assert got["method"] == "none"


def test_the_method_switches_on_relative_length():
    """Froehlich for a short abutment, HIRE past L/y of 25."""
    short = abutment_scour(BridgeOpening(abutment_length=10.0), 6.0, 1.2)
    long = abutment_scour(BridgeOpening(abutment_length=200.0), 6.0, 1.2)
    assert short["method"] == "froehlich"
    assert long["method"] == "hire"
    assert short["relative_length"] < 25.0 < long["relative_length"]


def test_either_method_can_be_forced():
    got = abutment_scour(BridgeOpening(abutment_length=10.0), 6.0, 1.2,
                         method="hire")
    assert got["method"] == "hire"
    with pytest.raises(ValueError):
        abutment_scour(BridgeOpening(abutment_length=10.0), 6.0, 1.2,
                       method="nchrp")


def test_froehlich_carries_its_safety_factor_visibly():
    """The +1 is a factor of safety, not physics, and is often most of it."""
    got = abutment_scour(BridgeOpening(abutment_length=22.0), 10.0, 0.8)
    assert got["method"] == "froehlich"
    assert got["safety_margin"] == pytest.approx(got["abutment_depth"])
    assert got["safety_margin"] > 0.3 * got["depth"]


def test_hire_has_no_safety_term():
    got = abutment_scour(BridgeOpening(abutment_length=300.0), 6.0, 1.2)
    assert got["method"] == "hire"
    assert got["safety_margin"] == 0.0


def test_the_abutment_stands_on_the_bank_not_in_the_channel():
    """Froehlich's ya is the depth at the embankment.

    Handing it the mid-channel depth is how the equation ends up promising
    a hole deeper than the river, because it carries a `+ ya` term.
    """
    shallow = BridgeOpening(abutment_length=22.0, abutment_depth_fraction=0.4)
    full = BridgeOpening(abutment_length=22.0, abutment_depth_fraction=1.0)
    channel = 11.0
    assert (abutment_scour(shallow, channel, 1.2)["abutment_depth"]
            == pytest.approx(0.4 * channel))
    assert (abutment_scour(shallow, channel, 1.2)["depth"]
            < abutment_scour(full, channel, 1.2)["depth"])


def test_an_explicit_abutment_depth_wins():
    got = abutment_scour(BridgeOpening(abutment_length=22.0), 11.0, 1.2,
                         abutment_depth=3.0)
    assert got["abutment_depth"] == pytest.approx(3.0)


def test_skew_pointing_upstream_scours_more():
    square = abutment_scour(BridgeOpening(abutment_length=22.0,
                                          abutment_skew=90.0), 6.0, 1.2)
    upstream = abutment_scour(BridgeOpening(abutment_length=22.0,
                                            abutment_skew=135.0), 6.0, 1.2)
    assert upstream["depth"] > square["depth"]


def test_abutment_scour_validates_itself():
    with pytest.raises(ValueError):
        abutment_scour(BridgeOpening(abutment_length=22.0), 0.0, 1.2)
    with pytest.raises(ValueError):
        abutment_scour(BridgeOpening(abutment_length=22.0), 6.0, 1.2,
                       abutment_depth=0.0)


# ---------------------------------------------------------------------------
# Putting the three together
# ---------------------------------------------------------------------------


def test_local_scour_uses_the_contracted_flow_not_the_approach(opening, pier):
    """The contraction accelerates and deepens the flow the pier stands in.

    Sizing a pier on approach conditions is the usual way it gets
    understated, so the state carries both and they must differ.
    """
    got = bridge_scour_state(opening, 6.0, 1.0, "medium_sand", pier=pier)
    assert got["opening_velocity"] > got["approach_velocity"]
    assert got["opening_depth"] > got["approach_depth"]


def test_the_totals_are_per_location_not_summed(opening, pier):
    got = bridge_scour_state(opening, 6.0, 1.0, "medium_sand", pier=pier)
    con = got["contraction"]["depth"]
    assert got["total_at_pier"] == pytest.approx(con + got["pier"]["depth"])
    assert got["total_at_abutment"] == pytest.approx(
        con + got["abutment"]["depth"])
    # Never all three at one point.
    assert got["total"] < con + got["pier"]["depth"] + got["abutment"]["depth"]


def test_a_crossing_with_no_pier_still_works(opening):
    got = bridge_scour_state(opening, 6.0, 1.0, "medium_sand")
    assert got["pier"] is None
    assert got["total_at_pier"] == pytest.approx(got["contraction"]["depth"])


def test_the_governing_location_is_the_deeper_one(opening, pier):
    got = bridge_scour_state(opening, 6.0, 1.0, "medium_sand", pier=pier)
    if got["total_at_abutment"] > got["total_at_pier"]:
        assert got["governing_location"] == "abutment"
    else:
        assert got["governing_location"] == "pier"


# ---------------------------------------------------------------------------
# The design sweep
# ---------------------------------------------------------------------------


def test_the_design_sweeps_the_cycle(opening, estuary, pier):
    got = design_bridge_scour(opening, estuary, pier, samples=37)
    assert len(got.states) == 37
    assert got.phases()[-1] == pytest.approx(360.0)


def test_each_component_is_enveloped_in_its_own_right(opening, estuary, pier):
    """They do not peak together, so each needs its own maximum."""
    got = design_bridge_scour(opening, estuary, pier)
    assert got.contraction == pytest.approx(got.component("contraction").max())
    assert got.abutment == pytest.approx(got.component("abutment").max())
    assert got.pier_local == pytest.approx(got.component("pier").max())


def test_the_component_envelopes_are_not_all_at_one_phase(opening, estuary,
                                                          pier):
    got = design_bridge_scour(opening, estuary, pier)
    phases = got.phases()
    peaks = {c: phases[got.component(c).argmax()]
             for c in ("contraction", "pier", "abutment")}
    assert len(set(peaks.values())) > 1


def test_an_unknown_component_names_the_options(opening, estuary, pier):
    got = design_bridge_scour(opening, estuary, pier, samples=13)
    with pytest.raises(ValueError) as excinfo:
        got.component("degradation")
    assert "contraction" in str(excinfo.value)


def test_the_total_is_the_worse_of_the_two_locations(opening, estuary, pier):
    got = design_bridge_scour(opening, estuary, pier)
    assert got.total == max(got.total_at_pier, got.total_at_abutment)
    assert got.governing_location in ("pier", "abutment")


def test_a_tighter_opening_scours_more(estuary, pier):
    def run(width):
        return design_bridge_scour(
            BridgeOpening(approach_width=140.0, opening_width=width,
                          abutment_length=22.0),
            estuary, pier, samples=25).contraction

    assert run(50.0) > run(90.0) > run(135.0)


def test_a_crossing_in_range_is_not_warned_about(estuary, pier):
    """A wide opening in deep water should not trip the out-of-range note."""
    got = design_bridge_scour(
        BridgeOpening(approach_width=140.0, opening_width=138.0,
                      abutment_length=4.0, abutment_depth_fraction=0.25),
        estuary, pier, samples=25)
    assert "pushed past where they were fitted" not in " ".join(got.notes)


def test_an_impossible_hole_is_flagged(estuary, pier):
    """A hole deeper than the water is a signal, not a foundation level."""
    got = design_bridge_scour(
        BridgeOpening(approach_width=400.0, opening_width=40.0,
                      abutment_length=120.0, abutment_shape="vertical",
                      abutment_depth_fraction=1.0),
        estuary, pier, samples=25)
    joined = " ".join(got.notes)
    assert "pushed past where they were fitted" in joined


def test_the_notes_explain_the_regime(opening, estuary, pier):
    got = design_bridge_scour(opening, estuary, pier, samples=25)
    joined = " ".join(got.notes)
    assert ("Live-bed contraction scour" in joined
            or "Clear-water contraction scour" in joined)
    assert "not added together" in joined


def test_the_design_needs_enough_phases(opening, estuary):
    with pytest.raises(ValueError):
        design_bridge_scour(opening, estuary, samples=2)


def test_the_design_sizes_protection(opening, estuary, pier):
    got = design_bridge_scour(opening, estuary, pier, samples=25)
    assert got.protection["d50"] > 0
    assert got.protection["extent"] > 0
