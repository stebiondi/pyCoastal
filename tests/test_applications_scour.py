"""Scour at a pier in combined waves, tide and river current.

The combined relation is only trustworthy because of its limits, so those
are pinned exactly: zero current must reproduce the waves-only relation of
Sumer, Fredsoe and Christiansen (1992) to floating-point, and pure current
must tend to the steady-current value of 1.3.

The rest is the machinery around it, and most of these tests exist because
the machinery is where the traps are: a base that changes the answer only
once the scour reaches it, a skew that reverses with the tide, and a
formula that reads as nonsense in the current-dominated corner.
"""

import math

import numpy as np
import pytest

from pyCoastal.applications.scour import (
    M2_PERIOD,
    EstuaryConditions,
    Pier,
    PierBase,
    alignment_factor,
    current_shields,
    depth_limitation,
    design_pier_scour,
    equilibrium_scour,
    equivalent_diameter,
    keulegan_carpenter,
    riprap_size,
    scour_development,
    scour_protection,
    scour_ratio_combined,
    scour_time_scale,
    shape_factor,
    tidal_state,
    velocity_ratio,
)


@pytest.fixture
def pier():
    return Pier(diameter=2.5, shape="circular")


@pytest.fixture
def base():
    return PierBase(width=7.0, length=12.0, height=2.5, top_level=-1.5,
                    skew=20.0)


@pytest.fixture
def estuary():
    return EstuaryConditions(mean_depth=9.0, tidal_amplitude=2.2,
                             tidal_current=1.1, river_current=0.4,
                             Hs=1.2, Tp=5.5, bed="medium_sand",
                             current_phase=75.0)


# ---------------------------------------------------------------------------
# The combined relation, at its limits
# ---------------------------------------------------------------------------


def test_zero_current_reproduces_the_waves_only_relation():
    """Sumer, Fredsoe and Christiansen (1992), exactly."""
    for KC in (7.0, 10.0, 20.0, 50.0, 100.0):
        expected = 1.3 * (1.0 - math.exp(-0.03 * (KC - 6.0)))
        assert scour_ratio_combined(KC, 0.0)["ratio"] == pytest.approx(
            expected, rel=1e-12)


def test_the_waves_only_threshold_sits_at_KC_six():
    """No horseshoe vortex below KC = 6, so no scour."""
    assert scour_ratio_combined(5.9, 0.0)["ratio"] == 0.0
    assert scour_ratio_combined(6.0, 0.0)["ratio"] == 0.0
    assert scour_ratio_combined(6.1, 0.0)["ratio"] > 0.0
    assert scour_ratio_combined(4.0, 0.0)["below_threshold"] is True


def test_the_coefficients_take_their_published_values_at_the_limits():
    still = scour_ratio_combined(10.0, 0.0)
    assert still["A"] == pytest.approx(0.03)
    assert still["B"] == pytest.approx(6.0)

    flowing = scour_ratio_combined(10.0, 1.0)
    assert flowing["A"] == pytest.approx(0.78)
    assert flowing["B"] == pytest.approx(6.0 * math.exp(-4.7))


def test_pure_current_tends_to_the_steady_value():
    assert scour_ratio_combined(100.0, 1.0)["ratio"] == pytest.approx(1.3)
    assert scour_ratio_combined(1000.0, 0.5)["ratio"] == pytest.approx(1.3)


def test_scour_grows_with_the_current_share():
    ratios = [scour_ratio_combined(10.0, u)["ratio"]
              for u in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)]
    assert all(b > a for a, b in zip(ratios, ratios[1:]))


def test_scour_grows_with_KC():
    ratios = [scour_ratio_combined(KC, 0.3)["ratio"]
              for KC in (5.0, 10.0, 30.0, 80.0)]
    assert all(b > a for a, b in zip(ratios, ratios[1:]))


def test_the_relation_validates_its_inputs():
    with pytest.raises(ValueError):
        scour_ratio_combined(-1.0, 0.5)
    with pytest.raises(ValueError):
        scour_ratio_combined(10.0, 1.5)
    with pytest.raises(ValueError):
        scour_ratio_combined(10.0, -0.1)


# ---------------------------------------------------------------------------
# The steady-current floor
# ---------------------------------------------------------------------------


