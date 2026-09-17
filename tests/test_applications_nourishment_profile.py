"""Cross-shore nourishment: equilibrium profiles and borrow compatibility."""

import math

import numpy as np
import pytest

from pyCoastal.applications.nourishment import (
    critical_volume,
    dean_scale,
    equilibrium_profile,
    fill_volume_for_advance,
    grain_compatibility,
    phi_size,
    profile_overfill_factor,
    profile_width,
    shoreline_advance,
    size_from_phi,
)
from pyCoastal.applications.sediment import sediment

BERM = 2.0
CLOSURE = 6.0


@pytest.fixture
def native():
    return dean_scale("medium_sand")


# ---------------------------------------------------------------------------
# Grain size on the phi scale
# ---------------------------------------------------------------------------


def test_phi_of_one_millimetre_is_zero():
    assert phi_size(0.001) == pytest.approx(0.0)


def test_phi_halves_with_each_doubling_of_size():
    assert phi_size(0.0005) - phi_size(0.001) == pytest.approx(1.0)
    assert phi_size(0.002) - phi_size(0.001) == pytest.approx(-1.0)


def test_phi_round_trips():
    for d in (0.06e-3, 0.2e-3, 0.5e-3, 2.0e-3):
        assert size_from_phi(phi_size(d)) == pytest.approx(d)


def test_coarser_sand_has_smaller_phi():
    assert phi_size(0.75e-3) < phi_size(0.19e-3)


def test_phi_rejects_a_zero_size():
    with pytest.raises(ValueError):
        phi_size(0.0)


# ---------------------------------------------------------------------------
# The profile scale
# ---------------------------------------------------------------------------


def test_dean_scale_matches_the_published_table():
    """Dean tabulates about 0.10 at 0.2 mm and 0.14 at 0.4 mm."""
    assert dean_scale("fine_sand") == pytest.approx(0.10, abs=0.015)
    assert dean_scale("medium_sand") == pytest.approx(0.14, abs=0.015)


def test_dean_scale_rises_with_grain_size():
    scales = [dean_scale(k) for k in
              ("very_fine_sand", "fine_sand", "medium_sand", "coarse_sand",
               "fine_gravel")]
    assert all(b > a for a, b in zip(scales, scales[1:]))


def test_a_beach_cannot_be_built_from_clay():
    with pytest.raises(ValueError) as excinfo:
        dean_scale("soft_clay")
    assert "cohesive" in str(excinfo.value)


def test_equilibrium_profile_is_the_two_thirds_power():
    A = 0.14
    y = np.array([0.0, 10.0, 40.0, 90.0])
    assert np.allclose(equilibrium_profile(A, y), A * y ** (2 / 3))


def test_profile_width_inverts_the_profile():
    A = 0.12
    for depth in (1.0, 3.0, 6.0):
        y = profile_width(A, depth)
        assert float(equilibrium_profile(A, y)) == pytest.approx(depth)


def test_a_coarser_beach_is_narrower_to_the_same_depth():
    assert (profile_width(dean_scale("coarse_sand"), 6.0)
            < profile_width(dean_scale("fine_sand"), 6.0))


# ---------------------------------------------------------------------------
# Volume and advance
# ---------------------------------------------------------------------------


def test_matched_sand_reduces_to_the_active_height_formula(native):
    """With borrow identical to native, V = (B + h*) a, exactly."""
    for advance in (1.0, 12.0, 60.0, 200.0):
        got = fill_volume_for_advance(native, native, advance, BERM, CLOSURE)
        assert got["volume"] == pytest.approx((BERM + CLOSURE) * advance)


def test_matched_sand_advance_inverts_that_formula(native):
    for volume in (20.0, 100.0, 400.0):
        got = shoreline_advance(native, native, volume, BERM, CLOSURE)
        assert got["advance"] == pytest.approx(volume / (BERM + CLOSURE), abs=1e-3)
        assert got["kind"] == "matched"


def test_coarser_fill_buys_more_beach_per_cubic_metre(native):
    volume = 250.0
    widths = [
        shoreline_advance(native, dean_scale(k), volume, BERM, CLOSURE)["advance"]
        for k in ("medium_sand", "coarse_sand", "fine_gravel")
    ]
    assert all(b > a for a, b in zip(widths, widths[1:]))


def test_coarser_fill_intersects_and_finer_does_not(native):
    coarse = shoreline_advance(native, dean_scale("coarse_sand"), 250.0,
                               BERM, CLOSURE)
    assert coarse["kind"] == "intersecting"
    assert coarse["meeting"] > coarse["advance"]
    assert 0.0 < coarse["meeting_depth"] <= CLOSURE

    fine = shoreline_advance(native, dean_scale("fine_sand"), 900.0,
                             BERM, CLOSURE)
    assert fine["kind"] == "non-intersecting"
    assert fine["meeting"] is None


