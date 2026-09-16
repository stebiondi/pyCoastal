"""Built-in port layouts and oblique wave incidence."""
import numpy as np
import pytest

from pyCoastal.applications.port import (
    LAYOUTS,
    IncidentWave,
    PortLayout,
    illuminated_mask,
    rotate_layout,
    detached_breakwater_layout,
    harbour_layout,
    hooked_breakwater_layout,
    marina_layout,
    offset_entrance_layout,
    simulate_port,
)


# --------------------------------------------------------------------------
# Layout catalogue
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name,builder", sorted(LAYOUTS.items()))
def test_every_layout_builds_a_usable_domain(name, builder):
    layout = builder(dx=10.0)
    mask = layout.land_mask()

    assert isinstance(layout, PortLayout)
    assert mask.shape == layout.shape
    assert mask.any(), f"{name} placed no structures"
    assert not mask.all(), f"{name} left no water"


@pytest.mark.parametrize("name,builder", sorted(LAYOUTS.items()))
def test_every_layout_leaves_a_navigable_opening(name, builder):
    """Some water column must connect the sea to the basin."""
    layout = builder(dx=10.0)
    mask = layout.land_mask()
    # At least one alongshore row is water all the way across the structures.
    open_rows = (~mask).all(axis=0)
    assert open_rows.any() or (~mask).sum() > 0.5 * mask.size


@pytest.mark.parametrize("name,builder", sorted(LAYOUTS.items()))
def test_absorption_is_applied_to_every_structure(name, builder):
    layout = builder(dx=20.0, absorption=0.4)
    assert all(bw.absorption == 0.4 for bw in layout.breakwaters)


@pytest.mark.parametrize("name,builder", sorted(LAYOUTS.items()))
def test_back_wall_can_be_turned_off(name, builder):
    closed = builder(dx=20.0, back_wall=True)
    open_ended = builder(dx=20.0, back_wall=False)
    assert len(closed.breakwaters) == len(open_ended.breakwaters) + 1
    assert any(bw.name == "quay" for bw in closed.breakwaters)
    assert not any(bw.name == "quay" for bw in open_ended.breakwaters)


def test_offset_entrance_has_no_straight_path_through_the_gap():
    """The overlapping arms must block every shore-normal line of sight."""
    layout = offset_entrance_layout(dx=8.0, back_wall=False)
    mask = layout.land_mask()
    x, y = layout.coordinates()

    # Restrict to the alongshore band spanned by the two arms.
    arms = [bw for bw in layout.breakwaters if "arm" in bw.name]
    ys = [p[1] for bw in arms for p in bw.points]
    band = (y >= max(min(ys), y[0])) & (y <= min(max(ys), y[-1]))

    # Every row in that band meets structure somewhere along x.
    blocked = mask[:, band].any(axis=0)
    assert blocked.all()


def test_hooked_layout_returns_a_limb_in_x():
    """The hook must extend the main arm alongshore-normal, not just in y."""
    layout = hooked_breakwater_layout(dx=8.0, back_wall=False)
    main = next(bw for bw in layout.breakwaters if "hook" in bw.name)
    xs = {p[0] for p in main.points}
    assert len(xs) > 1, "hook did not turn"


def test_detached_screen_sits_seaward_of_the_arms():
    layout = detached_breakwater_layout(dx=8.0, standoff=200.0, back_wall=False)
    screen = next(bw for bw in layout.breakwaters if "screen" in bw.name)
    arm = next(bw for bw in layout.breakwaters if bw.name == "south arm")
    assert screen.points[0][0] < arm.points[0][0]


def test_marina_inner_entrance_is_offset_from_the_outer_one():
    layout = marina_layout(dx=8.0, inner_offset=220.0, back_wall=False)
    y_mid = 0.5 * layout.Ly

    south_wall = next(bw for bw in layout.breakwaters if bw.name == "basin wall south")
    north_wall = next(bw for bw in layout.breakwaters if bw.name == "basin wall north")
    inner_gap_centre = 0.5 * (south_wall.points[-1][1] + north_wall.points[0][1])

    assert abs(inner_gap_centre - y_mid) > 100.0


def test_layouts_differ_from_one_another():
    masks = {name: builder(dx=16.0).land_mask() for name, builder in LAYOUTS.items()}
    names = sorted(masks)
    for a, b in zip(names, names[1:]):
        assert not np.array_equal(masks[a], masks[b]), f"{a} and {b} are identical"


