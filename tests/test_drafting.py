"""Drawing primitives: geometry, scale, and the DXF export."""

import math

import numpy as np
import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")

from pyCoastal.drafting import (  # noqa: E402
    MATERIALS,
    PAPER,
    Section,
    Sheet,
    TitleBlock,
    use_crisp_style,
    write_dxf,
)


def test_material_polygon_needs_three_points():
    dwg = Section()
    with pytest.raises(ValueError):
        dwg.material([[0, 0], [1, 1]], "concrete")


def test_unknown_material_names_the_options():
    dwg = Section()
    with pytest.raises(KeyError) as excinfo:
        dwg.material([[0, 0], [1, 0], [1, 1]], "unobtainium")
    assert "concrete" in str(excinfo.value)


def test_every_material_has_a_usable_hatch():
    # matplotlib silently ignores an unknown hatch character, which would
    # leave a layer looking like a plain fill on every drawing.
    allowed = set("/\\|-+xoO.*")
    for name, material in MATERIALS.items():
        if material.hatch is not None:
            assert set(material.hatch) <= allowed, name


def test_caps_only_affects_callouts_when_asked():
    plain, shouty = Section(caps=False), Section(caps=True)
    assert plain._t("crest level") == "crest level"
    assert shouty._t("crest level") == "CREST LEVEL"


def test_dim_style_is_validated():
    with pytest.raises(ValueError):
        Section(dim_style="squiggle")


def test_fit_scale_picks_a_standard_scale_that_fits():
    dwg = Section(figsize=(10.0, 5.0))
    dwg.fit_scale((0.0, 100.0), (-10.0, 10.0))
    assert dwg.scale in Section.STANDARD_SCALES

    # The requested extents must actually be inside the fitted view.
    x0, x1 = dwg.ax.get_xlim()
    z0, z1 = dwg.ax.get_ylim()
    assert x0 <= 0.0 and x1 >= 100.0
    assert z0 <= -10.0 and z1 >= 10.0


def test_fit_scale_is_a_true_scale_in_both_directions():
    """One metre of paper must be the same number of metres either way."""
    dwg = Section(figsize=(12.0, 6.0))
    scale = dwg.fit_scale((0.0, 80.0), (-5.0, 15.0))

    pos = dwg.ax.get_position()
    fig_w, fig_h = dwg.fig.get_size_inches()
    x0, x1 = dwg.ax.get_xlim()
    z0, z1 = dwg.ax.get_ylim()

    per_inch_x = (x1 - x0) / (pos.width * fig_w)
    per_inch_z = (z1 - z0) / (pos.height * fig_h)
    assert per_inch_x == pytest.approx(per_inch_z, rel=1e-9)
    assert per_inch_x / 0.0254 == pytest.approx(scale, rel=1e-9)


def test_fit_scale_reports_the_paper_size():
    dwg = Section(figsize=(8.0, 4.0))
    dwg.fit_scale((0.0, 50.0), (0.0, 10.0), paper="A3")
    assert dwg.scale_text.endswith("@ A3")
    assert dwg.scale_text.startswith("1:")


def test_fit_scale_rejects_a_zero_extent():
    dwg = Section()
    with pytest.raises(ValueError):
        dwg.fit_scale((5.0, 5.0), (0.0, 1.0))


def test_dxf_round_trip_has_one_line_per_edge(tmp_path):
    path = tmp_path / "out.dxf"
    square = [[0, 0], [1, 0], [1, 1], [0, 1]]
    write_dxf(path, [("POLY", square, "TEST")])
    text = path.read_text()

    # A closed square is four edges, and R12 needs the file markers.
    assert text.count("\nLINE\n") == 4
    assert text.startswith("0\nSECTION")
    assert text.rstrip().endswith("EOF")
    assert "TEST" in text


def test_dxf_open_polyline_is_not_closed(tmp_path):
    path = tmp_path / "open.dxf"
    write_dxf(path, [("LINE", [[0, 0], [1, 0], [2, 0]], "L")])
    assert path.read_text().count("\nLINE\n") == 2


def test_dxf_scale_multiplies_coordinates(tmp_path):
    path = tmp_path / "scaled.dxf"
    write_dxf(path, [("LINE", [[0, 0], [2, 0]], "L")], scale=1000.0)
    assert "2000.000000" in path.read_text()


def test_section_to_dxf_carries_the_drawn_geometry(tmp_path):
    dwg = Section()
    dwg.material([[0, 0], [4, 0], [4, 2], [0, 2]], "concrete")
    dwg.line([[0, 3], [4, 3]])
    path = tmp_path / "section.dxf"
    dwg.to_dxf(path)
    text = path.read_text()
    assert "CONCRETE" in text
    assert "LINES" in text


def test_sheet_rejects_an_unknown_paper_size():
    with pytest.raises(KeyError):
        Sheet(TitleBlock(), size="A9")


def test_sheet_rejects_a_strip_wider_than_the_sheet():
    with pytest.raises(ValueError):
        Sheet(TitleBlock(), size="A4", strip=400.0)


def test_sheet_paper_sizes_are_landscape():
    for name, (w, h) in PAPER.items():
        assert w > h, name


def test_sheet_viewport_scale_reaches_the_title_block():
    sheet = Sheet(TitleBlock(project="P", title="T"), size="A3")
    view = sheet.viewport()
    view.fit_scale((0.0, 40.0), (-5.0, 5.0), paper="A3")
    sheet.set_scale_from(view)
    assert sheet.titleblock.scale == view.scale_text


def test_sheet_refuses_to_state_a_scale_it_was_not_given():
    sheet = Sheet(TitleBlock(), size="A4")
    with pytest.raises(RuntimeError):
        sheet.set_scale_from(sheet.viewport())


def test_sheet_views_default_to_drawing_office_conventions():
    sheet = Sheet(TitleBlock(), size="A3")
    view = sheet.viewport()
    assert view.caps is True
    assert view.dim_style == "tick"
    assert view.frame is False


def test_sheet_dxf_gathers_every_view(tmp_path):
    sheet = Sheet(TitleBlock(), size="A3")
    left = sheet.viewport(rect=(0, 0, 0.5, 1))
    right = sheet.viewport(rect=(0.5, 0, 0.5, 1))
    left.material([[0, 0], [1, 0], [1, 1]], "concrete")
    right.material([[0, 0], [1, 0], [1, 1]], "sand")
    path = tmp_path / "sheet.dxf"
    sheet.to_dxf(path)
    text = path.read_text()
    assert "CONCRETE" in text and "SAND" in text


def test_use_crisp_style_sets_arial_and_keeps_hatching_thin():
    use_crisp_style()
    assert matplotlib.rcParams["font.sans-serif"][0] == "Arial"
    assert matplotlib.rcParams["hatch.linewidth"] < 1.0


def test_scale_bar_needs_divisions():
    dwg = Section()
    dwg.finish(xlim=(0, 10), zlim=(0, 5), grid=False)
    with pytest.raises(ValueError):
        dwg.scale_bar(5.0, divisions=0)


def test_notes_block_wraps_without_dropping_text():
    dwg = Section()
    long_note = "word " * 40
    dwg.notes_block([long_note], width=30)
    drawn = [t.get_text() for t in dwg.ax.texts]
    assert any("word" in t for t in drawn)
    # Nothing should exceed the wrap width by more than the numbering prefix.
    for line in drawn[0].split("\n")[1:]:
        assert len(line) <= 30 + 4
