"""Port layout simulator.

The solver is checked against what diffraction theory requires of a
semi-infinite breakwater: a deep, quiet shadow, a monotonic rise across the
geometric shadow boundary to roughly half the incident height there, and a
near-unit illuminated field carrying Fresnel fringes.

Runs here are deliberately coarse and short. They resolve the diffraction
pattern well enough to assert on, without making the suite slow.
"""
import math

import numpy as np
import pytest

from pyCoastal.applications.port import (
    Breakwater,
    IncidentWave,
    PortLayout,
    harbour_layout,
    simulate_port,
)
from pyCoastal.tools.wave import dispersion


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------

def test_breakwater_needs_at_least_two_points():
    with pytest.raises(ValueError, match="at least two points"):
        Breakwater(points=[(0.0, 0.0)])


def test_breakwater_width_must_be_positive():
    with pytest.raises(ValueError, match="width must be positive"):
        Breakwater(points=[(0.0, 0.0), (1.0, 0.0)], width=0.0)


@pytest.mark.parametrize(
    "kwargs", [{"Lx": -1.0}, {"dx": 0.0}, {"depth": -5.0}]
)
def test_invalid_layouts_are_rejected(kwargs):
    with pytest.raises(ValueError):
        PortLayout(**kwargs)


def test_land_mask_marks_the_structure_and_leaves_the_gap_open():
    layout = harbour_layout(dx=10.0, gap=120.0, back_wall=False)
    mask = layout.land_mask()
    x, y = layout.coordinates()

    i_wall = int(np.argmin(np.abs(x - 0.70 * layout.Lx)))
    j_mid = int(np.argmin(np.abs(y - 0.5 * layout.Ly)))

    assert not mask[i_wall, j_mid]                      # entrance is water
    assert mask[i_wall, int(np.argmin(np.abs(y - 200.0)))]   # south arm is land
    assert mask[i_wall, int(np.argmin(np.abs(y - 700.0)))]   # north arm is land


def test_land_mask_respects_the_requested_thickness():
    bw = Breakwater(points=[(500.0, 0.0), (500.0, 400.0)], width=40.0)
    layout = PortLayout(Lx=1000.0, Ly=400.0, dx=5.0, breakwaters=[bw])
    mask = layout.land_mask()
    x, _ = layout.coordinates()

    j = 40
    thickness = mask[:, j].sum() * layout.dx
    assert thickness == pytest.approx(40.0, abs=2 * layout.dx)


def test_back_wall_adds_a_closing_quay():
    with_wall = harbour_layout(dx=10.0, back_wall=True).land_mask().sum()
    without = harbour_layout(dx=10.0, back_wall=False).land_mask().sum()
    assert with_wall > without


def test_diagonal_breakwater_is_rasterized():
    bw = Breakwater(points=[(100.0, 100.0), (400.0, 400.0)], width=20.0)
    layout = PortLayout(Lx=500.0, Ly=500.0, dx=5.0, breakwaters=[bw])
    mask = layout.land_mask()
    x, y = layout.coordinates()
    # A point on the centreline is land; one well off it is not.
    assert mask[int(np.argmin(np.abs(x - 250.0))), int(np.argmin(np.abs(y - 250.0)))]
    assert not mask[int(np.argmin(np.abs(x - 250.0))), int(np.argmin(np.abs(y - 400.0)))]


# --------------------------------------------------------------------------
# Incident wave
# --------------------------------------------------------------------------

def test_wavelength_comes_from_the_dispersion_relation():
    wave = IncidentWave(height=1.0, period=8.0)
    assert wave.wavelength(10.0) == pytest.approx(dispersion(8.0, 10.0))


def test_celerity_is_wavelength_over_period():
    wave = IncidentWave(period=8.0)
    assert wave.celerity(10.0) == pytest.approx(wave.wavelength(10.0) / 8.0)


