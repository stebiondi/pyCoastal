"""Groynes and detached breakwaters.

The groyne half has an exact analytical solution, so it is tested against
the identities that solution must satisfy: the impounded volume has to
equal the transport rate times the elapsed time, and the fillet has to
reach the groyne tip at exactly the predicted bypassing time. Those two
catch any error in the diffusivity, the wave angle or the profile height.

The detached breakwater half is empirical classification, so it is tested
for the behaviour the published rules claim, and for honesty about their
disagreement.
"""

import math

import numpy as np
import pytest

from pyCoastal.applications.groynes import (
    RESPONSE_CRITERIA,
    DetachedBreakwater,
    Groyne,
    LittoralCell,
    bay_planform,
    bypassing_time,
    design_detached_scheme,
    design_groyne_field,
    fillet_geometry,
    groyne_impoundment,
    groyne_planform,
    ierfc,
    parabolic_bay,
    segment_layout,
    shoreline_response,
    wave_transmission,
)
from pyCoastal.applications.groynes import _BAY_C0, _BAY_C1, _BAY_C2, _poly
from pyCoastal.applications.nourishment import SECONDS_PER_YEAR, WaveClimate


@pytest.fixture
def cell():
    return LittoralCell(D=6.0, B=2.0, bed="medium_sand")


@pytest.fixture
def climate():
    return WaveClimate(Hb=1.0, T=7.0, alpha0=math.radians(4.0))


@pytest.fixture
def groyne():
    return Groyne(length=60.0)


# ---------------------------------------------------------------------------
# The littoral cell
# ---------------------------------------------------------------------------


def test_active_height_is_closure_plus_berm(cell):
    assert cell.active_height == pytest.approx(8.0)


def test_porosity_comes_from_the_bed_material():
    from pyCoastal.applications.sediment import sediment

    cell = LittoralCell(bed="coarse_sand")
    assert cell.porosity == pytest.approx(sediment("coarse_sand").porosity)


def test_an_explicit_porosity_wins():
    assert LittoralCell(bed="medium_sand", porosity=0.3).porosity == 0.3


def test_a_cohesive_bed_is_refused():
    """These are sandy-coast models; a clay shore does not diffuse."""
    with pytest.raises(ValueError) as excinfo:
        LittoralCell(bed="soft_clay")
    assert "cohesive" in str(excinfo.value)


def test_the_cell_validates_its_geometry():
    with pytest.raises(ValueError):
        LittoralCell(D=0.0)
    with pytest.raises(ValueError):
        LittoralCell(B=-1.0)
    with pytest.raises(ValueError):
        LittoralCell(porosity=1.0)


def test_a_deeper_profile_diffuses_more_slowly(climate):
    shallow = LittoralCell(D=4.0, B=2.0).diffusivity(climate)
    deep = LittoralCell(D=12.0, B=2.0).diffusivity(climate)
    assert deep < shallow


# ---------------------------------------------------------------------------
# ierfc
# ---------------------------------------------------------------------------


def test_ierfc_at_zero_is_one_over_root_pi():
    assert ierfc(0.0) == pytest.approx(1.0 / math.sqrt(math.pi))


def test_ierfc_decays_monotonically():
    values = ierfc(np.array([0.0, 0.5, 1.0, 2.0, 3.0]))
    assert all(b < a for a, b in zip(values, values[1:]))


def test_ierfc_is_effectively_zero_far_out():
    assert ierfc(6.0) == pytest.approx(0.0, abs=1e-15)


def test_ierfc_matches_its_definition():
    for u in (0.3, 1.2, 2.7):
        expected = math.exp(-u * u) / math.sqrt(math.pi) - u * math.erfc(u)
        assert ierfc(u) == pytest.approx(expected, rel=1e-12)


def test_ierfc_takes_an_array_and_a_scalar():
    assert isinstance(ierfc(1.0), float)
    assert ierfc(np.array([1.0, 2.0])).shape == (2,)


# ---------------------------------------------------------------------------
# The groyne solution, against the identities it must satisfy
# ---------------------------------------------------------------------------