def test_a_live_current_under_small_waves_is_floored():
    """The trap this floor exists for.

    KC is built on the wave orbital velocity, so a strong current under a
    ripple gives a high Ucw and a low KC at once, and the bare relation
    then returns almost nothing. A current that moves the bed digs its own
    hole whatever the waves do.
    """
    bare = scour_ratio_combined(0.5, 0.85)
    floored = scour_ratio_combined(0.5, 0.85, current_live_bed=True)
    assert bare["ratio"] < 0.3
    assert floored["ratio"] == pytest.approx(1.3)
    assert floored["ratio"] > 5.0 * bare["ratio"]
    assert floored["current_governs"] is True
    assert floored["published"] == pytest.approx(bare["ratio"])


def test_the_floor_is_off_by_default():
    """It is an addition to the published relation, never silent."""
    got = scour_ratio_combined(0.5, 0.85)
    assert got["current_governs"] is False
    assert got["ratio"] == pytest.approx(got["published"])


def test_a_dead_bed_is_not_floored():
    got = scour_ratio_combined(0.5, 0.85, current_live_bed=False)
    assert got["current_governs"] is False
    assert got["ratio"] < 0.3


def test_the_floor_never_reduces_a_deeper_prediction():
    """Where the waves already beat the current, the floor does nothing."""
    got = scour_ratio_combined(200.0, 0.4, current_live_bed=True)
    assert got["current_governs"] is False
    assert got["ratio"] == pytest.approx(got["published"])


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def test_shape_factors_match_hec18():
    assert shape_factor("circular") == 1.0
    assert shape_factor("square") == 1.1
    assert shape_factor("sharp_nose") == 0.9


def test_an_unknown_shape_names_the_options():
    with pytest.raises(ValueError) as excinfo:
        shape_factor("hexagonal")
    assert "circular" in str(excinfo.value)


def test_aligned_flow_has_no_skew_penalty():
    assert alignment_factor(6.0, 12.0, 0.0) == pytest.approx(1.0)


def test_skew_penalises_a_long_base_more_than_a_square_one():
    assert (alignment_factor(6.0, 24.0, 30.0)
            > alignment_factor(6.0, 6.0, 30.0))


def test_skew_peaks_normal_to_the_diagonal():
    """K2 follows the projected width of a rectangle, ``a cos + L sin``,
    which is largest when the flow meets the diagonal square on, at
    ``atan(L/a)``, and not at 90 degrees where only the length shows."""
    width, length = 6.0, 12.0
    worst = math.degrees(math.atan(length / width))
    peak = alignment_factor(width, length, worst)
    for angle in (0.0, 20.0, worst - 5, worst + 5, 75.0, 90.0):
        assert alignment_factor(width, length, angle) <= peak + 1e-12
    assert alignment_factor(width, length, 90.0) > alignment_factor(
        width, length, 0.0)


def test_skew_is_symmetric_about_the_flow_axis():
    """160 degrees of skew is 20 the other way, on a reversing tide."""
    assert (alignment_factor(6.0, 12.0, 160.0)
            == pytest.approx(alignment_factor(6.0, 12.0, 20.0)))


def test_the_length_ratio_is_capped():
    assert (alignment_factor(1.0, 20.0, 30.0)
            == pytest.approx(alignment_factor(1.0, 12.0, 30.0)))


def test_a_bare_pier_has_the_stem_diameter(pier):
    got = equivalent_diameter(pier, None, depth=10.0)
    assert got["D_e"] == pytest.approx(pier.diameter)
    assert got["base_exposed"] is False


def test_a_buried_base_does_nothing_until_the_scour_reaches_it(pier, base):
    shallow = equivalent_diameter(pier, base, depth=9.0, scour=1.0)
    assert shallow["base_exposed"] is False
    assert shallow["D_e"] == pytest.approx(pier.diameter)

    deep = equivalent_diameter(pier, base, depth=9.0, scour=2.0)
    assert deep["base_exposed"] is True
    assert deep["D_e"] > pier.diameter


def test_the_exposed_height_cannot_exceed_the_base(pier, base):
    got = equivalent_diameter(pier, base, depth=9.0, scour=50.0)
    assert got["exposed_height"] == pytest.approx(base.height)
    assert got["fully_exposed"] is True


