"""The nourishment planform: the analytical map and the scales it is drawn at.

The plan view broke assumptions the section views never exercised: extents
of kilometres against tens of metres, a stretched axis that is not vertical,
and a scale ladder that ran out. These cover what came of that.
"""

import math

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from pyCoastal.applications.nourishment import (  # noqa: E402
    SECONDS_PER_YEAR,
    NourishmentDesign,
    WaveClimate,
    dean_scale,
    longshore_diffusivity,
    pelnard_considere,
    shoreline_advance,
)
from pyCoastal.applications.sections import (  # noqa: E402
    draw_nourishment_plan,
    nourishment_plan_section,
    nourishment_sheet,
    plan_margin,
    spreading_half_life,
)
from pyCoastal.drafting import Section, Sheet, TitleBlock  # noqa: E402


@pytest.fixture
def design():
    return NourishmentDesign(length=1500.0, berm_width=40.0, taper=150.0,
                             D=6.0, B=2.0)


@pytest.fixture
def climate():
    return WaveClimate(Hb=1.2, T=8.0, alpha0=0.0)


# ---------------------------------------------------------------------------
# The fill's own clock
# ---------------------------------------------------------------------------


def test_half_life_halves_the_centre_width(design, climate):
    """The definition, checked against the solution it was derived from."""
    t = spreading_half_life(design, climate)
    centre = pelnard_considere(np.array([0.0]), t, design, climate)
    assert float(centre[0]) == pytest.approx(0.5 * design.berm_width, rel=1e-6)


def test_half_life_grows_with_the_square_of_the_length(climate):
    short = NourishmentDesign(length=1000.0, berm_width=40.0, taper=100.0,
                              D=6.0, B=2.0)
    long = NourishmentDesign(length=2000.0, berm_width=40.0, taper=100.0,
                             D=6.0, B=2.0)
    ratio = spreading_half_life(long, climate) / spreading_half_life(short, climate)
    assert ratio == pytest.approx(4.0, rel=1e-9)


def test_a_calmer_climate_keeps_the_fill_longer(design):
    calm = WaveClimate(Hb=0.6, T=8.0, alpha0=0.0)
    rough = WaveClimate(Hb=1.8, T=8.0, alpha0=0.0)
    assert spreading_half_life(design, calm) > spreading_half_life(design, rough)


def test_half_life_does_not_depend_on_the_width_placed(climate):
    """Diffusion is linear: a wider fill decays on the same clock."""
    thin = NourishmentDesign(length=1500.0, berm_width=20.0, taper=150.0,
                             D=6.0, B=2.0)
    fat = NourishmentDesign(length=1500.0, berm_width=80.0, taper=150.0,
                            D=6.0, B=2.0)
    assert (spreading_half_life(thin, climate)
            == pytest.approx(spreading_half_life(fat, climate), rel=1e-9))


# ---------------------------------------------------------------------------
# How far past the fill to draw
# ---------------------------------------------------------------------------


def test_margin_covers_the_spreading_length(design, climate):
    years = [0.0, 2.0]
    spread = math.sqrt(longshore_diffusivity(climate, design)
                       * 2.0 * SECONDS_PER_YEAR)
    assert plan_margin(design, climate, years) >= spread


def test_margin_grows_with_the_latest_time_drawn(design, climate):
    near = plan_margin(design, climate, [0.0, 1.0])
    far = plan_margin(design, climate, [0.0, 20.0])
    assert far > near


def test_margin_has_a_floor_for_a_fill_drawn_at_placement(design, climate):
    """At t = 0 nothing has spread, but the drawing still needs context."""
    assert plan_margin(design, climate, [0.0]) >= 0.6 * design.length


# ---------------------------------------------------------------------------
# The drawing itself
# ---------------------------------------------------------------------------


def test_plan_extents_straddle_the_fill(design, climate):
    dwg = Section(figsize=(10.0, 4.0))
    (x0, x1), (y0, y1) = draw_nourishment_plan(dwg, design, climate,
                                               [0.0, 1.0])
    assert x0 < -0.5 * design.length
    assert x1 > 0.5 * design.length
    assert x0 == pytest.approx(-x1)
    assert y0 < 0.0 < y1


def test_the_plan_shows_the_full_placed_width(design, climate):
    """A drawing that crops the fill it is drawing is worse than no drawing."""
    dwg = Section(figsize=(10.0, 4.0))
    _, (_, y1) = draw_nourishment_plan(dwg, design, climate, [0.0, 1.0])
    assert y1 >= design.berm_width


