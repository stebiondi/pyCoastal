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
    "draw_nourishment",
    "nourishment_notes",
    "nourishment_section",
    "nourishment_sheet",
    "draw_nourishment_plan",
    "nourishment_plan_section",
    "spreading_half_life",
    "plan_margin",
    "REPOSE_ANGLE",
    "scour_hole_profile",
    "draw_pier_scour",
    "pier_scour_notes",
    "pier_scour_section",
    "pier_scour_sheet",
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
                      annotate: bool = True, foundation: dict | None = None,
                      crown: dict | None = None, bed="medium_sand",
                      show_foundation: bool = True) -> tuple[tuple, tuple]:
    """Put a designed rubble mound into an open :class:`Section`.

    Draws the section the way a drawing office draws it: the mound on a
    levelling blanket on a geotextile, a toe berm of filter stone at each
    foot, and a stepped concrete crown block with its sand and gravel
    infill. The blanket runs past both toes far enough that the scour hole
    forms in the apron rather than under the structure.

    Parameters
    ----------
    foundation : dict, optional
        Output of :func:`~pyCoastal.applications.structures.mound_foundation`.
        Computed from ``bed`` when not given.
    crown : dict, optional
        Output of :func:`~pyCoastal.applications.structures.crown_wall`.
        Computed when not given. Pass ``False`` to leave it off.
    """
    from .structures import crown_wall, mound_foundation

    d = design
    swl = still_water_level
    depth = swl - seabed_level

    if show_foundation and foundation is None:
        foundation = mound_foundation(d, max(depth, 0.5), bed=bed)
    if crown is None and crown is not False:
        crown = crown_wall(d, swl)

    # The mound stands on the blanket, not on the seabed.
    blanket = foundation["bedding_thickness"] if foundation else 0.0
    base = seabed_level + blanket

    if crest_width is None:
        needed = crown["total_width"] + 1.0 if crown else 0.0
        crest_width = max(3.0 * d.Dn50, 4.0, needed)

    outer, under, core, crest, cot_land, Dn_under, crest_width = _mound_geometry(
        d, swl, base, cot_land, crest_width
    )

    sea_toe = outer.points(base)[0, 0]
    land_toe = outer.points(base)[-1, 0]
    extension = foundation["bedding_extension"] if foundation else 0.0
    x0 = sea_toe - extension - margin
    x1 = land_toe + extension + margin
    top = (crown["parapet_top"] if crown else crest) + 3.0
    z0 = seabed_level - 4.0

    dwg.material([[x0, z0 - 6.0], [x1, z0 - 6.0], [x1, seabed_level],
                  [x0, seabed_level]], "subgrade", zorder=1.5)
    dwg.water(x0, x1, swl, bed=seabed_level, zorder=1.8)

    # -- the blanket the whole thing stands on ----------------------------
    if foundation:
        blanket_x0 = sea_toe - extension
        blanket_x1 = land_toe + extension
        dwg.material(
            [[blanket_x0 - 1.5 * blanket, seabed_level],
             [blanket_x0, base], [blanket_x1, base],
             [blanket_x1 + 1.5 * blanket, seabed_level]],
            "sand",
            label=f"Bedding blanket, {foundation['bedding'].name.lower()}, "
                  f"{blanket:.2f} m",
            zorder=2.0,
        )
        # The geotextile is a line on a drawing, not a layer.
        dwg.line([[blanket_x0 - 1.5 * blanket, seabed_level],
                  [blanket_x1 + 1.5 * blanket, seabed_level]],
                 weight="heavy", style=(0, (7, 3)), color="#8a2f24", zorder=3.6)

    dwg.material(core.points(base), "core",
                 label="Quarry run core, 1 to 500 kg", zorder=2.2)
    dwg.material(under.band(core, base), "underlayer",
                 label=f"Filter layer, Dn50 = {Dn_under:.2f} m "
                       f"({2650 * Dn_under ** 3 / 1000:.1f} t)", zorder=2.4)
    dwg.material(outer.band(under, base), "armour",
                 label=f"Armour, Dn50 = {d.Dn50:.2f} m ({d.M50 / 1000:.1f} t), "
                       f"{d.layer['thickness']:.2f} m thick", zorder=2.6)

    # -- a toe berm at each foot, in filter stone -------------------------
    if foundation:
        tw = foundation["toe_width"]
        tt = foundation["toe_thickness"]
        for sign, toe_x in ((-1.0, sea_toe), (1.0, land_toe)):
            dwg.material(
                [[toe_x + sign * (tw + 1.5 * tt), base],
                 [toe_x + sign * tw, base + tt],
                 [toe_x - sign * 0.5, base + tt],
                 [toe_x - sign * 0.5, base]],
                "toe",
                label=f"Toe berm, Dn50 = {foundation['toe_Dn50']:.2f} m "
                      f"({foundation['toe_M50'] / 1000:.1f} t), both toes",
                zorder=2.8,
            )

    # -- crown block and its infill ---------------------------------------
    if crown:
        px0 = outer.x_sea
        px1 = px0 + crown["parapet_width"]
        dx1 = px1 + crown["deck_width"]
        dwg.material(
            [[px0, crown["base_level"]], [dx1, crown["base_level"]],
             [dx1, crown["deck_level"]], [px1, crown["deck_level"]],
             [px1, crown["parapet_top"]], [px0, crown["parapet_top"]]],
            "concrete", label="Crown block, mass concrete", zorder=3.2,
        )
        if dx1 < outer.x_land:
            dwg.material(
                [[dx1, crown["base_level"]], [outer.x_land, crown["base_level"]],
                 [outer.x_land, crest], [dx1, crest]],
                "granular", label="Sand and gravel infill", zorder=3.0,
            )

    if not annotate:
        return (x0, x1), (z0, top)

    # -- levels ------------------------------------------------------------
    dwg.level(x0 + 2, swl, f"SWL {fmt(swl)} m CD", side="right", symbol="water")
    if crown:
        dwg.level(outer.x_sea, crown["parapet_top"],
                  f"Parapet {fmt(crown['parapet_top'])}", side="left")
        dwg.level(outer.x_sea + crown["total_width"], crown["deck_level"],
                  f"Deck {fmt(crown['deck_level'])}", side="right")
    else:
        dwg.level(0.0, crest, f"Crest {fmt(crest)} m CD", side="left")
    # The blanket top is already given by its thickness dimension and the
    # seabed level, so it does not get a third callout in the same corner.
    dwg.level(land_toe + extension + 0.4 * margin, seabed_level,
              f"Seabed {fmt(seabed_level)} m CD", side="left")

    # -- dimensions --------------------------------------------------------
    dwg.dim_h(outer.x_sea, outer.x_land, crest + 2.2, f"{crest_width:.1f}",
              extend_from=(crest, crest))
    dwg.dim_v(swl, crest, land_toe + 0.35 * extension,
              f"Rc = {d.crest_freeboard:.2f}",
              extend_from=(outer.x_land, land_toe + 0.35 * extension))

    if foundation:
        chain = seabed_level - 2.2
        dwg.dim_h(sea_toe - extension, sea_toe, chain, f"{extension:.1f}",
                  extend_from=(base, base))
        dwg.dim_h(sea_toe, land_toe, chain, f"{land_toe - sea_toe:.1f}",
                  extend_from=(base, base))
        dwg.dim_h(land_toe, land_toe + extension, chain, f"{extension:.1f}",
                  extend_from=(base, base))
        dwg.dim_v(seabed_level, base, sea_toe - extension - 1.5,
                  f"{blanket:.2f}", side="left")
        dwg.note((0.5 * (sea_toe + land_toe), seabed_level),
                 f"Geotextile, {(land_toe - sea_toe) + 2 * extension + 3 * blanket:.0f} m wide",
                 offset=(0, -34), ha="center")
        scour = foundation["scour"]
        dwg.note((sea_toe - 0.6 * extension, base),
                 f"Toe scour {scour['depth']:.2f} m predicted\n"
                 f"(Kr = {scour['reflection']:.2f}, {scour['mobility'].get('regime', '')})",
                 offset=(-20, 34), ha="right")

    mid = 0.5 * (swl + crest)
    dwg.slope((outer.x_sea - d.cot_alpha * (crest - mid), mid), d.cot_alpha,
              rise=0.22 * (crest - base), direction="left")
    dwg.slope((outer.x_land + cot_land * (crest - mid), mid), cot_land,
              rise=0.22 * (crest - base), direction="right")

    dwg.note((outer.x_sea - d.cot_alpha * (crest - swl) * 0.5, 0.5 * (swl + crest)),
             f"Van der Meer, {d.regime}\n"
             f"S = 2, N = {d.conditions.wave_count:.0f} waves",
             offset=(-62, 30), ha="right")

    return (x0, x1), (z0, top)