def test_a_wider_base_gives_a_wider_effective_diameter(pier):
    narrow = PierBase(width=4.0, length=4.0, height=2.0, top_level=0.5)
    wide = PierBase(width=10.0, length=10.0, height=2.0, top_level=0.5)
    assert (equivalent_diameter(pier, wide, 9.0)["D_e"]
            > equivalent_diameter(pier, narrow, 9.0)["D_e"])


def test_shallower_water_weights_the_base_more_heavily(pier, base):
    """The flow-weighted average is why low water can beat peak current."""
    deep = equivalent_diameter(pier, base, depth=12.0, scour=4.0)["D_e"]
    shallow = equivalent_diameter(pier, base, depth=6.0, scour=4.0)["D_e"]
    assert shallow > deep


def test_equivalent_diameter_validates_itself(pier, base):
    with pytest.raises(ValueError):
        equivalent_diameter(pier, base, depth=0.0)
    with pytest.raises(ValueError):
        equivalent_diameter(pier, base, depth=9.0, scour=-1.0)


def test_the_base_reports_its_own_levels():
    got = PierBase(height=2.5, top_level=-1.5)
    assert got.bottom_level == pytest.approx(-4.0)
    assert got.buried is True
    assert PierBase(top_level=0.5).buried is False


def test_the_pier_validates_itself():
    with pytest.raises(ValueError):
        Pier(diameter=0.0)
    with pytest.raises(ValueError):
        Pier(diameter=2.0, shape="triangular")
    with pytest.raises(ValueError):
        Pier(diameter=2.0, length=-1.0)


def test_the_base_validates_itself():
    with pytest.raises(ValueError):
        PierBase(width=0.0)
    with pytest.raises(ValueError):
        PierBase(height=0.0)


# ---------------------------------------------------------------------------
# Flow parameters
# ---------------------------------------------------------------------------


def test_keulegan_carpenter_is_the_definition():
    assert keulegan_carpenter(0.5, 8.0, 2.0) == pytest.approx(2.0)


def test_velocity_ratio_spans_the_two_pure_cases():
    assert velocity_ratio(0.0, 1.0) == 0.0
    assert velocity_ratio(1.0, 0.0) == 1.0
    assert velocity_ratio(1.0, 1.0) == pytest.approx(0.5)
    assert velocity_ratio(0.0, 0.0) == 0.0


def test_depth_limitation_bites_only_in_shallow_water():
    assert depth_limitation(30.0, 2.0) == pytest.approx(1.0, abs=1e-6)
    assert depth_limitation(6.0, 2.0) == pytest.approx(0.995, abs=0.002)
    assert depth_limitation(1.0, 2.0) < 0.5


def test_current_shields_rises_with_velocity():
    slow = current_shields("medium_sand", 0.4, 10.0)
    fast = current_shields("medium_sand", 1.4, 10.0)
    assert fast["theta"] > slow["theta"]
    assert fast["live_bed"] is True


def test_current_shields_refuses_a_cohesive_bed():
    with pytest.raises(ValueError) as excinfo:
        current_shields("soft_clay", 1.0, 10.0)
    assert "cohesive" in str(excinfo.value)


def test_a_coarser_bed_is_harder_to_move():
    fine = current_shields("fine_sand", 0.5, 10.0)["mobility"]
    coarse = current_shields("coarse_sand", 0.5, 10.0)["mobility"]
    assert coarse < fine


# ---------------------------------------------------------------------------
# Time
# ---------------------------------------------------------------------------


def test_the_time_scale_is_linear_in_diameter_and_depth():
    """T = T* D^2 / scale with T* carrying h/D, so the D^2 cancels to D."""
    small = scour_time_scale("medium_sand", 2.0, 10.0, 0.1)["T"]
    big = scour_time_scale("medium_sand", 4.0, 10.0, 0.1)["T"]
    assert big / small == pytest.approx(2.0, rel=1e-9)

    shallow = scour_time_scale("medium_sand", 2.0, 5.0, 0.1)["T"]
    deep = scour_time_scale("medium_sand", 2.0, 15.0, 0.1)["T"]
    assert deep / shallow == pytest.approx(3.0, rel=1e-9)


def test_a_more_mobile_bed_scours_faster():
    slow = scour_time_scale("medium_sand", 2.0, 10.0, 0.06)["T"]
    fast = scour_time_scale("medium_sand", 2.0, 10.0, 0.30)["T"]
    assert fast < slow