def test_deep_water_celerity_exceeds_shallow_water_celerity():
    wave = IncidentWave(period=10.0)
    assert wave.celerity(200.0) > wave.celerity(3.0)


def test_amplitude_is_half_the_height():
    assert IncidentWave(height=2.4).amplitude == pytest.approx(1.2)


@pytest.mark.parametrize("kwargs", [{"height": 0.0}, {"period": -1.0}])
def test_invalid_waves_are_rejected(kwargs):
    with pytest.raises(ValueError):
        IncidentWave(**kwargs)


def test_unknown_sponge_side_is_rejected():
    layout = harbour_layout(dx=20.0, back_wall=False)
    with pytest.raises(ValueError, match="Unknown sponge sides"):
        simulate_port(
            layout, IncidentWave(), duration=20.0, n_snapshots=2,
            sponge_sides=("west", "up"),
        )


# --------------------------------------------------------------------------
# Solver behaviour
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def shadow_run():
    """Semi-infinite breakwater with its tip at y = 600 m."""
    y_tip = 600.0
    bw = Breakwater(points=[(1000.0, -50.0), (1000.0, y_tip)], width=16.0)
    layout = PortLayout(Lx=1600.0, Ly=1200.0, dx=10.0, depth=10.0, breakwaters=[bw])
    wave = IncidentWave(height=1.0, period=8.0, direction=0.0)
    crossing = layout.Lx / wave.celerity(layout.depth)
    result = simulate_port(
        layout, wave, duration=5.0 * crossing, n_snapshots=3, analysis_periods=12.0
    )
    return result, y_tip, wave.wavelength(layout.depth)


def test_solution_stays_finite(shadow_run):
    result, _, _ = shadow_run
    assert np.isfinite(result.snapshots).all()
    assert np.isfinite(result.wave_height).all()


def test_no_water_motion_inside_a_structure(shadow_run):
    result, _, _ = shadow_run
    assert np.abs(result.snapshots[:, result.land]).max() == 0.0


def test_incident_height_is_calibrated_to_the_requested_value(shadow_run):
    result, _, _ = shadow_run
    assert result.reference_height == pytest.approx(result.wave.height)


def test_the_shadow_is_much_quieter_than_the_illuminated_side(shadow_run):
    result, y_tip, L = shadow_run
    deep_shadow = result.probe((1000.0 + 2 * L, y_tip - 250.0))
    illuminated = result.probe((1000.0 + 2 * L, y_tip + 250.0))
    assert deep_shadow < 0.25
    assert illuminated > 0.7
    assert illuminated > 4 * deep_shadow


def test_disturbance_rises_toward_the_tip_across_the_shadow(shadow_run):
    """Energy leaks into the lee by diffraction, so Kd grows toward the tip.

    Only the part of the shadow carrying a meaningful signal is ordered
    strictly. Deeper in, Kd falls below about 0.1 and the ordering sits under
    the noise floor of a run this coarse.
    """
    result, y_tip, L = shadow_run
    near_tip = [
        result.probe((1000.0 + 2 * L, y_tip + dy)) for dy in (-150.0, -100.0, -50.0)
    ]
    assert all(a < b for a, b in zip(near_tip, near_tip[1:]))

    deep = result.probe((1000.0 + 2 * L, y_tip - 250.0))
    assert deep < near_tip[-1]


def test_shadow_boundary_is_near_half_the_incident_height(shadow_run):
    """Diffraction theory gives Kd = 0.5 on the geometric shadow line.

    The tolerance is wide because the classic result is for a zero-thickness
    screen, while this model rasterizes a finite-width, fully reflecting
    structure onto the grid.
    """
    result, y_tip, L = shadow_run
    for distance in (2.0, 3.0):
        kd = result.probe((1000.0 + distance * L, y_tip))
        assert 0.3 < kd < 0.7


