"""Storm surge components and flood mapping."""
import math

import numpy as np
import pytest

from pyCoastal.applications.surge import (
    STANDARD_PRESSURE,
    StormConditions,
    barometric_setup,
    bathtub_flood,
    flood_depths,
    flood_volume,
    flooded_area,
    inundation_limit,
    isolated_low_ground,
    stockdon_runup,
    surf_zone_setup,
    total_water_level,
    wind_setup,
    wind_setup_profile,
)

G = 9.81


# --------------------------------------------------------------------------
# Barometric setup
# --------------------------------------------------------------------------

def test_barometric_setup_is_about_one_centimetre_per_hectopascal():
    """The classic rule of thumb, and a good check on the units."""
    drop_hpa = 50.0
    rise = barometric_setup(STANDARD_PRESSURE - drop_hpa * 100.0)
    assert rise / drop_hpa == pytest.approx(0.01, rel=0.05)


def test_barometric_setup_closed_form():
    assert barometric_setup(95000.0) == pytest.approx(
        (STANDARD_PRESSURE - 95000.0) / (1025.0 * G)
    )


def test_no_pressure_drop_gives_no_setup():
    assert barometric_setup(STANDARD_PRESSURE) == pytest.approx(0.0)


def test_negative_pressure_is_rejected():
    with pytest.raises(ValueError):
        barometric_setup(-1.0)


# --------------------------------------------------------------------------
# Wind setup
# --------------------------------------------------------------------------

def test_wind_setup_closed_form():
    W, F, d, k = 40.0, 100e3, 20.0, 3.3e-6
    assert wind_setup(W, F, d, k=k) == pytest.approx(k * W**2 * F / (G * d))


def test_wind_setup_scales_with_the_square_of_wind_speed():
    a = wind_setup(20.0, 100e3, 20.0)
    b = wind_setup(40.0, 100e3, 20.0)
    assert b / a == pytest.approx(4.0)


def test_shallow_shelves_set_up_far_more_than_deep_ones():
    """Setup goes as 1/d, which is why wide shallow shelves flood badly."""
    shallow = wind_setup(40.0, 100e3, 10.0)
    deep = wind_setup(40.0, 100e3, 40.0)
    assert shallow == pytest.approx(4.0 * deep)


def test_oblique_wind_sets_up_less():
    head_on = wind_setup(40.0, 100e3, 20.0, wind_angle=0.0)
    oblique = wind_setup(40.0, 100e3, 20.0, wind_angle=math.radians(60))
    assert oblique == pytest.approx(0.5 * head_on)


def test_return_flow_increases_setup():
    plain = wind_setup(40.0, 100e3, 20.0, return_flow=1.0)
    with_flow = wind_setup(40.0, 100e3, 20.0, return_flow=1.3)
    assert with_flow == pytest.approx(1.3 * plain)


@pytest.mark.parametrize(
    "kwargs", [{"wind_speed": -1.0}, {"fetch": 0.0}, {"depth": 0.0}, {"return_flow": 0.5}]
)
def test_invalid_wind_setup_inputs_are_rejected(kwargs):
    base = {"wind_speed": 40.0, "fetch": 100e3, "depth": 20.0}
    with pytest.raises(ValueError):
        wind_setup(**{**base, **kwargs})


def test_setup_accumulates_landward_along_a_profile():
    depths = np.linspace(50.0, 10.0, 100)
    eta = wind_setup_profile(depths, dx=1000.0, wind_speed=40.0)
    assert eta[0] == 0.0
    assert all(a <= b for a, b in zip(eta, eta[1:]))
    assert eta[-1] > 0


def test_profile_integration_matches_the_closed_form_at_constant_depth():
    """With no depth variation the two must agree, bar the eta feedback."""
    depth, fetch, n = 20.0, 100e3, 400
    depths = np.full(n, depth)
    dx = fetch / (n - 1)
    numeric = wind_setup_profile(depths, dx, 40.0)[-1]
    closed = wind_setup(40.0, fetch, depth)
    # The integration carries setup into the local depth, so it sits slightly low.
    assert 0.8 * closed < numeric < closed