# --------------------------------------------------------------------------
# Sheltering performance
# --------------------------------------------------------------------------

def _basin_agitation(layout, wave, **kwargs):
    result = simulate_port(
        layout,
        wave,
        duration=kwargs.pop("duration", 500.0),
        n_snapshots=2,
        analysis_periods=8.0,
        sponge_sides=("west", "north", "south"),
        **kwargs,
    )
    x = result.x
    inside = x > 0.86 * layout.Lx
    water = np.zeros_like(result.land, dtype=bool)
    water[inside, :] = True
    water &= ~result.land
    return float(np.mean(result.wave_height[water])) / result.reference_height


def test_an_offset_entrance_shelters_better_than_a_straight_gap():
    """Forcing a second diffraction is the point of the dog-leg."""
    wave = IncidentWave(height=1.5, period=9.0)
    straight = _basin_agitation(harbour_layout(dx=10.0, gap=130.0), wave)
    offset = _basin_agitation(offset_entrance_layout(dx=10.0, gap=130.0), wave)
    assert offset < straight


def test_an_absorbing_detached_screen_shelters_the_basin():
    """With armour on it, the screen does its job and cuts basin agitation."""
    wave = IncidentWave(height=1.5, period=9.0)
    common = dict(dx=10.0, gap=150.0, arm_length=280.0, absorption=0.35)
    bare = _basin_agitation(harbour_layout(**common), wave)
    screened = _basin_agitation(detached_breakwater_layout(**common), wave)
    assert screened < 0.5 * bare


def test_a_fully_reflecting_detached_screen_can_amplify_instead():
    """A reflecting screen and the arms form a pocket that rings.

    This is the reason detached screens are armoured in practice, and it is
    worth pinning: a naive reading would expect any extra structure to
    shelter, and here it does the opposite.
    """
    wave = IncidentWave(height=1.5, period=9.0)
    common = dict(dx=10.0, gap=150.0, arm_length=280.0, absorption=0.0)
    bare = _basin_agitation(harbour_layout(**common), wave)
    screened = _basin_agitation(detached_breakwater_layout(**common), wave)
    assert screened > bare


# --------------------------------------------------------------------------
# Oblique incidence
# --------------------------------------------------------------------------

def _dominant_wavevector(field, dx):
    """Peak wavenumber of a 2D field, via its spectrum."""
    f = field - field.mean()
    spectrum = np.abs(np.fft.fftshift(np.fft.fft2(f)))
    kx = np.fft.fftshift(np.fft.fftfreq(f.shape[0], d=dx)) * 2 * np.pi
    ky = np.fft.fftshift(np.fft.fftfreq(f.shape[1], d=dx)) * 2 * np.pi
    i, j = np.unravel_index(np.argmax(spectrum), spectrum.shape)
    return kx[i], ky[j]


@pytest.mark.parametrize("degrees", [0.0, 20.0, 35.0])
def test_oblique_source_radiates_at_the_requested_angle(degrees):
    """A phased source line must launch the wave at the angle asked for."""
    layout = PortLayout(Lx=1200.0, Ly=1200.0, dx=6.0, depth=10.0, breakwaters=[])
    wave = IncidentWave(height=1.0, period=8.0, direction=np.deg2rad(degrees))
    result = simulate_port(layout, wave, duration=400.0, n_snapshots=2, analysis_periods=8.0)

    interior = result.snapshots[-1][60:160, 40:160]
    kx, ky = _dominant_wavevector(interior, layout.dx)
    measured = np.rad2deg(np.arctan2(abs(ky), abs(kx)))

    # The spectral grid is coarse, so allow a few degrees of bin width.
    assert measured == pytest.approx(degrees, abs=5.0)


def test_oblique_wave_keeps_the_dispersion_wavenumber():
    layout = PortLayout(Lx=1200.0, Ly=1200.0, dx=6.0, depth=10.0, breakwaters=[])
    wave = IncidentWave(height=1.0, period=8.0, direction=np.deg2rad(30.0))
    result = simulate_port(layout, wave, duration=400.0, n_snapshots=2, analysis_periods=8.0)

    kx, ky = _dominant_wavevector(result.snapshots[-1][60:160, 40:160], layout.dx)
    expected = 2 * np.pi / wave.wavelength(layout.depth)
    assert float(np.hypot(kx, ky)) == pytest.approx(expected, rel=0.12)