def test_the_time_scale_is_hours_to_days_for_a_real_pier():
    """A sanity band. Anything outside it means a units error."""
    flow = current_shields("medium_sand", 1.0, 10.0)
    hours = scour_time_scale("medium_sand", 2.5, 10.0, flow["theta"])["T"] / 3600
    assert 0.2 < hours < 200


def test_the_time_scale_refuses_a_dead_bed():
    with pytest.raises(ValueError):
        scour_time_scale("medium_sand", 2.0, 10.0, 0.0)


def test_development_approaches_equilibrium_from_below():
    assert scour_development(4.0, 0.0, 3600.0) == pytest.approx(0.0)
    assert scour_development(4.0, 3600.0, 3600.0) == pytest.approx(
        4.0 * (1 - math.exp(-1.0)))
    assert scour_development(4.0, 1e9, 3600.0) == pytest.approx(4.0)


def test_development_validates_itself():
    with pytest.raises(ValueError):
        scour_development(4.0, -1.0, 3600.0)
    with pytest.raises(ValueError):
        scour_development(4.0, 100.0, 0.0)


# ---------------------------------------------------------------------------
# The tide
# ---------------------------------------------------------------------------


def test_high_water_is_at_phase_zero(estuary):
    got = tidal_state(estuary, 0.0)
    assert got["elevation"] == pytest.approx(estuary.tidal_amplitude)
    assert got["depth"] == pytest.approx(estuary.mean_depth
                                         + estuary.tidal_amplitude)


def test_low_water_is_half_a_cycle_later(estuary):
    got = tidal_state(estuary, 180.0)
    assert got["depth"] == pytest.approx(estuary.mean_depth
                                         - estuary.tidal_amplitude)


def test_the_river_biases_the_current_seaward(estuary):
    """Ebb and flood peaks differ by twice the river current."""
    assert (estuary.peak_ebb_current - estuary.peak_flood_current
            == pytest.approx(2.0 * estuary.river_current))


def test_a_standing_tide_has_slack_water_at_high_water():
    standing = EstuaryConditions(tidal_current=1.0, river_current=0.0,
                                 current_phase=90.0)
    assert tidal_state(standing, 0.0)["tidal_current"] == pytest.approx(0.0,
                                                                       abs=1e-9)


def test_a_progressive_tide_runs_hardest_at_high_water():
    progressive = EstuaryConditions(tidal_current=1.0, river_current=0.0,
                                    current_phase=0.0)
    assert tidal_state(progressive, 0.0)["tidal_current"] == pytest.approx(1.0)


def test_a_depth_limited_chop_shrinks_at_low_water():
    est = EstuaryConditions(mean_depth=8.0, tidal_amplitude=2.0, Hs=1.0,
                            wave_follows_tide=True)
    assert tidal_state(est, 180.0)["Hs"] < tidal_state(est, 0.0)["Hs"]


def test_a_tide_that_dries_the_pier_is_refused():
    with pytest.raises(ValueError):
        EstuaryConditions(mean_depth=2.0, tidal_amplitude=2.5)


def test_the_estuary_refuses_a_cohesive_bed():
    with pytest.raises(ValueError) as excinfo:
        EstuaryConditions(bed="soft_clay")
    assert "cohesive" in str(excinfo.value)


def test_the_estuary_validates_its_waves():
    with pytest.raises(ValueError):
        EstuaryConditions(Hs=0.0)
    with pytest.raises(ValueError):
        EstuaryConditions(Tp=-1.0)


# ---------------------------------------------------------------------------
# The coupled scour and exposure
# ---------------------------------------------------------------------------


def test_a_bare_pier_converges_immediately(pier):
    got = equilibrium_scour(pier, None, depth=10.0, current=1.2, Um=0.4,
                            period=6.0, bed="medium_sand")
    assert got["converged"] is True
    assert got["D_e"] == pytest.approx(pier.diameter)


