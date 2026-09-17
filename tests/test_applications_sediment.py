"""Sediment and soil: material properties, mobility, and earth pressure."""

import math

import numpy as np
import pytest

from pyCoastal.applications.sediment import (
    GAMMA_W,
    SEDIMENTS,
    Sediment,
    bed_mobility,
    critical_shields,
    dimensionless_grain_size,
    earth_pressure_coefficient,
    fall_velocity,
    lateral_earth_force,
    lateral_earth_pressure,
    sediment,
    wave_orbital_velocity,
    wave_shields,
)


# ---------------------------------------------------------------------------
# The material
# ---------------------------------------------------------------------------


def test_unit_weights_are_consistent():
    """Saturated is dry plus the water in the voids; submerged is that less water."""
    for grains in SEDIMENTS.values():
        assert grains.saturated_unit_weight == pytest.approx(
            grains.dry_unit_weight + grains.porosity * GAMMA_W
        )
        assert grains.submerged_unit_weight == pytest.approx(
            grains.saturated_unit_weight - GAMMA_W
        )


def test_submerged_weight_is_about_half_the_saturated():
    """The buoyancy that makes a wet backfill push less hard, per unit soil."""
    sand = sediment("medium_sand")
    assert 0.45 < sand.submerged_unit_weight / sand.saturated_unit_weight < 0.55


def test_catalogue_is_ordered_by_grain_size_and_friction():
    order = ["silt", "very_fine_sand", "fine_sand", "medium_sand",
             "coarse_sand", "fine_gravel", "coarse_gravel", "rock_fill"]
    sizes = [SEDIMENTS[k].d50 for k in order]
    angles = [SEDIMENTS[k].friction_angle for k in order]
    assert all(b > a for a, b in zip(sizes, sizes[1:]))
    assert all(b >= a for a, b in zip(angles, angles[1:]))


def test_lookup_names_the_options():
    with pytest.raises(ValueError) as excinfo:
        sediment("unobtainium")
    assert "medium_sand" in str(excinfo.value)


def test_sediment_rejects_impossible_properties():
    for bad in (dict(d50=-1.0), dict(specific_gravity=0.5),
                dict(porosity=0.95), dict(friction_angle=75.0)):
        kwargs = dict(name="x", d50=0.2e-3)
        kwargs.update(bad)
        with pytest.raises(ValueError):
            Sediment(**kwargs)


def test_cohesive_flag_follows_cohesion():
    assert sediment("soft_clay").cohesive is True
    assert sediment("medium_sand").cohesive is False


# ---------------------------------------------------------------------------
# Mobility
# ---------------------------------------------------------------------------


def test_dimensionless_grain_size_matches_its_definition():
    grains = sediment("medium_sand")
    expected = grains.d50 * (9.81 * grains.relative_density / 1.19e-6 ** 2) ** (1 / 3)
    assert dimensionless_grain_size(grains) == pytest.approx(expected)


def test_grain_size_is_meaningless_for_clay():
    with pytest.raises(ValueError) as excinfo:
        dimensionless_grain_size("soft_clay")
    assert "cohesive" in str(excinfo.value)


def test_critical_shields_has_its_minimum_in_the_right_place():
    """The Shields curve dips near D* of about 17, then rises again."""
    sizes = np.logspace(-5, -1, 200)
    values = []
    for d in sizes:
        grains = Sediment("probe", d50=float(d))
        values.append((dimensionless_grain_size(grains), critical_shields(grains)))
    d_star = np.array([v[0] for v in values])
    theta = np.array([v[1] for v in values])
    at_minimum = d_star[int(np.argmin(theta))]
    assert 10.0 < at_minimum < 30.0


def test_critical_shields_tends_to_its_rough_limit():
    coarse = Sediment("very coarse", d50=0.2)
    assert critical_shields(coarse) == pytest.approx(0.055, abs=0.002)


def test_fall_velocity_rises_with_grain_size():
    order = ["silt", "fine_sand", "medium_sand", "coarse_sand", "fine_gravel"]
    speeds = [fall_velocity(k) for k in order]
    assert all(b > a for a, b in zip(speeds, speeds[1:]))


