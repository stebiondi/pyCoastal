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
    "draw_rubble_mound",
    "rubble_mound_section",
    "rubble_mound_sheet",
    "mound_layer_volumes",
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
    view = sheet.viewport(rect=(0.0, 0.05, 0.72, 0.95))
    xlim, zlim = draw_seawall(view, d, sea_extent, land_extent)
    view.fit_scale(xlim, zlim, paper=size)
    view.detail_bubble("A", title, view.scale_text, loc=(0.02, 0.04))
    view.scale_bar(10.0, loc=(0.62, 0.04))
    view.key(loc="upper left")

    notes = sheet.viewport(rect=(0.72, 0.05, 0.28, 0.95), frame=False)
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
