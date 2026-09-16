"""Finite-difference operators, checked against analytic derivatives.

Convention under test: x is axis 0 and y is axis 1, matching
``UniformGrid`` (which builds its coordinates with ``indexing="ij"``) and its
flat boundary index ``idx = i*ny + j``.

The grids here are deliberately anisotropic (dx != dy) and the test fields are
deliberately asymmetric in x and y, so that swapping an axis or a spacing
cannot pass by accident.
"""
import numpy as np
import pytest

from pyCoastal.numerics.grid import UniformGrid
from pyCoastal.numerics import operators as op


def _periodic_case(nx=64, ny=48):
    """f = sin(x) cos(2y) on [0,2pi)^2, with exact derivatives."""
    dx, dy = 2 * np.pi / nx, 2 * np.pi / ny
    grid = UniformGrid((nx, ny), (dx, dy))
    x = np.arange(nx) * dx
    y = np.arange(ny) * dy
    X, Y = np.meshgrid(x, y, indexing="ij")

    f = np.sin(X) * np.cos(2 * Y)
    exact = {
        "f": f,
        "fx": np.cos(X) * np.cos(2 * Y),
        "fy": -2 * np.sin(X) * np.sin(2 * Y),
        "lap": -5 * np.sin(X) * np.cos(2 * Y),
        "X": X,
        "Y": Y,
    }
    return grid, exact


def test_grad_x_matches_analytic_derivative():
    grid, e = _periodic_case()
    assert np.abs(op.grad_x(e["f"], grid) - e["fx"]).max() < 1e-2


def test_grad_y_matches_analytic_derivative():
    grid, e = _periodic_case()
    assert np.abs(op.grad_y(e["f"], grid) - e["fy"]).max() < 5e-2


def test_laplacian_matches_analytic():
    grid, e = _periodic_case()
    assert np.abs(op.laplacian(e["f"], grid) - e["lap"]).max() < 1e-1


@pytest.mark.parametrize("operator,key", [(op.grad_x, "fx"), (op.grad_y, "fy")])
def test_first_derivatives_are_second_order_accurate(operator, key):
    """Halving the mesh must cut the error by roughly four."""
    errs = []
    for n in (32, 64, 128):
        grid, e = _periodic_case(nx=n, ny=n)
        errs.append(np.abs(operator(e["f"], grid) - e[key]).max())
    for coarse, fine in zip(errs, errs[1:]):
        assert 3.5 < coarse / fine < 4.5


def test_laplacian_is_second_order_accurate():
    errs = []
    for n in (32, 64, 128):
        grid, e = _periodic_case(nx=n, ny=n)
        errs.append(np.abs(op.laplacian(e["f"], grid) - e["lap"]).max())
    for coarse, fine in zip(errs, errs[1:]):
        assert 3.5 < coarse / fine < 4.5


def test_gradient_agrees_with_grad_x_and_grad_y():
    """gradient() must return (d/dx, d/dy) in that order, same axes as grad_x/grad_y."""
    grid, e = _periodic_case()
    fx, fy = op.gradient(e["f"], grid)
    np.testing.assert_allclose(fx, op.grad_x(e["f"], grid), atol=1e-12)
    np.testing.assert_allclose(fy, op.grad_y(e["f"], grid), atol=1e-12)
    assert np.abs(fx - e["fx"]).max() < 1e-2
    assert np.abs(fy - e["fy"]).max() < 5e-2


def test_divergence_matches_analytic():
    grid, e = _periodic_case()
    X, Y = e["X"], e["Y"]
    u = np.sin(X) * np.cos(2 * Y)      # du/dx = cos(x) cos(2y)
    v = np.cos(X) * np.sin(2 * Y)      # dv/dy = 2 cos(x) cos(2y)
    exact = 3 * np.cos(X) * np.cos(2 * Y)
    assert np.abs(op.divergence(u, v, grid) - exact).max() < 5e-2


def test_divergence_of_a_constant_field_is_zero():
    grid, _ = _periodic_case()
    ones = np.ones(grid.shape)
    np.testing.assert_allclose(op.divergence(ones, ones, grid), 0.0, atol=1e-12)


def test_curl_of_a_gradient_vanishes():
    """A discrete identity: curl(grad f) = 0 to round-off on a periodic grid."""
    grid, e = _periodic_case()
    fx, fy = op.gradient(e["f"], grid)
    assert np.abs(op.curl_z(fx, fy, grid)).max() < 1e-10


def test_curl_z_of_solid_body_rotation():
    grid, e = _periodic_case()
    X, Y = e["X"], e["Y"]
    u, v = -Y, X          # curl = dv/dx - du/dy = 2
    interior = (slice(1, -1), slice(1, -1))
    assert np.abs(op.curl_z(u, v, grid)[interior] - 2.0).max() < 1e-9


def test_mixed_xy_matches_analytic():
    grid, e = _periodic_case()
    X, Y = e["X"], e["Y"]
    exact = -2 * np.cos(X) * np.sin(2 * Y)    # d2/dxdy of sin(x)cos(2y)
    assert np.abs(op.mixed_xy(e["f"], grid) - exact).max() < 5e-2


def test_biharmonic_matches_analytic():
    grid, e = _periodic_case()
    exact = 25 * np.sin(e["X"]) * np.cos(2 * e["Y"])
    assert np.abs(op.biharmonic(e["f"], grid) - exact).max() < 2.0


def test_upwind_uses_the_donor_cell():
    """For u>0 the stencil must look backwards; for u<0, forwards."""
    grid = UniformGrid((8, 4), (1.0, 1.0))
    f = np.zeros((8, 4))
    f[4, :] = 1.0                      # single spike at i=4

    pos = op.upwind_x(f, np.ones_like(f), grid)
    neg = op.upwind_x(f, -np.ones_like(f), grid)
    # Backward difference sees the spike arriving at i=4; forward sees it at i=3.
    assert pos[4, 0] == pytest.approx(1.0)
    assert neg[3, 0] == pytest.approx(1.0)


def test_upwind_of_a_uniform_field_is_zero():
    grid = UniformGrid((8, 8), (0.5, 0.5))
    f = np.full((8, 8), 3.0)
    u = np.random.default_rng(0).normal(size=(8, 8))
    np.testing.assert_allclose(op.upwind_x(f, u, grid), 0.0, atol=1e-12)
    np.testing.assert_allclose(op.upwind_y(f, u, grid), 0.0, atol=1e-12)


def test_advect_of_a_uniform_field_is_zero():
    grid = UniformGrid((8, 8), (0.5, 0.5))
    f = np.full((8, 8), -2.0)
    u = np.ones((8, 8))
    v = np.ones((8, 8))
    for scheme in ("upwind", "central"):
        np.testing.assert_allclose(op.advect(u, v, f, grid, scheme), 0.0, atol=1e-12)


def test_smooth3_preserves_constants():
    """A box filter must be a partition of unity, or it bleeds amplitude."""
    grid = UniformGrid((16, 16), (1.0, 1.0))
    ones = np.ones((16, 16))
    np.testing.assert_allclose(op.smooth3(ones, grid), 1.0, atol=1e-12)


def test_smooth3_damps_grid_scale_noise_without_shifting_the_mean():
    grid = UniformGrid((32, 32), (1.0, 1.0))
    rng = np.random.default_rng(42)
    field = 5.0 + rng.normal(scale=0.1, size=(32, 32))
    out = op.smooth3(field, grid)
    assert out.std() < field.std()
    assert out.mean() == pytest.approx(field.mean(), rel=1e-9)
