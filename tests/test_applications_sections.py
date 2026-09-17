"""Section drawings: geometry, layer offsets, quantities and sheets."""

import math

import numpy as np
import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")

from pyCoastal.applications.seawall import design_seawall  # noqa: E402
from pyCoastal.applications.sections import (  # noqa: E402
    MoundProfile,
    draw_rubble_mound,
    draw_seawall,
    mound_layer_volumes,
    rubble_mound_section,
    draw_channel,
    rubble_mound_sheet,
    seawall_notes,
    seawall_section,
    seawall_sheet,
)
from pyCoastal.applications.structures import (  # noqa: E402
    DesignConditions,
    design_rubble_mound,
)
from pyCoastal.drafting import Section  # noqa: E402


@pytest.fixture
def conditions():
    return DesignConditions.from_peak_period(Hm0=2.8, Tp=9.5, depth=8.5)


@pytest.fixture
def wall(conditions):
    return design_seawall(conditions, 2.9, -5.6, tolerable_use="trained_staff")


@pytest.fixture
def mound():
    c = DesignConditions.from_peak_period(Hm0=4.0, Tp=11.0, depth=14.0)
    return design_rubble_mound(c, cot_alpha=2.0)


# ---------------------------------------------------------------------------
# Mound geometry
# ---------------------------------------------------------------------------


def test_profile_points_run_toe_to_toe():
    p = MoundProfile(-3.0, 3.0, crest=5.0, cot_sea=2.0, cot_land=1.5)
    pts = p.points(bed=-5.0)
    assert pts.shape == (4, 2)
    # Seaward toe is 2 x 10 m out from the seaward crest edge.
    assert pts[0, 0] == pytest.approx(-3.0 - 2.0 * 10.0)
    assert pts[-1, 0] == pytest.approx(3.0 + 1.5 * 10.0)
    assert pts[1, 1] == pytest.approx(5.0)


def test_profile_refuses_a_crest_below_the_bed():
    p = MoundProfile(-3.0, 3.0, crest=-6.0, cot_sea=2.0, cot_land=2.0)
    with pytest.raises(ValueError):
        p.points(bed=-5.0)


def test_offset_is_a_true_perpendicular_distance():
    """The gap between the two faces, measured normal to them, is t."""
    t = 1.3
    outer = MoundProfile(-4.0, 4.0, crest=6.0, cot_sea=2.0, cot_land=2.0)
    inner = outer.offset(t)

    # Distance between two parallel lines x + cot z = c is |dc| / sqrt(1+cot^2).
    cot = outer.cot_sea
    c_outer = -outer.x_sea + cot * outer.crest
    c_inner = -inner.x_sea + cot * inner.crest
    assert abs(c_outer - c_inner) / math.hypot(1.0, cot) == pytest.approx(t)


def test_offset_lowers_the_crest_by_exactly_the_thickness():
    outer = MoundProfile(-4.0, 4.0, crest=6.0, cot_sea=2.0, cot_land=1.5)
    assert outer.offset(0.8).crest == pytest.approx(5.2)


def test_offset_of_zero_changes_nothing():
    outer = MoundProfile(-4.0, 4.0, crest=6.0, cot_sea=2.0, cot_land=1.5)
    assert outer.offset(0.0) == outer


def test_offset_rejects_a_negative_thickness():
    with pytest.raises(ValueError):
        MoundProfile(-4.0, 4.0, 6.0, 2.0, 2.0).offset(-0.5)


def test_area_matches_the_trapezoid_formula():
    bed, crest = -5.0, 5.0
    p = MoundProfile(-3.0, 3.0, crest=crest, cot_sea=2.0, cot_land=2.0)
    h = crest - bed
    top, base = 6.0, 6.0 + (2.0 + 2.0) * h
    assert p.area(bed) == pytest.approx(0.5 * (top + base) * h)


def test_layer_volumes_sum_to_the_outer_area():
    bed = -8.0
    outer = MoundProfile(-4.0, 4.0, crest=6.0, cot_sea=2.0, cot_land=1.5)
    under = outer.offset(2.0)
    core = under.offset(1.0)
    areas = mound_layer_volumes([outer, under, core], bed)
    assert sum(areas) == pytest.approx(outer.area(bed))
    assert all(a > 0 for a in areas)