def test_impounded_volume_equals_transport_times_time(cell, climate, groyne):
    """dV/dt must be the alongshore transport rate, exactly."""
    t = 0.5 * SECONDS_PER_YEAR
    rate = (math.tan(climate.alpha0) * cell.diffusivity(climate)
            * cell.active_height)
    assert groyne_impoundment(t, groyne, cell, climate) == pytest.approx(rate * t)


def test_the_integrated_fillet_matches_the_analytical_volume(cell, climate,
                                                            groyne):
    """Integrating the drawn shoreline has to give the stated volume."""
    t = 1.0 * SECONDS_PER_YEAR
    x = np.linspace(-40000.0, 0.0, 200001)
    y = groyne_planform(x, t, groyne, cell, climate)
    integrated = float(np.trapezoid(y, x)) * cell.active_height
    assert integrated == pytest.approx(
        groyne_impoundment(t, groyne, cell, climate), rel=1e-3)


def test_the_fillet_reaches_the_tip_at_the_bypassing_time(cell, climate,
                                                          groyne):
    t = bypassing_time(groyne, cell, climate)
    advance = float(groyne_planform(np.array([-1e-9]), t, groyne, cell,
                                    climate)[0])
    assert advance == pytest.approx(groyne.length, rel=1e-9)


def test_the_advance_grows_as_the_square_root_of_time(cell, climate, groyne):
    one = fillet_geometry(groyne, cell, climate, 1.0 * SECONDS_PER_YEAR)
    four = fillet_geometry(groyne, cell, climate, 4.0 * SECONDS_PER_YEAR)
    assert four["advance"] / one["advance"] == pytest.approx(2.0, rel=1e-9)


def test_updrift_accretes_and_downdrift_erodes(cell, climate, groyne):
    x = np.array([-500.0, -100.0, 100.0, 500.0])
    y = groyne_planform(x, SECONDS_PER_YEAR, groyne, cell, climate)
    assert y[0] > 0 and y[1] > 0
    assert y[2] < 0 and y[3] < 0


def test_the_downdrift_limb_mirrors_the_fillet(cell, climate, groyne):
    """The erosion is the same size as the accretion. That is the point."""
    x = np.array([250.0, 800.0])
    up = groyne_planform(-x, SECONDS_PER_YEAR, groyne, cell, climate)
    down = groyne_planform(x, SECONDS_PER_YEAR, groyne, cell, climate)
    assert np.allclose(up, -down)


def test_shore_normal_waves_build_nothing(cell, groyne):
    straight = WaveClimate(Hb=1.0, T=7.0, alpha0=0.0)
    y = groyne_planform(np.linspace(-500, 500, 11), SECONDS_PER_YEAR,
                        groyne, cell, straight)
    assert np.allclose(y, 0.0)
    assert bypassing_time(groyne, cell, straight) == math.inf


def test_nothing_has_happened_at_time_zero(cell, climate, groyne):
    y = groyne_planform(np.linspace(-500, 500, 11), 0.0, groyne, cell, climate)
    assert np.allclose(y, 0.0)
    assert groyne_impoundment(0.0, groyne, cell, climate) == 0.0


def test_time_cannot_run_backwards(cell, climate, groyne):
    with pytest.raises(ValueError):
        groyne_planform(np.array([0.0]), -1.0, groyne, cell, climate)
    with pytest.raises(ValueError):
        groyne_impoundment(-1.0, groyne, cell, climate)
    with pytest.raises(ValueError):
        fillet_geometry(groyne, cell, climate, -1.0)


def test_a_longer_groyne_takes_longer_to_bypass(cell, climate):
    short = bypassing_time(Groyne(length=30.0), cell, climate)
    long = bypassing_time(Groyne(length=60.0), cell, climate)
    assert long / short == pytest.approx(4.0, rel=1e-9)


def test_a_permeable_groyne_traps_less_and_fills_later(cell, climate):
    tight = Groyne(length=60.0, permeability=0.0)
    leaky = Groyne(length=60.0, permeability=0.4)
    t = 0.2 * SECONDS_PER_YEAR
    assert (groyne_impoundment(t, leaky, cell, climate)
            < groyne_impoundment(t, tight, cell, climate))
    assert bypassing_time(leaky, cell, climate) > bypassing_time(tight, cell, climate)