def test_exposing_the_base_deepens_the_hole(pier):
    """The feedback the iteration exists for."""
    shallow_base = PierBase(width=8.0, length=8.0, height=3.0, top_level=-0.5)
    deep_base = PierBase(width=8.0, length=8.0, height=3.0, top_level=-20.0)

    reachable = equilibrium_scour(pier, shallow_base, 10.0, 1.2, 0.4, 6.0,
                                  bed="medium_sand")
    buried = equilibrium_scour(pier, deep_base, 10.0, 1.2, 0.4, 6.0,
                               bed="medium_sand")

    assert reachable["geometry"]["base_exposed"] is True
    assert buried["geometry"]["base_exposed"] is False
    assert reachable["depth"] > buried["depth"]
    assert reachable["D_e"] > buried["D_e"]


def test_the_iteration_converges_across_the_exposure_step(pier):
    """A raw fixed point oscillates across the step change in D_e."""
    for top in np.linspace(-6.0, 0.5, 40):
        got = equilibrium_scour(
            pier, PierBase(width=9.0, length=9.0, height=3.0, top_level=top),
            depth=10.0, current=1.2, Um=0.4, period=6.0, bed="medium_sand")
        assert got["converged"] is True, f"did not converge at top={top}"


def test_the_solver_finds_the_deepest_self_consistent_depth(pier):
    """The answer must satisfy its own feedback, and be the deepest that does.

    Once the hole touches the base the system runs away, so more than one
    depth can be self-consistent. A scour hole does not refill, so the
    deepest root is the one the pier ends up with.
    """
    base = PierBase(width=9.0, length=9.0, height=3.0, top_level=-3.2)
    got = equilibrium_scour(pier, base, depth=10.0, current=1.2, Um=0.4,
                            period=6.0, bed="medium_sand")

    def predict(trial):
        geom = equivalent_diameter(pier, base, 10.0, trial)
        D_e = geom["D_e"]
        ratio = scour_ratio_combined(
            keulegan_carpenter(0.4, 6.0, D_e), velocity_ratio(1.2, 0.4),
            current_live_bed=True)["ratio"]
        return ratio * D_e * depth_limitation(10.0, D_e)

    # Self-consistent...
    assert predict(got["depth"]) == pytest.approx(got["depth"], abs=1e-6)
    # ...and nothing deeper is.
    for trial in np.linspace(got["depth"] + 0.2, got["depth"] + 3.0, 20):
        assert predict(trial) < trial


def test_deeper_burial_never_gives_deeper_scour(pier):
    """Burying the base further can only ever help, never hurt."""
    tops = np.linspace(-8.0, 0.5, 40)
    depths = [equilibrium_scour(
        pier, PierBase(width=9.0, length=9.0, height=3.0, top_level=t),
        depth=10.0, current=1.2, Um=0.4, period=6.0,
        bed="medium_sand")["depth"] for t in tops]
    assert all(b >= a - 1e-6 for a, b in zip(depths, depths[1:]))


def test_the_bed_is_needed_for_the_current_floor(pier):
    with_bed = equilibrium_scour(pier, None, 10.0, 1.2, 0.15, 5.0,
                                 bed="medium_sand")
    without = equilibrium_scour(pier, None, 10.0, 1.2, 0.15, 5.0)
    assert with_bed["current_governs"] is True
    assert without["current_governs"] is False
    assert with_bed["depth"] > without["depth"]


def test_equilibrium_scour_needs_at_least_one_iteration(pier):
    with pytest.raises(ValueError):
        equilibrium_scour(pier, None, 10.0, 1.0, 0.3, 6.0, iterations=0)


# ---------------------------------------------------------------------------
# Protection
# ---------------------------------------------------------------------------


def test_riprap_grows_with_the_square_of_velocity():
    slow = riprap_size(1.0)["d50"]
    fast = riprap_size(2.0)["d50"]
    assert fast / slow == pytest.approx(4.0, rel=1e-9)


def test_a_rectangular_pier_needs_bigger_stone():
    assert (riprap_size(1.5, shape="rectangular")["d50"]
            > riprap_size(1.5, shape="circular")["d50"])


def test_denser_stone_can_be_smaller():
    assert riprap_size(1.5, material_density=3000.0)["d50"] < riprap_size(1.5)["d50"]


def test_riprap_validates_itself():
    with pytest.raises(ValueError):
        riprap_size(0.0)
    with pytest.raises(ValueError):
        riprap_size(1.0, material_density=500.0)


def test_the_apron_reaches_two_obstacle_widths(pier, base):
    got = scour_protection(pier, base, 1.5, 3.0)
    assert got["extent"] == pytest.approx(2.0 * base.width)


