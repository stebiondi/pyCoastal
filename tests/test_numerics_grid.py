"""Grid geometry and boundary-index bookkeeping."""
import numpy as np
import pytest

from pyCoastal.numerics.grid import UniformGrid


def test_cell_centers_are_offset_by_half_a_cell():
    g = UniformGrid((4, 3), (0.5, 2.0))
    assert g.Xc[0][0, 0] == pytest.approx(0.25)
    assert g.Xc[1][0, 0] == pytest.approx(1.0)


def test_faces_span_the_full_domain():
    g = UniformGrid((4, 3), (0.5, 2.0))
    assert g.Xf[0][0, 0] == pytest.approx(0.0)
    assert g.Xf[0][-1, 0] == pytest.approx(2.0)
    assert g.Xf[1][0, -1] == pytest.approx(6.0)


def test_origin_shifts_the_grid():
    g = UniformGrid((4, 3), (1.0, 1.0), origin=(10.0, -5.0))
    assert g.Xc[0][0, 0] == pytest.approx(10.5)
    assert g.Xc[1][0, 0] == pytest.approx(-4.5)


def test_n_cells_and_cell_volume():
    g = UniformGrid((4, 3), (0.5, 2.0))
    assert g.n_cells == 12
    assert g.cell_volume == pytest.approx(1.0)


def test_boundary_indices_match_the_documented_flat_layout():
    """Flat index is idx = i*ny + j, i.e. x is the slow (first) axis."""
    nx, ny = 4, 3
    g = UniformGrid((nx, ny), (1.0, 1.0))
    flat = np.arange(nx * ny).reshape(nx, ny)

    np.testing.assert_array_equal(g.boundary_indices["west"], flat[0, :])
    np.testing.assert_array_equal(g.boundary_indices["east"], flat[-1, :])
    np.testing.assert_array_equal(g.boundary_indices["south"], flat[:, 0])
    np.testing.assert_array_equal(g.boundary_indices["north"], flat[:, -1])


@pytest.mark.parametrize("side", ["west", "east", "south", "north"])
def test_neumann_interior_is_exactly_one_cell_inward(side):
    nx, ny = 5, 4
    g = UniformGrid((nx, ny), (1.0, 1.0))
    bd, interior = g.neumann_indices(side)

    assert bd.shape == interior.shape
    # Interior cells must be real cells, and never on the same side they mirror.
    assert np.all(interior >= 0) and np.all(interior < g.n_cells)
    assert not np.any(np.isin(interior, bd))

    step = ny if side in ("west", "east") else 1
    assert np.all(np.abs(interior - bd) == step)


def test_1d_grid_boundaries():
    g = UniformGrid((6,), (0.25,))
    assert g.boundary_indices["west"].tolist() == [0]
    assert g.boundary_indices["east"].tolist() == [5]
    bd, interior = g.neumann_indices("west")
    assert interior.tolist() == [1]


def test_3d_is_rejected_rather_than_silently_wrong():
    with pytest.raises(NotImplementedError):
        UniformGrid((3, 3, 3), (1.0, 1.0, 1.0))
