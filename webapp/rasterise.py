"""
Rasterise the app's SVG sheets with matplotlib, so they can be looked at.

The usual rasterisers here all want cairo, which is not installed. The SVG
this app emits is deliberately narrow, though: paths built only from M, L,
H, V and Z, plus rects, circles and text. That is small enough to draw with
matplotlib, which is already a dependency.

It is a review tool, not a renderer. Hatch patterns are approximated by a
flat wash and fonts are whatever matplotlib has, so do not judge typography
from the output. It answers the question that matters after a drawing-code
change: is the thing actually on the page, in the right place, in the right
order.

    python webapp/rasterise.py media/webapp/seawall.svg
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

SVG = "{http://www.w3.org/2000/svg}"
NUMBER = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?")


def strip(tag: str) -> str:
    return tag[len(SVG):] if tag.startswith(SVG) else tag


def parse_path(d: str):
    """Subpaths from the M/L/H/V/Z subset this app emits."""
    subpaths, current, closed = [], [], []
    cursor = [0.0, 0.0]
    for command, body in re.findall(r"([MLHVZmlhvz])([^MLHVZmlhvz]*)", d):
        values = [float(v) for v in NUMBER.findall(body)]
        upper = command.upper()
        if upper == "M":
            if current:
                subpaths.append((current, False))
            current = []
            for i in range(0, len(values) - 1, 2):
                cursor = [values[i], values[i + 1]]
                current.append(tuple(cursor))
        elif upper == "L":
            for i in range(0, len(values) - 1, 2):
                cursor = [values[i], values[i + 1]]
                current.append(tuple(cursor))
        elif upper == "H":
            for v in values:
                cursor = [v, cursor[1]]
                current.append(tuple(cursor))
        elif upper == "V":
            for v in values:
                cursor = [cursor[0], v]
                current.append(tuple(cursor))
        elif upper == "Z":
            if current:
                subpaths.append((current, True))
                current = []
    if current:
        subpaths.append((current, False))
    return subpaths


def colour(value):
    """Returns (colour, alpha_override). None means do not paint.

    matplotlib's `alpha` argument overrides the alpha channel of an
    eight-digit hex, so a pattern wash written as "#00000018" comes out
    opaque black. The alpha has to travel separately.
    """
    if value in (None, "none", ""):
        return None, None
    if value.startswith("url("):
        # A hatch pattern, approximated by a light wash. This tool is for
        # checking placement, not for judging the hatching.
        return "#000000", 0.10
    return value, None


def draw_node(ax, node, inherited=None):
    inherited = dict(inherited or {})
    tag = strip(node.tag)
    if tag in ("defs", "pattern", "clipPath"):
        return

    attrs = dict(inherited)
    attrs.update(node.attrib)

    fill, fill_alpha = colour(attrs.get("fill"))
    stroke, _ = colour(attrs.get("stroke"))
    width = float(attrs.get("stroke-width", 1) or 1)
    opacity = float(attrs.get("opacity", 1) or 1)
    if fill_alpha is not None:
        opacity = fill_alpha
    dash = attrs.get("stroke-dasharray")
    linestyle = "-"
    if dash:
        parts = [float(v) for v in NUMBER.findall(dash)]
        if parts:
            linestyle = (0, tuple(parts))

    if tag == "rect":
        x = float(attrs.get("x", 0)); y = float(attrs.get("y", 0))
        w = float(attrs.get("width", 0)); h = float(attrs.get("height", 0))
        ax.add_patch(Rectangle((x, y), w, h,
                               facecolor=fill or "none",
                               edgecolor=stroke or "none",
                               linewidth=width, alpha=opacity, zorder=next_z()))
    elif tag == "circle":
        ax.add_patch(Circle((float(attrs.get("cx", 0)), float(attrs.get("cy", 0))),
                            float(attrs.get("r", 0)),
                            facecolor=fill or "none", edgecolor=stroke or "none",
                            linewidth=width, alpha=opacity, zorder=next_z()))
    elif tag == "path":
        for points, closed in parse_path(attrs.get("d", "")):
            if len(points) < 2:
                continue
            if closed and fill:
                ax.add_patch(Polygon(points, closed=True, facecolor=fill,
                                     edgecolor=stroke or "none", linewidth=width,
                                     alpha=opacity, zorder=next_z()))
            else:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                ax.plot(xs, ys, color=stroke or "#000000", linewidth=width,
                        linestyle=linestyle, alpha=opacity, zorder=next_z(),
                        solid_capstyle="butt")
    elif tag == "text":
        anchor = {"middle": "center", "end": "right"}.get(
            attrs.get("text-anchor", "start"), "left")
        rotation = 0.0
        transform = attrs.get("transform", "")
        if transform.startswith("rotate"):
            rotation = -float(NUMBER.findall(transform)[0])
        ax.text(float(attrs.get("x", 0)), float(attrs.get("y", 0)),
                node.text or "", fontsize=float(attrs.get("font-size", 10)) * 0.92,
                color=attrs.get("fill", "#000000"), ha=anchor, va="baseline",
                rotation=rotation, rotation_mode="anchor", zorder=next_z(),
                family="monospace")

    # A clipped group is honoured by clipping every patch it contains to the
    # named rectangle, which is all this app's clips ever are.
    clip = CLIPS.get(clip_id(attrs.get("clip-path")))
    passthrough = {k: v for k, v in attrs.items()
                   if k in ("fill", "stroke", "stroke-width", "opacity")}
    start = len(ax.patches), len(ax.lines), len(ax.texts)
    for child in node:
        draw_node(ax, child, passthrough if tag == "g" else inherited)
    if clip:
        window = Rectangle((clip[0], clip[1]), clip[2], clip[3],
                           transform=ax.transData)
        for artist in (list(ax.patches[start[0]:]) + list(ax.lines[start[1]:])
                       + list(ax.texts[start[2]:])):
            artist.set_clip_path(window)


CLIPS = {}


def clip_id(value):
    if not value:
        return None
    match = re.search(r"url\(#([^)]+)\)", value)
    return match.group(1) if match else None


def collect_clips(root):
    CLIPS.clear()
    for node in root.iter():
        if strip(node.tag) != "clipPath":
            continue
        for child in node:
            if strip(child.tag) == "rect":
                CLIPS[node.get("id")] = (
                    float(child.get("x", 0)), float(child.get("y", 0)),
                    float(child.get("width", 0)), float(child.get("height", 0)))


_Z = [0]


def next_z():
    _Z[0] += 1
    return _Z[0]


def rasterise(svg_path: Path, png_path: Path, dpi: int = 160) -> None:
    root = ET.parse(svg_path).getroot()
    box = [float(v) for v in NUMBER.findall(root.get("viewBox", "0 0 980 560"))]
    w, h = box[2], box[3]

    fig, ax = plt.subplots(figsize=(w / 100, h / 100))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    collect_clips(root)
    _Z[0] = 0
    for child in root:
        draw_node(ax, child)

    ax.set_xlim(box[0], box[0] + w)
    ax.set_ylim(box[1] + h, box[1])      # SVG is y-down
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(png_path, dpi=dpi, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path, nargs="+")
    parser.add_argument("--dpi", type=int, default=160)
    args = parser.parse_args()
    for path in args.svg:
        out = path.with_suffix(".png")
        rasterise(path, out, args.dpi)
        print(f"  {path.name} -> {out.name}")


if __name__ == "__main__":
    main()