def test_finer_fill_below_the_critical_volume_gives_no_dry_beach(native):
    fine = dean_scale("fine_sand")
    critical = critical_volume(native, fine, BERM, CLOSURE)
    assert critical > 0

    below = shoreline_advance(native, fine, 0.9 * critical, BERM, CLOSURE)
    assert below["kind"] == "submerged"
    assert below["advance"] == 0.0
    assert "submerged terrace" in below["note"]

    above = shoreline_advance(native, fine, 1.5 * critical, BERM, CLOSURE)
    assert above["advance"] > 0.0


def test_critical_volume_is_zero_for_matched_or_coarser_fill(native):
    assert critical_volume(native, native, BERM, CLOSURE) == 0.0
    assert critical_volume(native, dean_scale("coarse_sand"), BERM, CLOSURE) == 0.0


def test_critical_volume_grows_as_the_borrow_gets_finer(native):
    volumes = [critical_volume(native, dean_scale(k), BERM, CLOSURE)
               for k in ("coarse_sand", "medium_sand", "fine_sand",
                         "very_fine_sand")]
    assert all(b >= a for a, b in zip(volumes, volumes[1:]))
    assert volumes[-1] > volumes[1]


def test_critical_volume_matches_its_closed_form(native):
    """V_crit = 0.4 h*^(5/2) (A_f^-3/2 - A_n^-3/2)."""
    fill = dean_scale("fine_sand")
    expected = 0.4 * CLOSURE**2.5 * (fill**-1.5 - native**-1.5)
    assert critical_volume(native, fill, BERM, CLOSURE) == pytest.approx(expected)


def test_volume_rises_monotonically_with_advance(native):
    fill = dean_scale("coarse_sand")
    volumes = [fill_volume_for_advance(native, fill, a, BERM, CLOSURE)["volume"]
               for a in (0.0, 5.0, 20.0, 60.0, 150.0)]
    assert all(b > a for a, b in zip(volumes, volumes[1:]))


def test_a_deeper_closure_costs_more_sand(native):
    shallow = fill_volume_for_advance(native, native, 30.0, BERM, 4.0)["volume"]
    deep = fill_volume_for_advance(native, native, 30.0, BERM, 10.0)["volume"]
    assert deep > shallow


def test_volume_validates_its_inputs(native):
    with pytest.raises(ValueError):
        fill_volume_for_advance(native, native, -1.0, BERM, CLOSURE)
    with pytest.raises(ValueError):
        fill_volume_for_advance(native, native, 10.0, BERM, 0.0)
    with pytest.raises(ValueError):
        fill_volume_for_advance(native, -0.1, 10.0, BERM, CLOSURE)


def test_advance_rejects_a_negative_volume(native):
    with pytest.raises(ValueError):
        shoreline_advance(native, native, -5.0, BERM, CLOSURE)


# ---------------------------------------------------------------------------
# Comparing a borrow source with the native beach
# ---------------------------------------------------------------------------


def test_overfill_factor_is_one_for_matched_sand():
    got = profile_overfill_factor("medium_sand", "medium_sand", BERM, CLOSURE)
    assert got["factor"] == pytest.approx(1.0)


def test_overfill_factor_is_below_one_for_coarser_borrow():
    got = profile_overfill_factor("medium_sand", "coarse_sand", BERM, CLOSURE)
    assert got["factor"] < 1.0


def test_overfill_factor_is_above_one_for_finer_borrow():
    got = profile_overfill_factor("medium_sand", "fine_sand", BERM, CLOSURE)
    assert got["factor"] > 1.0


def test_compatibility_signs_follow_the_phi_convention():
    coarser = grain_compatibility("medium_sand", "coarse_sand")
    finer = grain_compatibility("medium_sand", "fine_sand")
    assert coarser["delta"] < 0 and coarser["coarser"] is True
    assert finer["delta"] > 0 and finer["coarser"] is False


def test_compatibility_verdicts_read_the_right_way():
    assert "well suited" in grain_compatibility("medium_sand", "coarse_sand")["verdict"]
    assert "suitable" in grain_compatibility("medium_sand", "medium_sand")["verdict"]
    assert "poorly suited" in grain_compatibility("medium_sand", "very_fine_sand")["verdict"]


def test_compatibility_flags_a_worse_graded_borrow():
    native = sediment("fine_sand")
    scruffy = sediment("fine_sand").__class__(
        "Mixed borrow", d50=native.d50, phi_sorting=3.0 * native.phi_sorting)
    got = grain_compatibility(native, scruffy)
    assert got["sorting_ratio"] == pytest.approx(3.0)
    assert "winnow" in got["verdict"]


def test_compatibility_refuses_a_cohesive_source():
    with pytest.raises(ValueError):
        grain_compatibility("medium_sand", "soft_clay")
