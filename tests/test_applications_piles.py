"""Morison wave loads on piles: kinematics, coefficients, loads and scour."""

import math

import numpy as np
import pytest

from pyCoastal.applications.piles import (
    RHO,
    design_monopile,
    drag_inertia_coefficients,
    integrate_load,
    keulegan_carpenter,
    morison_load_profile,
    morison_pile_load,
    phase_sweep,
    reynolds_number,
    scour_depth_pile,
    wave_kinematics,
)
from pyCoastal.tools.wave import dispersion


# ---------------------------------------------------------------------------
# Kinematics
# ---------------------------------------------------------------------------


def test_velocity_at_the_crest_matches_linear_theory():
    H, T, h = 4.0, 10.0, 20.0
    kin = wave_kinematics(H, T, h, [0.0], phase=0.0, stretching="none")
    L = dispersion(T, h)
    k, omega = 2 * math.pi / L, 2 * math.pi / T
    expected = 0.5 * H * omega * math.cosh(k * h) / math.sinh(k * h)
    assert kin["u"][0] == pytest.approx(expected)


def test_velocity_and_acceleration_are_a_quarter_cycle_apart():
    """Under the crest the velocity peaks and the acceleration vanishes."""
    crest = wave_kinematics(3.0, 9.0, 15.0, [-2.0], phase=0.0)
    quarter = wave_kinematics(3.0, 9.0, 15.0, [-2.0], phase=math.pi / 2)
    assert abs(crest["dudt"][0]) < 1e-9
    assert abs(quarter["u"][0]) < 1e-9
    assert crest["u"][0] > 0
    assert quarter["dudt"][0] > 0


def test_kinematics_decay_with_depth():
    kin = wave_kinematics(4.0, 10.0, 30.0, [0.0, -10.0, -20.0, -30.0],
                          phase=0.0, stretching="none")
    assert np.all(np.diff(kin["u"]) < 0)


def test_deep_water_kinematics_vanish_at_the_bed():
    kin = wave_kinematics(2.0, 5.0, 100.0, [-100.0], phase=0.0,
                          stretching="none")
    assert abs(kin["u"][0]) < 1e-3


def test_wheeler_stretching_maps_the_surface_to_zero():
    """At the instantaneous surface the stretched coordinate is zero."""
    H, T, h = 6.0, 12.0, 25.0
    kin = wave_kinematics(H, T, h, [3.0], phase=0.0, stretching="wheeler")
    assert kin["eta"] == pytest.approx(3.0)
    assert kin["z_eval"][0] == pytest.approx(0.0)


def test_wheeler_stretching_keeps_the_bed_at_the_bed():
    kin = wave_kinematics(6.0, 12.0, 25.0, [-25.0], phase=0.0,
                          stretching="wheeler")
    assert kin["z_eval"][0] == pytest.approx(-25.0)


def test_wheeler_is_gentler_than_extrapolating():
    """Extrapolating the cosh profile into the crest overstates the velocity."""
    H, T, h = 8.0, 12.0, 20.0
    z = [3.0]
    stretched = wave_kinematics(H, T, h, z, phase=0.0, stretching="wheeler")
    extrapolated = wave_kinematics(H, T, h, z, phase=0.0,
                                   stretching="extrapolate")
    assert stretched["u"][0] < extrapolated["u"][0]


def test_kinematics_are_zero_above_the_surface():
    kin = wave_kinematics(4.0, 10.0, 20.0, [5.0], phase=0.0)
    assert kin["u"][0] == 0.0
    assert kin["dudt"][0] == 0.0
    assert kin["wet"][0] is np.False_


def test_kinematics_reject_bad_inputs():
    with pytest.raises(ValueError):
        wave_kinematics(-1.0, 10.0, 20.0, [0.0])
    with pytest.raises(ValueError):
        wave_kinematics(4.0, 10.0, 20.0, [0.0], stretching="magic")


# ---------------------------------------------------------------------------
# Coefficients
# ---------------------------------------------------------------------------


def test_keulegan_carpenter_shrinks_as_the_pile_grows():
    small = keulegan_carpenter(6.0, 12.0, 25.0, 1.0)
    large = keulegan_carpenter(6.0, 12.0, 25.0, 10.0)
    assert small == pytest.approx(10.0 * large)


def test_reynolds_number_scales_with_diameter():
    a = reynolds_number(6.0, 12.0, 25.0, 2.0)
    b = reynolds_number(6.0, 12.0, 25.0, 4.0)
    assert b == pytest.approx(2.0 * a)


def test_rough_cylinders_take_more_drag():
    assert (drag_inertia_coefficients(10.0, rough=True)["Cd"]
            > drag_inertia_coefficients(10.0, rough=False)["Cd"])


def test_regimes_are_named_by_keulegan_carpenter():
    assert drag_inertia_coefficients(1.0)["regime"] == "inertia dominated"
    assert drag_inertia_coefficients(8.0)["regime"] == "mixed"
    assert drag_inertia_coefficients(40.0)["regime"] == "drag dominated"


