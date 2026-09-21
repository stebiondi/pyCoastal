"""Berthing energy and fender selection.

PIANC's chain is four multipliers on a kinetic energy, so most of these
tests are limits: each factor has a configuration in which it must be
exactly one, and the fender scaling has exponents that must be exactly
three and two. Those pin the arithmetic. The rest cover the three ways a
berth fails, which are all different from each other.
"""

import math

import pytest

from pyCoastal.applications.berthing import (
    ABNORMAL_FACTOR,
    BERTH_CONFIGURATION,
    BERTHING_VELOCITY,
    CONE_FENDER,
    HULL_PRESSURE_LIMIT,
    FenderFamily,
    abnormal_energy,
    added_mass_factor,
    berthing_energy,
    berthing_velocity,
    design_berth,
    eccentricity_factor,
    fender_spacing,
    hull_pressure,
    select_fender,
)
from pyCoastal.applications.channel import Vessel


@pytest.fixture
def ship():
    return Vessel(name="Post-Panamax container", length=366.0, beam=48.2,
                  draught=15.2, block_coefficient=0.68)


@pytest.fixture
def feeder():
    return Vessel(name="Feeder", length=140.0, beam=22.0, draught=8.5,
                  block_coefficient=0.68)


# ---------------------------------------------------------------------------
# The factors, at their limits
# ---------------------------------------------------------------------------


def test_added_mass_is_the_vasco_costa_form(ship):
    got = added_mass_factor(ship)
    assert got["Cm"] == pytest.approx(1.0 + 2.0 * 15.2 / 48.2)
    assert got["Cm"] > 1.0


def test_added_mass_is_the_only_factor_that_adds(ship):
    """Everything else in the chain reduces the energy."""
    got = berthing_energy(ship, 0.15, configuration="solid_quay")
    assert got["Cm"] > 1.0
    assert got["Ce"] <= 1.0
    assert got["Cs"] <= 1.0
    assert got["Cc"] <= 1.0


def test_a_deeper_laden_ship_drags_more_water():
    shallow = Vessel(name="a", length=200.0, beam=30.0, draught=6.0)
    laden = Vessel(name="b", length=200.0, beam=30.0, draught=12.0)
    assert added_mass_factor(laden)["Cm"] > added_mass_factor(shallow)["Cm"]


def test_a_tight_underkeel_clearance_is_warned_about(ship):
    assert added_mass_factor(ship, depth=25.0)["note"] == ""
    assert "escape" in added_mass_factor(ship, depth=16.0)["note"]


def test_a_berth_shallower_than_the_ship_is_refused(ship):
    with pytest.raises(ValueError):
        added_mass_factor(ship, depth=10.0)


def test_landing_flat_amidships_carries_nothing_away(ship):
    """No lever arm, so no rotation, so Ce is exactly one."""
    assert eccentricity_factor(ship, contact_distance=0.0)["Ce"] == pytest.approx(1.0)


def test_an_end_on_approach_carries_nothing_away(ship):
    """Velocity along the line to the centre of mass cannot spin the ship."""
    assert eccentricity_factor(ship, approach_angle=0.0)["Ce"] == pytest.approx(1.0)
    assert eccentricity_factor(ship, approach_angle=180.0)["Ce"] == pytest.approx(1.0)


def test_the_quarter_point_takes_about_half_the_energy(ship):
    got = eccentricity_factor(ship)
    assert got["quarter_point"] is True
    assert 0.35 < got["Ce"] < 0.65


def test_a_contact_further_from_midships_carries_more_away(ship):
    near = eccentricity_factor(ship, contact_distance=10.0)["Ce"]
    far = eccentricity_factor(ship, contact_distance=120.0)["Ce"]
    assert far < near


def test_the_radius_of_gyration_follows_the_block_coefficient(ship):
    got = eccentricity_factor(ship)
    assert got["K"] == pytest.approx(
        (0.19 * ship.block_coefficient + 0.11) * ship.length_pp)


def test_a_negative_contact_distance_is_refused(ship):
    with pytest.raises(ValueError):
        eccentricity_factor(ship, contact_distance=-1.0)


# ---------------------------------------------------------------------------
# The energy
# ---------------------------------------------------------------------------


def test_the_energy_is_the_product_of_the_chain(ship):
    got = berthing_energy(ship, 0.15)
    expected = (got["kinetic"] * got["Cm"] * got["Ce"] * got["Cs"]
                * got["Cc"])
    assert got["energy"] == pytest.approx(expected)


def test_the_kinetic_energy_is_half_m_v_squared(ship):
    got = berthing_energy(ship, 0.2)
    assert got["kinetic"] == pytest.approx(
        0.5 * ship.displacement * 1000.0 * 0.2**2 / 1000.0)


def test_energy_goes_with_the_square_of_velocity(ship):
    slow = berthing_energy(ship, 0.1)["energy"]
    fast = berthing_energy(ship, 0.2)["energy"]
    assert fast / slow == pytest.approx(4.0, rel=1e-9)