def test_fall_velocity_of_fine_sand_is_about_two_centimetres_a_second():
    """A number every coastal engineer carries around."""
    assert fall_velocity("fine_sand") == pytest.approx(0.021, abs=0.004)


def test_fall_velocity_approaches_stokes_for_the_finest_grains():
    """For small D* the Soulsby form tends towards the Stokes law.

    It is a fit across the whole range rather than an asymptotic expansion,
    so it lands within about a tenth of Stokes at silt sizes rather than on
    top of it. Close enough to confirm the branch, not close enough to
    claim it reduces to Stokes exactly.
    """
    fine = Sediment("very fine", d50=8e-6)
    stokes = (9.81 * fine.relative_density * fine.d50 ** 2) / (18 * 1.19e-6)
    assert fall_velocity(fine) == pytest.approx(stokes, rel=0.12)
    assert fall_velocity(fine) < stokes


def test_orbital_velocity_decays_with_depth():
    speeds = [wave_orbital_velocity(2.0, 9.0, h) for h in (5, 10, 20, 40)]
    assert all(b < a for a, b in zip(speeds, speeds[1:]))


def test_wave_shields_moves_fine_sand_and_not_gravel():
    fine = wave_shields("fine_sand", Hs=1.5, T=8.0, depth=10.0)
    coarse = wave_shields("coarse_gravel", Hs=1.5, T=8.0, depth=10.0)
    assert fine["mobile"] is True
    assert coarse["mobile"] is False
    assert fine["mobility"] > coarse["mobility"]


def test_bigger_waves_move_more_bed():
    calm = wave_shields("medium_sand", Hs=0.4, T=8.0, depth=15.0)
    storm = wave_shields("medium_sand", Hs=4.0, T=8.0, depth=15.0)
    assert storm["shields"] > calm["shields"]


def test_bed_mobility_names_the_regime():
    assert bed_mobility("fine_sand", 3.0, 9.0, 8.0)["regime"] == "live bed"
    assert bed_mobility("coarse_gravel", 0.3, 6.0, 25.0)["regime"] == "clear water"
    assert bed_mobility("soft_clay", 3.0, 9.0, 8.0)["regime"] == "cohesive"


def test_cohesive_bed_is_never_reported_as_mobile():
    result = bed_mobility("stiff_clay", 6.0, 12.0, 5.0)
    assert result["mobile"] is False
    assert "erodibility" in result["note"]


# ---------------------------------------------------------------------------
# Earth pressure coefficients
# ---------------------------------------------------------------------------


def test_rankine_active_and_passive_are_reciprocal():
    for phi in (25.0, 30.0, 35.0, 40.0):
        Ka = earth_pressure_coefficient(phi, "active")
        Kp = earth_pressure_coefficient(phi, "passive")
        assert Ka * Kp == pytest.approx(1.0)


def test_at_rest_is_jaky():
    for phi in (28.0, 33.0, 38.0):
        assert earth_pressure_coefficient(phi, "at_rest") == pytest.approx(
            1.0 - math.sin(math.radians(phi))
        )


def test_active_is_below_at_rest_is_below_passive():
    phi = 33.0
    Ka = earth_pressure_coefficient(phi, "active")
    K0 = earth_pressure_coefficient(phi, "at_rest")
    Kp = earth_pressure_coefficient(phi, "passive")
    assert Ka < K0 < Kp


def test_active_coefficient_falls_as_the_soil_gets_stronger():
    values = [earth_pressure_coefficient(phi, "active")
              for phi in (25, 30, 35, 40, 45)]
    assert all(b < a for a, b in zip(values, values[1:]))


def test_wall_friction_reduces_the_active_coefficient():
    smooth = earth_pressure_coefficient(33.0, "active", wall_friction=0.0)
    rough = earth_pressure_coefficient(33.0, "active", wall_friction=22.0)
    assert rough < smooth


def test_backslope_increases_the_active_coefficient():
    level = earth_pressure_coefficient(33.0, "active")
    sloping = earth_pressure_coefficient(33.0, "active", backslope=15.0)
    assert sloping > level


def test_backslope_steeper_than_the_soil_is_refused():
    with pytest.raises(ValueError):
        earth_pressure_coefficient(30.0, "active", backslope=35.0)