def test_the_apron_is_measured_from_the_base_not_the_stem(pier, base):
    with_base = scour_protection(pier, base, 1.5, 3.0)
    without = scour_protection(pier, None, 1.5, 3.0)
    assert with_base["extent"] > without["extent"]


def test_a_deeper_hole_needs_more_launch_stone(pier, base):
    shallow = scour_protection(pier, base, 1.5, 1.0)
    deep = scour_protection(pier, base, 1.5, 5.0)
    assert deep["launch_volume"] > shallow["launch_volume"]
    assert deep["volume"] > shallow["volume"]


def test_the_apron_is_specified_as_a_falling_apron(pier, base):
    assert "falling apron" in scour_protection(pier, base, 1.5, 3.0)["note"]


# ---------------------------------------------------------------------------
# The whole design
# ---------------------------------------------------------------------------


def test_the_design_sweeps_the_whole_cycle(pier, estuary, base):
    got = design_pier_scour(pier, estuary, base, samples=37)
    assert len(got.states) == 37
    assert got.phases()[0] == pytest.approx(0.0)
    assert got.phases()[-1] == pytest.approx(360.0)


def test_the_governing_phase_is_the_deepest(pier, estuary, base):
    got = design_pier_scour(pier, estuary, base)
    assert got.equilibrium == pytest.approx(got.envelope().max())
    assert got.governing["scour"]["depth"] == pytest.approx(got.equilibrium)


def test_the_ebb_governs_when_a_river_runs(pier, base):
    """Tide and river add on the ebb and oppose on the flood."""
    est = EstuaryConditions(mean_depth=10.0, tidal_amplitude=1.0,
                            tidal_current=1.0, river_current=0.5,
                            Hs=0.8, Tp=5.0, current_phase=90.0)
    got = design_pier_scour(pier, est, base)
    assert got.governing["state"]["ebb"] is True


def test_a_reachable_base_is_reported_as_exposed(pier, estuary):
    got = design_pier_scour(pier, estuary,
                            PierBase(width=8.0, length=8.0, height=3.0,
                                     top_level=-0.3))
    assert got.base_exposed is True
    assert "exposes" in " ".join(got.notes)


def test_a_deep_base_stays_buried_and_says_so(pier, estuary):
    got = design_pier_scour(pier, estuary,
                            PierBase(width=8.0, length=8.0, height=3.0,
                                     top_level=-40.0))
    assert got.base_exposed is False
    assert got.undermined is False
    assert "stays buried" in " ".join(got.notes)


def test_undermining_is_called_out(pier, estuary, base):
    got = design_pier_scour(pier, estuary, base)
    if got.undermined:
        assert "undermined" in " ".join(got.notes)


def test_a_pier_with_no_base_still_designs(pier, estuary):
    got = design_pier_scour(pier, estuary)
    assert got.equilibrium > 0
    assert got.base_exposed is False
    assert got.undermined is False


def test_the_tidal_limit_never_exceeds_the_equilibrium(pier, estuary, base):
    got = design_pier_scour(pier, estuary, base)
    assert got.tidal_limited <= got.equilibrium + 1e-9


def test_the_design_carries_a_scatter_warning(pier, estuary, base):
    assert "standard deviation" in " ".join(
        design_pier_scour(pier, estuary, base).notes)


def test_the_design_needs_enough_phases(pier, estuary):
    with pytest.raises(ValueError):
        design_pier_scour(pier, estuary, samples=2)


def test_a_bigger_pier_scours_deeper(estuary):
    small = design_pier_scour(Pier(diameter=1.0), estuary).equilibrium
    large = design_pier_scour(Pier(diameter=4.0), estuary).equilibrium
    assert large > small


def test_a_stronger_river_scours_deeper(pier, base):
    def run(river):
        return design_pier_scour(pier, EstuaryConditions(
            mean_depth=10.0, tidal_amplitude=1.5, tidal_current=0.8,
            river_current=river, Hs=0.8, Tp=5.0), base).equilibrium

    assert run(1.2) >= run(0.1)


def test_the_tidal_period_defaults_to_M2(estuary):
    assert estuary.tidal_period == pytest.approx(M2_PERIOD)
    assert M2_PERIOD / 3600 == pytest.approx(12.42, abs=0.01)