def test_a_fully_permeable_groyne_is_not_a_groyne():
    with pytest.raises(ValueError):
        Groyne(length=60.0, permeability=1.0)


def test_the_groyne_validates_itself():
    with pytest.raises(ValueError):
        Groyne(length=0.0)
    with pytest.raises(ValueError):
        Groyne(length=10.0, permeability=-0.1)


def test_capacity_matches_the_impoundment_at_bypassing(cell, climate, groyne):
    state = fillet_geometry(groyne, cell, climate, 0.1 * SECONDS_PER_YEAR)
    assert state["capacity"] == pytest.approx(
        groyne_impoundment(state["bypassing_time"], groyne, cell, climate),
        rel=1e-9)


def test_gentler_waves_impound_more_before_bypassing(cell, groyne):
    """V_full = pi L^2 (D+B) / 4m: a shallow fillet must run further."""
    gentle = fillet_geometry(groyne, cell,
                             WaveClimate(Hb=1.0, T=7.0, alpha0=math.radians(2.0)),
                             1.0)["capacity"]
    oblique = fillet_geometry(groyne, cell,
                              WaveClimate(Hb=1.0, T=7.0, alpha0=math.radians(8.0)),
                              1.0)["capacity"]
    assert gentle > oblique


def test_past_bypassing_the_result_says_so(cell, climate, groyne):
    """Returning a 90 m fillet against a 60 m groyne without a word is a trap."""
    late = fillet_geometry(groyne, cell, climate, 5.0 * SECONDS_PER_YEAR)
    assert late["bypassing"] is True
    assert late["valid"] is False
    assert late["filled_fraction"] == 1.0
    assert "cannot happen" in late["note"]


def test_before_bypassing_the_result_is_clean(cell, climate, groyne):
    early = fillet_geometry(groyne, cell, climate, 0.1 * SECONDS_PER_YEAR)
    assert early["valid"] is True
    assert early["note"] == ""
    assert early["filled_fraction"] < 1.0


# ---------------------------------------------------------------------------
# The field
# ---------------------------------------------------------------------------


def test_a_field_reports_its_spacing_ratio(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0)
    assert got.spacing_ratio == pytest.approx(2.5)
    assert "inside the conventional" in " ".join(got.notes)


def test_a_cramped_field_is_flagged(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=60.0)
    assert "closer than the usual" in " ".join(got.notes)


def test_a_sparse_field_is_flagged(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=300.0)
    assert "wider than the usual" in " ".join(got.notes)


def test_outflanking_is_detected(cell):
    """Wide spacing plus oblique waves rotates the bay past the groyne root."""
    oblique = WaveClimate(Hb=1.0, T=7.0, alpha0=math.radians(20.0))
    got = design_groyne_field(cell, oblique, length=30.0, spacing=400.0)
    assert got.outflanked is True
    assert "outflanked" in " ".join(got.notes)


def test_a_well_proportioned_field_is_not_outflanked(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0)
    assert got.outflanked is False
    assert "holds" in " ".join(got.notes)


def test_prefilling_removes_the_downdrift_deficit(cell, climate):
    taken = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                                prefill=False)
    given = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                                prefill=True)
    assert taken.downdrift_deficit > 0
    assert given.downdrift_deficit == 0.0
    assert "comes off the coast downdrift" in " ".join(taken.notes)
    assert "takes nothing from downdrift" in " ".join(given.notes)


def test_the_deficit_cannot_exceed_what_the_field_holds(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              horizon=200.0 * SECONDS_PER_YEAR)
    assert got.downdrift_deficit <= got.field_capacity


def test_field_length_spans_the_groynes(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=5)
    assert got.field_length == pytest.approx(600.0)


def test_the_field_planform_has_three_regions(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=3, horizon=0.05 * SECONDS_PER_YEAR)
    x = np.linspace(-600.0, 600.0, 1200)
    y = got.planform(x)
    # Updrift of the whole field accretes, downdrift of it erodes.
    assert y[0] > 0
    assert y[-1] < 0
    # And the two ends are mirror images of each other.
    assert y[0] == pytest.approx(-y[-1], rel=1e-9)


