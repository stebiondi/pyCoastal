"""Wave kinematics and spectra, checked against analytic limits."""
import numpy as np
import pytest

from pyCoastal.tools import wave


G = 9.81


def test_dispersion_satisfies_the_dispersion_relation():
    """The real check: omega^2 = g k tanh(k h) must hold for the returned L."""
    for T, h in [(8.0, 3.0), (10.0, 20.0), (6.0, 1.0), (12.0, 200.0)]:
        L = wave.dispersion(T, h)
        k = 2 * np.pi / L
        omega = 2 * np.pi / T
        residual = omega**2 - G * k * np.tanh(k * h)
        assert abs(residual) < 1e-3 * omega**2, f"T={T}, h={h}"


def test_deep_water_limit_approaches_the_airy_wavelength():
    """For h/L > 0.5, L -> L0 = g T^2 / 2pi."""
    T, h = 8.0, 200.0
    L0 = G * T**2 / (2 * np.pi)
    assert wave.dispersion(T, h) == pytest.approx(L0, rel=1e-3)


def test_shallow_water_limit_approaches_non_dispersive_celerity():
    """For h/L < 1/20, L -> T sqrt(g h)."""
    T, h = 60.0, 2.0
    assert wave.dispersion(T, h) == pytest.approx(T * np.sqrt(G * h), rel=0.02)


def test_wavelength_decreases_as_water_shoals():
    depths = [100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0]
    lengths = [wave.dispersion(10.0, h) for h in depths]
    assert all(a > b for a, b in zip(lengths, lengths[1:]))


def test_wave_number_is_consistent_with_wavelength():
    T, h = 9.0, 12.0
    assert wave.wave_number(T, h) == pytest.approx(2 * np.pi / wave.dispersion(T, h))


def test_surf_similarity_known_value():
    """xi = tan(beta) / sqrt(H/L0), computed by hand."""
    beta, H, T = np.arctan(0.1), 1.0, 8.0
    L0 = G * T**2 / (2 * np.pi)
    assert wave.surf_similarity(beta, H, T) == pytest.approx(0.1 / np.sqrt(1.0 / L0))


def test_surf_similarity_grows_on_steeper_slopes():
    mild = wave.surf_similarity(np.arctan(0.02), 1.0, 8.0)
    steep = wave.surf_similarity(np.arctan(0.20), 1.0, 8.0)
    assert steep > mild


@pytest.mark.parametrize(
    "slope,H,T,expected",
    [
        (0.01, 2.0, 6.0, "Spilling"),     # flat slope, steep wave
        (0.10, 1.0, 9.0, "Plunging"),
        (0.50, 0.5, 12.0, "Collapsing"),  # steep slope, long swell
    ],
)
def test_breaker_type_classification(slope, H, T, expected):
    assert wave.breaker_type(np.arctan(slope), H, T).startswith(expected)


def test_ursell_number_flags_the_nonlinear_regime():
    linear_U, linear_text = wave.ursell_number(0.05, 6.0, 30.0)
    nonlinear_U, nonlinear_text = wave.ursell_number(1.5, 14.0, 2.0)
    assert linear_U < 32 < nonlinear_U
    assert "Linear regime" in linear_text
    assert "Nonlinear regime" in nonlinear_text


def test_wave_setup_is_linear_in_breaker_height():
    assert wave.wave_setup(2.0) == pytest.approx(2 * wave.wave_setup(1.0))
    assert wave.wave_setup(1.0, gamma=0.8) == pytest.approx(5 / 16 * 0.8)


@pytest.mark.parametrize("spectrum", ["pm", "jonswap"])
def test_irregular_wave_record_has_the_requested_shape(spectrum):
    t, eta = wave.generate_irregular_wave(
        Hs=2.0, Tp=8.0, duration=600.0, dt=0.25, spectrum=spectrum
    )
    assert t.shape == eta.shape == (2400,)
    assert t[1] - t[0] == pytest.approx(0.25)


@pytest.mark.parametrize("spectrum", ["pm", "jonswap"])
def test_irregular_wave_recovers_the_target_significant_height(spectrum):
    """Hs = 4 sigma for a narrow-banded Gaussian sea."""
    t, eta = wave.generate_irregular_wave(
        Hs=2.0, Tp=8.0, duration=3600.0, dt=0.25, spectrum=spectrum
    )
    assert 4 * eta.std() == pytest.approx(2.0, rel=0.1)


def test_irregular_wave_is_zero_mean():
    t, eta = wave.generate_irregular_wave(Hs=1.5, Tp=7.0, duration=3600.0, dt=0.2)
    assert abs(eta.mean()) < 0.05 * 1.5


def test_unknown_spectrum_is_rejected():
    with pytest.raises(ValueError, match="pm.*jonswap"):
        wave.generate_irregular_wave(1.0, 8.0, 100.0, 0.5, spectrum="bretschneider")


def test_jonswap_peak_is_sharper_than_pierson_moskowitz():
    """The peak enhancement factor must concentrate variance near fp."""
    f = np.linspace(0.02, 0.5, 2000)
    Tp, Hs = 10.0, 3.0
    pm = wave._pm_spectrum(f, Tp)
    pm *= Hs**2 / (8 * 2 * np.sum(pm) * (f[1] - f[0]))
    js = wave._jonswap_spectrum(f, Tp, Hs)
    assert js.max() > pm.max()