def fmt(value: float) -> str:
    """Signed level, the way a drawing writes one."""
    return f"{value:+.2f}"


def rubble_mound_notes(design, still_water_level, seabed_level,
                       cot_land=None, crest_width=None, foundation=None,
                       crown=None) -> list[str]:
    """Specification notes generated from a rubble-mound design."""
    d = design
    outer, under, core, crest, cot_land, Dn_under, crest_width = _mound_geometry(
        d, still_water_level, seabed_level, cot_land, crest_width
    )
    areas = mound_layer_volumes([outer, under, core], seabed_level)
    notes = [
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
    if foundation:
        notes[7:7] = [
            f"Bedding blanket: {foundation['bedding'].name.lower()}, "
            f"{foundation['bedding_thickness']:.2f} m thick, laid on a "
            "geotextile and carried "
            f"{foundation['bedding_extension']:.1f} m beyond each toe so the "
            "scour hole forms in the apron and not under the structure.",
            f"Toe berm at each foot: Dn50 = {foundation['toe_Dn50']:.2f} m, "
            f"M50 = {foundation['toe_M50'] / 1000:.1f} t, the same stone as "
            f"the filter layer, {foundation['toe_width']:.1f} m wide and "
            f"{foundation['toe_thickness']:.2f} m thick.",
            f"Predicted toe scour {foundation['scour']['depth']:.2f} m at a "
            f"reflection coefficient of {foundation['scour']['reflection']:.2f}. "
            "A screening estimate; confirm by a mobile bed model before "
            "fixing the apron.",
        ]
    if crown:
        notes[7:7] = [
            f"Crown block: parapet to {crown['parapet_top']:+.2f} m CD, deck "
            f"at {crown['deck_level']:+.2f} m CD, founded at "
            f"{crown['base_level']:+.2f} m CD, "
            f"{crown['concrete_m3_per_m']:.1f} m3/m. Proportioned only: "
            "sliding, overturning and uplift under wave impact are a separate "
            "calculation.",
        ]
    return notes


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
    title: str = "Breakwater typical sections",
    size: str = "A3",
    margin: float = 12.0,
    file: str = "breakwater_sheet.py",
    bed="medium_sand",
    show_head: bool = True,
    head_kd_ratio: float | None = None,
    **titleblock,
) -> Sheet:
    """A drawing sheet of a designed rubble mound, trunk and head.

    Two sections, as a real set carries them: the trunk, and the roundhead
    with the heavier armour its exposure needs. Set ``show_head`` False for
    a trunk-only sheet.
    """
    from .structures import crown_wall, mound_foundation, roundhead

    d = design
    depth = max(still_water_level - seabed_level, 0.5)
    sheet = Sheet(_sheet_for(title, project, file, **titleblock), size=size)

    head = roundhead(d, kd_ratio=head_kd_ratio) if show_head else None
    sections = [("A", "Trunk section", d)]
    if head is not None:
        sections.append(("B", "Head section", head))

    height = 1.0 / len(sections)
    views = []
    for index, (bubble, label, section) in enumerate(sections):
        bottom = 1.0 - (index + 1) * height
        view = sheet.viewport(rect=(0.0, bottom, 0.70, height))
        xlim, zlim = draw_rubble_mound(view, section, still_water_level,
                                       seabed_level, cot_land, crest_width,
                                       margin, bed=bed)
        view.fit_scale(xlim, zlim, paper=size)
        caption = f"{label}, armour {section.M50 / 1000:.1f} t"
        view.detail_bubble(bubble, caption, view.scale_text, loc=(0.02, 0.05))
        if index == 0:
            view.key(loc="upper left")
        views.append(view)

    foundation = mound_foundation(d, depth, bed=bed)
    crown = crown_wall(d, still_water_level)
    base = seabed_level + foundation["bedding_thickness"]
    outer, under, core, crest, _, _, _ = _mound_geometry(
        d, still_water_level, base, cot_land, crest_width
    )
    areas = mound_layer_volumes([outer, under, core], base)
    span = (outer.points(base)[-1, 0] - outer.points(base)[0, 0]
            + 2 * foundation["bedding_extension"])

    notes_text = rubble_mound_notes(d, still_water_level, base, cot_land,
                                    crest_width, foundation=foundation,
                                    crown=crown)
    if head is not None:
        notes_text.insert(2, (
            f"Head section: armour Dn50 = {head.Dn50:.2f} m, "
            f"M50 = {head.M50 / 1000:.1f} t, "
            f"{head.M50 / d.M50:.2f} times the trunk mass, from a stability "
            f"coefficient {head.kd_ratio:.2f} of the trunk value. A roundhead "
            "is attacked from more directions, its convex face gives each "
            "unit less support from its neighbours, and the run-down "
            "concentrates where the flow turns the corner."
        ))

    notes = sheet.viewport(rect=(0.70, 0.0, 0.30, 1.0), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    notes.notes_block(notes_text, title="NOTES", width=36, loc=(0.0, 1.0),
                      fontsize=5.6)
    rows = [
        ("ARMOUR, TRUNK", f"{areas[0]:.0f} m3/m"),
        ("FILTER", f"{areas[1]:.0f} m3/m"),
        ("CORE", f"{areas[2]:.0f} m3/m"),
        ("BEDDING", f"{foundation['bedding_thickness'] * span:.0f} m3/m"),
        ("TOE BERM",
         f"{2 * foundation['toe_width'] * foundation['toe_thickness']:.0f} m3/m"),
        ("CROWN CONCRETE", f"{crown['concrete_m3_per_m']:.1f} m3/m"),
    ]
    if head is not None:
        rows.insert(1, ("  HEAD M50", f"{head.M50 / 1000:.1f} t"))
    notes.table(rows, title="QUANTITIES PER METRE RUN", loc=(0.0, 0.0),
                align="left", fontsize=6.2)
    sheet.set_scale_from(views[0])
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


# ---------------------------------------------------------------------------
# Beach nourishment
# ---------------------------------------------------------------------------


def draw_nourishment(dwg: Section, result, native, borrow, berm_height: float,
                     closure_depth: float, water_level: float = 0.0,
                     annotate: bool = True,
                     landward: float = 40.0) -> tuple[tuple, tuple]:
    """Put a nourishment cross-section into an open :class:`Section`.

    The native profile, the design fill over it, and the closure contour
    that bounds the whole exercise. The fill wedge is drawn as the borrow
    material, so a section placed with coarse sand and one placed with fine
    sand do not look alike, which they should not.

    Parameters
    ----------
    result : dict
        Output of :func:`~pyCoastal.applications.nourishment.shoreline_advance`.
    native, borrow : Sediment or str
        The beach and the borrow source.
    """
    from .nourishment import dean_scale, equilibrium_profile, profile_width
    from .sediment import sediment as _lookup

    native = _lookup(native) if isinstance(native, str) else native
    borrow = _lookup(borrow) if isinstance(borrow, str) else borrow
    A_native = dean_scale(native)
    A_fill = dean_scale(borrow)
    advance = result["advance"]

    native_end = profile_width(A_native, closure_depth)
    fill_end = advance + profile_width(A_fill, closure_depth)
    offshore = max(native_end, fill_end) * 1.12
    x0, x1 = -landward, offshore
    z_bed = water_level - closure_depth
    z0 = z_bed - 3.0
    z1 = water_level + berm_height + 3.0

    y = np.linspace(0.0, offshore, 500)
    native_z = water_level - equilibrium_profile(A_native, y)

    # Ground below the native profile.
    dwg.material(
        np.vstack(([[x0, z0]], [[0.0, z0]],
                   np.column_stack((y, native_z)),
                   [[offshore, z0]])),
        "subgrade", label="Native beach and seabed", zorder=1.6,
    )
    # The dry native beach landward of the original waterline.
    dwg.material([[x0, z0], [0.0, z0], [0.0, water_level + berm_height],
                  [x0, water_level + berm_height]], "subgrade",
                 label="Native beach and seabed", zorder=1.6)

    dwg.water(x0, x1, water_level,
              bed=np.column_stack((np.concatenate(([x0], y)),
                                   np.concatenate(([water_level + berm_height],
                                                   native_z)))),
              zorder=1.2)

    # The fill: between the nourished profile and the native one.
    if advance > 0:
        yf = np.linspace(0.0, max(fill_end, advance + 1e-6), 500)
        fill_z = np.where(
            yf <= advance,
            water_level + berm_height,
            water_level - equilibrium_profile(A_fill, np.maximum(yf - advance, 0.0)),
        )
        native_on_yf = water_level - equilibrium_profile(A_native, yf)
        above = fill_z > native_on_yf + 1e-9
        if above.any():
            last = int(np.max(np.nonzero(above)))
            wedge = np.vstack((
                np.column_stack((yf[: last + 1], fill_z[: last + 1])),
                np.column_stack((yf[: last + 1][::-1],
                                 native_on_yf[: last + 1][::-1])),
            ))
            dwg.material(wedge, "sand",
                         label=f"Nourishment, {borrow.name.lower()} "
                               f"(d50 = {borrow.d50 * 1000:.2f} mm)",
                         zorder=2.4)

    # Profiles drawn over the fills, so both are readable.
    dwg.line(np.column_stack((y, native_z)), weight="medium",
             style=(0, (6, 3)), zorder=4.0)
    if advance > 0:
        drawn = yf <= (result["meeting"] if result.get("meeting") else yf[-1])
        dwg.line(np.column_stack((yf[drawn], fill_z[drawn])), weight="heavy",
                 zorder=4.2)

    # The closure contour bounds the whole problem.
    dwg.line([[x0, z_bed], [x1, z_bed]], weight="thin", style=(0, (2, 3)),
             color="#8a2f24", zorder=3.8)

    if not annotate:
        return (x0, x1), (z0, z1)

    dwg.level(x0 + 0.1 * landward, water_level,
              f"MSL {water_level:+.2f} m", side="right", symbol="water")
    dwg.level(x0 + 0.1 * landward, water_level + berm_height,
              f"Berm {water_level + berm_height:+.2f} m", side="right")
    dwg.level(offshore * 0.30, z_bed,
              f"Closure {z_bed:+.2f} m", side="right")

    if advance > 0:
        dwg.dim_h(0.0, advance, water_level + berm_height + 1.4,
                  f"dry beach gained {advance:.1f} m",
                  extend_from=(water_level + berm_height,
                               water_level + berm_height))
    if result.get("meeting"):
        dwg.note((result["meeting"], water_level - result["meeting_depth"]),
                 f"profiles meet, {result['meeting']:.0f} m out",
                 offset=(30, 26))
    else:
        dwg.note((0.75 * fill_end, water_level - 0.8 * closure_depth),
                 "fill runs to closure without meeting\nthe native profile",
                 offset=(0, -40), ha="center")

    dwg.note((0.35 * advance if advance > 2 else 6.0, water_level + berm_height),
             f"{result['volume']:.0f} m3 per metre of beach",
             offset=(-20, 34), ha="right")

    return (x0, x1), (z0, z1)


def nourishment_notes(result, native, borrow, berm_height: float,
                      closure_depth: float, design=None) -> list[str]:
    """Specification notes generated from a nourishment design."""
    from .nourishment import (dean_scale, grain_compatibility,
                              profile_overfill_factor)
    from .sediment import sediment as _lookup

    native = _lookup(native) if isinstance(native, str) else native
    borrow = _lookup(borrow) if isinstance(borrow, str) else borrow
    match = grain_compatibility(native, borrow)
    overfill = profile_overfill_factor(native, borrow, berm_height,
                                       closure_depth,
                                       advance=max(result["advance"], 1.0))

    notes = [
        f"Native beach: {native.name.lower()}, d50 = "
        f"{native.d50 * 1000:.2f} mm, phi = {match['phi_native']:.2f}, "
        f"sorting {native.phi_sorting:.2f}. Profile scale A = "
        f"{dean_scale(native):.3f} m^(1/3).",
        f"Borrow source: {borrow.name.lower()}, d50 = "
        f"{borrow.d50 * 1000:.2f} mm, phi = {match['phi_borrow']:.2f}, "
        f"sorting {borrow.phi_sorting:.2f}. Profile scale A = "
        f"{dean_scale(borrow):.3f} m^(1/3).",
        f"Compatibility: the borrow sits {abs(match['delta']):.2f} native "
        f"standard deviations "
        + ("coarser" if match["coarser"] else "finer")
        + f" than the beach it is going on. Verdict: {match['verdict']}.",
        f"Profile type: {result['kind']}. {result['note']}",
        f"Placed volume {result['volume']:.0f} m3 per metre of beach for "
        f"{result['advance']:.1f} m of dry beach, over an active profile "
        f"from the {berm_height:.1f} m berm to the {closure_depth:.1f} m "
        "closure depth.",
        f"Profile overfill factor {overfill['factor']:.2f}: that many cubic "
        "metres of this borrow are needed for every cubic metre of native "
        "sand, to reach the same beach width. This is a profile comparison "
        "and not James's textural overfill ratio, which also accounts for "
        "the fines winnowing out.",
        "The equilibrium profile is Dean's h = A y^(2/3) with A from the "
        "fall velocity (Kriebel, Kraus and Larson 1991). It describes the "
        "profile a beach settles to, not the one it has on any given day.",
        "Volumes are in place. Add the contractor's bulking, the overfill "
        "for losses during placement, and the advance nourishment that buys "
        "the design life.",
    ]
    if result["critical_volume"] > 0:
        notes.insert(4, (
            f"Critical volume {result['critical_volume']:.0f} m3/m: below "
            "this, fill this fine produces no dry beach at all, because the "
            "whole placement goes into flattening the underwater profile."
        ))
    return notes


def nourishment_section(
    result, native, borrow, berm_height: float, closure_depth: float,
    water_level: float = 0.0,
    title: str = "Beach nourishment, design profile",
    figsize: tuple[float, float] = (14.0, 7.0),
    exaggeration: float | None = None,
    ax=None,
) -> Section:
    """A standalone figure of a nourishment profile.

    Vertically exaggerated, because a beach profile is hundreds of metres
    long and a few metres deep and at a true scale it is a line. Left to
    itself the exaggeration is chosen so the profile fills the sheet, which
    is what makes it readable; pass a number to fix it instead.
    """
    from .nourishment import dean_scale, grain_compatibility

    if exaggeration is None:
        probe = Section(figsize=figsize, ax=ax)
        xlim, zlim = draw_nourishment(probe, result, native, borrow,
                                      berm_height, closure_depth, water_level,
                                      annotate=False)
        probe.fig.clear()
        span = (xlim[1] - xlim[0]) / (zlim[1] - zlim[0])
        exaggeration = max(1.0, round(span / (figsize[0] / figsize[1])))

    native_name = native if isinstance(native, str) else native.name
    dwg = Section(
        title,
        subtitle=(
            f"Native {native_name.replace('_', ' ')}, borrow "
            f"{(borrow if isinstance(borrow, str) else borrow.name).replace('_', ' ')}. "
            f"Berm {berm_height:.1f} m, closure {closure_depth:.1f} m. "
            f"VERTICAL EXAGGERATION {exaggeration:g}:1"
        ),
        figsize=figsize,
        exaggeration=exaggeration,
        ax=ax,
    )
    xlim, zlim = draw_nourishment(dwg, result, native, borrow, berm_height,
                                 closure_depth, water_level)
    match = grain_compatibility(native, borrow)
    dwg.key(loc="lower left")
    dwg.table(
        [
            ("Native d50", f"{match['phi_native']:.2f} phi"),
            ("Borrow d50", f"{match['phi_borrow']:.2f} phi"),
            ("A native", f"{dean_scale(native):.3f}"),
            ("A borrow", f"{dean_scale(borrow):.3f}"),
            ("", ""),
            ("Profile type", result["kind"]),
            ("Volume", f"{result['volume']:.0f} m3/m"),
            ("Dry beach", f"{result['advance']:.1f} m"),
            ("Critical volume", f"{result['critical_volume']:.0f} m3/m"),
        ],
        title="Design basis",
    )
    dwg.finish(xlim=xlim, zlim=zlim)
    return dwg


def nourishment_sheet(
    result, native, borrow, berm_height: float, closure_depth: float,
    water_level: float = 0.0,
    project: str = "Beach management scheme",
    title: str = "Nourishment design profile",
    size: str = "A3",
    exaggeration: float = 6.0,
    plan_design=None,
    plan_climate=None,
    plan_years=None,
    file: str = "nourishment_sheet.py",
    **titleblock,
) -> Sheet:
    """A drawing sheet of a nourishment profile, with its borrow notes.

    Pass ``plan_design`` and ``plan_climate`` to add a second view below the
    section: the planform spreading alongshore, from the same
    Pelnard-Considere solution the app plots. A fill is designed in two
    directions at once, and a sheet that shows only the profile leaves the
    reader to imagine how long it stays there.
    """
    sheet = Sheet(_sheet_for(title, project, file, **titleblock), size=size)
    has_plan = plan_design is not None and plan_climate is not None
    rect = (0.0, 0.52, 0.70, 0.44) if has_plan else (0.0, 0.05, 0.70, 0.95)
    view = sheet.viewport(rect=rect, exaggeration=exaggeration)
    xlim, zlim = draw_nourishment(view, result, native, borrow, berm_height,
                                 closure_depth, water_level)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", title, view.scale_text, loc=(0.02, 0.05))
    view.key(loc="upper right")

    if has_plan:
        plan_years = plan_years if plan_years is not None else _plan_years(
            plan_design, plan_climate)
        # The plan is kilometres by tens of metres, so it gets its own
        # exaggeration; the section's would flatten it to a line.
        plan = sheet.viewport(rect=(0.0, 0.11, 0.70, 0.40))
        plan.exaggeration_axis = "CROSS-SHORE"
        # The ladder is coarse this far out (1:25000, then 1:50000), and
        # falling a couple of percent over a rung would waste half the
        # paper. Trim the discretionary margin instead, the way a drafter
        # would, but never by more than a sixth of the width.
        margin = plan_margin(plan_design, plan_climate, plan_years)
        width = plan_design.length + 2.0 * margin
        pos = plan.ax.get_position()
        paper_w = pos.width * plan.fig.get_size_inches()[0] * 0.0254
        rungs = [c for c in plan.STANDARD_SCALES if c * paper_w >= 0.84 * width]
        if rungs:
            fits = rungs[0] * paper_w
            if fits < width:
                margin = max(0.0, 0.5 * (fits - plan_design.length))
        px, py = draw_nourishment_plan(plan, plan_design, plan_climate,
                                       plan_years, margin=margin)
        plan.auto_exaggeration(px, py)
        plan.fit_scale(px, py, paper=size, round_vertical=True)
        # The plan fills its viewport edge to edge, so its bubble goes in
        # the strip below it rather than on top of the sand.
        plan.detail_bubble("B", "PLANFORM EVOLUTION", plan.scale_text,
                           loc=(0.02, -0.16))

    notes = sheet.viewport(rect=(0.70, 0.0, 0.30, 1.0), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    text = nourishment_notes(result, native, borrow, berm_height, closure_depth)
    if view.exaggeration_note:
        text.insert(0, view.exaggeration_note.capitalize()
                    + ". Slopes are not true angles on this drawing.")
    notes.notes_block(text, title="NOTES", width=36, loc=(0.0, 1.0),
                      fontsize=6.0)
    notes.table(
        [("VOLUME", f"{result['volume']:.0f} m3/m"),
         ("DRY BEACH", f"{result['advance']:.1f} m"),
         ("PROFILE", result["kind"].upper())],
        title="SUMMARY", loc=(0.0, 0.0), align="left", fontsize=6.4,
    )
    sheet.set_scale_from(view)
    return sheet


#: erfinv(1/2), to the precision the half-life deserves.
_ERFINV_HALF = 0.4769362762044698733814

def plan_margin(design, climate, years) -> float:
    """How far past the fill a planform has to be drawn, in metres.

    Enough to show the sand that has left: 1.4 spreading lengths at the
    latest time, and never less than the fill is long. Split out from the
    drawing so a sheet can ask for the extents before it commits to a
    scale, and trim them to hold a rung of the scale ladder.
    """
    from .nourishment import SECONDS_PER_YEAR, longshore_diffusivity

    longest = max(years) * SECONDS_PER_YEAR
    spread = math.sqrt(longshore_diffusivity(climate, design) * longest)         if longest > 0 else 0.0
    return max(1.4 * spread, 0.6 * design.length, 200.0)


def _plan_years(design, climate) -> list[float]:
    """Times to draw a planform at, keyed to the fill's own half-life."""
    from .nourishment import SECONDS_PER_YEAR

    half_life = spreading_half_life(design, climate) / SECONDS_PER_YEAR
    return [0.0] + [round(f * half_life, 2) for f in (0.5, 1.0, 2.0, 4.0)]


def spreading_half_life(design, climate) -> float:
    """Time for the centre of a fill to lose half its width [s].

    From the Pelnard-Considere solution: the centre width is
    ``W erf(a / (2 sqrt(eps t)))``, which is halved when the argument
    reaches erfinv(1/2) = 0.476936... It is the natural clock of a fill, and the right basis
    for choosing what times to draw: a plan at ten years tells you nothing
    about a fill whose half-life is seven months.
    """
    from .nourishment import longshore_diffusivity

    diffusivity = longshore_diffusivity(climate, design)
    half = 0.5 * design.length
    return half**2 / (4.0 * _ERFINV_HALF**2 * diffusivity)


def draw_nourishment_plan(dwg: Section, design, climate, years=(0, 1, 2, 5, 10),
                          annotate: bool = True, samples: int = 601,
                          margin: float | None = None) -> tuple[tuple, tuple]:
    """Plan view of a fill spreading alongshore, from the analytical solution.

    Pelnard-Considere (1956) linearises the one-line equation into a
    diffusion equation, so a rectangular fill spreads exactly as a slug of
    heat does: the planform is a pair of error functions whose width grows
    as the square root of time. This draws that solution as a map, which is
    how a beach manager actually looks at it.

    Parameters
    ----------
    design, climate : NourishmentDesign, WaveClimate
        The fill and the wave climate driving it.
    years : sequence
        Times to draw, in years. Zero is the placed planform.

    Returns
    -------
    (xlim, ylim)
        Extents in metres.

    Notes on the scale
    ------------------
    Both axes are distance, so this could be drawn 1:1. It should not be. A
    fill is kilometres long and tens of metres wide, and at a true scale the
    whole story is a hairline. Shoreline-change plans are conventionally
    drawn with the cross-shore axis stretched, and
    :func:`nourishment_plan_section` picks the factor and prints it.

    Notes
    -----
    The analytical solution is for a rectangular fill with no tapers and a
    constant diffusivity. A real fill is tapered, the diffusivity varies
    with the wave climate, and the ends interact with whatever is next to
    them. It is the reference case, and it is the right one for seeing what
    the spreading does; it is not the numerical solver.
    """
    from .nourishment import SECONDS_PER_YEAR, longshore_diffusivity, pelnard_considere

    years = list(years)
    if not years:
        raise ValueError("Need at least one time to draw")
    if min(years) < 0:
        raise ValueError("Times must be non-negative")

    diffusivity = longshore_diffusivity(climate, design)
    longest = max(years) * SECONDS_PER_YEAR
    spread = math.sqrt(diffusivity * longest) if longest > 0 else 0.0
    half = 0.5 * design.length
    margin = plan_margin(design, climate, years) if margin is None else margin

    x0, x1 = -half - margin, half + margin
    x = np.linspace(x0, x1, samples)
    centred = _recentre_free(design, x)

    widths = {}
    for year in years:
        widths[year] = pelnard_considere(x, year * SECONDS_PER_YEAR,
                                         centred, climate)

    peak = float(max(w.max() for w in widths.values()))
    y0 = -0.45 * peak
    y1 = peak * 1.55

    # The sea above the original shoreline, the land below it.
    dwg.material([[x0, y0], [x1, y0], [x1, 0.0], [x0, 0.0]], "sand",
                 label="Existing beach", zorder=1.4)
    dwg.water(x0, x1, y1, bed=0.0, zorder=1.2)

    # The placed fill.
    placed = widths[0] if 0 in widths else None
    if placed is None:
        placed = pelnard_considere(x, 0.0, centred, climate)
    dwg.material(
        np.vstack((np.column_stack((x, np.zeros_like(x))),
                   np.column_stack((x[::-1], placed[::-1])))),
        "granular", label=f"Fill as placed, {design.berm_width:.0f} m wide",
        zorder=2.0,
    )

    # Later shorelines, cool to warm with age.
    ramp = ["#0b3554", "#1b6fa0", "#2f93b8", "#79c6d6", "#c47f1a", "#8a2f24"]
    later = [year for year in years if year > 0]
    for index, year in enumerate(later):
        colour = ramp[index % len(ramp)]
        dwg.line(np.column_stack((x, widths[year])), weight="medium",
                 color=colour, zorder=4.0 + 0.01 * index)
        if annotate:
            peak_here = float(widths[year].max())
            dwg.note((0.0, peak_here),
                     f"{year:g} yr, {peak_here:.0f} m at the centre",
                     offset=(70 + 0 * index, 18 - 18 * index))

    dwg.line([[x0, 0.0], [x1, 0.0]], weight="medium", style=(0, (6, 3)),
             zorder=3.8)

    if not annotate:
        return (x0, x1), (y0, y1)

    dwg.dim_h(-half, half, -0.22 * peak, f"fill length {design.length:.0f} m",
              extend_from=(0.0, 0.0))
    dwg.note((x0 + 0.06 * (x1 - x0), 0.0), "original shoreline",
             offset=(0, -26), ha="left")
    dwg.note((half + 0.45 * margin, 0.12 * peak),
             f"spreading reaches\n{spread:.0f} m in {max(years):g} yr",
             offset=(20, 40))

    return (x0, x1), (y0, y1)


def _recentre_free(design, x: np.ndarray):
    """A copy of the design centred on the drawn window."""
    from dataclasses import replace

    return replace(design, center=0.0)


def nourishment_plan_section(
    design, climate, years=None,
    title: str = "Beach nourishment, planform evolution",
    figsize: tuple[float, float] = (14.0, 6.5),
    exaggeration: float | None = None,
    ax=None,
) -> Section:
    """A standalone plan-view figure of a fill spreading alongshore.

    Left to themselves the times come from the fill's own half-life, so the
    plan always shows the part of the evolution that is worth looking at,
    and the cross-shore exaggeration is chosen to fill the sheet and printed
    on it.
    """
    from .nourishment import SECONDS_PER_YEAR, longshore_diffusivity

    diffusivity = longshore_diffusivity(climate, design)
    if years is None:
        years = _plan_years(design, climate)

    if exaggeration is None:
        import matplotlib.pyplot as plt

        probe = Section(figsize=figsize, ax=ax)
        xlim, ylim = draw_nourishment_plan(probe, design, climate, years,
                                           annotate=False)
        exaggeration = round(probe.auto_exaggeration(xlim, ylim))
        if ax is None:
            plt.close(probe.fig)
        else:
            probe.fig.clear()

    dwg = Section(
        title,
        subtitle=(
            f"Pelnard-Considere (1956). Fill {design.length:.0f} m long, "
            f"{design.berm_width:.0f} m wide, diffusivity "
            f"{diffusivity * SECONDS_PER_YEAR / 1e3:.0f} thousand m2/yr. "
            f"Half-life {spreading_half_life(design, climate) / SECONDS_PER_YEAR:.2f} yr. "
            f"CROSS-SHORE EXAGGERATION {exaggeration:g}:1"
        ),
        figsize=figsize,
        exaggeration=exaggeration,
        ax=ax,
    )
    dwg.exaggeration_axis = "CROSS-SHORE"
    xlim, ylim = draw_nourishment_plan(dwg, design, climate, years)
    dwg.key(loc="lower right")
    dwg.finish(xlim=xlim, zlim=ylim)
    dwg.ax.set_xlabel("alongshore distance (m)")
    dwg.ax.set_ylabel("shoreline advance (m)")
    return dwg


# ---------------------------------------------------------------------------
# Pier scour
# ---------------------------------------------------------------------------

#: Angle of repose of the scoured face, in degrees. The hole cannot stand
#: steeper than the sand will, so this sets how wide it is for a given
#: depth, and therefore how far the protection has to reach.
REPOSE_ANGLE = 32.0


def scour_hole_profile(scour: float, radius: float, repose: float = REPOSE_ANGLE,
                       samples: int = 2):
    """Points tracing one side of the scour hole, from the pier face out.

    The hole is drawn as a straight face at the angle of repose, because
    that is what a scour hole in sand is: it deepens until the sides stand
    at their limiting slope, and then widens. Anything smoother would be an
    invention.
    """
    if scour < 0:
        raise ValueError(f"Scour cannot be negative, got {scour}")
    if repose <= 0 or repose >= 90:
        raise ValueError(f"Repose angle must be in (0,90), got {repose}")
    reach = scour / math.tan(math.radians(repose))
    return [[radius, -scour], [radius + reach, 0.0]], reach


def draw_pier_scour(dwg: Section, design, annotate: bool = True,
                    protected: bool = False):
    """Section through a pier, either scoured or protected.

    Levels are to the initial bed, which is the datum that matters here:
    every dimension on the drawing is either a depth below it or a height
    above it, and the base level relative to it is the design lever.

    The two cases are drawn separately and deliberately so. An apron and a
    fully developed scour hole cannot both appear on one section: the
    apron exists to stop that hole, and showing them together says the
    protection failed and worked at the same time. ``protected=False`` is
    the prediction if nothing is done; ``protected=True`` is the proposed
    works, on an intact bed.

    Returns
    -------
    (xlim, zlim)
        Extents in metres.
    """
    pier = design.pier
    base = design.base
    conditions = design.conditions
    scour = design.equilibrium

    stem_r = 0.5 * pier.diameter
    base_r = 0.5 * base.width if base is not None else stem_r

    hole, reach = scour_hole_profile(scour, max(stem_r, base_r))
    if protected:
        reach = max(reach, design.protection["extent"])
    mwl = conditions.mean_depth
    hw = mwl + conditions.tidal_amplitude
    lw = mwl - conditions.tidal_amplitude

    half = max(stem_r, base_r) + reach
    margin = max(0.45 * half, 3.0)
    x0, x1 = -half - margin, half + margin
    lowest = min(-scour, base.bottom_level if base is not None else 0.0)
    z0 = lowest - max(0.30 * scour, 1.5)
    z1 = hw + max(0.22 * hw, 1.5)

    if protected:
        # Intact bed: the apron is here so the hole below never forms.
        dwg.material([[x0, z0], [x1, z0], [x1, 0.0], [x0, 0.0]],
                     "subgrade", label="Estuary bed", zorder=1.4)
        dwg.material([[x0, 0.0], [x1, 0.0], [x1, z1], [x0, z1]],
                     "water", zorder=1.2)
        apron = design.protection
        outer = max(stem_r, base_r) + apron["extent"]
        dwg.material(
            [[-outer, 0.0], [outer, 0.0],
             [outer, apron["thickness"]], [-outer, apron["thickness"]]],
            "toe", label=f"Rock apron, d50 = {apron['d50'] * 1000:.0f} mm",
            zorder=2.2)
    else:
        # Bed, with the hole carved out of it.
        left = [[p[0] * -1.0, p[1]] for p in reversed(hole)]
        bed = ([[x0, z0], [x0, 0.0]] + left
               + [[-max(stem_r, base_r), -scour], [max(stem_r, base_r), -scour]]
               + hole + [[x1, 0.0], [x1, z0]])
        dwg.material(bed, "subgrade", label="Estuary bed", zorder=1.4)

        # Water over everything, down into the hole.
        water = ([[x0, z1], [x1, z1], [x1, 0.0]] + [p for p in reversed(hole)]
                 + [[max(stem_r, base_r), -scour], [-max(stem_r, base_r), -scour]]
                 + [[p[0] * -1.0, p[1]] for p in hole] + [[x0, 0.0]])
        dwg.material(water, "water", zorder=1.2)

    # The base, then the stem over it.
    if base is not None:
        dwg.material(
            [[-base_r, base.bottom_level], [base_r, base.bottom_level],
             [base_r, base.top_level], [-base_r, base.top_level]],
            "reinforced", label="Pile cap / footing", zorder=4.0)
        stem_from = base.top_level
    else:
        stem_from = 0.0 if protected else -scour

    dwg.material([[-stem_r, stem_from], [stem_r, stem_from],
                  [stem_r, z1], [-stem_r, z1]],
                 "concrete", label="Pier stem", zorder=4.2)

    dwg.line([[x0, 0.0], [x1, 0.0]], weight="thin", style="--", zorder=3.0)

    if not annotate:
        return (x0, x1), (z0, z1)

    dwg.level(x0 + 0.04 * (x1 - x0), hw, f"HW +{hw:.2f} m", "water")
    dwg.level(x0 + 0.04 * (x1 - x0), mwl, f"MWL +{mwl:.2f} m", "water")
    dwg.level(x0 + 0.04 * (x1 - x0), lw, f"LW +{lw:.2f} m", "water")
    dwg.level(x1 - 0.04 * (x1 - x0), 0.0, "Initial bed 0.00 m", side="right")

    dwg.dim_h(-stem_r, stem_r, z1 - 0.10 * (z1 - z0),
              f"stem {pier.diameter:.2f} m")
    if base is not None:
        dwg.dim_h(-base_r, base_r, base.top_level + 0.055 * (z1 - z0),
                  f"base {base.width:.2f} m")

    state = design.governing["state"]
    dwg.note((0.0, z1 - 0.03 * (z1 - z0)),
             f"{abs(state['current']):.2f} m/s at the governing phase",
             offset=(0, 26), ha="center")

    if protected:
        apron = design.protection
        outer = max(stem_r, base_r) + apron["extent"]
        dwg.dim_h(max(stem_r, base_r), outer, 0.35 * z1,
                  f"apron {apron['extent']:.1f} m", extend_from=(0.0, 0.0))
        dwg.note((0.5 * (max(stem_r, base_r) + outer), 0.35 * z1),
                 f"{apron['thickness']:.2f} m thick, falling apron, "
                 f"{apron['launch_allowance']:.1f} m launch allowance",
                 offset=(0, -34), ha="center")
    else:
        dwg.level(x1 - 0.04 * (x1 - x0), -scour,
                  f"Scoured bed {-scour:.2f} m", side="right")
        dwg.dim_v(-scour, 0.0, -half - 0.45 * margin, f"scour {scour:.2f} m")
        dwg.slope((max(stem_r, base_r) + reach, 0.0),
                  round(1.0 / math.tan(math.radians(REPOSE_ANGLE)), 2),
                  -0.35 * scour)
        if base is not None and design.undermined:
            dwg.note((base_r, base.bottom_level),
                     "hole reaches below the footing",
                     offset=(34, -26), ha="left")

    return (x0, x1), (z0, z1)


def pier_scour_notes(design) -> list[str]:
    """Drawing notes for a pier scour assessment."""
    conditions = design.conditions
    material = conditions.material
    pier = design.pier
    base = design.base

    notes = [
        f"Bed: {material.name.lower()}, d50 = {material.d50 * 1000:.2f} mm.",
        f"Tide: {2 * conditions.tidal_amplitude:.1f} m range on a "
        f"{conditions.tidal_period / 3600:.2f} hour period, peak tidal "
        f"current {conditions.tidal_current:.2f} m/s, "
        f"{conditions.current_phase:.0f} deg ahead of the elevation.",
        f"River: {conditions.river_current:.2f} m/s steady and seaward, so "
        f"peak ebb is {conditions.peak_ebb_current:.2f} m/s against "
        f"{conditions.peak_flood_current:.2f} m/s on the flood.",
        f"Waves: Hs = {conditions.Hs:.2f} m, Tp = {conditions.Tp:.1f} s.",
        f"Pier: {pier.diameter:.2f} m {pier.shape.replace('_', ' ')} stem"
        + (f" on a {base.width:.1f} by {base.length:.1f} m base "
           f"{base.height:.1f} m thick, top at {base.top_level:+.2f} m to "
           f"the initial bed, skewed {base.skew:.0f} deg to the ebb."
           if base is not None else ", no base."),
    ]
    notes.extend(design.notes)
    notes.append(
        f"Scour hole drawn at the {REPOSE_ANGLE:.0f} degree angle of repose, "
        "which sets its width and therefore how far protection must reach.")
    notes.append(
        f"Protection: {design.protection['note']}")
    return notes


def pier_scour_section(design,
                       title: str = "Pier scour, estuary",
                       figsize: tuple[float, float] = (11.0, 7.0),
                       protected: bool = False,
                       exaggeration: float = 1.0,
                       ax=None) -> Section:
    """A standalone section of the pier and its scour hole.

    Drawn true to scale by default. A scour section is one of the few
    drawings in coastal work whose horizontal and vertical extents are
    comparable, so there is no reason to distort it, and the angle of
    repose then reads as the angle it actually is.
    """
    state = design.governing["state"]
    dwg = Section(
        title,
        subtitle=(
            f"Governing phase {state['phase']:.0f} deg on the "
            f"{'ebb' if state['ebb'] else 'flood'}: "
            f"{abs(state['current']):.2f} m/s current, "
            f"{state['Um']:.2f} m/s near-bed orbital, "
            f"{state['depth']:.2f} m depth. "
            f"Equilibrium scour {design.equilibrium:.2f} m."
        ),
        figsize=figsize,
        exaggeration=exaggeration,
        ax=ax,
    )
    xlim, zlim = draw_pier_scour(dwg, design, protected=protected)
    dwg.key(loc="upper right")
    dwg.finish(xlim=xlim, zlim=zlim)
    dwg.ax.set_xlabel("distance from pier axis (m)")
    dwg.ax.set_ylabel("level to initial bed (m)")
    return dwg


def pier_scour_sheet(design,
                     project: str = "Estuary crossing",
                     title: str = "Pier scour assessment",
                     size: str = "A3",
                     show_protection: bool = True,
                     file: str = "pier_scour_sheet.py",
                     **titleblock) -> Sheet:
    """A drawing sheet of the pier, its scour hole and its protection."""
    sheet = Sheet(_sheet_for(title, project, file, **titleblock), size=size)

    rect = ((0.0, 0.56, 0.70, 0.40) if show_protection
            else (0.0, 0.10, 0.70, 0.86))
    view = sheet.viewport(rect=rect)
    xlim, zlim = draw_pier_scour(view, design, protected=False)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", "PREDICTED SCOUR, UNPROTECTED", view.scale_text,
                       loc=(0.02, -0.12))
    view.key(loc="upper right")

    if show_protection:
        works = sheet.viewport(rect=(0.0, 0.08, 0.70, 0.40))
        wx, wz = draw_pier_scour(works, design, protected=True)
        works.fit_scale(wx, wz, paper=size)
        works.detail_bubble("B", "PROPOSED PROTECTION", works.scale_text,
                            loc=(0.02, -0.12))
        works.key(loc="upper right")

    notes = sheet.viewport(rect=(0.70, 0.0, 0.30, 1.0), frame=False)
    notes.ax.set_xlim(0, 1)
    notes.ax.set_ylim(0, 1)
    notes.ax.set_aspect("auto")
    text = pier_scour_notes(design)
    if view.exaggeration_note:
        text.insert(0, view.exaggeration_note.capitalize() + ".")
    notes.notes_block(text, title="NOTES", width=36, loc=(0.0, 1.0),
                      fontsize=5.6)

    base = design.base
    rows = [
        ("SCOUR", f"{design.equilibrium:.2f} m"),
        ("ONE TIDE", f"{design.tidal_limited:.2f} m"),
        ("D EFF", f"{design.governing['scour']['D_e']:.2f} m"),
        ("APRON d50", f"{design.protection['d50'] * 1000:.0f} mm"),
        ("APRON", f"{design.protection['extent']:.1f} m"),
    ]
    if base is not None:
        rows.insert(2, ("BASE", "UNDERMINED" if design.undermined
                        else "EXPOSED" if design.base_exposed else "BURIED"))
    notes.table(rows, title="SUMMARY", loc=(0.0, 0.0), align="left",
                fontsize=6.4)
    sheet.set_scale_from(view)
    return sheet
