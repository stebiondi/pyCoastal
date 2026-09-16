"""The whole package uses one array layout: x is axis 0, y is axis 1.

These tests exist because the physics modules used to hand-roll stencils on
the opposite convention from the grid and the operators. They pin the layout
so it cannot drift apart again.
"""
import numpy as np
import pytest

from pyCoastal.numerics.grid import UniformGrid
from pyCoastal.physics.shallow_water import ShallowWater2D
from pyCoastal.physics.turbulence import SmagorinskyModel


def test_bed_slope_source_responds_to_an_x_slope_only():
    """A bed sloping purely in x must give Sx != 0 and Sy == 0."""
    grid = UniformGrid((32, 16), (2.0, 5.0))
    x = np.arange(32) * 2.0
    zb = np.broadcast_to(-0.02 * x[:, None], (32, 16)).copy()   # slope in x
    h = np.ones((32, 16)) * 3.0

    Sx, Sy = ShallowWater2D().source_bed_slope(h, zb, grid)
    assert np.abs(Sy).max() < 1e-12
    # Sx = -g h dzb/dx = -9.81 * 3 * (-0.02)
    assert Sx[5, 5] == pytest.approx(9.81 * 3.0 * 0.02, rel=1e-9)


def test_bed_slope_source_responds_to_a_y_slope_only():
    grid = UniformGrid((32, 16), (2.0, 5.0))
    y = np.arange(16) * 5.0
    zb = np.broadcast_to(-0.01 * y[None, :], (32, 16)).copy()   # slope in y
    h = np.ones((32, 16)) * 2.0

    Sx, Sy = ShallowWater2D().source_bed_slope(h, zb, grid)
    assert np.abs(Sx).max() < 1e-12
    assert Sy[5, 5] == pytest.approx(9.81 * 2.0 * 0.01, rel=1e-9)


def test_bed_slope_uses_real_cell_spacing():
    """Doubling dx must halve the computed x-slope for the same array."""
    zb = np.broadcast_to(np.arange(32.0)[:, None], (32, 16)).copy()
    h = np.ones((32, 16))

    coarse = ShallowWater2D().source_bed_slope(h, zb, UniformGrid((32, 16), (2.0, 1.0)))[0]
    fine = ShallowWater2D().source_bed_slope(h, zb, UniformGrid((32, 16), (1.0, 1.0)))[0]
    assert coarse[5, 5] == pytest.approx(0.5 * fine[5, 5])


def test_flat_bed_produces_no_source():
    grid = UniformGrid((16, 16), (1.0, 1.0))
    zb = np.full((16, 16), -5.0)
    h = np.ones((16, 16)) * 5.0
    Sx, Sy = ShallowWater2D().source_bed_slope(h, zb, grid)
    np.testing.assert_allclose(Sx, 0.0, atol=1e-12)
    np.testing.assert_allclose(Sy, 0.0, atol=1e-12)


def test_shallow_water_mass_flux_is_symmetric_under_axis_exchange():
    """Swapping (u,x) with (v,y) must swap the flux pair, nothing else."""
    h = np.full((8, 8), 2.0)
    hu = np.full((8, 8), 1.0)
    hv = np.full((8, 8), -0.5)

    swe = ShallowWater2D()
    (Fh, Gh), _, _ = swe.fluxes(h, hu, hv)
    np.testing.assert_allclose(Fh, hu)
    np.testing.assert_allclose(Gh, hv)


def test_smagorinsky_detects_pure_x_shear():
    """u varying in x only: Sxx is the sole nonzero strain component."""
    grid = UniformGrid((32, 16), (0.5, 0.5))
    x = np.arange(32) * 0.5
    u = np.broadcast_to(0.1 * x[:, None], (32, 16)).copy()
    v = np.zeros((32, 16))

    nu_t = SmagorinskyModel(Cs=0.17, filter_width=0.5).eddy_viscosity(u, v, grid)
    # |S| = sqrt(2 * Sxx^2) with Sxx = 0.1
    expected = (0.17 * 0.5) ** 2 * np.sqrt(2 * 0.1**2)
    assert nu_t[5, 5] == pytest.approx(expected, rel=1e-9)


def test_smagorinsky_is_zero_for_uniform_flow():
    grid = UniformGrid((16, 16), (1.0, 1.0))
    u = np.full((16, 16), 2.0)
    v = np.full((16, 16), -1.0)
    nu_t = SmagorinskyModel().eddy_viscosity(u, v, grid)
    np.testing.assert_allclose(nu_t, 0.0, atol=1e-12)


def test_smagorinsky_uses_real_cell_spacing():
    grid_coarse = UniformGrid((32, 16), (2.0, 2.0))
    grid_fine = UniformGrid((32, 16), (1.0, 1.0))
    u = np.broadcast_to(np.arange(32.0)[:, None], (32, 16)).copy()
    v = np.zeros((32, 16))

    model = SmagorinskyModel()
    coarse = model.eddy_viscosity(u, v, grid_coarse)[5, 5]
    fine = model.eddy_viscosity(u, v, grid_fine)[5, 5]
    assert coarse == pytest.approx(0.5 * fine)