# ---------------------------------------------------------------------------
# Seawall drawing
# ---------------------------------------------------------------------------


def test_draw_seawall_extents_contain_the_structure(wall):
    dwg = Section()
    (x0, x1), (z0, z1) = draw_seawall(dwg, wall)
    assert x0 < 0.0 < wall.base_width < x1
    assert z0 < wall.founding_level
    assert z1 > wall.crest_level


def test_draw_seawall_puts_every_layer_in_the_dxf_queue(wall):
    dwg = Section()
    draw_seawall(dwg, wall)
    layers = {entry[2] for entry in dwg._dxf}
    for expected in ("SUBGRADE", "REINFORCED", "TOE", "GRANULAR", "BLINDING"):
        assert expected in layers


def test_draw_seawall_can_be_drawn_bare(wall):
    """Without annotation there are no dimensions, only geometry."""
    bare = Section()
    draw_seawall(bare, wall, annotate=False)
    assert not bare.ax.texts


def test_seawall_notes_carry_the_governing_numbers(wall):
    text = " ".join(seawall_notes(wall))
    assert f"{wall.crest_level:+.2f}" in text
    assert f"{wall.toe_Dn50:.2f}" in text
    assert "EurOtop" in text


def test_seawall_notes_repeat_the_design_warnings():
    shallow = DesignConditions.from_peak_period(Hm0=2.2, Tp=9.0, depth=3.6)
    result = design_seawall(shallow, 2.9, -0.7)
    assert any(n.startswith("WARNING") for n in seawall_notes(result))


def test_seawall_section_builds_a_figure(wall):
    dwg = seawall_section(wall)
    assert dwg.ax.patches
    assert dwg.ax.get_aspect() == 1.0


def test_seawall_sheet_states_the_scale_it_drew(wall):
    sheet = seawall_sheet(wall, size="A3")
    assert sheet.titleblock.scale.startswith("1:")
    assert sheet.titleblock.scale.endswith("@ A3")
    assert sheet.views[0].scale_text == sheet.titleblock.scale


def test_seawall_sheet_scale_shows_the_whole_structure(wall):
    sheet = seawall_sheet(wall, size="A3")
    view = sheet.views[0]
    x0, x1 = view.ax.get_xlim()
    z0, z1 = view.ax.get_ylim()
    assert x0 <= 0.0 and x1 >= wall.base_width
    assert z0 <= wall.founding_level and z1 >= wall.crest_level


def test_seawall_sheet_exports_geometry(wall, tmp_path):
    sheet = seawall_sheet(wall, size="A3")
    path = tmp_path / "wall.dxf"
    sheet.to_dxf(path)
    assert "REINFORCED" in path.read_text()


# ---------------------------------------------------------------------------
# Rubble mound drawing
# ---------------------------------------------------------------------------


def test_draw_rubble_mound_layers_nest(mound):
    dwg = Section()
    draw_rubble_mound(dwg, mound, still_water_level=0.0, seabed_level=-14.0)
    layers = {entry[2] for entry in dwg._dxf}
    assert {"ARMOUR", "UNDERLAYER", "CORE", "TOE"} <= layers


def test_rubble_mound_refuses_a_crest_under_the_seabed(mound):
    dwg = Section()
    with pytest.raises(ValueError):
        draw_rubble_mound(dwg, mound, still_water_level=0.0, seabed_level=50.0)


def test_rubble_mound_section_builds_a_figure(mound):
    dwg = rubble_mound_section(mound, still_water_level=0.0, seabed_level=-14.0)
    assert dwg.ax.patches


def test_rubble_mound_sheet_states_its_scale(mound):
    sheet = rubble_mound_sheet(mound, still_water_level=0.0, seabed_level=-14.0,
                               size="A3")
    assert sheet.titleblock.scale.startswith("1:")


