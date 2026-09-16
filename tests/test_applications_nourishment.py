"""Beach nourishment simulator.

The central check is against the Pelnard-Considere (1956) analytical solution
for a rectangular fill, which the one-line model must reproduce when the
linearization behind that solution holds (small wave angles, shore-normal
incidence, constant wave height).
"""
import math

import numpy as np
import pytest

from pyCoastal.applications.nourishment import (
    KCERC_DEFAULT,
    NourishmentDesign,
    WaveClimate,
    SECONDS_PER_YEAR,
    cerc_coefficient,
    initial_planform,
    longshore_diffusivity,
    pelnard_considere,
    renourishment_schedule,
    simulate_nourishment,
)


# --------------------------------------------------------------------------
# Design geometry
# --------------------------------------------------------------------------

def test_placed_volume_is_planform_area_times_active_height():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=100.0, D=8.0, B=2.0)
    assert d.active_height == pytest.approx(10.0)
    assert d.placed_volume == pytest.approx(30.0 * 1100.0 * 10.0)


def test_initial_planform_has_the_design_width_over_the_full_section():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=100.0, center=2500.0)
    x = np.arange(0.0, 5001.0, 10.0)
    y = initial_planform(x, d)

    assert y[np.argmin(np.abs(x - 2500.0))] == pytest.approx(30.0)
    assert y[np.argmin(np.abs(x - 2100.0))] == pytest.approx(30.0)   # inside
    assert y[np.argmin(np.abs(x - 3050.0))] == pytest.approx(15.0)   # mid-taper
    assert y[np.argmin(np.abs(x - 500.0))] == pytest.approx(0.0)     # far field


def test_initial_planform_taper_is_linear():
    d = NourishmentDesign(length=400.0, berm_width=20.0, taper=200.0, center=1000.0)
    x = np.arange(0.0, 2001.0, 5.0)
    y = initial_planform(x, d)

    quarter = y[np.argmin(np.abs(x - 1250.0))]   # 50 m into a 200 m taper
    half = y[np.argmin(np.abs(x - 1300.0))]      # 100 m into the taper
    assert quarter == pytest.approx(15.0)
    assert half == pytest.approx(10.0)


def test_integrated_planform_matches_the_stated_placed_volume():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=100.0, center=2500.0)
    x = np.arange(0.0, 5001.0, 1.0)
    area = np.trapezoid(initial_planform(x, d), x)
    assert area * d.active_height == pytest.approx(d.placed_volume, rel=1e-3)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"length": -100.0},
        {"berm_width": 0.0},
        {"taper": -1.0},
        {"porosity": 1.0},
    ],
)
def test_invalid_designs_are_rejected(kwargs):
    with pytest.raises(ValueError):
        NourishmentDesign(**kwargs)


@pytest.mark.parametrize("kwargs", [{"Hb": 0.0}, {"T": -1.0}, {"Kcerc": 0.0}])
def test_invalid_climates_are_rejected(kwargs):
    with pytest.raises(ValueError):
        WaveClimate(**kwargs)


# --------------------------------------------------------------------------
# Transport coefficient and diffusivity
# --------------------------------------------------------------------------

def test_cerc_coefficient_closed_form():
    expected = 0.39 * math.sqrt(9.81 / 0.78) / (16.0 * 1.65)
    assert cerc_coefficient() == pytest.approx(expected)
    assert KCERC_DEFAULT == pytest.approx(expected)


def test_cerc_coefficient_falls_for_denser_sediment():
    assert cerc_coefficient(s=3.0) < cerc_coefficient(s=2.65)


def test_diffusivity_scales_with_wave_height_to_the_five_halves():
    d = NourishmentDesign()
    one = longshore_diffusivity(WaveClimate(Hb=1.0), d)
    two = longshore_diffusivity(WaveClimate(Hb=2.0), d)
    assert two / one == pytest.approx(2.0**2.5)


def test_diffusivity_falls_with_a_deeper_active_profile():
    c = WaveClimate()
    shallow = longshore_diffusivity(c, NourishmentDesign(D=4.0))
    deep = longshore_diffusivity(c, NourishmentDesign(D=16.0))
    assert deep < shallow


# --------------------------------------------------------------------------
# Analytical solution
# --------------------------------------------------------------------------