def test_a_solid_quay_absorbs_some_of_it(ship):
    solid = berthing_energy(ship, 0.15, configuration="solid_quay")["energy"]
    piled = berthing_energy(ship, 0.15, configuration="open_piled")["energy"]
    assert solid < piled
    assert solid / piled == pytest.approx(BERTH_CONFIGURATION["solid_quay"])


def test_the_retained_fraction_is_reported(ship):
    got = berthing_energy(ship, 0.15)
    assert got["retained_fraction"] == pytest.approx(
        got["energy"] / got["kinetic"])
    assert 0.3 < got["retained_fraction"] < 1.0


def test_energy_validates_its_inputs(ship):
    with pytest.raises(ValueError):
        berthing_energy(ship, 0.0)
    with pytest.raises(ValueError):
        berthing_energy(ship, 0.15, softness=0.5)
    with pytest.raises(ValueError):
        berthing_energy(ship, 0.15, configuration="floating")


def test_the_velocity_table_is_ordered(ship):
    """Harder conditions and smaller ships both mean faster approaches."""
    for condition in BERTHING_VELOCITY:
        band = BERTHING_VELOCITY[condition]
        assert band["small"] >= band["medium"] >= band["large"]
    assert (BERTHING_VELOCITY["difficult_exposed"]["large"]
            > BERTHING_VELOCITY["easy_sheltered"]["large"])


def test_the_velocity_is_picked_by_displacement(ship, feeder):
    assert berthing_velocity(ship)["band"] == "large"
    assert berthing_velocity(feeder)["band"] in ("small", "medium")


def test_an_unknown_condition_names_the_options(ship):
    with pytest.raises(ValueError) as excinfo:
        berthing_velocity(ship, "hurricane")
    assert "easy_sheltered" in str(excinfo.value)


def test_the_abnormal_factor_is_reported_separately(ship):
    normal = berthing_energy(ship, 0.15)["energy"]
    got = abnormal_energy(normal, "container")
    assert got["energy"] == pytest.approx(normal * ABNORMAL_FACTOR["container"])
    assert got["normal"] == pytest.approx(normal)


def test_small_vessels_carry_the_larger_abnormal_factors():
    assert ABNORMAL_FACTOR["tanker_small"] > ABNORMAL_FACTOR["tanker_large"]
    assert all(1.0 <= f <= 2.0 for f in ABNORMAL_FACTOR.values())


def test_an_abnormal_factor_below_one_is_refused():
    with pytest.raises(ValueError):
        abnormal_energy(100.0, factor=0.9)


def test_an_unknown_vessel_class_names_the_options():
    with pytest.raises(ValueError) as excinfo:
        abnormal_energy(100.0, "submarine")
    assert "container" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Fenders
# ---------------------------------------------------------------------------


def test_energy_scales_with_the_cube_and_reaction_with_the_square():
    """Why the answer to too much reaction is usually a bigger fender."""
    f = CONE_FENDER
    assert f.energy(2.0) / f.energy(1.0) == pytest.approx(8.0)
    assert f.reaction(2.0) / f.reaction(1.0) == pytest.approx(4.0)


def test_the_reference_size_returns_its_reference_values():
    f = CONE_FENDER
    assert f.energy(f.reference_height) == pytest.approx(f.reference_energy)
    assert f.reaction(f.reference_height) == pytest.approx(f.reference_reaction)


def test_the_height_for_an_energy_inverts_the_scaling():
    f = CONE_FENDER
    for energy in (100.0, 500.0, 3000.0):
        assert f.energy(f.height_for(energy)) == pytest.approx(energy)


def test_selection_takes_the_smallest_size_that_fits():
    got = select_fender(600.0)
    assert got["adequate"] is True
    assert got["rated_energy"] >= 600.0
    assert got["utilisation"] <= 1.0
    smaller = [h for h in CONE_FENDER.heights if h < got["height"]]
    assert all(CONE_FENDER.energy(h) < 600.0 for h in smaller)


def test_an_energy_beyond_the_family_says_so():
    got = select_fender(1e7)
    assert got["adequate"] is False
    assert got["height"] is None
    assert "two fenders" in got["note"]


def test_a_bigger_fender_reacts_harder_but_not_proportionally():
    small = select_fender(500.0)
    big = select_fender(4000.0)
    assert big["reaction"] > small["reaction"]
    assert (big["reaction"] / small["reaction"]
            < big["rated_energy"] / small["rated_energy"])


def test_the_family_validates_itself():
    with pytest.raises(ValueError):
        FenderFamily(reference_height=0.0)
    with pytest.raises(ValueError):
        FenderFamily(reference_energy=0.0)
    with pytest.raises(ValueError):
        FenderFamily(deflection=1.0)
    with pytest.raises(ValueError):
        FenderFamily(heights=())


def test_selection_refuses_a_non_positive_energy():
    with pytest.raises(ValueError):
        select_fender(0.0)


# ---------------------------------------------------------------------------
# Hull pressure
# ---------------------------------------------------------------------------


def test_pressure_is_reaction_over_area():
    got = hull_pressure(1000.0, 2.0, 2.5, "container")
    assert got["area"] == pytest.approx(5.0)
    assert got["pressure"] == pytest.approx(200.0)