def test_a_respected_margin_sets_the_extents(design, climate):
    dwg = Section(figsize=(10.0, 4.0))
    (x0, x1), _ = draw_nourishment_plan(dwg, design, climate, [0.0, 1.0],
                                        margin=900.0)
    assert x1 == pytest.approx(0.5 * design.length + 900.0)


def test_later_times_are_drawn_lower_at_the_centre(design, climate):
    """Each curve must sit under the one before it, or the plan is wrong."""
    years = [0.0, 0.5, 1.0, 4.0]
    centres = [float(pelnard_considere(np.array([0.0]),
                                       y * SECONDS_PER_YEAR, design, climate)[0])
               for y in years]
    assert all(b < a for a, b in zip(centres, centres[1:]))


def test_the_plan_rejects_a_negative_time(design, climate):
    dwg = Section(figsize=(8.0, 3.0))
    with pytest.raises(ValueError):
        draw_nourishment_plan(dwg, design, climate, [0.0, -1.0])


def test_the_plan_rejects_an_empty_set_of_times(design, climate):
    dwg = Section(figsize=(8.0, 3.0))
    with pytest.raises(ValueError):
        draw_nourishment_plan(dwg, design, climate, [])


# ---------------------------------------------------------------------------
# The standalone figure
# ---------------------------------------------------------------------------


def test_plan_section_picks_times_from_the_half_life(design, climate):
    dwg = nourishment_plan_section(design, climate)
    half = spreading_half_life(design, climate) / SECONDS_PER_YEAR
    assert f"{half:.2f}" in dwg.subtitle


def test_plan_section_states_which_axis_is_stretched(design, climate):
    dwg = nourishment_plan_section(design, climate)
    assert "CROSS-SHORE EXAGGERATION" in dwg.subtitle
    assert "VERTICAL" not in dwg.subtitle
    assert dwg.exaggeration_axis == "CROSS-SHORE"


def test_plan_section_actually_exaggerates(design, climate):
    """A true-scale plan of a 1.5 km fill is a hairline; refuse to draw one."""
    dwg = nourishment_plan_section(design, climate)
    assert dwg.exaggeration > 5.0


def test_plan_section_honours_an_explicit_exaggeration(design, climate):
    dwg = nourishment_plan_section(design, climate, exaggeration=12.0)
    assert dwg.exaggeration == pytest.approx(12.0)
    assert "12:1" in dwg.subtitle


def test_plan_section_honours_explicit_times(design, climate):
    dwg = nourishment_plan_section(design, climate, years=[0.0, 3.0])
    assert "3 yr" in "".join(t.get_text() for t in dwg.ax.texts)


# ---------------------------------------------------------------------------
# On a sheet
# ---------------------------------------------------------------------------


@pytest.fixture
def profile_result():
    return shoreline_advance(dean_scale("medium_sand"),
                             dean_scale("coarse_sand"), 250.0, 2.0, 6.0)


def test_sheet_without_a_plan_keeps_one_view(profile_result):
    sheet = nourishment_sheet(profile_result, "medium_sand", "coarse_sand",
                              2.0, 6.0)
    labels = [t.get_text() for ax in sheet.fig.axes for t in ax.texts]
    assert not any("PLANFORM EVOLUTION" in t for t in labels)


def test_sheet_with_a_plan_adds_a_second_view(profile_result, design, climate):
    sheet = nourishment_sheet(profile_result, "medium_sand", "coarse_sand",
                              2.0, 6.0, plan_design=design, plan_climate=climate)
    labels = [t.get_text() for ax in sheet.fig.axes for t in ax.texts]
    assert any("PLANFORM EVOLUTION" in t for t in labels)
    assert any("CROSS-SHORE EXAGGERATION" in t for t in labels)


def test_a_plan_needs_both_a_design_and_a_climate(profile_result, design):
    """Half the pair is a mistake, not a request for a plan."""
    sheet = nourishment_sheet(profile_result, "medium_sand", "coarse_sand",
                              2.0, 6.0, plan_design=design)
    labels = [t.get_text() for ax in sheet.fig.axes for t in ax.texts]
    assert not any("PLANFORM EVOLUTION" in t for t in labels)