def test_pelnard_considere_at_t0_is_the_rectangular_fill():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=0.0, center=2500.0)
    x = np.arange(0.0, 5001.0, 10.0)
    y = pelnard_considere(x, 0.0, d, WaveClimate())

    assert y[np.argmin(np.abs(x - 2500.0))] == pytest.approx(30.0)
    assert y[np.argmin(np.abs(x - 500.0))] == pytest.approx(0.0)


def test_pelnard_considere_conserves_volume():
    """Diffusion spreads the fill but must not create or destroy sand."""
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=0.0, center=5000.0)
    c = WaveClimate()
    x = np.arange(-40000.0, 50001.0, 5.0)

    # Compare against the exact placed area. Trapezoidal integration of the
    # discontinuous t=0 step overshoots by half a cell at each jump, so it is
    # not itself an exact reference.
    exact = d.berm_width * d.length
    for years in (1.0, 5.0, 20.0):
        later = np.trapezoid(pelnard_considere(x, years * SECONDS_PER_YEAR, d, c), x)
        assert later == pytest.approx(exact, rel=2e-3)


def test_pelnard_considere_centre_width_decays_monotonically():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=0.0, center=5000.0)
    c = WaveClimate()
    x = np.array([5000.0])
    widths = [pelnard_considere(x, yr * SECONDS_PER_YEAR, d, c)[0] for yr in range(0, 11)]
    assert all(a >= b for a, b in zip(widths, widths[1:]))
    assert widths[-1] < widths[0]


def test_pelnard_considere_is_symmetric_about_the_fill_centre():
    d = NourishmentDesign(length=800.0, berm_width=25.0, taper=0.0, center=2500.0)
    x = np.arange(0.0, 5001.0, 10.0)
    y = pelnard_considere(x, 2.0 * SECONDS_PER_YEAR, d, WaveClimate())
    np.testing.assert_allclose(y, y[::-1], atol=1e-9)


# --------------------------------------------------------------------------
# Numerical solver against the analytical solution
# --------------------------------------------------------------------------

def test_simulation_reproduces_the_analytical_planform():
    """The one-line solver must match Pelnard-Considere where it is valid."""
    d = NourishmentDesign(
        length=2000.0, berm_width=30.0, taper=0.0, D=8.0, B=2.0, porosity=0.4
    )
    c = WaveClimate(Hb=1.0, alpha0=0.0)
    years = 3.0

    result = simulate_nourishment(
        d, c, duration=years * SECONDS_PER_YEAR, dx=10.0, n_outputs=13
    )
    analytic = pelnard_considere(result.x, result.times[-1], result.design, c)
    numeric = result.planforms[-1]

    # Compare where the signal is meaningful, in units of the placed width.
    assert np.abs(numeric - analytic).max() / d.berm_width < 0.05


def test_simulation_matches_analytical_centre_width_through_time():
    d = NourishmentDesign(length=2000.0, berm_width=30.0, taper=0.0)
    c = WaveClimate(Hb=1.0, alpha0=0.0)
    result = simulate_nourishment(
        d, c, duration=5.0 * SECONDS_PER_YEAR, dx=10.0, n_outputs=11
    )
    centre = np.argmin(np.abs(result.x - result.design.center))

    for t, planform in zip(result.times[1:], result.planforms[1:]):
        analytic = pelnard_considere(result.x, t, result.design, c)[centre]
        assert planform[centre] == pytest.approx(analytic, abs=0.05 * d.berm_width)


def test_simulation_conserves_sand_over_the_whole_domain():
    d = NourishmentDesign(length=1000.0, berm_width=30.0, taper=100.0)
    c = WaveClimate(Hb=1.0, alpha0=0.0)
    result = simulate_nourishment(
        d, c, duration=2.0 * SECONDS_PER_YEAR, dx=10.0, n_outputs=5
    )

    total = [np.trapezoid(p, result.x) for p in result.planforms]
    assert total[-1] == pytest.approx(total[0], rel=0.02)


# --------------------------------------------------------------------------
# Engineering outputs
# --------------------------------------------------------------------------

