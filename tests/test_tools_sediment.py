"""Sediment transport formulae: closed-form checks and physical scaling."""
import math

import numpy as np
import pytest

from pyCoastal.tools import sediment_transport as st


def test_shields_parameter_closed_form():
    tau, rho_s, rho, d = 1.5, 2650.0, 1025.0, 0.0002
    expected = tau / ((rho_s - rho) * 9.81 * d)
    assert st.shields_parameter(tau, rho_s, rho, d) == pytest.approx(expected)


def test_shields_parameter_is_linear_in_bed_shear_stress():
    args = (2650.0, 1025.0, 0.0002)
    assert st.shields_parameter(2.0, *args) == pytest.approx(
        2 * st.shields_parameter(1.0, *args)
    )


def test_shields_parameter_falls_with_coarser_grains():
    fine = st.shields_parameter(1.0, 2650.0, 1025.0, 0.0001)
    coarse = st.shields_parameter(1.0, 2650.0, 1025.0, 0.01)
    assert fine > coarse


def test_einstein_bedload_closed_form():
    tau_star, d, s = 0.08, 0.0005, 2.65
    expected = 8 * math.sqrt(9.81 * (s - 1) * d**3) * tau_star**1.5
    assert st.einstein_bedload(tau_star, d, s) == pytest.approx(expected)


def test_einstein_bedload_vanishes_at_zero_shear():
    assert st.einstein_bedload(0.0, 0.0005, 2.65) == pytest.approx(0.0)


def test_izbash_current_closed_form():
    rho_s, rho, d = 2650.0, 1025.0, 0.05
    expected = 1.7 * math.sqrt((rho_s / rho - 1) * 9.81 * d)
    assert st.izbash_current(rho_s, rho, d) == pytest.approx(expected)


def test_izbash_critical_velocity_grows_with_stone_size():
    small = st.izbash_current(2650.0, 1025.0, 0.01)
    large = st.izbash_current(2650.0, 1025.0, 1.0)
    assert large > small


def test_cerc_transport_vanishes_at_normal_and_parallel_incidence():
    assert st.cerc_transport(1000.0, 0.0) == pytest.approx(0.0, abs=1e-12)
    assert st.cerc_transport(1000.0, np.pi / 2) == pytest.approx(0.0, abs=1e-9)


def test_cerc_transport_peaks_near_45_degrees():
    """sin(a)cos(a) is maximal at 45 degrees."""
    angles = np.deg2rad([10, 30, 45, 60, 80])
    q = [st.cerc_transport(1000.0, a) for a in angles]
    assert np.argmax(q) == 2


def test_cerc_transport_reverses_with_incidence_direction():
    assert st.cerc_transport(1000.0, -np.pi / 6) == pytest.approx(
        -st.cerc_transport(1000.0, np.pi / 6)
    )


def test_bijker_bedload_combines_wave_and_current_stress():
    """Adding wave stress must increase transport over the current-only case."""
    current_only = st.bijker_bedload(0.0, 1.0, 2650.0, 1025.0, 0.0002)
    combined = st.bijker_bedload(2.0, 1.0, 2650.0, 1025.0, 0.0002)
    assert combined > current_only


def test_van_rijn_transport_increases_with_excess_velocity():
    args = (5.0, 0.0002, 2650.0, 1025.0)
    assert st.van_rijn_bedload(1.2, *args) > st.van_rijn_bedload(0.4, *args)
    assert st.van_rijn_suspended(1.2, *args) > st.van_rijn_suspended(0.4, *args)


def test_bagnold_scales_with_wave_height_squared():
    a = st.bagnold_sediment(1.0, 3.0, 2650.0)
    b = st.bagnold_sediment(2.0, 3.0, 2650.0)
    assert b == pytest.approx(4 * a)