def test_steeper_landward_slope_uses_less_material(mound):
    """A 1:1.5 back slope is a smaller section than 1:3, at the same crest."""
    dwg = Section()
    (x0_steep, x1_steep), _ = draw_rubble_mound(
        dwg, mound, 0.0, -14.0, cot_land=1.5, annotate=False
    )
    dwg2 = Section()
    (x0_flat, x1_flat), _ = draw_rubble_mound(
        dwg2, mound, 0.0, -14.0, cot_land=3.0, annotate=False
    )
    assert x1_steep < x1_flat


# ---------------------------------------------------------------------------
# Navigation channel drawing
# ---------------------------------------------------------------------------


@pytest.fixture
def waterway():
    from pyCoastal.applications.channel import Vessel, design_channel

    ship = Vessel(name="Test ship", length=300.0, beam=45.0, draught=14.0,
                  block_coefficient=0.70)
    return design_channel(ship, speed=8.0, design_water_level=1.2, Hs=1.5,
                          Tp=9.0, existing_bed=-11.0, two_way=True)


def test_vessel_outline_is_closed_and_the_right_size():
    from pyCoastal.applications.sections import vessel_outline

    hull = vessel_outline(beam=40.0, draught=12.0, freeboard=6.0)
    assert hull[:, 1].min() == pytest.approx(-12.0)
    assert hull[:, 1].max() == pytest.approx(6.0)
    # The waterline beam is the moulded beam; only the flare is wider.
    at_waterline = hull[np.isclose(hull[:, 1], 0.0)][:, 0]
    assert at_waterline.max() - at_waterline.min() == pytest.approx(40.0)


def test_vessel_outline_rejects_nonsense():
    from pyCoastal.applications.sections import vessel_outline

    with pytest.raises(ValueError):
        vessel_outline(beam=0.0, draught=5.0, freeboard=2.0)


def test_draw_channel_covers_the_dredged_prism(waterway):
    dwg = Section()
    (x0, x1), (z0, z1) = draw_channel(dwg, waterway)
    assert x0 < -0.5 * waterway.width
    assert x1 > 0.5 * waterway.width
    assert z0 < waterway.dredge_level
    assert z1 > waterway.design_water_level


def test_draw_channel_can_omit_the_depth_chain(waterway):
    with_chain = Section()
    draw_channel(with_chain, waterway, show_depth_chain=True)
    without = Section()
    draw_channel(without, waterway, show_depth_chain=False)
    assert len(without.ax.texts) < len(with_chain.ax.texts)


def test_channel_detail_is_cropped_to_the_keel(waterway):
    from pyCoastal.applications.sections import draw_channel_detail

    dwg = Section()
    (x0, x1), (z0, z1) = draw_channel_detail(dwg, waterway)
    assert x1 - x0 < waterway.vessel.beam
    assert z0 < waterway.dredge_level
    # The view stops just above the keel, not at the waterline.
    assert z1 < waterway.design_water_level


def test_channel_section_is_exaggerated_and_says_so(waterway):
    from pyCoastal.applications.sections import channel_section

    dwg = channel_section(waterway, exaggeration=8.0)
    assert dwg.exaggeration == 8.0
    assert "EXAGGERATION" in dwg.subtitle.upper()


def test_channel_section_can_be_drawn_true(waterway):
    from pyCoastal.applications.sections import channel_section

    dwg = channel_section(waterway, exaggeration=1.0)
    assert "EXAGGERATION" not in dwg.subtitle.upper()


def test_channel_sheet_carries_both_views(waterway):
    from pyCoastal.applications.sections import channel_sheet

    sheet = channel_sheet(waterway, size="A3")
    assert len(sheet.views) == 3          # section, detail, notes column
    overall, detail = sheet.views[0], sheet.views[1]
    assert overall.exaggeration > 1.0
    assert detail.exaggeration == 1.0
    assert overall.exaggeration_note
    assert not detail.exaggeration_note


def test_channel_notes_name_the_governing_numbers(waterway):
    from pyCoastal.applications.sections import channel_notes

    text = " ".join(channel_notes(waterway))
    assert f"{waterway.dredge_level:+.2f}" in text
    assert "PIANC" in text
    assert "ICORELS" in text
