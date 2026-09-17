"""
Engineering section drawings, drawn the way a design office draws them.

A coastal cross-section is not a plot. It is a scaled drawing: the geometry
is in real metres, the line weights carry meaning, materials are hatched
rather than coloured by value, and every dimension that governs the design
is called out on the paper. This module gives the small set of primitives
that takes matplotlib from plotting to drafting.

The pieces
----------
``Section``
    A drawing sheet in real-world coordinates (x cross-shore, z elevation),
    locked to equal aspect so a 1:2 slope looks like a 1:2 slope.
``Material``
    Fill, hatch and edge weight for one material, so quarry run reads as
    quarry run on any drawing in the package.
``Section.dim_h`` and ``Section.dim_v``
    Dimension lines with extension lines and arrowheads, offset in points
    so they stay legible whatever the scale.
``Section.level``
    The standard levelling triangle and elevation callout.
``Section.slope``
    The slope triangle, labelled as 1 : cot(alpha).
``Section.table``
    The parameter block. A drawing that does not carry its design inputs is
    not a deliverable.

Everything is drawn in metres. Text is sized in points and placed with
offsets in points, so annotation stays readable when the section is
rescaled; only the geometry scales.

Importing this module needs matplotlib::

    pip install pyCoastal[plots]
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = [
    "Material",
    "MATERIALS",
    "Section",
    "Sheet",
    "TitleBlock",
    "PAPER",
    "use_crisp_style",
    "write_dxf",
    "WEIGHTS",
    "TEXT",
    "INK",
]


# ---------------------------------------------------------------------------
# Drawing conventions
# ---------------------------------------------------------------------------

#: Line weights in points, in the usual drafting ratio 1 : 2 : 4.
WEIGHTS = {"thin": 0.5, "medium": 1.0, "heavy": 1.8, "extra": 2.4}

#: Text sizes in points.
TEXT = {"dim": 8.0, "note": 8.5, "label": 9.5, "title": 12.0, "table": 8.5}

#: Colour of every annotation: dimensions, leaders, levels, text.
INK = "#1a1a1a"


def WRAP(text: str, width: int) -> str:
    """Wrap a title-block field so it keeps inside the strip."""
    import textwrap

    return "\n".join(textwrap.wrap(text, width=width)) if text else ""


@dataclass
class Material:
    """How one material is drawn.

    Attributes
    ----------
    name : str
        Legend entry, for example "Rock armour, 6 t".
    face : str
        Fill colour. Kept desaturated: a section is read by its hatching and
        its line weights, not by colour.
    edge : str
        Outline colour.
    hatch : str or None
        A matplotlib hatch string, or None for a plain fill.
    weight : str
        Key into :data:`WEIGHTS` for the outline.
    stones : float
        If greater than zero, individual stones of this nominal diameter in
        metres are drawn inside the polygon. This is what makes a rubble
        mound read as rubble rather than as a shaded wedge.
    """

    name: str
    face: str
    edge: str = INK
    hatch: str | None = None
    weight: str = "medium"
    stones: float = 0.0


#: The standard material set. Extend it in a project rather than inventing
#: new colours per drawing, so sections stay comparable.
MATERIALS: dict[str, Material] = {
    "armour": Material("Primary armour", "#9b978f", "#2f2d2a", stones=1.0),
    "secondary": Material("Secondary armour", "#b0aca3", "#3a3833", stones=0.5),
    "underlayer": Material("Underlayer", "#c0bcb2", "#45433e", stones=0.35),
    "core": Material("Quarry run core", "#d5d1c6", "#54514b", hatch="...."),
    "toe": Material("Toe protection", "#a8a49b", "#35332f", stones=0.6),
    "concrete": Material("Mass concrete", "#cfcbc4", "#2a2a2a", hatch="//", weight="heavy"),
    "reinforced": Material("Reinforced concrete", "#c4c0b8", "#1f1f1f", hatch="xx", weight="heavy"),
    "blinding": Material("Blinding layer", "#bdb9b1", "#45433e", hatch="\\\\"),
    "rock_fill": Material("Rock fill", "#c9c5bb", "#4a4843", hatch="oo"),
    "granular": Material("Granular backfill", "#ddd2b6", "#6f6343", hatch="..."),
    "sand": Material("Sand", "#e6d5ad", "#8a7648", hatch="...."),
    "subgrade": Material("In-situ seabed", "#cdc0a6", "#6d6243", hatch="////"),
    "pavement": Material("Promenade surfacing", "#b8b4ae", "#33322f"),
    "water": Material("Water", "#c3dce7", "#4d7f97", weight="thin"),
}


def use_crisp_style() -> None:
    """Global matplotlib settings for legible technical figures.

    Arial throughout as the workspace requires, hairline spines, real black
    ink for text, and hatching thin enough to read at 600 dpi rather than
    filling in solid. Call it once at the top of a script.
    """
    import matplotlib

    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans"],
            "font.size": 9.5,
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.edgecolor": INK,
            "axes.linewidth": 0.8,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.minor.width": 0.5,
            "ytick.minor.width": 0.5,
            "lines.linewidth": 1.4,
            "lines.solid_capstyle": "round",
            "legend.frameon": False,
            "legend.fontsize": 8.5,
            "grid.linewidth": 0.5,
            "grid.alpha": 0.35,
            "hatch.linewidth": 0.45,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "image.interpolation": "nearest",
        }
    )


# ---------------------------------------------------------------------------
# The drawing sheet
# ---------------------------------------------------------------------------


class Section:
    """A cross-section drawing in real coordinates.

    Parameters
    ----------
    title, subtitle : str
        Drawing title and a one-line description.
    figsize : tuple
        Sheet size in inches.
    ax : matplotlib Axes, optional
        Draw into an existing axes, for a multi-panel comparison sheet. A
        new figure is made if this is None.

    exaggeration : float
        Vertical exaggeration. One is a true section, where a 1:2 slope
        looks like a 1:2 slope. Anything else distorts every angle on the
        drawing, and :meth:`fit_scale` then reports separate horizontal and
        vertical scales and sets ``exaggeration_note`` so the distortion is
        stated rather than hidden.

    Notes
    -----
    A section drawn at a true scale is the default, and the right choice
    whenever the structure is not far wider than it is tall. A navigation
    channel six hundred metres wide and twenty deep is the case where it is
    not: at true scale it is an unreadable sliver, and dredging drawings
    have always been exaggerated. Exaggerate deliberately, and say so.
    """

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        figsize: tuple[float, float] = (13.0, 7.0),
        ax=None,
        caps: bool = False,
        dim_style: str = "arrow",
        frame: bool = True,
        exaggeration: float = 1.0,
    ) -> None:
        import matplotlib.pyplot as plt

        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        else:
            self.fig, self.ax = ax.figure, ax

        self.title = title
        self.subtitle = subtitle
        #: Set True to render every callout in capitals, as a drawing office
        #: does, so hand-written site notes are visibly different from
        #: drafted text.
        self.caps = caps
        if dim_style not in ("arrow", "tick"):
            raise ValueError(f"dim_style must be 'arrow' or 'tick', got {dim_style!r}")
        #: "arrow" for engineering arrowheads, "tick" for the architectural
        #: 45 degree slash.
        self.dim_style = dim_style
        self.frame = frame
        if exaggeration <= 0:
            raise ValueError(
                f"Exaggeration must be positive, got {exaggeration}"
            )
        #: Vertical exaggeration. One is a true section. Anything else must
        #: be stated on the drawing, which :meth:`fit_scale` does for you.
        self.exaggeration = float(exaggeration)
        #: Filled in by :meth:`fit_scale`.
        self.scale: float | None = None
        self.vertical_scale: float | None = None
        self.scale_text: str = ""
        #: Set by :meth:`fit_scale` when the section is exaggerated.
        self.exaggeration_note: str = ""
        #: What the stretched axis is called on this view. A plan stretches
        #: the cross-shore axis, not a vertical one, and the drawing has to
        #: say which or the reader measures the wrong thing.
        self.exaggeration_axis: str = "VERTICAL"
        #: Paper size, set when the view belongs to a :class:`Sheet`.
        self.paper: str = ""
        self._used: dict[str, Material] = {}
        self._dxf: list[tuple] = []
        self._rng = np.random.default_rng(12345)

        self.ax.set_aspect(self.exaggeration, adjustable="datalim")
        if frame:
            for side in ("top", "right"):
                self.ax.spines[side].set_visible(False)
            self.ax.set_xlabel("distance (m)")
            self.ax.set_ylabel("level (m CD)")
        else:
            # Inside a drawing sheet the scale bar and the levels carry the
            # measurements, so plot axes would only be clutter.
            self.ax.set_axis_off()

    def _t(self, text: str) -> str:
        """Apply the sheet's text case to a callout."""
        return text.upper() if self.caps else text

    # -- geometry ----------------------------------------------------------

    def material(self, points, kind: str, label: str | None = None, zorder: float = 2.0):
        """Fill a closed polygon with a material.

        Parameters
        ----------
        points : sequence of (x, z)
            Polygon vertices in metres. It is closed automatically.
        kind : str
            Key into :data:`MATERIALS`.
        label : str or False, optional
            Overrides the material name in the key, for a size callout such
            as "Rock armour, Dn50 = 1.45 m". Pass ``False`` to draw the
            polygon but keep it out of the key: a field of five groynes or
            six breakwater segments wants one entry, not six identical
            ones.
        """
        from matplotlib.patches import Polygon

        if kind not in MATERIALS:
            raise KeyError(f"Unknown material {kind!r}. Known: {sorted(MATERIALS)}")
        spec = MATERIALS[kind]
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 2 or len(pts) < 3:
            raise ValueError("A material polygon needs at least three (x, z) points")

        patch = Polygon(
            pts,
            closed=True,
            facecolor=spec.face,
            edgecolor=spec.edge,
            hatch=spec.hatch,
            linewidth=WEIGHTS[spec.weight],
            zorder=zorder,
            joinstyle="miter",
        )
        self.ax.add_patch(patch)
        if spec.stones > 0:
            self._stone_texture(patch, pts, spec, zorder + 0.1)

        if label is not False:
            key = label or spec.name
            self._used.setdefault(
                key, Material(key, spec.face, spec.edge, spec.hatch, spec.weight)
            )
        self._dxf.append(("POLY", pts, kind.upper()))
        return patch

    def _stone_texture(self, patch, pts, spec: Material, zorder: float) -> None:
        """Scatter irregular stones inside a layer, clipped to it.

        Drawn from a fixed seed, so the same section redraws identically.
        The stones are a texture at the nominal diameter, not a packing
        calculation; the stone count in the quantities comes from the Rock
        Manual layer relation, never from what is on the paper.
        """
        from matplotlib.patches import Polygon

        d = spec.stones
        x0, x1 = pts[:, 0].min(), pts[:, 0].max()
        z0, z1 = pts[:, 1].min(), pts[:, 1].max()
        if d <= 0 or x1 - x0 <= 0 or z1 - z0 <= 0:
            return

        # Cap the count so a large mound does not turn into a solid mat of
        # outlines at print resolution.
        nx = int(np.clip((x1 - x0) / (0.9 * d), 1, 90))
        nz = int(np.clip((z1 - z0) / (0.9 * d), 1, 60))
        if nx * nz > 2600:
            return

        xs = np.linspace(x0, x1, nx)
        zs = np.linspace(z0, z1, nz)
        theta = np.linspace(0, 2 * np.pi, 7, endpoint=False)
        for iz, z in enumerate(zs):
            shift = 0.45 * d if iz % 2 else 0.0
            for x in xs + shift:
                r = 0.5 * d * (0.72 + 0.34 * self._rng.random(7))
                ang = theta + 0.25 * self._rng.random(7)
                stone = np.column_stack((x + r * np.cos(ang), z + r * np.sin(ang)))
                poly = Polygon(
                    stone,
                    closed=True,
                    facecolor="none",
                    edgecolor=spec.edge,
                    linewidth=0.4,
                    alpha=0.75,
                    zorder=zorder,
                )
                poly.set_clip_path(patch)
                self.ax.add_patch(poly)

    def line(self, points, weight: str = "medium", style: str = "-",
             color: str | None = None, zorder: float = 4.0, **kwargs):
        """A construction, ground or hidden line."""
        pts = np.asarray(points, dtype=float)
        (ln,) = self.ax.plot(
            pts[:, 0], pts[:, 1],
            color=color or INK, linewidth=WEIGHTS[weight], linestyle=style,
            zorder=zorder, **kwargs,
        )
        self._dxf.append(("LINE", pts, "LINES"))
        return ln

    def water(self, x0: float, x1: float, level: float, bed=None,
              label: str | None = None, zorder: float = 1.0):
        """Fill water between a level and the bed, with the level symbol.

        ``bed`` is either a constant level or an (x, z) polyline. Water is
        drawn under everything else, so structures sit in it rather than
        floating on it.
        """
        from matplotlib.patches import Polygon

        spec = MATERIALS["water"]
        if bed is None:
            floor = np.array([[x0, level - 100.0], [x1, level - 100.0]])
        else:
            bed = np.asarray(bed, dtype=float)
            floor = bed if bed.ndim == 2 else np.array(
                [[x0, float(bed)], [x1, float(bed)]]
            )

        poly = np.vstack(([[x0, level]], [[x1, level]], floor[::-1]))
        patch = Polygon(poly, closed=True, facecolor=spec.face, edgecolor="none",
                        zorder=zorder)
        self.ax.add_patch(patch)
        self.ax.plot([x0, x1], [level, level], color=spec.edge,
                     linewidth=WEIGHTS["medium"], zorder=zorder + 0.2)
        self._used.setdefault("Water", spec)
        if label:
            self.level(x0 + 0.05 * (x1 - x0), level, label, side="right",
                       symbol="water")
        return patch

    # -- annotation --------------------------------------------------------

    def _arrow(self, p0, p1, both: bool = True) -> None:
        """Dimension line between two points, in the sheet's terminator style."""
        if self.dim_style == "tick":
            x0, z0 = p0
            x1, z1 = p1
            # The line runs a little past each terminator, as a drafted
            # dimension does, and the slash sits on the extension line.
            dx, dz = x1 - x0, z1 - z0
            over = 0.06
            self.ax.plot(
                [x0 - over * dx, x1 + over * dx], [z0 - over * dz, z1 + over * dz],
                color=INK, linewidth=WEIGHTS["thin"], zorder=7,
            )
            self.ax.plot(
                [x0, x1], [z0, z1], linestyle="none", marker=(2, 0, 45),
                markersize=7, markeredgewidth=0.9, color=INK, zorder=7,
            )
            return
        style = "<->" if both else "->"
        self.ax.annotate(
            "", xy=p1, xytext=p0,
            arrowprops=dict(arrowstyle=style, color=INK, linewidth=WEIGHTS["thin"],
                            shrinkA=0, shrinkB=0, mutation_scale=9),
            zorder=7,
        )

    def dim_h(self, x0: float, x1: float, z: float, text: str | None = None,
              extend_from: tuple[float, float] | None = None) -> None:
        """Horizontal dimension between x0 and x1, drawn at level z.

        ``extend_from`` gives the two levels the extension lines run back
        to, so the dimension ties visibly to the geometry it measures.
        """
        if text is None:
            text = f"{abs(x1 - x0):.2f} m"
        if extend_from is not None:
            for x, zf in zip((x0, x1), extend_from):
                self.ax.plot([x, x], [zf, z], color=INK, linewidth=WEIGHTS["thin"],
                             linestyle=(0, (4, 3)), zorder=6, alpha=0.8)
        self._arrow((x0, z), (x1, z))
        self.ax.annotate(
            self._t(text), xy=(0.5 * (x0 + x1), z), xytext=(0, 3),
            textcoords="offset points",
            ha="center", va="bottom", fontsize=TEXT["dim"], color=INK, zorder=8,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
        )

    def dim_v(self, z0: float, z1: float, x: float, text: str | None = None,
              extend_from: tuple[float, float] | None = None,
              side: str = "right") -> None:
        """Vertical dimension between z0 and z1, drawn at chainage x."""
        if text is None:
            text = f"{abs(z1 - z0):.2f} m"
        if extend_from is not None:
            for z, xf in zip((z0, z1), extend_from):
                self.ax.plot([xf, x], [z, z], color=INK, linewidth=WEIGHTS["thin"],
                             linestyle=(0, (4, 3)), zorder=6, alpha=0.8)
        self._arrow((x, z0), (x, z1))
        dx = 4 if side == "right" else -4
        self.ax.annotate(
            self._t(text), xy=(x, 0.5 * (z0 + z1)), xytext=(dx, 0),
            textcoords="offset points",
            ha="left" if side == "right" else "right", va="center",
            fontsize=TEXT["dim"], color=INK, zorder=8, rotation=90,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
        )

    def level(self, x: float, z: float, text: str | None = None, side: str = "left",
              symbol: str = "level", run: float = 0.0) -> None:
        """Levelling triangle and elevation callout at (x, z).

        ``symbol`` is "level" for the solid surveyor's triangle used on
        structure levels, or "water" for the open triangle used on a water
        level. ``run`` draws a witness line of that length before the
        triangle, to pull the callout clear of the structure.
        """
        if text is None:
            text = f"{z:+.2f} m CD"
        if run:
            self.ax.plot([x, x + run], [z, z], color=INK, linewidth=WEIGHTS["thin"],
                         linestyle=(0, (4, 3)), zorder=6)
            x = x + run

        # The triangle is sized in points so it survives any drawing scale.
        self.ax.plot([x], [z], marker="v", markersize=6.5,
                     markerfacecolor=INK if symbol == "level" else "white",
                     markeredgecolor=INK, markeredgewidth=0.9, zorder=8,
                     clip_on=False, linestyle="none")
        dx = -6 if side == "left" else 6
        self.ax.annotate(
            self._t(text), xy=(x, z), xytext=(dx, 7), textcoords="offset points",
            ha="right" if side == "left" else "left", va="bottom",
            fontsize=TEXT["dim"], color=INK, fontweight="bold", zorder=9,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=INK, lw=0.4,
                      alpha=0.92),
        )

    def slope(self, apex: tuple[float, float], cot_alpha: float, rise: float,
              direction: str = "left", label: str | None = None) -> None:
        """Slope triangle at a point on a face, labelled 1 : cot(alpha).

        ``apex`` is the upper point of the triangle on the slope face and
        ``rise`` its vertical leg. ``direction`` says which way the face
        falls away, so the triangle sits on the material side.
        """
        sign = -1.0 if direction == "left" else 1.0
        x, z = apex
        run = sign * cot_alpha * rise
        tri = np.array([[x, z], [x, z - rise], [x + run, z - rise], [x, z]])
        self.ax.plot(tri[:, 0], tri[:, 1], color=INK, linewidth=WEIGHTS["thin"],
                     zorder=7)
        self.ax.annotate(
            self._t(label or f"1 : {cot_alpha:g}"),
            xy=(x + 0.5 * run, z - rise), xytext=(0, -4),
            textcoords="offset points", ha="center", va="top",
            fontsize=TEXT["dim"], color=INK, zorder=8,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
        )

    def note(self, xy: tuple[float, float], text: str,
             offset: tuple[float, float] = (40, 30), ha: str | None = None) -> None:
        """Leader line with a note, the offset given in points."""
        if ha is None:
            ha = "left" if offset[0] >= 0 else "right"
        self.ax.annotate(
            self._t(text), xy=xy, xytext=offset, textcoords="offset points",
            ha=ha, va="center", fontsize=TEXT["note"], color=INK, zorder=9,
            arrowprops=dict(arrowstyle="-", color=INK, linewidth=WEIGHTS["thin"],
                            shrinkA=0, shrinkB=2,
                            connectionstyle="angle,angleA=0,angleB=60,rad=0"),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9),
        )

    # -- sheet furniture ---------------------------------------------------

    def detail_bubble(self, label: str, title: str, scale: str = "",
                      loc: tuple[float, float] = (0.02, -0.06)) -> None:
        """The drawing-office detail marker: circled letter, then the title.

        ``label`` is the single letter or number that a key plan points to,
        ``title`` the name of the view, and ``scale`` its drawn scale. Placed
        in axes coordinates, so it stays put when the geometry changes.
        """
        x, y = loc
        self.ax.text(
            x, y, label.upper(), transform=self.ax.transAxes, ha="center",
            va="center", fontsize=TEXT["label"], fontweight="bold", color=INK,
            zorder=11, clip_on=False,
            bbox=dict(boxstyle="circle,pad=0.42", fc="white", ec=INK, lw=1.0),
        )
        self.ax.annotate(
            title.upper(), xy=(x, y), xycoords=self.ax.transAxes,
            xytext=(16, 2), textcoords="offset points", ha="left", va="bottom",
            fontsize=TEXT["title"] - 1.0, fontweight="bold", color=INK,
            zorder=11, annotation_clip=False,
        )
        caption = f"SCALE {scale}" if scale else ""
        if self.exaggeration_note:
            caption = (caption + "   " if caption else "") + self.exaggeration_note
        self.ax.annotate(
            caption, xy=(x, y), xycoords=self.ax.transAxes, xytext=(16, -9),
            textcoords="offset points", ha="left", va="top",
            fontsize=TEXT["dim"] - 0.5, color=INK, zorder=11,
            fontweight="bold" if self.exaggeration_note else "normal",
            annotation_clip=False,
        )
        # The rule under the title, drawn to the width of the title text.
        self.ax.annotate(
            "", xy=(x, y), xycoords=self.ax.transAxes,
            xytext=(16, -2), textcoords="offset points",
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.0), zorder=0,
        )

    def notes_block(self, lines, title: str = "NOTES",
                    loc: tuple[float, float] = (0.015, 0.985),
                    numbered: bool = True, width: int = 52,
                    fontsize: float | None = None) -> None:
        """Boxed notes, numbered the way a specification note block is.

        ``lines`` is a sequence of strings, or of (heading, body) pairs for a
        note with a bold-looking lead-in. Long lines are wrapped to ``width``
        characters so the block keeps a straight right edge.
        """
        import textwrap

        entries = []
        for i, item in enumerate(lines, start=1):
            if isinstance(item, (tuple, list)):
                head, body = item
                text = f"{head.upper()}: {body}"
            else:
                text = str(item)
            prefix = f"{i}. " if numbered else "- "
            wrapped = textwrap.wrap(text, width=width) or [""]
            entries.append(prefix + wrapped[0])
            entries += [" " * len(prefix) + line for line in wrapped[1:]]

        body = "\n".join(entries)
        self.ax.text(
            loc[0], loc[1], f"{title.upper()}\n{body}",
            transform=self.ax.transAxes, ha="left", va="top",
            fontsize=fontsize or TEXT["dim"] - 0.5, color=INK, zorder=11,
            linespacing=1.45,
            bbox=dict(boxstyle="square,pad=0.6", fc="white", ec=INK, lw=0.8),
        )

    def scale_bar(self, length: float, loc: tuple[float, float] = (0.03, 0.06),
                  divisions: int = 4, unit: str = "m") -> None:
        """Chequered scale bar, in data units, placed in axes coordinates.

        A drawing without plot axes needs one of these, and a drawing with
        plot axes is better with one anyway: it survives being cropped,
        pasted into a report, or printed at the wrong size.
        """
        from matplotlib.patches import Rectangle
        from matplotlib.transforms import blended_transform_factory as blend

        if divisions < 1:
            raise ValueError(f"Need at least one division, got {divisions}")
        x0, x1 = self.ax.get_xlim()
        z0, z1 = self.ax.get_ylim()
        start = x0 + loc[0] * (x1 - x0)
        base = z0 + loc[1] * (z1 - z0)
        height = 0.012 * (z1 - z0)
        step = length / divisions

        for i in range(divisions):
            self.ax.add_patch(Rectangle(
                (start + i * step, base), step, height,
                facecolor=INK if i % 2 else "white", edgecolor=INK,
                linewidth=0.7, zorder=11,
            ))
        for i in range(divisions + 1):
            self.ax.annotate(
                f"{i * step:g}", xy=(start + i * step, base + height),
                xytext=(0, 2), textcoords="offset points", ha="center",
                va="bottom", fontsize=TEXT["dim"] - 1.0, color=INK, zorder=11,
            )
        self.ax.annotate(
            unit, xy=(start + length, base), xytext=(6, 0),
            textcoords="offset points", ha="left", va="bottom",
            fontsize=TEXT["dim"] - 1.0, color=INK, zorder=11,
        )

    def key(self, loc: str = "upper left", ncol: int = 1):
        """Material key, in drawing order."""
        from matplotlib.patches import Patch

        handles = [
            Patch(facecolor=m.face, edgecolor=m.edge, hatch=m.hatch,
                  linewidth=0.7, label=name)
            for name, m in self._used.items()
        ]
        if not handles:
            return None
        leg = self.ax.legend(
            handles=handles, loc=loc, ncol=ncol, fontsize=TEXT["dim"],
            frameon=True, framealpha=0.94, edgecolor=INK, borderpad=0.6,
            labelspacing=0.7, handlelength=2.0, handleheight=1.3,
        )
        leg.get_frame().set_linewidth(0.5)
        leg.set_zorder(10)
        return leg

    def table(self, rows, title: str = "Design parameters",
              loc: tuple[float, float] = (0.985, 0.03), align: str = "right",
              fontsize: float | None = None) -> None:
        """Parameter block, as monospaced rows in axes coordinates.

        ``rows`` is a sequence of (label, value) pairs. Values are already
        formatted strings: the drawing shows what the engineer decided, not
        a float repr.
        """
        rows = list(rows)
        if not rows:
            return
        width = max(len(str(a)) for a, _ in rows)
        body = "\n".join(f"{a:<{width}}  {b}" for a, b in rows)
        text = f"{title}\n" + "-" * (width + 12) + f"\n{body}"
        self.ax.text(
            loc[0], loc[1], text, transform=self.ax.transAxes,
            ha=align, va="bottom", fontsize=fontsize or TEXT["table"],
            family="monospace", color=INK, zorder=10,
            bbox=dict(boxstyle="square,pad=0.6", fc="#fbfbf9", ec=INK, lw=0.7),
        )

    #: Scales a drawing office will actually print at.
    STANDARD_SCALES = (5, 10, 20, 25, 50, 75, 100, 125, 150, 200, 250, 500,
                       750, 1000, 1250, 2000, 2500, 5000, 10000, 20000,
                       25000, 50000)

    def auto_exaggeration(self, xlim, zlim, cap: float = 200.0) -> float:
        """Stretch the second axis just enough to fill this viewport.

        A guessed exaggeration is nearly always wrong, and the cost is not
        cosmetic: :meth:`fit_scale` sizes the drawing to whichever axis is
        tighter, so an exaggeration a little too large throws the whole view
        onto the next scale up and leaves half the paper empty. The viewport
        already knows its own proportions, so let it do the arithmetic.

        Returns the factor, and sets :attr:`exaggeration` to it.
        """
        pos = self.ax.get_position()
        fig_w, fig_h = self.fig.get_size_inches()
        paper_aspect = (pos.width * fig_w) / (pos.height * fig_h)
        need_w = float(xlim[1] - xlim[0])
        need_h = float(zlim[1] - zlim[0])
        if need_w <= 0 or need_h <= 0:
            raise ValueError("Extents must be positive")
        e = min(cap, max(1.0, (need_w / need_h) / paper_aspect))
        self.exaggeration = e
        self.ax.set_aspect(e)
        return e

    def fit_scale(self, xlim, zlim, scales=None, paper: str = "",
                  round_vertical: bool = False) -> float:
        """Set the view to a true, round drawing scale that fits the extents.

        Picks the smallest standard scale at which the requested extents fit
        inside the axes, then centres the view on them and sets the limits to
        exactly that scale. The returned denominator is what belongs in the
        title block: a drawing whose stated scale is not the scale it was
        plotted at is worse than one with no scale at all.

        Parameters
        ----------
        xlim, zlim : tuple
            The extents that must be visible, in metres.
        scales : sequence, optional
            Candidate denominators. Defaults to :data:`STANDARD_SCALES`.
        paper : str
            Paper size to name in the returned string, e.g. "A3".
        round_vertical : bool
            Snap the vertical scale to a standard denominator too, adjusting
            the exaggeration to suit. A section labelled "V 1:1210.83" cannot
            be scaled off the paper by anyone; "V 1:1250" can.

        Returns
        -------
        float
            The scale denominator S, for a scale of 1 : S. Use
            ``scale_text`` for the string.
        """
        candidates = tuple(scales) if scales else self.STANDARD_SCALES
        pos = self.ax.get_position()
        fig_w, fig_h = self.fig.get_size_inches()
        w_in, h_in = pos.width * fig_w, pos.height * fig_h
        if w_in <= 0 or h_in <= 0:
            raise RuntimeError("The axes has no size; add it to a figure first")

        need_w = float(xlim[1] - xlim[0])
        need_h = float(zlim[1] - zlim[0])
        if need_w <= 0 or need_h <= 0:
            raise ValueError("Extents must be positive")

        # Metres of drawing per metre of paper. An exaggerated section takes
        # more paper vertically for the same depth, so the vertical extent
        # is scaled up before the two are compared.
        e = self.exaggeration
        required = max(need_w / (w_in * 0.0254),
                       need_h * e / (h_in * 0.0254))
        # A hair of tolerance: extents fitted to a rung come back as
        # required = rung + 1e-9, and a strict test would skip to the next
        # rung up and leave half the paper empty.
        chosen = next((c for c in candidates if c >= required * (1.0 - 1e-9)),
                      None)
        if chosen is None:
            chosen = required        # nothing standard is large enough

        if round_vertical:
            # The vertical scale must stay large enough for the extents to
            # fit, so snap it up, never down, and back out the exaggeration.
            needed_v = need_h / (h_in * 0.0254)
            snapped = next((c for c in candidates
                            if c >= needed_v * (1.0 - 1e-9)), None)
            if snapped is not None and snapped <= chosen:
                e = chosen / snapped
                self.exaggeration = e

        span_x = w_in * 0.0254 * chosen
        span_z = h_in * 0.0254 * chosen / e
        cx = 0.5 * (xlim[0] + xlim[1])
        cz = 0.5 * (zlim[0] + zlim[1])
        self.ax.set_xlim(cx - 0.5 * span_x, cx + 0.5 * span_x)
        self.ax.set_ylim(cz - 0.5 * span_z, cz + 0.5 * span_z)

        self.scale = float(chosen)
        self.vertical_scale = float(chosen) / e
        on = f" @ {paper}" if paper else ""
        if abs(e - 1.0) < 1e-9:
            self.scale_text = f"1:{chosen:g}{on}"
            self.exaggeration_note = ""
        else:
            self.scale_text = (
                f"H 1:{chosen:g}  V 1:{self.vertical_scale:g}{on}"
            )
            self.exaggeration_note = (
                f"{self.exaggeration_axis} EXAGGERATION {e:.4g} : 1"
            )
        return self.scale

    def finish(self, xlim=None, zlim=None, grid: bool = True) -> "Section":
        """Set limits, titles and the background grid."""
        if xlim is not None:
            self.ax.set_xlim(*xlim)
        if zlim is not None:
            self.ax.set_ylim(*zlim)
        if grid:
            self.ax.minorticks_on()
            self.ax.grid(True, which="major", color="#b9b9b9", linewidth=0.5,
                         alpha=0.55)
            self.ax.grid(True, which="minor", color="#d5d5d5", linewidth=0.35,
                         alpha=0.5)
            self.ax.set_axisbelow(True)
        if self.title:
            self.ax.set_title(self.title, loc="left", fontsize=TEXT["title"],
                              fontweight="bold", pad=14)
        if self.subtitle:
            self.ax.annotate(
                self.subtitle, xy=(0, 1), xycoords="axes fraction",
                xytext=(0, 6), textcoords="offset points", ha="left", va="bottom",
                fontsize=TEXT["note"], color="#4a4a4a",
            )
        return self

    def save(self, path, dpi: int = 600) -> None:
        """Write the drawing as a PNG at print resolution."""
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight")

    def to_dxf(self, path, scale: float = 1.0) -> None:
        """Export the geometry as DXF, for import into a CAD package.

        Only the material polygons and construction lines are exported,
        each on a layer named after its material. Dimensions, notes and the
        parameter block are left behind: they are drawing furniture, and a
        CAD user will want to place their own, to their own house style.
        """
        write_dxf(path, self._dxf, scale=scale)