def test_profile_setup_is_damped_by_its_own_depth_feedback():
    """Setup deepens the water, which slows further setup."""
    depths = np.full(200, 8.0)
    eta = wind_setup_profile(depths, dx=500.0, wind_speed=45.0)
    naive = wind_setup(45.0, 500.0 * 199, 8.0)
    assert eta[-1] < naive


def test_a_deeper_shelf_sets_up_less_over_the_same_fetch():
    dx = 1000.0
    shallow = wind_setup_profile(np.full(100, 10.0), dx, 40.0)[-1]
    deep = wind_setup_profile(np.full(100, 40.0), dx, 40.0)[-1]
    assert deep < shallow


@pytest.mark.parametrize(
    "depths,dx", [(np.array([10.0]), 100.0), (np.array([10.0, -5.0]), 100.0)]
)
def test_invalid_profiles_are_rejected(depths, dx):
    with pytest.raises(ValueError):
        wind_setup_profile(depths, dx, 40.0)


# --------------------------------------------------------------------------
# Wave setup and runup
# --------------------------------------------------------------------------

def test_surf_zone_setup_is_a_quarter_of_the_breaking_height():
    assert surf_zone_setup(4.0, gamma=0.8) == pytest.approx(5 / 16 * 0.8 * 4.0)


def test_surf_zone_setup_rejects_a_nonpositive_height():
    with pytest.raises(ValueError):
        surf_zone_setup(0.0)


def test_stockdon_splits_setup_from_swash():
    out = stockdon_runup(Hm0=3.0, Tp=12.0, beach_slope=0.05)
    assert out["R2"] == pytest.approx(out["setup"] + out["swash"])
    assert out["setup"] > 0 and out["swash"] > 0


def test_runup_grows_on_steeper_beaches():
    flat = stockdon_runup(3.0, 12.0, 0.01)["R2"]
    steep = stockdon_runup(3.0, 12.0, 0.10)["R2"]
    assert steep > flat


def test_runup_grows_with_wave_height_and_period():
    base = stockdon_runup(2.0, 10.0, 0.05)["R2"]
    bigger = stockdon_runup(4.0, 10.0, 0.05)["R2"]
    longer = stockdon_runup(2.0, 16.0, 0.05)["R2"]
    assert bigger > base and longer > base


def test_runup_matches_its_published_form():
    Hm0, Tp, beta = 3.0, 12.0, 0.05
    L0 = G * Tp**2 / (2 * math.pi)
    setup = 0.35 * beta * math.sqrt(Hm0 * L0)
    swash = math.sqrt(Hm0 * L0 * (0.563 * beta**2 + 0.004))
    assert stockdon_runup(Hm0, Tp, beta)["R2"] == pytest.approx(
        1.1 * (setup + 0.5 * swash)
    )


@pytest.mark.parametrize("kwargs", [{"Hm0": 0.0}, {"Tp": 0.0}, {"beach_slope": 0.0}])
def test_invalid_runup_inputs_are_rejected(kwargs):
    base = {"Hm0": 2.0, "Tp": 10.0, "beach_slope": 0.05}
    with pytest.raises(ValueError):
        stockdon_runup(**{**base, **kwargs})


# --------------------------------------------------------------------------
# Total water level
# --------------------------------------------------------------------------

def test_still_water_level_is_the_sum_of_its_sustained_components():
    storm = StormConditions(
        wind_speed=40.0, central_pressure=95000.0, tide=0.5,
        Hm0=5.0, Tp=12.0, sea_level_rise=0.3,
    )
    out = total_water_level(storm)
    assert out["still_water_level"] == pytest.approx(
        out["tide"] + out["sea_level_rise"] + out["barometric_setup"]
        + out["wind_setup"] + out["wave_setup"]
    )


def test_total_water_level_adds_runup_on_top_of_still_water():
    out = total_water_level(StormConditions())
    assert out["total_water_level"] == pytest.approx(
        out["still_water_level"] + out["runup_R2"]
    )
    assert out["runup_R2"] > 0


def test_sea_level_rise_raises_the_level_one_for_one():
    base = total_water_level(StormConditions(sea_level_rise=0.0))
    raised = total_water_level(StormConditions(sea_level_rise=0.5))
    assert raised["still_water_level"] - base["still_water_level"] == pytest.approx(0.5)