def test_both_of_the_plans_scales_are_standard(profile_result, design, climate):
    """The whole point of a stated scale is that it can be measured off."""
    sheet = nourishment_sheet(profile_result, "medium_sand", "coarse_sand",
                              2.0, 6.0, plan_design=design, plan_climate=climate)
    text = next(t.get_text() for ax in sheet.fig.axes for t in ax.texts
                if t.get_text().startswith("SCALE H 1:")
                and "CROSS-SHORE" in t.get_text())
    horizontal, vertical = text.split("1:")[1:3]
    for value in (horizontal.split()[0], vertical.split()[0]):
        assert float(value) in Section.STANDARD_SCALES


# ---------------------------------------------------------------------------
# The drafting machinery the plan view needed
# ---------------------------------------------------------------------------


def test_auto_exaggeration_fills_the_viewport():
    view = Section(figsize=(10.0, 2.5))
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    e = view.auto_exaggeration((0.0, 4000.0), (0.0, 50.0))
    # 4000/50 = 80 wide against a 4:1 sheet.
    assert e == pytest.approx(20.0, rel=1e-6)
    assert view.exaggeration == pytest.approx(e)


def test_auto_exaggeration_never_squashes_a_view():
    """Content taller than its paper would want e < 1; it gets 1 instead."""
    view = Section(figsize=(4.0, 8.0))
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    assert view.auto_exaggeration((0.0, 10.0), (0.0, 100.0)) == pytest.approx(1.0)


def test_auto_exaggeration_is_capped():
    view = Section(figsize=(8.0, 4.0))
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    assert view.auto_exaggeration((0.0, 1e6), (0.0, 1.0), cap=50.0) == 50.0


def test_auto_exaggeration_rejects_a_flat_extent():
    view = Section(figsize=(8.0, 4.0))
    with pytest.raises(ValueError):
        view.auto_exaggeration((0.0, 100.0), (5.0, 5.0))


def test_the_ladder_reaches_site_plan_scales():
    assert 25000 in Section.STANDARD_SCALES
    assert max(Section.STANDARD_SCALES) >= 50000


def test_extents_fitted_to_a_rung_stay_on_that_rung():
    """The bug this came from: required = rung + 1e-9 skipped a whole rung."""
    view = Section(figsize=(10.0, 5.0))
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    width = 10.0 * 0.0254 * 2500          # exactly 1:2500 across the paper
    assert view.fit_scale((0.0, width), (0.0, 1.0)) == 2500


def test_round_vertical_lands_on_a_standard_denominator():
    view = Section(figsize=(10.0, 5.0), exaggeration=7.0)
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    view.fit_scale((0.0, 3000.0), (0.0, 40.0), round_vertical=True)
    assert view.vertical_scale in Section.STANDARD_SCALES


def test_round_vertical_still_fits_the_extents():
    view = Section(figsize=(10.0, 5.0), exaggeration=7.0)
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    view.fit_scale((0.0, 3000.0), (0.0, 40.0), round_vertical=True)
    lo, hi = view.ax.get_ylim()
    assert lo <= 0.0 and hi >= 40.0


def test_round_vertical_is_off_by_default():
    view = Section(figsize=(10.0, 5.0), exaggeration=7.0)
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    view.fit_scale((0.0, 3000.0), (0.0, 40.0))
    assert view.exaggeration == pytest.approx(7.0)


def test_the_exaggeration_note_names_its_axis():
    view = Section(figsize=(10.0, 5.0), exaggeration=4.0)
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    view.exaggeration_axis = "CROSS-SHORE"
    view.fit_scale((0.0, 1000.0), (0.0, 20.0))
    assert view.exaggeration_note.startswith("CROSS-SHORE")


def test_a_true_scale_view_carries_no_exaggeration_note():
    view = Section(figsize=(10.0, 5.0))
    view.ax.set_position((0.0, 0.0, 1.0, 1.0))
    view.fit_scale((0.0, 100.0), (0.0, 20.0))
    assert view.exaggeration_note == ""


def test_a_sheet_viewport_defaults_to_a_vertical_note():
    sheet = Sheet(TitleBlock(title="t"), size="A3")
    view = sheet.viewport(rect=(0.0, 0.0, 0.6, 0.6), exaggeration=3.0)
    view.fit_scale((0.0, 300.0), (0.0, 20.0))
    assert view.exaggeration_note.startswith("VERTICAL")