def test_inertia_coefficient_falls_then_holds():
    values = [drag_inertia_coefficients(kc)["Cm"] for kc in (2, 6, 12, 30, 60)]
    assert values[0] == pytest.approx(2.0)
    assert all(b <= a + 1e-12 for a, b in zip(values, values[1:]))
    assert values[-1] >= 1.5


def test_coefficients_reject_a_zero_kc():
    with pytest.raises(ValueError):
        drag_inertia_coefficients(0.0)


# ---------------------------------------------------------------------------
# Morison load
# ---------------------------------------------------------------------------


def test_load_profile_matches_the_morison_equation():
    D, Cd, Cm = 2.0, 1.0, 2.0
    u, dudt = np.array([3.0]), np.array([0.5])
    out = morison_load_profile(D, u, dudt, Cd, Cm)
    assert out["drag"][0] == pytest.approx(0.5 * RHO * Cd * D * 9.0)
    assert out["inertia"][0] == pytest.approx(
        RHO * Cm * 0.25 * math.pi * D**2 * 0.5
    )
    assert out["total"][0] == pytest.approx(out["drag"][0] + out["inertia"][0])


def test_drag_keeps_the_sign_of_the_velocity():
    forward = morison_load_profile(2.0, [3.0], [0.0])["drag"][0]
    backward = morison_load_profile(2.0, [-3.0], [0.0])["drag"][0]
    assert forward == pytest.approx(-backward)
    assert forward > 0


def test_drag_is_quadratic_in_velocity():
    a = morison_load_profile(2.0, [1.0], [0.0])["drag"][0]
    b = morison_load_profile(2.0, [3.0], [0.0])["drag"][0]
    assert b == pytest.approx(9.0 * a)


def test_load_profile_rejects_bad_inputs():
    with pytest.raises(ValueError):
        morison_load_profile(0.0, [1.0], [0.0])
    with pytest.raises(ValueError):
        morison_load_profile(2.0, [1.0], [0.0], Cd=-1.0)


def test_integrate_load_matches_a_uniform_profile():
    z = np.linspace(-20.0, 0.0, 201)
    load = np.full_like(z, 100.0)
    out = integrate_load(z, load, mudline=-20.0)
    assert out["force"] == pytest.approx(2000.0)
    assert out["moment"] == pytest.approx(2000.0 * 10.0)
    assert out["arm"] == pytest.approx(10.0)


def test_integrate_load_arm_for_a_triangular_profile():
    """A load growing linearly from the bed acts at two thirds height."""
    z = np.linspace(-15.0, 0.0, 1501)
    load = (z + 15.0) * 10.0
    out = integrate_load(z, load, mudline=-15.0)
    assert out["arm"] == pytest.approx(10.0, rel=1e-3)


def test_integrate_load_validates_shapes():
    with pytest.raises(ValueError):
        integrate_load([0.0, 1.0], [1.0], mudline=0.0)
    with pytest.raises(ValueError):
        integrate_load([0.0], [1.0], mudline=0.0)


# ---------------------------------------------------------------------------
# Whole-pile load
# ---------------------------------------------------------------------------


def test_large_pile_is_inertia_dominated():
    big = morison_pile_load(8.0, 12.0, 13.0, 30.0, phase=math.pi / 2)
    assert big.inertia_fraction > 0.8


def test_small_pile_is_drag_dominated():
    thin = morison_pile_load(0.8, 12.0, 13.0, 30.0, phase=0.0)
    assert thin.inertia_fraction < 0.3


def test_inertia_load_scales_with_the_square_of_the_diameter():
    """At the acceleration peak the load is pure inertia, so it goes as D^2."""
    kwargs = dict(H=8.0, T=14.0, depth=40.0, phase=math.pi / 2, Cd=1.0, Cm=2.0)
    a = morison_pile_load(diameter=2.0, **kwargs)
    b = morison_pile_load(diameter=4.0, **kwargs)
    assert b.force == pytest.approx(4.0 * a.force, rel=1e-6)


def test_drag_load_scales_with_the_diameter():
    """Under the crest the load is pure drag, so it goes as D."""
    kwargs = dict(H=8.0, T=14.0, depth=40.0, phase=0.0, Cd=1.0, Cm=2.0)
    a = morison_pile_load(diameter=2.0, **kwargs)
    b = morison_pile_load(diameter=4.0, **kwargs)
    assert b.force == pytest.approx(2.0 * a.force, rel=1e-6)


def test_moment_arm_lies_within_the_water_column():
    load = morison_pile_load(4.0, 10.0, 12.0, 25.0, phase=math.pi / 3)
    assert 0.0 < load.arm < 25.0 + 0.5 * 10.0