def test_illuminated_field_is_close_to_the_incident_height(shadow_run):
    """Away from the structure the total field should be near Kd = 1."""
    result, y_tip, L = shadow_run
    samples = [
        result.probe((1000.0 + 2 * L, y_tip + dy)) for dy in (200.0, 250.0, 300.0)
    ]
    assert 0.7 < float(np.mean(samples)) < 1.35


def test_diffraction_reaches_places_straight_line_propagation_cannot(shadow_run):
    """The lee is sheltered but not dead: some energy must bend into it."""
    result, y_tip, L = shadow_run
    assert result.probe((1000.0 + 2 * L, y_tip - 200.0)) > 0.02


# --------------------------------------------------------------------------
# Harbour performance
# --------------------------------------------------------------------------

def _harbour_run(gap, dx=12.0):
    layout = harbour_layout(dx=dx, gap=gap, back_wall=False)
    wave = IncidentWave(height=1.5, period=8.0)
    crossing = layout.Lx / wave.celerity(layout.depth)
    return simulate_port(
        layout, wave, duration=4.0 * crossing, n_snapshots=3, analysis_periods=10.0
    )


def test_a_wider_entrance_lets_more_energy_into_the_harbour():
    narrow = _harbour_run(gap=80.0)
    wide = _harbour_run(gap=240.0)

    def basin_energy(result):
        x, y = result.x, result.y
        inside = (x > 0.72 * result.layout.Lx)[:, None] & np.ones_like(y, dtype=bool)
        water = inside & ~result.land
        return float(np.mean(result.wave_height[water]))

    assert basin_energy(wide) > basin_energy(narrow)


def test_wave_height_decays_with_distance_into_the_harbour():
    result = _harbour_run(gap=120.0)
    y_mid = 0.5 * result.layout.Ly
    entrance = result.probe((0.72 * result.layout.Lx, y_mid))
    deeper = result.probe((0.80 * result.layout.Lx, y_mid))
    assert deeper < entrance


def test_symmetric_layout_under_normal_incidence_gives_a_symmetric_field():
    result = _harbour_run(gap=120.0)
    y_mid = 0.5 * result.layout.Ly
    x_probe = 0.78 * result.layout.Lx
    for dy in (60.0, 120.0, 180.0):
        north = result.probe((x_probe, y_mid + dy))
        south = result.probe((x_probe, y_mid - dy))
        assert north == pytest.approx(south, rel=0.15)


def test_berth_report_and_operability():
    result = _harbour_run(gap=120.0)
    berths = {
        "outer": (0.73 * result.layout.Lx, 0.5 * result.layout.Ly),
        "inner": (0.82 * result.layout.Lx, 0.42 * result.layout.Ly),
    }
    report = result.berth_report(berths)

    assert set(report) == {"outer", "inner"}
    for info in report.values():
        assert info["Hs"] == pytest.approx(info["Kd"] * result.wave.height)
        assert info["Kd"] >= 0.0

    generous = result.operable_fraction(berths, limit=10.0)
    assert all(generous.values())
    strict = result.operable_fraction(berths, limit=1e-6)
    assert not any(strict.values())


def test_probing_inside_a_breakwater_is_an_error():
    result = _harbour_run(gap=120.0)
    x_wall = 0.70 * result.layout.Lx
    with pytest.raises(ValueError, match="inside a breakwater"):
        result.probe((x_wall, 200.0))


def test_disturbance_coefficient_is_nan_on_land():
    result = _harbour_run(gap=120.0)
    kd = result.disturbance_coefficient
    assert np.isnan(kd[result.land]).all()
    assert np.isfinite(kd[~result.land]).all()


def test_snapshots_have_the_requested_shape():
    layout = harbour_layout(dx=20.0, back_wall=False)
    wave = IncidentWave(height=1.0, period=8.0)
    result = simulate_port(layout, wave, duration=60.0, n_snapshots=7, analysis_periods=4.0)
    nx, ny = layout.shape
    assert result.snapshots.shape == (7, nx, ny)
    assert result.times.shape == (7,)