# ---------------------------------------------------------------------------
# Drawing sheets
# ---------------------------------------------------------------------------

#: Paper sizes in millimetres, landscape (width, height).
PAPER = {
    "A0": (1189.0, 841.0),
    "A1": (841.0, 594.0),
    "A2": (594.0, 420.0),
    "A3": (420.0, 297.0),
    "A4": (297.0, 210.0),
}


@dataclass
class TitleBlock:
    """What goes in the strip down the right-hand edge of a sheet.

    Every field is a plain string, because a title block records what a
    human decided, not what a calculation produced. Leave a field empty and
    its row is skipped.

    Attributes
    ----------
    project : str
        The job. Printed rotated down the strip, as on a real sheet.
    title : str
        What this sheet shows.
    organisation, client : str
        Who drew it and who for.
    scale : str
        Drawn scale, for example "1:100 @ A3". Say the paper size: a scale
        without one is meaningless the moment the sheet is reprinted.
    date, file, sheet, revision : str
        The usual issue record.
    drawn_by, checked_by : str
        Initials.
    disclaimer : str
        The small print set vertically in the strip.
    """

    project: str = ""
    title: str = ""
    organisation: str = ""
    client: str = ""
    scale: str = "AS SHOWN"
    date: str = ""
    file: str = ""
    sheet: str = "1/1"
    revision: str = "A"
    drawn_by: str = ""
    checked_by: str = ""
    disclaimer: str = (
        "Do not scale from this drawing. All dimensions in metres unless "
        "noted. Levels to chart datum."
    )
    status: str = "PRELIMINARY"