def test_the_bays_never_exceed_their_sawtooth(cell, climate):
    """The failure the superposed model had: unbounded growth along the field.

    A sealed bay can only tilt. Whatever it gains at the downdrift groyne
    it takes from the updrift one, so the interior of a field is bounded by
    the equilibrium sawtooth however long it runs.
    """
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=6, horizon=0.0)
    limit = math.tan(climate.alpha0) * got.spacing / 2.0
    groynes = got.positions
    x = np.linspace(groynes[0], groynes[-1], 2001)
    for years in (0.05, 0.5, 5.0, 50.0):
        y = got.planform(x, years * SECONDS_PER_YEAR)
        interior = (x > groynes[0]) & (x < groynes[-1])
        assert np.max(np.abs(y[interior])) <= limit * (1.0 + 1e-9)


def test_a_bay_conserves_its_sand_exactly(cell, climate):
    """Sealed at both ends, so the volume inside can never change."""
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=3)
    a, b = got.positions[0], got.positions[1]
    x = np.linspace(a + 1e-6, b - 1e-6, 4001)
    for years in (0.02, 0.2, 2.0):
        y = got.planform(x, years * SECONDS_PER_YEAR)
        assert float(np.trapezoid(y, x)) == pytest.approx(0.0, abs=1e-6)


def test_a_bay_starts_flat_and_relaxes_to_the_sawtooth(cell, climate):
    spacing = 150.0
    xi = np.linspace(0.0, spacing, 401)
    assert np.allclose(bay_planform(xi, 0.0, spacing, cell, climate), 0.0)

    late = bay_planform(xi, 200.0 * SECONDS_PER_YEAR, spacing, cell, climate)
    equilibrium = math.tan(climate.alpha0) * (xi - 0.5 * spacing)
    assert np.allclose(late, equilibrium, atol=1e-9)


def test_a_bay_erodes_updrift_and_accretes_downdrift(cell, climate):
    """Sand is blocked at the downdrift groyne, so that is where it piles."""
    spacing = 150.0
    y = bay_planform(np.array([0.0, 0.5 * spacing, spacing]),
                     0.1 * SECONDS_PER_YEAR, spacing, cell, climate)
    assert y[0] < 0 < y[2]
    assert y[1] == pytest.approx(0.0, abs=1e-9)
    assert y[0] == pytest.approx(-y[2], rel=1e-9)


def test_shore_normal_waves_leave_a_bay_flat(cell):
    straight = WaveClimate(Hb=1.0, T=7.0, alpha0=0.0)
    y = bay_planform(np.linspace(0, 150, 51), SECONDS_PER_YEAR, 150.0,
                     cell, straight)
    assert np.allclose(y, 0.0)


def test_a_bay_validates_its_inputs(cell, climate):
    with pytest.raises(ValueError):
        bay_planform(np.array([0.0]), -1.0, 150.0, cell, climate)
    with pytest.raises(ValueError):
        bay_planform(np.array([0.0]), 1.0, 0.0, cell, climate)


def test_wider_bays_take_longer_to_tilt(cell, climate):
    """The relaxation time goes as the square of the spacing."""
    near = design_groyne_field(cell, climate, length=60.0, spacing=100.0)
    far = design_groyne_field(cell, climate, length=60.0, spacing=200.0)
    assert far.relaxation_time / near.relaxation_time == pytest.approx(4.0)


def test_groyne_positions_are_centred_and_evenly_spaced(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=5)
    assert np.allclose(got.positions, [-300.0, -150.0, 0.0, 150.0, 300.0])


def test_a_point_on_a_groyne_takes_the_accreted_side(cell, climate):
    """The beach steps across a groyne, so the value there needs a rule."""
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                              count=3, horizon=0.2 * SECONDS_PER_YEAR)
    middle = got.positions[1]
    on = float(got.planform(np.array([middle]))[0])
    just_after = float(got.planform(np.array([middle + 0.01]))[0])
    assert on > 0 > just_after