def test_a_stronger_storm_gives_a_higher_level():
    weak = total_water_level(StormConditions(wind_speed=25.0, central_pressure=100000.0))
    strong = total_water_level(StormConditions(wind_speed=55.0, central_pressure=92000.0))
    assert strong["still_water_level"] > weak["still_water_level"]


def test_breaking_height_is_depth_limited():
    """A big offshore wave cannot survive a shallow shelf."""
    out = total_water_level(StormConditions(Hm0=9.0, shelf_depth=4.0), breaker_index=0.78)
    assert out["breaking_height"] == pytest.approx(0.78 * 4.0)


def test_shelf_profile_can_replace_the_representative_depth():
    storm = StormConditions(wind_speed=45.0, fetch=100e3, shelf_depth=20.0)
    depths = np.linspace(60.0, 8.0, 150)
    out = total_water_level(storm, shelf_depths=depths, dx=100e3 / 149)
    assert out["wind_setup"] > 0
    assert out["wind_setup"] != total_water_level(storm)["wind_setup"]


def test_shelf_depths_without_spacing_is_an_error():
    with pytest.raises(ValueError, match="dx"):
        total_water_level(StormConditions(), shelf_depths=np.full(10, 20.0))


def test_invalid_storms_are_rejected():
    with pytest.raises(ValueError):
        StormConditions(wind_speed=-5.0)
    with pytest.raises(ValueError):
        StormConditions(Hm0=0.0)


# --------------------------------------------------------------------------
# Profile inundation
# --------------------------------------------------------------------------

def test_inundation_limit_on_a_uniform_slope():
    x = np.linspace(0.0, 1000.0, 1001)
    z = -2.0 + 0.01 * x            # crosses 3 m at x = 500
    assert inundation_limit(x, z, level=3.0) == pytest.approx(500.0, abs=1.0)


def test_a_higher_level_floods_further_inland():
    x = np.linspace(0.0, 1000.0, 1001)
    z = -2.0 + 0.01 * x
    assert inundation_limit(x, z, 4.0) > inundation_limit(x, z, 2.0)


def test_a_dune_stops_the_water_until_it_is_overtopped():
    """Low ground behind an intact dune is not flooded, even though it lies
    below the level: the water cannot get there."""
    x = np.linspace(0.0, 1000.0, 1001)
    z = -2.0 + 0.01 * x
    z[(x > 300) & (x < 360)] = 6.0        # a dune crest at 6 m

    assert inundation_limit(x, z, 5.0) == pytest.approx(300.0, abs=5.0)
    # The ground just behind the dune is below 5 m but stays dry.
    behind = (x > 360) & (x < 500)
    assert (z[behind] < 5.0).all()

    # Raise the level over the dune crest and the water runs on inland.
    assert inundation_limit(x, z, 7.0) > 400.0


def test_nothing_floods_when_the_land_starts_above_the_level():
    x = np.linspace(0.0, 100.0, 101)
    z = np.full_like(x, 5.0)
    assert inundation_limit(x, z, 1.0) == pytest.approx(0.0)


def test_everything_floods_when_the_level_tops_the_profile():
    x = np.linspace(0.0, 100.0, 101)
    z = np.full_like(x, 1.0)
    assert inundation_limit(x, z, 5.0) == pytest.approx(100.0)


def test_mismatched_profile_arrays_are_rejected():
    with pytest.raises(ValueError):
        inundation_limit(np.arange(5.0), np.arange(4.0), 1.0)


def test_flood_depths_are_never_negative():
    z = np.array([-1.0, 0.0, 1.0, 2.0, 3.0])
    d = flood_depths(z, level=1.5)
    assert (d >= 0).all()
    np.testing.assert_allclose(d, [2.5, 1.5, 0.5, 0.0, 0.0])


# --------------------------------------------------------------------------
# Flood mapping with connectivity
# --------------------------------------------------------------------------

def test_connected_flooding_leaves_sealed_basins_dry():
    """The point of the connectivity check: a bathtub map would flood this."""
    terrain = np.full((20, 20), 5.0)
    terrain[:5, :] = -1.0          # the sea, along the x = 0 edge
    terrain[12:16, 8:12] = -2.0    # a deep basin, walled off by 5 m ground

    flooded = bathtub_flood(terrain, level=1.0)
    assert flooded[:5, :].all()
    assert not flooded[12:16, 8:12].any()

    # The naive threshold would have flooded it.
    assert (terrain[12:16, 8:12] <= 1.0).all()