class Sheet:
    """A drawing sheet: border, title block strip, and one or more views.

    Parameters
    ----------
    titleblock : TitleBlock
        The strip down the right-hand edge.
    size : str
        Key into :data:`PAPER`, or a (width, height) pair in millimetres.
    dpi : int
        Raster resolution on save. A full A3 at 400 dpi is already 6600 px
        across, finer than the line work can carry; go higher only if the
        sheet is going to be enlarged.
    margin : float
        Border inset in millimetres.
    strip : float
        Width of the title block strip in millimetres.

    Examples
    --------
    >>> sheet = Sheet(TitleBlock(project="Harbour works", title="Seawall"))
    >>> view = sheet.viewport()          # doctest: +SKIP
    >>> # draw into view, which is an ordinary Section
    >>> sheet.save("seawall.png")        # doctest: +SKIP
    """

    def __init__(
        self,
        titleblock: "TitleBlock",
        size: str | tuple[float, float] = "A3",
        dpi: int = 400,
        margin: float = 8.0,
        strip: float = 52.0,
    ) -> None:
        import matplotlib.pyplot as plt

        if isinstance(size, str):
            if size not in PAPER:
                raise KeyError(f"Unknown paper size {size!r}. Known: {sorted(PAPER)}")
            width_mm, height_mm = PAPER[size]
            self.size_name = size
        else:
            width_mm, height_mm = size
            self.size_name = f"{width_mm:g}x{height_mm:g}"

        if strip >= width_mm - 2 * margin:
            raise ValueError("Title block strip is wider than the sheet")

        self.titleblock = titleblock
        self.dpi = dpi
        self.width_mm, self.height_mm = width_mm, height_mm
        self.fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
        self.fig.patch.set_facecolor("white")
        self.views: list[Section] = []

        # Everything below is in figure fractions of the sheet.
        self._m = (margin / width_mm, margin / height_mm)
        self._strip_w = strip / width_mm
        self._draw_frame()

    # -- frame -------------------------------------------------------------

    @property
    def _area(self) -> tuple[float, float, float, float]:
        """Left, bottom, width, height of the usable drawing area."""
        mx, my = self._m
        return mx, my, 1.0 - 2 * mx - self._strip_w, 1.0 - 2 * my

    def _rule(self, x0, y0, x1, y1, weight: str = "medium") -> None:
        from matplotlib.lines import Line2D

        self.fig.add_artist(Line2D([x0, x1], [y0, y1], color=INK,
                                   linewidth=WEIGHTS[weight], zorder=20))

    def _text(self, x, y, text, size=6.5, weight="normal", ha="left",
              va="center", rotation=0.0) -> None:
        if not text:
            return
        self.fig.text(x, y, text, fontsize=size, fontweight=weight, color=INK,
                      ha=ha, va=va, rotation=rotation, zorder=21)

    def _draw_frame(self) -> None:
        import textwrap

        from matplotlib.patches import Rectangle

        mx, my = self._m
        tb = self.titleblock

        # Sheet border.
        self.fig.add_artist(Rectangle(
            (mx, my), 1 - 2 * mx, 1 - 2 * my, transform=self.fig.transFigure,
            facecolor="none", edgecolor=INK, linewidth=WEIGHTS["heavy"],
            zorder=20,
        ))

        x_strip = 1 - mx - self._strip_w
        self._rule(x_strip, my, x_strip, 1 - my, "heavy")

        bot, top = my, 1 - my
        height = top - bot
        xl = x_strip + 0.010
        xr = 1 - mx - 0.010
        xc = x_strip + 0.5 * self._strip_w

        # Row edges as fractions of the strip height, bottom first. The issue
        # record sits at the bottom because that is where people look for it.
        edges = [0.0, 0.08, 0.16, 0.26, 0.36, 0.64, 0.76, 0.88, 1.0]
        for f in edges[1:-1]:
            y = bot + f * height
            self._rule(x_strip, y, 1 - mx, y, "thin")

        def band(i: int) -> tuple[float, float, float]:
            """Bottom, top and height of row i, in figure fractions."""
            y0 = bot + edges[i] * height
            y1 = bot + edges[i + 1] * height
            return y0, y1, y1 - y0

        def label_value(i: int, label: str, value: str, size: float = 7.0,
                        weight: str = "normal", x: float | None = None,
                        ha: str = "left", frac: float = 0.62) -> None:
            """A small caption with its value under it, inside row i."""
            y0, y1, h = band(i)
            xx = xl if x is None else x
            self._text(xx, y0 + (frac + 0.26) * h, label, 5.5, ha=ha)
            self._text(xx, y0 + frac * h - 0.22 * h, value, size, weight, ha=ha)

        # Sheet number.
        y0, y1, h = band(0)
        self._text(xl, y0 + 0.72 * h, "SHEET", 5.5)
        self._text(xc, y0 + 0.34 * h, tb.sheet, 13, "bold", ha="center")

        # Revision and status.
        y0, y1, h = band(1)
        self._text(xl, y0 + 0.72 * h, "REV", 5.5)
        self._text(xl, y0 + 0.30 * h, tb.revision, 9, "bold")
        self._text(xr, y0 + 0.72 * h, "STATUS", 5.5, ha="right")
        self._text(xr, y0 + 0.30 * h, tb.status, 7, "bold", ha="right")

        # Date and file.
        y0, y1, h = band(2)
        self._text(xl, y0 + 0.78 * h, "DATE", 5.5)
        self._text(xl, y0 + 0.56 * h, tb.date, 7)
        self._text(xl, y0 + 0.30 * h, "FILE", 5.5)
        self._text(xl, y0 + 0.10 * h, tb.file, 6.0)

        # Scale and initials.
        y0, y1, h = band(3)
        self._text(xl, y0 + 0.78 * h, "SCALE", 5.5)
        self._text(xl, y0 + 0.56 * h, tb.scale, 7, "bold")
        self._text(xl, y0 + 0.30 * h, "DRAWN / CHECKED", 5.5)
        self._text(xl, y0 + 0.10 * h, " / ".join(
            q for q in (tb.drawn_by, tb.checked_by) if q), 6.5)

        # Drawing title, rotated, as on the sheet this imitates.
        y0, y1, h = band(4)
        self._text(xc, y0 + 0.5 * h, WRAP(tb.title.upper(), 34), 10.0, "bold",
                   ha="center", rotation=90)

        # Organisation and client.
        y0, y1, h = band(5)
        self._text(xc, y0 + 0.66 * h, tb.organisation.upper(), 8.5, "bold",
                   ha="center")
        self._text(xc, y0 + 0.28 * h, WRAP(tb.client, 30), 6.0, ha="center")

        # The small print.
        y0, y1, h = band(6)
        self._text(xc, y0 + 0.5 * h, WRAP(tb.disclaimer.upper(), 30), 4.6,
                   ha="center")

        # Project.
        y0, y1, h = band(7)
        self._text(xc, y0 + 0.5 * h, WRAP(tb.project.upper(), 26), 8.5, "bold",
                   ha="center")

    # -- views -------------------------------------------------------------

    def viewport(self, rect: tuple[float, float, float, float] = (0, 0, 1, 1),
                 pad: float = 0.02, **kwargs) -> "Section":
        """Add a drawing view, positioned within the usable area.

        ``rect`` is (left, bottom, width, height) as fractions of the
        drawing area, so (0, 0, 0.5, 1) is the left half of the sheet.
        Keyword arguments go to :class:`Section`.
        """
        left, bottom, width, height = rect
        if not (0 <= left <= 1 and 0 <= bottom <= 1):
            raise ValueError(f"Viewport origin {rect[:2]} is off the sheet")
        ax0, ay0, aw, ah = self._area
        ax = self.fig.add_axes([
            ax0 + (left + pad) * aw,
            ay0 + (bottom + pad) * ah,
            max(width - 2 * pad, 0.05) * aw,
            max(height - 2 * pad, 0.05) * ah,
        ])
        kwargs.setdefault("frame", False)
        kwargs.setdefault("caps", True)
        kwargs.setdefault("dim_style", "tick")
        view = Section(ax=ax, **kwargs)
        view.paper = self.size_name
        self.views.append(view)
        return view

    def set_scale_from(self, view: "Section") -> None:
        """Copy a view's fitted scale into the title block and redraw it.

        Call it after :meth:`Section.fit_scale` so the strip states the
        scale the drawing was actually plotted at.
        """
        if not view.scale_text:
            raise RuntimeError("That view has no fitted scale; call fit_scale first")
        self.titleblock.scale = view.scale_text
        for artist in list(self.fig.artists) + list(self.fig.texts):
            artist.remove()
        self._draw_frame()

    def save(self, path, dpi: int | None = None) -> None:
        """Write the sheet. No bounding-box trim: the border is the edge."""
        self.fig.savefig(path, dpi=dpi or self.dpi, facecolor="white",
                         bbox_inches=None)

    def to_dxf(self, path, scale: float = 1.0) -> None:
        """Export every view's geometry to one DXF."""
        entities: list[tuple] = []
        for view in self.views:
            entities += view._dxf
        write_dxf(path, entities, scale=scale)