def test_the_field_planform_refuses_negative_time(cell, climate):
    got = design_groyne_field(cell, climate, length=60.0, spacing=150.0)
    with pytest.raises(ValueError):
        got.planform(np.array([0.0]), -1.0)


def test_the_shoreline_steps_across_a_groyne(cell, climate, groyne):
    """Sand piles on the updrift face and is scoured from the downdrift one.

    That step is the whole visible signature of a groyne on a beach, and
    it is why the planform is discontinuous at the structure rather than
    passing smoothly through zero.
    """
    t = 0.05 * SECONDS_PER_YEAR
    eps = 1e-6
    up = float(groyne_planform(np.array([-eps]), t, groyne, cell, climate)[0])
    down = float(groyne_planform(np.array([eps]), t, groyne, cell, climate)[0])
    advance = fillet_geometry(groyne, cell, climate, t)["advance"]
    assert up == pytest.approx(advance, rel=1e-6)
    assert up - down == pytest.approx(2.0 * advance, rel=1e-6)


def test_a_field_validates_its_layout(cell, climate):
    with pytest.raises(ValueError):
        design_groyne_field(cell, climate, length=60.0, spacing=150.0, count=0)
    with pytest.raises(ValueError):
        design_groyne_field(cell, climate, length=60.0, spacing=0.0)
    with pytest.raises(ValueError):
        design_groyne_field(cell, climate, length=60.0, spacing=150.0,
                            horizon=-1.0)


# ---------------------------------------------------------------------------
# Wave transmission
# ---------------------------------------------------------------------------


def test_a_submerged_crest_transmits_more_than_an_emergent_one():
    low = wave_transmission(2.0, -0.5, 5.0, 1.0, period=8.0)["Kt"]
    high = wave_transmission(2.0, 2.0, 5.0, 1.0, period=8.0)["Kt"]
    assert low > high


def test_a_wider_crest_transmits_less():
    narrow = wave_transmission(2.0, 0.0, 3.0, 1.0, period=8.0)["Kt"]
    wide = wave_transmission(2.0, 0.0, 12.0, 1.0, period=8.0)["Kt"]
    assert wide < narrow


def test_transmission_is_bounded_and_says_when_it_clipped():
    deep = wave_transmission(1.0, 6.0, 5.0, 1.0, period=8.0)
    assert deep["Kt"] == 0.075
    assert deep["clipped"] is True
    assert deep["unbounded"] < 0.075


def test_transmission_is_not_clipped_in_the_normal_range():
    got = wave_transmission(2.0, 1.0, 5.0, 1.0, period=8.0)
    assert 0.075 < got["Kt"] < 0.8
    assert got["clipped"] is False


def test_transmitted_energy_is_the_square_of_the_height_ratio():
    got = wave_transmission(2.0, 0.5, 5.0, 1.0, period=8.0)
    assert got["energy_transmitted"] == pytest.approx(got["Kt"] ** 2)


def test_steepness_and_period_are_interchangeable():
    Hs, T = 2.0, 8.0
    steepness = 2.0 * math.pi * Hs / (9.81 * T**2)
    assert (wave_transmission(Hs, 1.0, 5.0, 1.0, period=T)["Kt"]
            == pytest.approx(
                wave_transmission(Hs, 1.0, 5.0, 1.0, steepness=steepness)["Kt"]))


def test_transmission_needs_a_period_or_a_steepness():
    with pytest.raises(ValueError):
        wave_transmission(2.0, 1.0, 5.0, 1.0)


def test_transmission_validates_its_inputs():
    with pytest.raises(ValueError):
        wave_transmission(0.0, 1.0, 5.0, 1.0, period=8.0)
    with pytest.raises(ValueError):
        wave_transmission(2.0, 1.0, 0.0, 1.0, period=8.0)
    with pytest.raises(ValueError):
        wave_transmission(2.0, 1.0, 5.0, 0.0, period=8.0)


def test_transmission_flags_being_outside_its_fitted_range():
    assert wave_transmission(2.0, 1.0, 5.0, 1.0, period=8.0)["in_range"]
    assert not wave_transmission(2.0, 9.0, 5.0, 1.0, period=8.0)["in_range"]


# ---------------------------------------------------------------------------
# Shoreline response
# ---------------------------------------------------------------------------


