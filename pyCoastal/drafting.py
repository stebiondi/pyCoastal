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

    Notes
    -----
    The axes are set to equal aspect and the vertical axis is not
    exaggerated. A section with a true 1:2 slope that looks steeper than
    1:2 on the paper is a drawing error, not a styling choice; if you need
    exaggeration, say so on the drawing.
    """

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        figsize: tuple[float, float] = (13.0, 7.0),
        ax=None,
    ) -> None:
        import matplotlib.pyplot as plt

        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=figsize)
        else:
            self.fig, self.ax = ax.figure, ax

        self.title = title
        self.subtitle = subtitle
        self._used: dict[str, Material] = {}
        self._dxf: list[tuple] = []
        self._rng = np.random.default_rng(12345)

        self.ax.set_aspect("equal", adjustable="datalim")
        for side in ("top", "right"):
            self.ax.spines[side].set_visible(False)
        self.ax.set_xlabel("distance (m)")
        self.ax.set_ylabel("level (m CD)")

    # -- geometry ----------------------------------------------------------

    def material(self, points, kind: str, label: str | None = None, zorder: float = 2.0):
        """Fill a closed polygon with a material.

        Parameters
        ----------
        points : sequence of (x, z)
            Polygon vertices in metres. It is closed automatically.
        kind : str
            Key into :data:`MATERIALS`.
        label : str, optional
            Overrides the material name in the key, for a size callout such
            as "Rock armour, Dn50 = 1.45 m".
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
            text, xy=(0.5 * (x0 + x1), z), xytext=(0, 3), textcoords="offset points",
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
            text, xy=(x, 0.5 * (z0 + z1)), xytext=(dx, 0), textcoords="offset points",
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
            text, xy=(x, z), xytext=(dx, 7), textcoords="offset points",
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
            label or f"1 : {cot_alpha:g}",
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
            text, xy=xy, xytext=offset, textcoords="offset points",
            ha=ha, va="center", fontsize=TEXT["note"], color=INK, zorder=9,
            arrowprops=dict(arrowstyle="-", color=INK, linewidth=WEIGHTS["thin"],
                            shrinkA=0, shrinkB=2,
                            connectionstyle="angle,angleA=0,angleB=60,rad=0"),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9),
        )

    # -- sheet furniture ---------------------------------------------------

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