def test_unknown_pressure_kind_is_refused():
    with pytest.raises(ValueError):
        earth_pressure_coefficient(33.0, "sideways")


# ---------------------------------------------------------------------------
# The pressure diagram
# ---------------------------------------------------------------------------


def test_dry_backfill_matches_the_closed_form():
    """A drained granular backfill is exactly 0.5 K gamma H^2 at H/3."""
    grains = sediment("medium_sand")
    H = 8.0
    result = lateral_earth_force(grains, H, water_table=H, kind="active")
    K = earth_pressure_coefficient(grains.friction_angle, "active")
    assert result["soil"] == pytest.approx(
        0.5 * K * grains.dry_unit_weight * H ** 2, rel=1e-4)
    assert result["water"] == pytest.approx(0.0)
    assert result["arm"] == pytest.approx(H / 3.0, rel=1e-3)


def test_saturated_backfill_splits_into_buoyant_soil_and_full_water():
    grains = sediment("medium_sand")
    H = 8.0
    result = lateral_earth_force(grains, H, water_table=0.0, kind="active")
    K = earth_pressure_coefficient(grains.friction_angle, "active")
    assert result["soil"] == pytest.approx(
        0.5 * K * grains.submerged_unit_weight * H ** 2, rel=1e-4)
    assert result["water"] == pytest.approx(0.5 * GAMMA_W * H ** 2, rel=1e-4)


def test_saturating_the_backfill_multiplies_the_force():
    """The result that decides whether a seawall needs a drain."""
    grains = sediment("medium_sand")
    H = 10.0
    drained = lateral_earth_force(grains, H, water_table=H)["total"]
    saturated = lateral_earth_force(grains, H, water_table=0.0)["total"]
    assert saturated > 2.5 * drained


def test_water_is_most_of_the_pressure_when_saturated():
    result = lateral_earth_force("medium_sand", 10.0, water_table=0.0)
    assert result["water_fraction"] > 0.6


def test_surcharge_adds_a_rectangle():
    """A uniform surcharge adds K q H, acting at mid height."""
    grains = sediment("medium_sand")
    H, q = 6.0, 20.0
    K = earth_pressure_coefficient(grains.friction_angle, "active")
    bare = lateral_earth_force(grains, H, water_table=H, surcharge=0.0)
    loaded = lateral_earth_force(grains, H, water_table=H, surcharge=q)
    assert loaded["soil"] - bare["soil"] == pytest.approx(K * q * H, rel=1e-4)


def test_at_rest_pushes_harder_than_active():
    active = lateral_earth_force("medium_sand", 9.0, 0.0, kind="active")
    at_rest = lateral_earth_force("medium_sand", 9.0, 0.0, kind="at_rest")
    assert at_rest["total"] > active["total"]


def test_stronger_backfill_pushes_less():
    forces = [lateral_earth_force(k, 9.0, 0.0)["total"]
              for k in ("fine_sand", "medium_sand", "coarse_sand", "fine_gravel")]
    assert all(b < a for a, b in zip(forces, forces[1:]))


def test_cohesion_cuts_the_top_of_the_diagram_off():
    """Soil cannot pull, so the tension zone is removed, not left negative."""
    diagram = lateral_earth_pressure("stiff_clay", 6.0, water_table=6.0)
    assert np.all(diagram["effective"] >= 0.0)
    assert diagram["effective"][0] == pytest.approx(0.0)


def test_pressure_diagram_rejects_nonsense():
    with pytest.raises(ValueError):
        lateral_earth_pressure("medium_sand", height=0.0)
    with pytest.raises(ValueError):
        lateral_earth_pressure("medium_sand", 5.0, water_table=-1.0)
    with pytest.raises(ValueError):
        lateral_earth_pressure("medium_sand", 5.0, surcharge=-5.0)


def test_force_equals_the_integral_of_its_own_diagram():
    result = lateral_earth_force("coarse_sand", 7.0, water_table=2.0, surcharge=15.0)
    diagram = result["diagram"]
    assert result["total"] == pytest.approx(
        float(np.trapezoid(diagram["total"], diagram["depth"])), rel=1e-9)
    assert result["soil"] + result["water"] == pytest.approx(result["total"])