def test_a_long_close_breakwater_builds_a_tombolo():
    got = shoreline_response(DetachedBreakwater(length=300.0, offshore=100.0))
    assert got["consensus"] == "tombolo"
    assert got["unanimous"] is True


def test_a_short_distant_breakwater_does_nothing():
    got = shoreline_response(DetachedBreakwater(length=30.0, offshore=200.0))
    assert got["consensus"] == "no sinuosity"


def test_a_mid_range_layout_gives_a_salient():
    got = shoreline_response(DetachedBreakwater(length=70.0, offshore=100.0))
    assert got["consensus"] == "salient"


def test_the_criteria_are_allowed_to_disagree():
    """Ls/X = 1.5 is a tombolo to two of the three, and the result says so."""
    got = shoreline_response(DetachedBreakwater(length=150.0, offshore=100.0))
    assert got["unanimous"] is False
    assert got["consensus"] is None
    assert len(set(got["verdicts"].values())) > 1
    assert "threshold" in got["note"]


def test_every_criterion_can_be_asked_alone():
    bw = DetachedBreakwater(length=150.0, offshore=100.0)
    for key in RESPONSE_CRITERIA:
        got = shoreline_response(bw, criterion=key)
        assert list(got["verdicts"]) == [key]
        assert got["unanimous"] is True


def test_an_unknown_criterion_names_the_options():
    with pytest.raises(ValueError) as excinfo:
        shoreline_response(DetachedBreakwater(), criterion="nope")
    assert "dally_pope_1986" in str(excinfo.value)


def test_the_response_is_monotone_in_the_ratio():
    """More sheltering can never give a weaker response."""
    order = ["no sinuosity", "salient", "periodic tombolo", "tombolo"]
    ranks = [order.index(shoreline_response(
        DetachedBreakwater(length=L, offshore=100.0),
        criterion="spm_1984")["verdicts"]["spm_1984"])
        for L in (20.0, 60.0, 90.0, 120.0, 250.0)]
    assert all(b >= a for a, b in zip(ranks, ranks[1:]))


def test_a_wide_gap_prevents_a_tombolo():
    tight = shoreline_response(
        DetachedBreakwater(length=150.0, offshore=100.0, gap=30.0))
    wide = shoreline_response(
        DetachedBreakwater(length=150.0, offshore=100.0, gap=200.0))
    assert tight["gap_allows_tombolo"] is True
    assert wide["gap_allows_tombolo"] is False
    assert "whatever Ls/X says" in wide["note"]


def test_a_single_breakwater_has_no_gap_index():
    got = shoreline_response(DetachedBreakwater(length=150.0, offshore=100.0))
    assert got["gap_index"] is None


def test_the_breakwater_validates_itself():
    with pytest.raises(ValueError):
        DetachedBreakwater(length=0.0)
    with pytest.raises(ValueError):
        DetachedBreakwater(offshore=0.0)
    with pytest.raises(ValueError):
        DetachedBreakwater(gap=-1.0)


# ---------------------------------------------------------------------------
# The parabolic bay
# ---------------------------------------------------------------------------


def test_the_bay_coefficients_sum_to_one():
    """C0 + C1 + C2 = 1 at theta = beta, since R must equal R0 there.

    These are least-squares fits so it holds to about half a percent, but
    a mistyped digit breaks it by very much more.
    """
    for beta in (20.0, 30.0, 45.0, 60.0, 80.0):
        total = (_poly(_BAY_C0, beta) + _poly(_BAY_C1, beta)
                 + _poly(_BAY_C2, beta))
        assert total == pytest.approx(1.0, abs=0.02)


def test_the_bay_returns_the_control_line_at_theta_equals_beta():
    R = parabolic_bay(45.0, 200.0, np.array([45.0]))
    assert float(R[0]) == pytest.approx(200.0, rel=0.02)


def test_the_bay_tightens_towards_the_headland():
    """R shrinks as theta grows: the control point at theta = beta is the
    far, open end of the bay, and large theta is close in under the
    diffraction point."""
    R = parabolic_bay(30.0, 200.0, np.array([30.0, 45.0, 60.0, 90.0, 140.0]))
    assert all(b < a for a, b in zip(R, R[1:]))
    assert R[-1] > 0