def test_isolated_low_ground_is_exactly_the_difference():
    terrain = np.full((20, 20), 5.0)
    terrain[:5, :] = -1.0
    terrain[12:16, 8:12] = -2.0

    isolated = isolated_low_ground(terrain, level=1.0)
    assert isolated[12:16, 8:12].all()
    assert not isolated[:5, :].any()


def test_a_breached_barrier_lets_the_water_through():
    """Seeded from the sea edge only, as a real coastal DEM would be."""
    terrain = np.full((20, 20), 5.0)
    terrain[:5, :] = -1.0
    terrain[5:8, :] = 3.0          # a barrier
    terrain[8:, :] = 0.0           # low ground behind it

    sea = np.zeros_like(terrain, dtype=bool)
    sea[0, :] = True               # the sea enters along x = 0 only

    assert not bathtub_flood(terrain, level=2.0, seed=sea)[8:, :].any()
    # Cut a gap in the barrier and the same level now gets behind it.
    terrain[5:8, 9:11] = 0.0
    assert bathtub_flood(terrain, level=2.0, seed=sea)[8:, :].any()


def test_the_default_seed_lets_water_in_from_every_open_edge():
    """Documented default: without a seed, any low edge cell is an entry."""
    terrain = np.full((20, 20), 5.0)
    terrain[:5, :] = -1.0
    terrain[5:8, :] = 3.0
    terrain[8:, :] = 0.0           # touches the far and side edges

    sea = np.zeros_like(terrain, dtype=bool)
    sea[0, :] = True

    assert bathtub_flood(terrain, level=2.0)[8:, :].any()
    assert not bathtub_flood(terrain, level=2.0, seed=sea)[8:, :].any()


def test_higher_levels_flood_at_least_as_much():
    rng = np.random.default_rng(0)
    terrain = rng.normal(2.0, 1.5, size=(40, 40))
    terrain[0, :] = -5.0
    areas = [bathtub_flood(terrain, lvl).sum() for lvl in (0.0, 1.0, 2.0, 3.0)]
    assert all(a <= b for a, b in zip(areas, areas[1:]))


def test_eight_connectivity_floods_at_least_as_much_as_four():
    rng = np.random.default_rng(1)
    terrain = rng.normal(2.0, 1.5, size=(40, 40))
    terrain[0, :] = -5.0
    four = bathtub_flood(terrain, 2.0, connectivity=4).sum()
    eight = bathtub_flood(terrain, 2.0, connectivity=8).sum()
    assert eight >= four


def test_a_custom_seed_controls_where_the_sea_enters():
    terrain = np.full((10, 10), 0.0)
    seed = np.zeros_like(terrain, dtype=bool)
    seed[0, 0] = True
    flooded = bathtub_flood(terrain, level=1.0, seed=seed)
    assert flooded.all()          # flat ground, so it spreads everywhere

    # With no wet seed cell nothing floods.
    high = np.full((10, 10), 9.0)
    assert not bathtub_flood(high, level=1.0).any()


def test_area_and_volume_use_the_cell_size():
    terrain = np.full((10, 10), 0.0)
    terrain[0, :] = -1.0
    flooded = bathtub_flood(terrain, level=1.0)
    assert flooded_area(flooded, dx=5.0) == pytest.approx(flooded.sum() * 25.0)

    volume = flood_volume(terrain, flooded, level=1.0, dx=5.0)
    expected = (np.maximum(1.0 - terrain, 0.0) * flooded).sum() * 25.0
    assert volume == pytest.approx(expected)


@pytest.mark.parametrize("bad", [np.zeros(5), np.zeros((2, 2, 2))])
def test_non_2d_terrain_is_rejected(bad):
    with pytest.raises(ValueError):
        bathtub_flood(bad, level=1.0)


def test_bad_connectivity_is_rejected():
    with pytest.raises(ValueError):
        bathtub_flood(np.zeros((5, 5)), level=1.0, connectivity=6)


def test_seed_shape_must_match_terrain():
    with pytest.raises(ValueError):
        bathtub_flood(np.zeros((5, 5)), level=1.0, seed=np.zeros((4, 4), dtype=bool))