def test_oblique_source_warns_when_a_structure_is_outside_the_lit_region():
    """Silently scoring a structure against a wave it never received is worse
    than a warning."""
    layout = harbour_layout(dx=16.0, back_wall=False)
    wave = IncidentWave(height=1.0, period=9.0, direction=np.deg2rad(35.0))
    with pytest.warns(RuntimeWarning, match="illuminates"):
        simulate_port(layout, wave, duration=200.0, n_snapshots=2, analysis_periods=4.0)


def test_illuminated_mask_marks_the_lit_parallelogram():
    layout = PortLayout(Lx=1000.0, Ly=600.0, dx=10.0, breakwaters=[])
    wave = IncidentWave(period=9.0, direction=np.deg2rad(30.0))
    lit = illuminated_mask(layout, wave, source_x=100.0)
    x, y = layout.coordinates()

    # Far downwave and low in y the source cannot reach.
    i = int(np.argmin(np.abs(x - 900.0)))
    assert not lit[i, int(np.argmin(np.abs(y - 20.0)))]
    assert lit[i, int(np.argmin(np.abs(y - 550.0)))]
    # Everything upwave of the source counts as lit.
    assert lit[int(np.argmin(np.abs(x - 50.0))), :].all()


def test_normal_incidence_illuminates_everything():
    layout = PortLayout(Lx=1000.0, Ly=600.0, dx=10.0, breakwaters=[])
    wave = IncidentWave(period=9.0, direction=0.0)
    assert illuminated_mask(layout, wave, source_x=100.0).all()


# --------------------------------------------------------------------------
# Wave direction by rotating the layout
# --------------------------------------------------------------------------

def test_rotating_by_zero_leaves_the_layout_alone():
    base = harbour_layout(dx=12.0, back_wall=False)
    np.testing.assert_array_equal(
        rotate_layout(base, 0.0).land_mask(), base.land_mask()
    )


def test_rotation_preserves_structure_count_and_properties():
    base = harbour_layout(dx=12.0, absorption=0.4)
    spun = rotate_layout(base, 30.0)
    assert len(spun.breakwaters) == len(base.breakwaters)
    assert [bw.name for bw in spun.breakwaters] == [bw.name for bw in base.breakwaters]
    assert all(bw.absorption == 0.4 for bw in spun.breakwaters)


def test_rotation_actually_moves_the_structures():
    base = harbour_layout(dx=12.0, back_wall=False)
    spun = rotate_layout(base, 25.0)
    assert not np.array_equal(spun.land_mask(), base.land_mask())


def test_rotation_preserves_arm_length():
    """A rigid rotation must not stretch the breakwaters."""
    base = harbour_layout(dx=12.0, back_wall=False)
    spun = rotate_layout(base, 37.0)
    for a, b in zip(base.breakwaters, spun.breakwaters):
        for (p0, p1), (q0, q1) in zip(zip(a.points, a.points[1:]),
                                      zip(b.points, b.points[1:])):
            assert np.hypot(p1[0] - p0[0], p1[1] - p0[1]) == pytest.approx(
                np.hypot(q1[0] - q0[0], q1[1] - q0[1])
            )


def _lee_pair(rotation):
    """Kd on each side of the basin for a harbour turned into the waves."""
    base = harbour_layout(
        Lx=1400.0, Ly=900.0, dx=12.0, gap=140.0, arm_length=280.0,
        back_wall=False, absorption=0.35,
    )
    result = simulate_port(
        rotate_layout(base, rotation),
        IncidentWave(height=1.5, period=9.0, direction=0.0),
        duration=600.0, n_snapshots=2, analysis_periods=8.0,
    )
    return result.probe((1150.0, 600.0)), result.probe((1150.0, 300.0))


def test_a_square_on_harbour_is_symmetric():
    north, south = _lee_pair(0.0)
    assert north == pytest.approx(south, rel=0.1)


def test_turning_the_harbour_shelters_one_side():
    north, south = _lee_pair(20.0)
    assert north > 3 * south


def test_opposite_rotations_mirror_each_other():
    """The clean check that oblique attack is being modelled correctly."""
    north_pos, south_pos = _lee_pair(20.0)
    north_neg, south_neg = _lee_pair(-20.0)
    assert north_pos == pytest.approx(south_neg, rel=0.15)
    assert south_pos == pytest.approx(north_neg, rel=0.15)