def test_beyond_the_control_point_the_relation_does_not_hold():
    R = parabolic_bay(45.0, 200.0, np.array([20.0, 44.9, 45.0, 90.0]))
    assert np.isnan(R[0]) and np.isnan(R[1])
    assert not np.isnan(R[2]) and not np.isnan(R[3])


def test_the_bay_scales_with_the_control_line():
    theta = np.array([60.0, 90.0])
    assert np.allclose(parabolic_bay(30.0, 400.0, theta),
                       2.0 * parabolic_bay(30.0, 200.0, theta))


def test_the_bay_validates_its_inputs():
    with pytest.raises(ValueError):
        parabolic_bay(0.0, 200.0, np.array([45.0]))
    with pytest.raises(ValueError):
        parabolic_bay(45.0, 0.0, np.array([45.0]))


# ---------------------------------------------------------------------------
# Segment layout and the whole scheme
# ---------------------------------------------------------------------------


def test_segments_and_gaps_fill_the_frontage():
    got = segment_layout(1200.0, DetachedBreakwater(length=150.0, gap=60.0))
    assert got["count"] == 6
    assert got["span"] == pytest.approx(6 * 210.0 - 60.0)
    assert got["sheltered_fraction"] + got["gap_fraction"] == pytest.approx(1.0)


def test_a_single_breakwater_shelters_everything_it_spans():
    got = segment_layout(150.0, DetachedBreakwater(length=150.0, gap=0.0))
    assert got["count"] == 1
    assert got["sheltered_fraction"] == pytest.approx(1.0)


def test_a_wider_gap_shelters_less():
    tight = segment_layout(1200.0, DetachedBreakwater(length=150.0, gap=30.0))
    wide = segment_layout(1200.0, DetachedBreakwater(length=150.0, gap=150.0))
    assert wide["sheltered_fraction"] < tight["sheltered_fraction"]


def test_a_frontage_must_be_positive():
    with pytest.raises(ValueError):
        segment_layout(0.0, DetachedBreakwater())


def test_the_scheme_reports_a_verdict_and_a_transmission(cell, climate):
    got = design_detached_scheme(
        cell, climate, DetachedBreakwater(length=300.0, offshore=100.0),
        frontage=1200.0, Hs=2.0, period=8.0, Dn50=1.1)
    assert got.verdict == "tombolo"
    assert 0.075 <= got.transmission["Kt"] <= 0.8


def test_a_split_verdict_reads_as_disputed(cell, climate):
    got = design_detached_scheme(
        cell, climate, DetachedBreakwater(length=150.0, offshore=100.0),
        frontage=1200.0, Hs=2.0, period=8.0)
    assert got.verdict == "disputed"


def test_a_transmissive_scheme_is_warned_about(cell, climate):
    """A sill passing half the wave height will not build what Ls/X promises."""
    got = design_detached_scheme(
        cell, climate,
        DetachedBreakwater(length=300.0, offshore=100.0, crest_level=-1.0),
        frontage=1200.0, Hs=2.0, period=8.0, Dn50=1.1)
    assert got.submerged is True
    assert got.transmission["Kt"] > 0.3
    joined = " ".join(got.notes)
    assert "smaller response" in joined or "upper bound" in joined
    assert "return flow" in joined


def test_an_emergent_scheme_is_not_warned_about(cell, climate):
    got = design_detached_scheme(
        cell, climate,
        DetachedBreakwater(length=300.0, offshore=100.0, crest_level=3.0),
        frontage=1200.0, Hs=2.0, period=8.0, Dn50=1.1)
    assert got.submerged is False
    assert "blocks most of the wave energy" in " ".join(got.notes)


def test_the_scheme_defaults_its_wave_to_the_climate(cell, climate):
    got = design_detached_scheme(
        cell, climate, DetachedBreakwater(length=300.0, offshore=100.0),
        frontage=1200.0, Dn50=1.1)
    assert got.Hs == pytest.approx(climate.Hb)
    assert got.period == pytest.approx(climate.T)
