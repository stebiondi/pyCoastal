"""Armour sizing, run-up and wave force formulae."""
import math

import numpy as np
import pytest

from pyCoastal.tools import structural as sr


def test_hudson_dn50_closed_form():
    Hs, Delta, theta, Kd = 3.0, 1.585, math.atan(0.5), 4.0
    expected = Hs / (Delta * ((Kd / math.tan(theta)) ** (1 / 3)) / 1.27)
    assert sr.hudson_dn50(Hs, Delta, theta, Kd) == pytest.approx(expected)


def test_hudson_dn50_is_linear_in_wave_height():
    args = (1.585, math.atan(0.5), 4.0)
    assert sr.hudson_dn50(4.0, *args) == pytest.approx(2 * sr.hudson_dn50(2.0, *args))


def test_hudson_dn50_shrinks_for_better_interlocking():
    """A higher stability coefficient Kd permits smaller stone."""
    smooth = sr.hudson_dn50(3.0, 1.585, math.atan(0.5), Kd=2.0)
    interlocking = sr.hudson_dn50(3.0, 1.585, math.atan(0.5), Kd=16.0)
    assert interlocking < smooth


def test_hudson_dn50_shrinks_on_gentler_slopes():
    steep = sr.hudson_dn50(3.0, 1.585, math.atan(1.0), Kd=4.0)
    gentle = sr.hudson_dn50(3.0, 1.585, math.atan(0.25), Kd=4.0)
    assert gentle < steep


def test_hunt_runup_is_height_times_iribarren():
    H, L, beta = 1.5, 80.0, math.atan(0.1)
    xi = math.tan(beta) / math.sqrt(H / L)
    assert sr.hunt_runup(beta, H, L) == pytest.approx(H * xi)


def test_runup_grows_on_steeper_slopes():
    mild = sr.hunt_runup(math.atan(0.02), 1.5, 80.0)
    steep = sr.hunt_runup(math.atan(0.20), 1.5, 80.0)
    assert steep > mild


def test_stockdon_runup_is_positive_and_grows_with_wave_height():
    small = sr.stockdon_runup(1.0, 80.0, math.atan(0.05))
    large = sr.stockdon_runup(3.0, 80.0, math.atan(0.05))
    assert 0 < small < large


def test_goda_force_is_maximal_for_normal_incidence():
    head_on = sr.goda_wave_force(3.0, 9.0, 8.0, beta=0.0)
    oblique = sr.goda_wave_force(3.0, 9.0, 8.0, beta=math.radians(60))
    assert head_on > oblique


def test_goda_force_scales_with_the_square_of_wave_height():
    a = sr.goda_wave_force(1.0, 9.0, 8.0, beta=0.0)
    b = sr.goda_wave_force(2.0, 9.0, 8.0, beta=0.0)
    assert b == pytest.approx(4 * a)


def test_iribarren_weight_grows_with_the_cube_of_wave_height():
    args = (math.atan(0.3), 2650.0, 1025.0, 2.0, 1.0)
    assert sr.iribarren_stability(2.0, *args) == pytest.approx(
        8 * sr.iribarren_stability(1.0, *args)
    )


def test_iribarren_weight_is_positive_for_a_stable_slope():
    # Friction must exceed the down-slope component for the formula to be meaningful.
    assert sr.iribarren_stability(2.0, math.atan(0.3), 2650.0, 1025.0, 2.0, 1.0) > 0


def test_vandermeer_dn50_is_positive_and_grows_with_wave_height():
    kw = dict(Delta=1.585, P=0.4, N=3000, alpha=math.atan(0.25), xi_m=2.5)
    small = sr.vandermeer_dn50(Hs=1.0, **kw)
    large = sr.vandermeer_dn50(Hs=4.0, **kw)
    assert 0 < small < large


def test_vandermeer_uses_the_damage_level_not_the_wave_height():
    """S is the eroded-area damage number, and must enter as (S/sqrt(N))^0.2."""
    kw = dict(Hs=3.0, Delta=1.585, P=0.4, N=3000, alpha=math.atan(0.5), xi_m=2.2)
    expected = 3.0 / (1.585 * 6.2 * 0.4**0.18 * (2.0 / math.sqrt(3000)) ** 0.2 * 2.2**-0.5)
    assert sr.vandermeer_dn50(**kw, damage=2.0) == pytest.approx(expected)


def test_vandermeer_allowing_more_damage_permits_smaller_stone():
    kw = dict(Hs=3.0, Delta=1.585, P=0.4, N=3000, alpha=math.atan(0.5), xi_m=2.2)
    assert sr.vandermeer_dn50(**kw, damage=8.0) < sr.vandermeer_dn50(**kw, damage=2.0)


def test_vandermeer_requires_the_breaker_parameter():
    """It used to default to a leftover T = 1 s, undersizing stone 2.7 times."""
    with pytest.raises(TypeError):
        sr.vandermeer_dn50(Hs=3.0, Delta=1.585, P=0.4, N=3000, alpha=math.atan(0.5))


def test_vandermeer_wave_count_saturates():
    kw = dict(Hs=3.0, Delta=1.585, P=0.4, alpha=math.atan(0.5), xi_m=2.2)
    assert sr.vandermeer_dn50(N=7500, **kw) == pytest.approx(
        sr.vandermeer_dn50(N=50000, **kw)
    )