# ---------------------------------------------------------------------------
# DXF export
# ---------------------------------------------------------------------------


def write_dxf(path, entities, scale: float = 1.0) -> None:
    """Write polylines to a minimal DXF R12 file.

    ``entities`` is a sequence of ``(kind, points, layer)``, where kind is
    "POLY" for a closed polygon or "LINE" for an open polyline. R12 LINE
    entities are used throughout: the format is ancient, which is exactly
    why every CAD package still reads it without complaint.
    """
    out = ["0", "SECTION", "2", "ENTITIES"]
    for kind, pts, layer in entities:
        pts = np.asarray(pts, dtype=float) * scale
        if len(pts) < 2:
            continue
        segments = list(zip(pts[:-1], pts[1:]))
        if kind == "POLY" and len(pts) > 2:
            segments.append((pts[-1], pts[0]))
        for (x0, z0), (x1, z1) in segments:
            out += ["0", "LINE", "8", str(layer),
                    "10", f"{x0:.6f}", "20", f"{z0:.6f}", "30", "0.0",
                    "11", f"{x1:.6f}", "21", f"{z1:.6f}", "31", "0.0"]
    out += ["0", "ENDSEC", "0", "EOF"]
    with open(path, "w", encoding="ascii") as fh:
        fh.write("\n".join(out) + "\n")