def test_load_reverses_half_a_cycle_later():
    forward = morison_pile_load(4.0, 8.0, 11.0, 25.0, phase=math.pi / 4)
    backward = morison_pile_load(4.0, 8.0, 11.0, 25.0,
                                 phase=math.pi / 4 + math.pi)
    assert forward.force * backward.force < 0


def test_pile_warns_when_it_diffracts():
    """A fat pile in a short wave is outside the Morison equation."""
    load = morison_pile_load(30.0, 2.0, 5.0, 40.0, phase=0.0)
    assert load.diffraction_ratio > 0.2
    assert any("diffracts" in w for w in load.warnings)


def test_pile_warns_about_a_broken_wave():
    load = morison_pile_load(2.0, 9.0, 11.0, 10.0, phase=0.0)
    assert any("broken" in w for w in load.warnings)


def test_pile_warns_when_kinematics_are_extrapolated():
    load = morison_pile_load(3.0, 6.0, 11.0, 30.0, stretching="extrapolate")
    assert any("extrapolated" in w for w in load.warnings)


def test_pile_needs_enough_points():
    with pytest.raises(ValueError):
        morison_pile_load(3.0, 6.0, 11.0, 30.0, points=1)


def test_summary_reports_the_governing_numbers():
    load = morison_pile_load(6.0, 10.0, 12.0, 28.0, phase=1.0)
    text = load.summary()
    for phrase in ("Base shear", "Mudline moment", "Inertia share", "KC"):
        assert phrase in text


# ---------------------------------------------------------------------------
# Phase sweep
# ---------------------------------------------------------------------------


def test_phase_sweep_finds_the_peak_it_reports():
    sweep = phase_sweep(8.0, 12.0, 13.0, 30.0, phases=73)
    assert sweep["max_moment"] == pytest.approx(np.abs(sweep["moment"]).max())
    assert sweep["max_force"] == pytest.approx(np.abs(sweep["force"]).max())


def test_inertia_dominated_pile_peaks_away_from_the_crest():
    """The load follows the acceleration, which leads the crest."""
    sweep = phase_sweep(8.0, 12.0, 13.0, 30.0, phases=181)
    peak = math.degrees(sweep["phase_of_max_moment"])
    assert 20.0 < peak < 120.0


def test_drag_dominated_pile_peaks_near_the_crest():
    sweep = phase_sweep(0.8, 12.0, 13.0, 30.0, phases=181)
    peak = math.degrees(sweep["phase_of_max_moment"])
    assert peak < 30.0 or peak > 330.0


def test_phase_sweep_needs_enough_samples():
    with pytest.raises(ValueError):
        phase_sweep(4.0, 6.0, 10.0, 20.0, phases=2)


# ---------------------------------------------------------------------------
# Scour
# ---------------------------------------------------------------------------


def test_no_wave_scour_below_the_threshold():
    result = scour_depth_pile(5.0, KC=4.0)
    assert result["depth"] == 0.0
    assert result["no_scour"] is True


def test_wave_scour_grows_with_kc_towards_the_current_limit():
    ratios = [scour_depth_pile(5.0, kc)["ratio"] for kc in (8, 20, 60, 400)]
    assert all(b > a for a, b in zip(ratios, ratios[1:]))
    assert ratios[-1] < 1.3
    assert ratios[-1] == pytest.approx(1.3, rel=0.02)


def test_current_scour_is_one_point_three_diameters():
    result = scour_depth_pile(6.0, KC=10.0, current_only=True)
    assert result["depth"] == pytest.approx(1.3 * 6.0)
    assert result["standard_deviation"] == pytest.approx(0.7 * 6.0)


def test_scour_scales_with_diameter():
    a = scour_depth_pile(2.0, KC=30.0)["depth"]
    b = scour_depth_pile(6.0, KC=30.0)["depth"]
    assert b == pytest.approx(3.0 * a)


def test_scour_validates_its_inputs():
    with pytest.raises(ValueError):
        scour_depth_pile(0.0, KC=10.0)
    with pytest.raises(ValueError):
        scour_depth_pile(2.0, KC=0.0)


# ---------------------------------------------------------------------------
# The whole design
# ---------------------------------------------------------------------------


def test_design_monopile_reports_the_worst_not_the_crest():
    result = design_monopile(8.0, 12.0, 13.0, 30.0)
    assert abs(result["load"].moment) >= abs(result["crest_load"].moment)
    assert result["crest_underestimate"] > 0.0
    assert any("crest" in w for w in result["load"].warnings)


def test_design_monopile_agrees_with_its_own_sweep():
    result = design_monopile(6.0, 10.0, 12.0, 28.0)
    assert abs(result["load"].moment) == pytest.approx(
        result["sweep"]["max_moment"], rel=1e-9
    )


def test_design_monopile_does_not_warn_for_a_drag_dominated_pile():
    """A thin pile does peak at the crest, so there is nothing to flag."""
    result = design_monopile(0.6, 10.0, 12.0, 28.0)
    assert result["crest_underestimate"] < 0.02
    assert not any("crest" in w for w in result["load"].warnings)