def test_a_wider_panel_lowers_the_pressure():
    narrow = hull_pressure(1000.0, 1.0, 2.0, "container")["pressure"]
    wide = hull_pressure(1000.0, 3.0, 2.0, "container")["pressure"]
    assert wide < narrow


def test_a_tanker_takes_far_less_than_a_container_ship():
    assert (HULL_PRESSURE_LIMIT["tanker_large"]
            < HULL_PRESSURE_LIMIT["container"])
    hard = hull_pressure(1000.0, 2.0, 2.5, "container")
    soft = hull_pressure(1000.0, 2.0, 2.5, "tanker_large")
    assert hard["acceptable"] and not soft["acceptable"]


def test_the_required_area_is_reported_when_it_fails():
    got = hull_pressure(2000.0, 1.0, 1.0, "tanker_large")
    assert got["acceptable"] is False
    assert got["required_area"] == pytest.approx(2000.0 / 150.0)
    assert got["required_area"] > got["area"]


def test_pressure_validates_its_inputs():
    with pytest.raises(ValueError):
        hull_pressure(0.0, 2.0, 2.0)
    with pytest.raises(ValueError):
        hull_pressure(1000.0, 0.0, 2.0)
    with pytest.raises(ValueError):
        hull_pressure(1000.0, 2.0, 2.0, "hovercraft")


# ---------------------------------------------------------------------------
# Spacing
# ---------------------------------------------------------------------------


def test_a_straight_midbody_cannot_reach_between_fenders(ship):
    """No curvature, so geometry cannot bind however wide the gap."""
    got = fender_spacing(ship, 30.0, 0.9)
    assert got["midbody"] is True
    assert got["geometric_limit"] == math.inf
    assert got["governing"] == "vessel length"


def test_a_curved_bow_can(ship):
    got = fender_spacing(ship, 30.0, 0.9, bow_radius=24.0)
    assert got["midbody"] is False
    assert math.isfinite(got["geometric_limit"])
    assert got["geometric_limit"] < 30.0
    assert got["acceptable"] is False


def test_more_standoff_allows_wider_spacing(ship):
    tight = fender_spacing(ship, 10.0, 0.6, bow_radius=24.0)["geometric_limit"]
    proud = fender_spacing(ship, 10.0, 1.5, bow_radius=24.0)["geometric_limit"]
    assert proud > tight


def test_the_practical_rule_follows_the_smallest_vessel(ship, feeder):
    """It exists so the smallest ship reaches two fenders, not the largest."""
    alone = fender_spacing(ship, 20.0, 0.9)
    mixed = fender_spacing(ship, 20.0, 0.9, smallest_vessel=feeder)
    assert mixed["practical_limit"] < alone["practical_limit"]
    assert mixed["reference_vessel"] == feeder.name


def test_spacing_validates_its_inputs(ship):
    with pytest.raises(ValueError):
        fender_spacing(ship, 0.0, 0.9)
    with pytest.raises(ValueError):
        fender_spacing(ship, 10.0, 0.0)
    with pytest.raises(ValueError):
        fender_spacing(ship, 10.0, 0.9, clearance=-1.0)
    with pytest.raises(ValueError):
        fender_spacing(ship, 10.0, 0.9, bow_radius=0.0)


# ---------------------------------------------------------------------------
# The whole berth
# ---------------------------------------------------------------------------


def test_a_reasonable_berth_passes_every_check(ship, feeder):
    got = design_berth(ship, velocity=0.15, vessel_class="container",
                       depth=17.0, smallest_vessel=feeder,
                       panel_aspect=(1.4, 2.2))
    assert got.adequate is True
    assert got.energy == pytest.approx(got.abnormal["energy"])


def test_the_design_energy_is_the_abnormal_one(ship):
    got = design_berth(ship, velocity=0.15)
    assert got.energy > got.normal["energy"]


def test_a_narrow_panel_fails_on_hull_pressure(ship):
    got = design_berth(ship, velocity=0.15, vessel_class="tanker_large",
                       panel_aspect=(0.6, 1.0))
    assert got.pressure["acceptable"] is False
    assert got.adequate is False
    assert "side shell" in " ".join(got.notes)


def test_wide_spacing_fails_and_says_where(ship, feeder):
    got = design_berth(ship, velocity=0.15, spacing=60.0,
                       smallest_vessel=feeder)
    assert got.spacing["acceptable"] is False
    assert got.adequate is False
    assert "between them" in " ".join(got.notes)


def test_the_velocity_defaults_from_the_table(ship):
    got = design_berth(ship, condition="difficult_exposed")
    assert got.velocity == pytest.approx(
        BERTHING_VELOCITY["difficult_exposed"]["large"])
    assert "indicative value" in " ".join(got.notes)


def test_an_oversized_fender_is_flagged(ship):
    """A fender at a third of its rating is stiff, and the hull pays."""
    got = design_berth(ship, velocity=0.02)
    if got.fender["utilisation"] < 0.5:
        assert "oversized" in " ".join(got.notes)


def test_the_notes_keep_the_catalogue_caveat(ship):
    got = design_berth(ship, velocity=0.15)
    assert "not a catalogue" in " ".join(got.notes)