def test_retained_fraction_starts_at_one_and_decreases():
    d = NourishmentDesign(length=2000.0, berm_width=30.0, taper=100.0)
    result = simulate_nourishment(
        d, WaveClimate(), duration=10.0 * SECONDS_PER_YEAR, dx=20.0, n_outputs=11
    )
    frac = result.retained_fraction
    assert frac[0] == pytest.approx(1.0, rel=0.02)
    assert all(a >= b - 1e-9 for a, b in zip(frac, frac[1:]))
    assert frac[-1] < frac[0]


def test_longer_fills_last_disproportionately_longer():
    """Diffusive spreading gives a design life that scales roughly as L^2."""
    c = WaveClimate(Hb=1.0)
    lives = []
    for L in (2000.0, 4000.0):
        d = NourishmentDesign(length=L, berm_width=30.0, taper=100.0)
        r = simulate_nourishment(
            d, c, duration=40.0 * SECONDS_PER_YEAR, dx=50.0, n_outputs=81
        )
        lives.append(r.design_life())

    assert all(math.isfinite(v) for v in lives)
    assert 3.0 < lives[1] / lives[0] < 5.0


def test_bigger_waves_shorten_the_design_life():
    d = NourishmentDesign(length=3000.0, berm_width=30.0, taper=100.0)
    calm = simulate_nourishment(
        d, WaveClimate(Hb=0.7), duration=30.0 * SECONDS_PER_YEAR, dx=50.0, n_outputs=61
    ).design_life()
    stormy = simulate_nourishment(
        d, WaveClimate(Hb=1.5), duration=30.0 * SECONDS_PER_YEAR, dx=50.0, n_outputs=61
    ).design_life()
    assert stormy < calm


def test_design_life_is_infinite_when_the_threshold_is_never_reached():
    d = NourishmentDesign(length=20000.0, berm_width=30.0, taper=100.0)
    result = simulate_nourishment(
        d, WaveClimate(Hb=0.5), duration=1.0 * SECONDS_PER_YEAR, dx=50.0, n_outputs=5
    )
    assert result.design_life() == float("inf")


def test_berm_width_history_starts_at_the_design_width():
    d = NourishmentDesign(length=2000.0, berm_width=25.0, taper=100.0)
    result = simulate_nourishment(
        d, WaveClimate(), duration=5.0 * SECONDS_PER_YEAR, dx=20.0, n_outputs=6
    )
    assert result.berm_width[0] == pytest.approx(25.0)
    assert result.berm_width[-1] < 25.0


def test_oblique_waves_migrate_the_fill_alongshore():
    """A net transport gradient must shift the centroid downdrift."""
    d = NourishmentDesign(length=2000.0, berm_width=30.0, taper=100.0)
    result = simulate_nourishment(
        d,
        WaveClimate(Hb=1.0, alpha0=np.deg2rad(10.0)),
        duration=3.0 * SECONDS_PER_YEAR,
        dx=20.0,
        n_outputs=4,
    )
    x = result.x

    def centroid(y):
        return float(np.trapezoid(y * x, x) / np.trapezoid(y, x))

    assert centroid(result.planforms[-1]) != pytest.approx(centroid(result.planforms[0]), abs=1.0)


def test_renourishment_schedule_reports_consistent_totals():
    d = NourishmentDesign(length=3000.0, berm_width=30.0, taper=100.0)
    plan = renourishment_schedule(
        d,
        WaveClimate(Hb=1.0),
        horizon=30.0 * SECONDS_PER_YEAR,
        threshold=0.5,
        dx=50.0,
        n_outputs=61,
    )

    assert math.isfinite(plan["interval"])
    assert plan["n_renourishments"] == len(plan["placement_times"]) - 1
    assert plan["total_volume"] == pytest.approx(
        d.placed_volume * len(plan["placement_times"])
    )
    assert plan["placement_times"][0] == 0.0
    assert all(b > a for a, b in zip(plan["placement_times"], plan["placement_times"][1:]))


def test_simulation_rejects_nonsense_controls():
    d, c = NourishmentDesign(), WaveClimate()
    with pytest.raises(ValueError):
        simulate_nourishment(d, c, duration=-1.0)
    with pytest.raises(ValueError):
        simulate_nourishment(d, c, duration=SECONDS_PER_YEAR, n_outputs=1)
