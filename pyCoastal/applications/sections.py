"""
Design sections: a sized structure in, a drawing and a take-off out.

The design modules decide the numbers. This module turns those numbers into
the deliverable an engineer actually hands over: a dimensioned cross-section
with the materials hatched, the governing levels called out, the design
inputs printed on the sheet, and specification notes beside it.

Each structure has three entry points.

``draw_*``
    Puts the geometry and annotation into a :class:`~pyCoastal.drafting.Section`
    you already have, and returns the extents it needs.
``*_section``
    A standalone figure with plot axes, for a report or a slide.
``*_sheet``
    A full drawing sheet with a border, a title block and notes, at a true
    stated scale.

All three take a design object, not a pile of loose numbers, so the drawing
cannot drift out of step with the calculation behind it.

Needs matplotlib::

    pip install pyCoastal[plots]
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date

import numpy as np

from ..drafting import Section, Sheet, TitleBlock

__all__ = [
    "MoundProfile",
    "draw_seawall",
    "seawall_section",
    "seawall_sheet",
    "draw_seawall_toe_detail",
    "draw_rubble_mound",
    "rubble_mound_section",
    "rubble_mound_sheet",
    "mound_layer_volumes",
    "vessel_outline",
    "draw_channel",
    "channel_notes",
    "channel_section",
    "channel_sheet",
    "draw_channel_detail",
]


# ---------------------------------------------------------------------------
# Trapezoidal mound geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MoundProfile:
    """A trapezoidal mound, described by its crest and its two slopes.

    Attributes
    ----------
    x_sea, x_land : float
        Chainage of the seaward and landward crest edges [m].
    crest : float
        Crest level [m].
    cot_sea, cot_land : float
        Slopes as horizontal run per unit rise.
    """

    x_sea: float
    x_land: float
    crest: float
    cot_sea: float
    cot_land: float

    def points(self, bed: float) -> np.ndarray:
        """Closed polygon from the seaward toe round to the landward toe."""
        if self.crest <= bed:
            raise ValueError(
                f"Crest {self.crest} is not above the bed {bed}; nothing to draw"
            )
        rise = self.crest - bed
        return np.array(
            [
                [self.x_sea - self.cot_sea * rise, bed],
                [self.x_sea, self.crest],
                [self.x_land, self.crest],
                [self.x_land + self.cot_land * rise, bed],
            ]
        )

    def offset(self, thickness: float) -> "MoundProfile":
        """The profile a uniform layer of ``thickness`` inside this one.

        The offset is perpendicular to each face, which is how a layer
        thickness is specified and measured on site. Lowering the crest by
        the thickness and pulling the crest edges in by
        ``t (sqrt(1 + cot^2) - cot)`` is the exact perpendicular offset of a
        trapezoid, not an approximation.
        """
        if thickness < 0:
            raise ValueError(f"Thickness must be non-negative, got {thickness}")
        pull_sea = thickness * (math.hypot(1.0, self.cot_sea) - self.cot_sea)
        pull_land = thickness * (math.hypot(1.0, self.cot_land) - self.cot_land)
        return MoundProfile(
            x_sea=self.x_sea + pull_sea,
            x_land=self.x_land - pull_land,
            crest=self.crest - thickness,
            cot_sea=self.cot_sea,
            cot_land=self.cot_land,
        )

    def band(self, inner: "MoundProfile", bed: float) -> np.ndarray:
        """Closed polygon of the layer between this profile and ``inner``."""
        return np.vstack((self.points(bed), inner.points(bed)[::-1]))

    def area(self, bed: float) -> float:
        """Cross-sectional area above the bed [m2 per metre run]."""
        pts = self.points(bed)
        x, z = pts[:, 0], pts[:, 1]
        return 0.5 * abs(np.dot(x, np.roll(z, -1)) - np.dot(z, np.roll(x, -1)))


def mound_layer_volumes(profiles, bed: float) -> list[float]:
    """Area of each layer, from a list of profiles outermost first.

    Each entry is the area between one profile and the next, in m2 per metre
    run, with the innermost profile taken as solid. Multiply by the length of
    the trunk for a volume.
    """
    areas = [p.area(bed) for p in profiles]
    return [a - b for a, b in zip(areas, areas[1:])] + [areas[-1]]


def _sheet_for(title: str, project: str, file: str, **kwargs) -> TitleBlock:
    """A title block with the fields a generated drawing can honestly fill."""
    fields = dict(
        project=project,
        title=title,
        organisation="pyCoastal",
        file=file,
        date=date.today().isoformat(),
        sheet="1/1",
        revision="A",
        status="PRELIMINARY",
        drawn_by="pyCoastal",
        checked_by="",
    )
    fields.update(kwargs)
    return TitleBlock(**fields)


# ---------------------------------------------------------------------------
# Seawall
# ---------------------------------------------------------------------------


def draw_seawall(dwg: Section, design, sea_extent: float = 22.0,
                 land_extent: float = 8.0, show_scour: bool = True,
                 annotate: bool = True) -> tuple[tuple, tuple]:
    """Put a designed seawall into an open :class:`Section`.

    Returns the (xlim, zlim) the section needs, so the caller can either set
    them directly or hand them to
    :meth:`~pyCoastal.drafting.Section.fit_scale`.
    """
    d = design
    x0, x1 = -sea_extent, d.base_width + land_extent
    bed, swl = d.seabed_level, d.still_water_level
    found = d.founding_level
    base_top = found + d.base_thickness
    blinding = 0.15

    # -- ground and water --------------------------------------------------
    dwg.material(
        [[x0, bed - 12.0], [x1, bed - 12.0], [x1, bed], [x0, bed]],
        "subgrade", zorder=1.5,
    )
    dwg.water(x0, 0.0, swl, bed=bed, zorder=1.8)

    # -- toe protection ----------------------------------------------------
    berm_face = 1.5 * d.toe_berm_thickness
    dwg.material(
        [
            [-d.toe_berm_width - berm_face, bed],
            [-d.toe_berm_width, bed + d.toe_berm_thickness],
            [0.0, bed + d.toe_berm_thickness],
            [0.0, bed],
        ],
        "toe",
        label=f"Toe rock, Dn50 = {d.toe_Dn50:.2f} m ({d.toe_M50 / 1000:.2f} t)",
        zorder=2.5,
    )

    # -- the wall ----------------------------------------------------------
    dwg.material(
        [[0.0, found - blinding], [d.base_width, found - blinding],
         [d.base_width, found], [0.0, found]],
        "blinding", zorder=2.6,
    )
    for polygon in (
        [[0.0, found], [d.base_width, found],
         [d.base_width, base_top], [0.0, base_top]],
        [[0.0, base_top], [d.stem_thickness, base_top],
         [d.stem_thickness, d.crest_level], [0.0, d.crest_level]],
    ):
        dwg.material(polygon, "reinforced",
                     label="Reinforced concrete, base slab and stem", zorder=3.0)

    # -- backfill and promenade --------------------------------------------
    surfacing = 0.3
    dwg.material(
        [[d.stem_thickness, base_top], [x1, base_top],
         [x1, d.promenade_level - surfacing],
         [d.stem_thickness, d.promenade_level - surfacing]],
        "granular", zorder=2.2,
    )
    dwg.material(
        [[d.stem_thickness, d.promenade_level - surfacing],
         [x1, d.promenade_level - surfacing],
         [x1, d.promenade_level], [d.stem_thickness, d.promenade_level]],
        "pavement", label="Promenade surfacing", zorder=2.4,
    )

    # -- scour ------------------------------------------------------------
    wavelength = d.pressures.get("wavelength", 4.0 * d.water_depth)
    if show_scour and d.scour_depth > 0:
        # The hole sits at the first standing-wave node, a quarter wavelength
        # out. On a long wave that is off the sheet, so it is pulled in to
        # stay visible and the note says where it really is.
        half = min(max(2.0 * d.scour_depth, 0.10 * wavelength), 0.22 * sea_extent)
        centre = max(-0.25 * wavelength, -0.55 * sea_extent + half)
        xs = np.linspace(centre - half, centre + half, 120)
        hole = bed - d.scour_depth * np.cos(
            0.5 * np.pi * (xs - centre) / half
        ) ** 2
        dwg.line(np.column_stack((xs, hole)), weight="medium", style=(0, (6, 3)),
                 color="#8a2f24", zorder=3.5)
        if annotate:
            dwg.note(
                (centre, bed - d.scour_depth),
                f"Predicted scour {d.scour_depth:.2f} m at the node,\n"
                f"{0.25 * wavelength:.0f} m out (Xie 1981)",
                offset=(-14, -34), ha="right",
            )

    if annotate:
        # -- levels --------------------------------------------------------
        dwg.level(x0 + 0.5, swl, f"SWL {swl:+.2f} m CD", side="right",
                  symbol="water")
        dwg.level(d.stem_thickness, d.crest_level,
                  f"Crest {d.crest_level:+.2f} m CD", side="left")
        dwg.level(d.base_width, d.promenade_level,
                  f"Promenade {d.promenade_level:+.2f} m CD", side="right",
                  run=land_extent * 0.45)
        dwg.level(-d.toe_berm_width - berm_face, bed, f"Seabed {bed:+.2f} m CD",
                  side="right", run=-3.0)
        dwg.level(0.0, found, f"Founding {found:+.2f} m CD", side="left", run=-5.0)

        # -- dimensions ----------------------------------------------------
        dim_z = d.crest_level + 1.6
        dwg.dim_h(0.0, d.base_width, dim_z, f"B = {d.base_width:.2f}",
                  extend_from=(d.crest_level, d.promenade_level))
        dwg.dim_h(0.0, d.stem_thickness, dim_z + 1.4, f"{d.stem_thickness:.2f}",
                  extend_from=(d.crest_level, d.crest_level))
        dwg.dim_h(-d.toe_berm_width, 0.0, bed + d.toe_berm_thickness + 1.2,
                  f"{d.toe_berm_width:.1f}",
                  extend_from=(bed + d.toe_berm_thickness,
                               bed + d.toe_berm_thickness))

        dwg.dim_v(swl, d.crest_level, d.base_width + land_extent * 0.85,
                  f"Rc = {d.crest_freeboard:.2f}",
                  extend_from=(x0, d.stem_thickness))
        dwg.dim_v(found, bed, x0 + 3.0, f"{d.embedment:.2f}",
                  extend_from=(0.0, 0.0), side="left")
        dwg.dim_v(found, found + d.base_thickness, d.base_width + 1.4,
                  f"{d.base_thickness:.2f}",
                  extend_from=(d.base_width, d.base_width))
        dwg.dim_v(found, d.crest_level, x0 + 0.17 * sea_extent,
                  f"H = {d.wall_height:.2f}", extend_from=(0.0, 0.0), side="left")

        # -- notes ---------------------------------------------------------
        dwg.note(
            (0.5 * d.stem_thickness, swl - 0.35 * d.water_depth),
            f"Goda p1 = {d.pressures['p1']:.0f} kPa\n"
            f"F = {d.wave_force:.0f} kN/m at {d.wave_arm:.2f} m",
            offset=(-70, 26), ha="right",
        )
        dwg.note(
            (d.base_width, found),
            f"Uplift pu = {d.pressures['pu']:.0f} kPa\nU = {d.uplift:.0f} kN/m",
            offset=(46, -26),
        )

    depth_below = min(found - 2.5, bed - d.scour_depth - 1.5)
    return (x0, x1), (depth_below, d.crest_level + 4.0)


def seawall_notes(design) -> list[str]:
    """Specification notes generated from a seawall design.

    The numbers come from the calculation; the material clauses are the
    generic ones a coastal designer would expect to see and still has to
    confirm for the project. Nothing here is a substitute for a
    specification.
    """
    d = design
    notes = [
        f"Design condition: Hm0 = {d.conditions.Hm0:.2f} m and "
        f"Tm-1,0 = {d.conditions.Tm10:.2f} s at the toe, still water level "
        f"{d.still_water_level:+.2f} m CD. Return period to be confirmed by "
        "the extreme value analysis.",
        f"Crest level {d.crest_level:+.2f} m CD, set for a mean overtopping "
        f"discharge of {d.q_upper:.3g} l/s/m at the upper bound of the "
        "EurOtop (2018) scatter band.",
        "Concrete to be specified for exposure class XS3, marine tidal and "
        "splash zone, with cover to reinforcement confirmed by the "
        "structural designer.",
        f"Toe rock: Dn50 = {d.toe_Dn50:.2f} m, M50 = {d.toe_M50 / 1000:.2f} t, "
        f"berm {d.toe_berm_width:.1f} m wide and "
        f"{d.toe_berm_thickness:.2f} m thick, two layers.",
        "Geotextile filter between rock and in-situ material, lapped 0.5 m "
        "minimum at all joints.",
        f"Founding level {d.founding_level:+.2f} m CD allows "
        f"{d.embedment:.2f} m of embedment against a predicted equilibrium "
        f"scour of {d.scour_depth:.2f} m. Confirm against a scour survey.",
        f"Stability under the design wave: sliding {d.sliding_FoS:.2f}, "
        f"overturning {d.overturning_FoS:.2f}, bearing "
        f"{d.bearing['p_max']:.0f} kPa peak. Bearing capacity to be confirmed "
        "by the geotechnical designer.",
        "Levels in metres to chart datum. Dimensions in metres unless noted.",
    ]
    notes += [f"WARNING: {w}" for w in d.warnings]
    return notes


def seawall_section(
    design,
    title: str = "Vertical seawall, typical cross-section",
    sea_extent: float = 22.0,
    land_extent: float = 8.0,
    figsize: tuple[float, float] = (14.5, 8.5),
    show_scour: bool = True,
    ax=None,
) -> Section:
    """A standalone figure of a designed seawall, with plot axes.

    Returns the :class:`~pyCoastal.drafting.Section` still open, so you can
    add project notes before saving.
    """
    d = design
    dwg = Section(
        title,
        subtitle=(
            f"Designed for Hm0 = {d.conditions.Hm0:.2f} m, "
            f"Tm-1,0 = {d.conditions.Tm10:.2f} s, "
            f"SWL {d.still_water_level:+.2f} m CD. "
            "Levels in metres to chart datum. Dimensions in metres."
        ),
        figsize=figsize,
        ax=ax,
    )
    xlim, zlim = draw_seawall(dwg, d, sea_extent, land_extent, show_scour)
    dwg.key(loc="upper left")
    q = d.quantities()
    dwg.table(
        [
            ("Hm0 at toe", f"{d.conditions.Hm0:.2f} m"),
            ("Tm-1,0", f"{d.conditions.Tm10:.2f} s"),
            ("Still water level", f"{d.still_water_level:+.2f} m CD"),
            ("Depth at wall", f"{d.water_depth:.2f} m"),
            ("", ""),
            ("Overtopping q", f"{d.q_mean:.3g} l/s/m (mean)"),
            ("  upper bound", f"{d.q_upper:.3g} l/s/m"),
            ("  limit", d.governing_limit.replace("_", " ")),
            ("Sliding FoS", f"{d.sliding_FoS:.2f}"),
            ("Overturning FoS", f"{d.overturning_FoS:.2f}"),
            ("Bearing p_max", f"{d.bearing['p_max']:.0f} kPa"),
            ("Resultant e", f"{d.bearing['e']:+.2f} m"
             + ("" if d.bearing["middle_third"] else "  OUT")),
            ("", ""),
            ("Concrete", f"{q['concrete_total_m3_per_m']:.1f} m3/m"),
            ("Toe rock", f"{q['toe_rock_t_per_m']:.1f} t/m"),
            ("Excavation", f"{q['excavation_m3_per_m']:.1f} m3/m"),
        ],
        title="Design basis and checks",
    )
    dwg.finish(xlim=xlim, zlim=zlim)
    return dwg


def seawall_sheet(
    design,
    project: str = "Coastal protection works",
    title: str = "Seawall typical cross-section",
    size: str = "A3",
    sea_extent: float = 22.0,
    land_extent: float = 8.0,
    file: str = "seawall_sheet.py",
    **titleblock,
) -> Sheet:
    """A full drawing sheet of a designed seawall, at a true stated scale.

    The view is fitted to a standard scale, the title block records that
    scale, and the specification notes are generated from the design. Extra
    keyword arguments go to the :class:`~pyCoastal.drafting.TitleBlock`.
    """
    d = design
    sheet = Sheet(
        _sheet_for(title, project, file, **titleblock), size=size,
    )

    # View A: the typical section, showing where everything is.
    view = sheet.viewport(rect=(0.0, 0.34, 0.72, 0.66))
    xlim, zlim = draw_seawall(view, d, sea_extent, land_extent)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", "Typical cross-section", view.scale_text,
                       loc=(0.02, 0.05))
    view.scale_bar(10.0, loc=(0.62, 0.05))
    view.key(loc="upper left")

    # View B: the toe, enlarged, showing what it is made of.
    toe = sheet.viewport(rect=(0.0, 0.0, 0.72, 0.33))
    txlim, tzlim = draw_seawall_toe_detail(toe, d)
    toe.fit_scale(txlim, tzlim, paper=size)
    toe.detail_bubble("B", "Toe detail", toe.scale_text, loc=(0.02, 0.06))
    toe.key(loc="upper right", ncol=2)

    notes = sheet.viewport(rect=(0.72, 0.0, 0.28, 1.0), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    notes.notes_block(seawall_notes(d), title="NOTES", width=40,
                      loc=(0.0, 1.0), fontsize=6.4)
    q = d.quantities()
    notes.table(
        [
            ("CONCRETE", f"{q['concrete_total_m3_per_m']:.1f} m3/m"),
            ("BACKFILL", f"{q['backfill_m3_per_m']:.1f} m3/m"),
            ("TOE ROCK", f"{q['toe_rock_t_per_m']:.1f} t/m"),
            ("EXCAVATION", f"{q['excavation_m3_per_m']:.1f} m3/m"),
        ],
        title="QUANTITIES PER METRE RUN", loc=(0.0, 0.0), align="left",
        fontsize=6.8,
    )
    sheet.set_scale_from(view)
    return sheet


# ---------------------------------------------------------------------------
# Rubble mound
# ---------------------------------------------------------------------------


def _mound_geometry(design, still_water_level, seabed_level, cot_land,
                    crest_width):
    """Layer profiles and derived sizes for a rubble-mound section."""
    d = design
    crest = still_water_level + d.crest_freeboard
    if crest <= seabed_level:
        raise ValueError("Crest level is below the seabed")

    cot_sea = d.cot_alpha
    cot_land = max(cot_sea - 0.5, 1.5) if cot_land is None else cot_land
    t_armour = d.layer["thickness"]
    Dn_under = d.Dn50 / 10.0 ** (1.0 / 3.0)
    t_under = 2.0 * Dn_under
    crest_width = max(3.0 * d.Dn50, 4.0) if crest_width is None else crest_width

    outer = MoundProfile(
        x_sea=-0.5 * crest_width, x_land=0.5 * crest_width, crest=crest,
        cot_sea=cot_sea, cot_land=cot_land,
    )
    under = outer.offset(t_armour)
    core = under.offset(t_under)
    return outer, under, core, crest, cot_land, Dn_under, crest_width


def draw_rubble_mound(dwg: Section, design, still_water_level: float,
                      seabed_level: float, cot_land: float | None = None,
                      crest_width: float | None = None, margin: float = 12.0,
                      annotate: bool = True) -> tuple[tuple, tuple]:
    """Put a designed rubble mound into an open :class:`Section`."""
    d = design
    bed, swl = seabed_level, still_water_level
    outer, under, core, crest, cot_land, Dn_under, crest_width = _mound_geometry(
        d, swl, bed, cot_land, crest_width
    )

    toe_x = outer.points(bed)[0, 0]
    x0 = toe_x - margin
    x1 = outer.points(bed)[-1, 0] + margin

    dwg.material([[x0, bed - 10.0], [x1, bed - 10.0], [x1, bed], [x0, bed]],
                 "subgrade", zorder=1.5)
    dwg.water(x0, x1, swl, bed=bed, zorder=1.8)

    dwg.material(core.points(bed), "core",
                 label="Quarry run core, 1 to 500 kg", zorder=2.2)
    dwg.material(under.band(core, bed), "underlayer",
                 label=f"Underlayer, Dn50 = {Dn_under:.2f} m "
                       f"({2650 * Dn_under ** 3 / 1000:.1f} t)", zorder=2.4)
    dwg.material(outer.band(under, bed), "armour",
                 label=f"Primary armour, Dn50 = {d.Dn50:.2f} m "
                       f"({d.M50 / 1000:.1f} t), "
                       f"{d.layer['thickness']:.2f} m thick", zorder=2.6)

    toe_w = max(3.0 * d.Dn50, 3.0)
    toe_t = 2.0 * d.Dn50
    dwg.material(
        [[toe_x - toe_w - 1.5 * toe_t, bed], [toe_x - toe_w, bed + toe_t],
         [toe_x + 0.5, bed + toe_t], [toe_x + 0.5, bed]],
        "toe", label="Toe berm", zorder=2.8,
    )

    if annotate:
        dwg.level(x0 + 1.0, swl, f"SWL {swl:+.2f} m CD", side="right",
                  symbol="water")
        dwg.level(0.0, crest, f"Crest {crest:+.2f} m CD", side="left")
        dwg.level(x1 - 1.0, bed, f"Seabed {bed:+.2f} m CD", side="left")

        dwg.dim_h(outer.x_sea, outer.x_land, crest + 1.8, f"{crest_width:.1f}",
                  extend_from=(crest, crest))
        dwg.dim_v(swl, crest, x1 - margin * 0.35,
                  f"Rc = {d.crest_freeboard:.2f}",
                  extend_from=(outer.x_land, x1))

        mid = 0.5 * (swl + crest)
        dwg.slope((outer.x_sea - cot_land * 0 - d.cot_alpha * (crest - mid), mid),
                  d.cot_alpha, rise=0.22 * (crest - bed), direction="left")
        dwg.slope((outer.x_land + cot_land * (crest - mid), mid), cot_land,
                  rise=0.22 * (crest - bed), direction="right")

        dwg.note(
            (outer.x_sea - d.cot_alpha * (crest - swl) * 0.5, 0.5 * (swl + crest)),
            f"Van der Meer, {d.regime}\n"
            f"S = 2, N = {d.conditions.wave_count:.0f} waves",
            offset=(-62, 30), ha="right",
        )
        dwg.note((0.0, crest),
                 f"q = {d.q_mean:.2g} l/s/m mean\n"
                 f"{d.q_upper:.2g} l/s/m upper bound", offset=(58, 34))

    return (x0, x1), (bed - 4.0, crest + 5.0)


def rubble_mound_notes(design, still_water_level, seabed_level,
                       cot_land=None, crest_width=None) -> list[str]:
    """Specification notes generated from a rubble-mound design."""
    d = design
    outer, under, core, crest, cot_land, Dn_under, crest_width = _mound_geometry(
        d, still_water_level, seabed_level, cot_land, crest_width
    )
    areas = mound_layer_volumes([outer, under, core], seabed_level)
    return [
        f"Design condition: Hm0 = {d.conditions.Hm0:.2f} m and "
        f"Tm-1,0 = {d.conditions.Tm10:.2f} s at the toe, "
        f"{d.conditions.wave_count:.0f} waves in the design storm.",
        f"Primary armour: Dn50 = {d.Dn50:.2f} m, M50 = {d.M50 / 1000:.1f} t, "
        f"two layers {d.layer['thickness']:.2f} m thick, "
        f"{d.layer['stones_per_m2']:.2f} stones per m2. Sized by Van der Meer "
        f"(1988), {d.regime} regime, damage level S = 2.",
        f"Underlayer: Dn50 = {Dn_under:.2f} m, nominally a tenth of the armour "
        "mass, two layers. Filter compatibility with the core to be checked "
        "against the actual gradings.",
        "Core: quarry run, 1 to 500 kg, placed in layers and compacted by the "
        "placing plant only.",
        f"Crest at {crest:+.2f} m CD, {crest_width:.1f} m wide, giving a mean "
        f"overtopping discharge of {d.q_mean:.2g} l/s/m and "
        f"{d.q_upper:.2g} l/s/m at the upper bound (EurOtop 2018).",
        f"Slopes 1:{d.cot_alpha:g} seaward and 1:{cot_land:g} landward.",
        f"Indicative quantities: armour {areas[0]:.0f} m3/m, underlayer "
        f"{areas[1]:.0f} m3/m, core {areas[2]:.0f} m3/m.",
        "Rock quality, grading and placement tolerances to the Rock Manual "
        "(CIRIA/CUR/CETMEF 2007).",
        "Levels in metres to chart datum. Dimensions in metres unless noted.",
    ]


def rubble_mound_section(
    design,
    still_water_level: float,
    seabed_level: float,
    cot_land: float | None = None,
    crest_width: float | None = None,
    title: str = "Rubble-mound breakwater, typical cross-section",
    figsize: tuple[float, float] = (14.5, 8.0),
    margin: float = 12.0,
    ax=None,
) -> Section:
    """A standalone figure of a designed rubble mound, with plot axes.

    Notes
    -----
    The underlayer follows the Rock Manual rule of a tenth of the armour
    mass, so Dn50 falls by 10^(1/3), about 2.15. The layers drawn are the
    ones the stability calculation assumes are there; a filter check against
    the core grading is a separate exercise.
    """
    d = design
    dwg = Section(
        title,
        subtitle=(
            f"Designed for Hm0 = {d.conditions.Hm0:.2f} m, "
            f"Tm-1,0 = {d.conditions.Tm10:.2f} s, "
            f"SWL {still_water_level:+.2f} m CD. "
            "Levels in metres to chart datum. Dimensions in metres."
        ),
        figsize=figsize,
        ax=ax,
    )
    xlim, zlim = draw_rubble_mound(dwg, d, still_water_level, seabed_level,
                                  cot_land, crest_width, margin)
    outer, under, core, crest, cot_land_used, Dn_under, crest_width_used = (
        _mound_geometry(d, still_water_level, seabed_level, cot_land, crest_width)
    )
    areas = mound_layer_volumes([outer, under, core], seabed_level)
    dwg.key(loc="upper left")
    dwg.table(
        [
            ("Hm0 at toe", f"{d.conditions.Hm0:.2f} m"),
            ("Tm-1,0", f"{d.conditions.Tm10:.2f} s"),
            ("Still water level", f"{still_water_level:+.2f} m CD"),
            ("Seaward slope", f"1 : {d.cot_alpha:g}"),
            ("Landward slope", f"1 : {cot_land_used:g}"),
            ("", ""),
            ("Armour Dn50", f"{d.Dn50:.2f} m"),
            ("Armour M50", f"{d.M50 / 1000:.1f} t"),
            ("Breaking regime", d.regime),
            ("Crest freeboard", f"{d.crest_freeboard:.2f} m"),
            ("", ""),
            ("Armour", f"{areas[0]:.0f} m3/m"),
            ("Underlayer", f"{areas[1]:.0f} m3/m"),
            ("Core", f"{areas[2]:.0f} m3/m"),
        ],
        title="Design basis and quantities",
    )
    dwg.finish(xlim=xlim, zlim=zlim)
    return dwg


def rubble_mound_sheet(
    design,
    still_water_level: float,
    seabed_level: float,
    cot_land: float | None = None,
    crest_width: float | None = None,
    project: str = "Harbour protection works",
    title: str = "Breakwater typical cross-section",
    size: str = "A3",
    margin: float = 12.0,
    file: str = "breakwater_sheet.py",
    **titleblock,
) -> Sheet:
    """A full drawing sheet of a designed rubble mound, at a true scale."""
    d = design
    sheet = Sheet(_sheet_for(title, project, file, **titleblock), size=size)
    view = sheet.viewport(rect=(0.0, 0.05, 0.72, 0.95))
    xlim, zlim = draw_rubble_mound(view, d, still_water_level, seabed_level,
                                   cot_land, crest_width, margin)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", title, view.scale_text, loc=(0.02, 0.04))
    view.scale_bar(20.0, loc=(0.62, 0.04))
    view.key(loc="upper left")

    outer, under, core, crest, _, _, _ = _mound_geometry(
        d, still_water_level, seabed_level, cot_land, crest_width
    )
    areas = mound_layer_volumes([outer, under, core], seabed_level)

    notes = sheet.viewport(rect=(0.72, 0.05, 0.28, 0.95), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    notes.notes_block(
        rubble_mound_notes(d, still_water_level, seabed_level, cot_land,
                           crest_width),
        title="NOTES", width=40, loc=(0.0, 1.0), fontsize=6.4,
    )
    notes.table(
        [
            ("ARMOUR", f"{areas[0]:.0f} m3/m"),
            ("UNDERLAYER", f"{areas[1]:.0f} m3/m"),
            ("CORE", f"{areas[2]:.0f} m3/m"),
        ],
        title="QUANTITIES PER METRE RUN", loc=(0.0, 0.0), align="left",
        fontsize=6.8,
    )
    sheet.set_scale_from(view)
    return sheet


# ---------------------------------------------------------------------------
# Navigation channel
# ---------------------------------------------------------------------------


def vessel_outline(beam: float, draught: float, freeboard: float,
                   bilge: float = 0.18, centre: float = 0.0) -> np.ndarray:
    """Midship section of a hull, as a closed polygon.

    A box with chamfered bilges and a little flare. Enough to read as a ship
    at the scale a channel section is drawn at, and deliberately not more:
    the hull form is not what the drawing is about.
    """
    if beam <= 0 or draught <= 0:
        raise ValueError("Beam and draught must be positive")
    r = bilge * beam
    half = 0.5 * beam
    return np.array([
        [centre - half - 0.03 * beam, freeboard],
        [centre - half, 0.0],
        [centre - half, -draught + r],
        [centre - half + r, -draught],
        [centre + half - r, -draught],
        [centre + half, -draught + r],
        [centre + half, 0.0],
        [centre + half + 0.03 * beam, freeboard],
    ])


def draw_channel(dwg: Section, design, margin: float = 60.0,
                 show_vessel: bool = True, annotate: bool = True,
                 show_depth_chain: bool = True,
                 seabed_extent: float | None = None) -> tuple[tuple, tuple]:
    """Put a designed navigation channel into an open :class:`Section`.

    Draws the dredged prism, the existing bed, the design vessel at her
    static draught, and the underkeel clearance stack as a dimension chain,
    so every allowance can be read off the paper.
    """
    d = design
    wl = d.design_water_level
    bed = d.existing_bed if d.existing_bed is not None else d.dredge_level + 2.0
    half = 0.5 * d.width
    rise = max(bed - d.dredge_level, 0.0)
    toe = half + d.side_slope * rise
    extent = seabed_extent if seabed_extent is not None else toe + margin

    # Ground, with the dredged prism cut out of it.
    dwg.material(
        [[-extent, bed - 30.0], [extent, bed - 30.0], [extent, bed],
         [toe, bed], [half, d.dredge_level], [-half, d.dredge_level],
         [-toe, bed], [-extent, bed]],
        "subgrade", label="In-situ material", zorder=1.5,
    )
    dwg.water(-extent, extent, wl,
              bed=[[-extent, bed], [-toe, bed], [-half, d.dredge_level],
                   [half, d.dredge_level], [toe, bed], [extent, bed]],
              zorder=1.2)

    # The design dredge level, drawn heavy: it is the line the contract is
    # let on and the line the survey is checked against.
    dwg.line([[-toe, bed], [-half, d.dredge_level], [half, d.dredge_level],
              [toe, bed]], weight="heavy", zorder=4.0)

    if show_vessel:
        lanes = d.width_result["lanes"]
        beam = d.vessel.beam
        offsets = (0.0,) if lanes == 1 else (-0.25 * d.width, 0.25 * d.width)
        for i, centre in enumerate(offsets):
            hull = vessel_outline(beam, d.vessel.draught, 0.18 * beam,
                                  centre=centre)
            hull[:, 1] += wl
            dwg.material(
                hull, "pavement",
                label=f"Design vessel, {d.vessel.name}" if i == 0 else None,
                zorder=5.0,
            )

    if not annotate:
        return ((-extent, extent),
                (d.dredge_level - 6.0, wl + 0.35 * d.vessel.beam))

    # -- the depth chain ---------------------------------------------------
    # Each allowance gets its own dimension, stacked down from the keel, so
    # the dredge level is visibly the sum of its parts rather than a round
    # number someone chose.
    span = extent - half
    ladder_x = half + 0.26 * span
    level = wl - d.vessel.draught
    if show_depth_chain:
        dwg.dim_v(wl, level, half + 0.07 * span,
                  f"draught {d.vessel.draught:.2f}",
                  extend_from=(0.0, 0.0), side="left")

    # Two staggered columns: the allowances are thin bands, and stacking
    # their labels in one column would overlap them into mush.
    live = ([(n, v) for n, v in d.clearance["components"].items() if v > 0]
            if show_depth_chain else [])
    for i, (name, value) in enumerate(live):
        column = ladder_x + (i % 2) * 0.22 * span
        dwg.line([[-half, level], [column, level]], weight="thin",
                 style=(0, (5, 4)), zorder=3.5)
        dwg.dim_v(level, level - value, column, f"{name} {value:.2f}")
        level -= value

    dwg.level(-0.96 * extent, wl, f"Design water level {wl:+.2f} m CD",
              side="right", symbol="water")
    dwg.level(0.0, d.dredge_level, f"Dredge level {d.dredge_level:+.2f} m CD",
              side="left", run=-0.35 * half)
    if d.existing_bed is not None:
        dwg.level(-0.82 * extent, bed, f"Existing bed {bed:+.2f} m CD",
                  side="right")

    # -- widths ------------------------------------------------------------
    dwg.dim_h(-half, half, d.dredge_level - 2.2, f"bed width {d.width:.0f}",
              extend_from=(d.dredge_level, d.dredge_level))
    if rise > 0:
        dwg.dim_h(-toe, toe, bed + 0.30 * d.vessel.beam,
                  f"top width {d.top_width:.0f}", extend_from=(bed, bed))
        dwg.slope((toe, bed), d.side_slope, rise=0.8 * rise, direction="left",
                  label=f"1 : {d.side_slope:g}")

    dwg.note((0.0, wl - d.vessel.draught - d.squat["squat"]),
             f"Squat {d.squat['squat']:.2f} m at {d.speed:.0f} kn\n"
             f"(ICORELS, Fnh = {d.squat['froude']:.2f})",
             offset=(0, -50), ha="center")

    return (-extent, extent), (level - 3.0, wl + 0.45 * d.vessel.beam)


def channel_notes(design) -> list[str]:
    """Specification notes generated from a channel design."""
    d = design
    v = d.vessel
    notes = [
        f"Design vessel: {v.name}, {v.length:.0f} m x {v.beam:.1f} m x "
        f"{v.draught:.1f} m draught, Cb = {v.block_coefficient:.2f}, "
        f"{v.displacement:,.0f} t displacement.",
        f"Design speed {d.speed:.1f} knots through the water, giving "
        f"{d.squat['squat']:.2f} m of bow squat by ICORELS at a depth Froude "
        f"number of {d.squat['froude']:.2f}.",
        f"Wave response allowance {d.waves['allowance']:.2f} m, taken as "
        f"{d.waves['factor']:.2f} of the significant wave height in the "
        "channel. Confirm by a motion study before construction.",
        f"Dredge level {d.dredge_level:+.2f} m CD, being the design water "
        f"level {d.design_water_level:+.2f} m CD less the "
        f"{d.required_depth:.2f} m depth chain shown.",
        f"Channel width {d.width:.0f} m at the bed, "
        f"{d.width_result['lanes']}-way, built up by the PIANC concept design "
        "method. Confirm by manoeuvring simulation.",
        f"Side slopes 1:{d.side_slope:g}, to be confirmed against the "
        "geotechnical investigation and the dredging method.",
        "Dredging and survey tolerances are included in the depth chain and "
        "are not to be taken again by the contractor.",
        "Levels in metres to chart datum. Dimensions in metres.",
    ]
    if d.width_result["assumed"]:
        notes.append(
            "Width components not specified were taken at their most benign "
            "class: " + "; ".join(d.width_result["assumed"]) + "."
        )
    notes += [f"WARNING: {w}" for w in d.warnings]
    return notes


def channel_section(
    design,
    title: str = "Navigation channel, typical cross-section",
    figsize: tuple[float, float] = (14.5, 8.0),
    margin: float = 60.0,
    exaggeration: float = 8.0,
    ax=None,
) -> Section:
    """A standalone figure of a designed navigation channel.

    Drawn with vertical exaggeration by default. A channel several hundred
    metres wide and twenty deep is unreadable at a true scale, which is why
    dredging drawings have always been exaggerated; the factor is stated on
    the drawing rather than left for the reader to infer.
    """
    d = design
    exaggerated = abs(exaggeration - 1.0) > 1e-9
    dwg = Section(
        title,
        subtitle=(
            f"{d.vessel.name} at {d.speed:.0f} knots, design water level "
            f"{d.design_water_level:+.2f} m CD. "
            "Levels in metres to chart datum. Dimensions in metres."
            + (f"  VERTICAL EXAGGERATION {exaggeration:g}:1" if exaggerated else "")
        ),
        figsize=figsize,
        exaggeration=exaggeration,
        ax=ax,
    )
    xlim, zlim = draw_channel(dwg, d, margin=margin)
    dwg.key(loc="upper left")
    rows = [
        ("Vessel", f"{d.vessel.length:.0f} x {d.vessel.beam:.1f} m"),
        ("Draught", f"{d.vessel.draught:.2f} m"),
        ("Speed", f"{d.speed:.1f} kn"),
        ("Squat", f"{d.squat['squat']:.2f} m"),
        ("Wave response", f"{d.waves['allowance']:.2f} m"),
        ("", ""),
        ("Required depth", f"{d.required_depth:.2f} m"),
        ("Dredge level", f"{d.dredge_level:+.2f} m CD"),
        ("Bed width", f"{d.width:.0f} m"),
    ]
    if d.existing_bed is not None:
        rows += [
            ("", ""),
            ("Dredge depth", f"{d.existing_bed - d.dredge_level:.2f} m"),
            ("Volume", f"{d.dredge_volume(1000.0) / 1e3:,.0f} k m3/km"),
        ]
    dwg.table(rows, title="Design basis")
    dwg.finish(xlim=xlim, zlim=zlim)
    return dwg


def channel_sheet(
    design,
    project: str = "Port approach works",
    title: str = "Navigation channel typical section",
    size: str = "A3",
    margin: float = 60.0,
    exaggeration: float = 8.0,
    file: str = "channel_sheet.py",
    **titleblock,
) -> Sheet:
    """A full drawing sheet of a designed navigation channel.

    Vertically exaggerated by default, with the factor stated beside the
    detail title and in the notes.
    """
    d = design
    sheet = Sheet(_sheet_for(title, project, file, **titleblock), size=size)

    # View A: the whole channel, exaggerated so it is readable at all.
    view = sheet.viewport(rect=(0.0, 0.46, 0.70, 0.54),
                          exaggeration=exaggeration)
    xlim, zlim = draw_channel(view, d, margin=margin, show_depth_chain=False)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", "Channel cross-section", view.scale_text,
                       loc=(0.02, 0.06))
    view.scale_bar(100.0, loc=(0.60, 0.06))
    view.key(loc="upper left")

    # View B: the keel and the allowances, at a true scale, where the
    # underkeel clearance can be read as a real thickness.
    detail = sheet.viewport(rect=(0.0, 0.0, 0.70, 0.44))
    dxlim, dzlim = draw_channel_detail(detail, d)
    detail.fit_scale(dxlim, dzlim, paper=size)
    detail.detail_bubble("B", "Underkeel clearance detail",
                         detail.scale_text, loc=(0.02, 0.06))
    detail.key(loc="upper right", ncol=2)

    notes = sheet.viewport(rect=(0.70, 0.0, 0.30, 1.0), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    extra = channel_notes(d)
    if view.exaggeration_note:
        extra = [view.exaggeration_note.capitalize()
                 + ". Slopes are not true angles on this drawing."] + extra
    notes.notes_block(extra, title="NOTES", width=40, loc=(0.0, 1.0),
                      fontsize=6.2)
    rows = [(name.upper(), f"{value:.2f} m")
            for name, value in d.clearance["components"].items() if value > 0]
    notes.table(
        [("STATIC DRAUGHT", f"{d.vessel.draught:.2f} m")] + rows
        + [("REQUIRED DEPTH", f"{d.required_depth:.2f} m")],
        title="DEPTH CHAIN", loc=(0.0, 0.0), align="left", fontsize=6.4,
    )
    sheet.set_scale_from(view)
    return sheet


def draw_channel_detail(dwg: Section, design, width_in_beams: float = 0.35,
                        hull_shown: float = 1.3,
                        annotate: bool = True) -> tuple[tuple, tuple]:
    """True-scale detail of the keel, the allowances and the dredge level.

    The overall channel section has to be exaggerated to be readable, which
    stretches the vessel into a tower and makes every slope a lie. This is
    the companion view a drawing set always carries: the part that matters,
    at a true scale, cropped to the keel, where the underkeel clearance can
    be read as a real thickness rather than as a band on a distorted
    picture.
    """
    d = design
    wl = d.design_water_level
    beam = d.vessel.beam
    half = 0.5 * width_in_beams * beam
    keel = wl - d.vessel.draught
    # Only a slice of the hull: the bands are the subject, and a full
    # draught of steel above them would swamp the view.
    hull_top = keel + hull_shown

    dwg.water(-half, half, hull_top, bed=d.dredge_level - 2.0, zorder=1.0)

    # Only the flat of bottom: this is a detail, and the rest of the hull is
    # on view A.
    dwg.material(
        [[-half * 0.92, keel], [half * 0.92, keel],
         [half * 0.92, hull_top], [-half * 0.92, hull_top]],
        "pavement", label="Design vessel, flat of bottom", zorder=5.0,
    )

    # Each allowance as a band, so the stack is a picture and not only a
    # column of numbers. The key names them; leaders would cross.
    # Hatched materials only. A band of drawn stones would read as rock
    # placed on the bed, and these are allowances, not materials.
    shades = ("core", "granular", "sand", "blinding", "rock_fill",
              "concrete", "reinforced", "subgrade")
    level = keel
    for i, (name, value) in enumerate(d.clearance["components"].items()):
        if value <= 0:
            continue
        dwg.material(
            [[-half, level - value], [half, level - value],
             [half, level], [-half, level]],
            shades[i % len(shades)],
            label=f"{name} {value:.2f} m", zorder=2.0,
        )
        if annotate:
            # Alternate the column so consecutive thin bands do not stack
            # their labels on top of each other.
            column = half * (0.55 if i % 2 else 0.82)
            dwg.dim_v(level, level - value, column, f"{value:.2f}")
        level -= value

    dwg.material(
        [[-half, level - 2.0], [half, level - 2.0], [half, level],
         [-half, level]],
        "subgrade", zorder=1.8,
    )
    dwg.line([[-half, level], [half, level]], weight="heavy", zorder=4.0)

    if annotate:
        dwg.level(-half * 0.80, keel, f"Keel {keel:+.2f} m CD", side="right")
        dwg.level(-half * 0.80, level, f"Dredge level {level:+.2f} m CD",
                  side="right")
        dwg.dim_v(keel, level, -half * 0.92,
                  f"gross UKC {d.clearance['gross']:.2f}", side="left")

    return (-half, half), (level - 1.2, hull_top + 0.2)


def draw_seawall_toe_detail(dwg: Section, design, annotate: bool = True
                            ) -> tuple[tuple, tuple]:
    """Enlarged detail of the toe, where the section is actually decided.

    The typical section shows where everything is. This shows what the toe
    is made of: the blinding under the heel, the founding level against the
    scour allowance, the rock berm and its geotextile, and the seabed the
    whole thing is sitting on. It is the part of a seawall that fails first
    and the part a typical section is always too small to explain.
    """
    d = design
    bed, found = d.seabed_level, d.founding_level
    berm_face = 1.5 * d.toe_berm_thickness
    blinding = 0.15

    x0 = -(d.toe_berm_width + berm_face + 2.6)
    x1 = 2.2 * d.stem_thickness + 1.0
    floor = found - 1.8

    dwg.material([[x0, floor], [x1, floor], [x1, bed], [x0, bed]],
                 "subgrade", label="In-situ seabed", zorder=1.5)
    dwg.water(x0, 0.0, d.still_water_level, bed=bed, zorder=1.2)

    # The excavation the wall sits in, backfilled around the base.
    dwg.material([[0.0, found - blinding], [x1, found - blinding],
                  [x1, bed], [0.0, bed]], "granular",
                 label="Granular surround", zorder=2.0)

    dwg.material(
        [[-d.toe_berm_width - berm_face, bed],
         [-d.toe_berm_width, bed + d.toe_berm_thickness],
         [0.0, bed + d.toe_berm_thickness], [0.0, bed]],
        "toe",
        label=f"Toe rock, Dn50 = {d.toe_Dn50:.2f} m ({d.toe_M50 / 1000:.2f} t)",
        zorder=2.6,
    )
    dwg.material([[0.0, found - blinding], [x1, found - blinding],
                  [x1, found], [0.0, found]], "blinding",
                 label=f"Blinding, {blinding * 1000:.0f} mm", zorder=2.8)
    dwg.material([[0.0, found], [x1, found],
                  [x1, found + d.base_thickness], [0.0, found + d.base_thickness]],
                 "reinforced", label="Reinforced concrete", zorder=3.0)

    # Geotextile under the rock, drawn as the line it is on a drawing.
    dwg.line([[-d.toe_berm_width - berm_face - 0.4, bed],
              [0.0, bed]], weight="medium", style=(0, (2, 2)),
             color="#8a2f24", zorder=3.4)

    if annotate:
        dwg.note((-0.5 * d.toe_berm_width, bed),
                 "Geotextile filter,\n0.5 m lap minimum", offset=(-18, -34),
                 ha="right")
        dwg.level(x1 * 0.55, bed, f"Seabed {bed:+.2f} m CD", side="left")
        dwg.level(x1 * 0.55, found, f"Founding {found:+.2f} m CD", side="left")
        dwg.dim_v(found, bed, x0 + 0.35, f"embedment {d.embedment:.2f}",
                  side="right")
        dwg.dim_v(found - blinding, found, x1 - 0.25, f"{blinding:.2f}",
                  side="left")
        dwg.dim_h(-d.toe_berm_width, 0.0, bed + d.toe_berm_thickness + 0.55,
                  f"{d.toe_berm_width:.1f}",
                  extend_from=(bed + d.toe_berm_thickness,
                               bed + d.toe_berm_thickness))
        # Kept a clear metre from the embedment dimension: two rotated
        # labels on top of each other is the usual way a detail becomes
        # unreadable.
        dwg.dim_v(bed, bed + d.toe_berm_thickness, x0 + 1.5,
                  f"{d.toe_berm_thickness:.2f}", side="right")
        dwg.slope((-d.toe_berm_width, bed + d.toe_berm_thickness), 1.5,
                  rise=d.toe_berm_thickness, direction="left", label="1 : 1.5")

    return (x0, x1), (floor, bed + d.toe_berm_thickness + 2.2)
