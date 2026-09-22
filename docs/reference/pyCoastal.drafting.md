# `pyCoastal.drafting`

Source: [`pyCoastal/drafting.py`](../../pyCoastal/drafting.py)

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

## `WEIGHTS`

```python
WEIGHTS = {'thin': 0.5, 'medium': 1.0, 'heavy': 1.8, 'extra': 2.4}
```

## `TEXT`

```python
TEXT = {'dim': 8.0, 'note': 8.5, 'label': 9.5, 'title': 12.0, 'table': 8.5}
```

## `INK`

```python
INK = '#1a1a1a'
```

## `WRAP`

```python
def WRAP(text: str, width: int) -> str
```

```text
Wrap a title-block field so it keeps inside the strip.
```

## `Material`

```python
class Material
    name: str
    face: str
    edge: str = INK
    hatch: str | None = None
    weight: str = 'medium'
    stones: float = 0.0
```

```text
How one material is drawn.

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
```

## `MATERIALS`

```python
MATERIALS = {'armour': Material('Primary armour', '#9b978f', '#2f2d2a', stones=1.0), 'secondary': Material('Secondary armour', '#b0aca3', '#3a3833', stones=0.5), 'underlayer': Material('Underlayer', '#c0bcb2', '#45433e', stones=0.35), 'core': Material('Quarry run core', '#d5d1c6', '#54514b', hatch='....'), 'toe': Material('Toe protection', '#a8a49b', '#35332f', stones=0.6), 'concrete': Material('Mass concrete', '#cfcbc4', '#2a2a2a', hatch='//', weight='heavy'), 'reinforced': Material('Reinforced concrete', '#c4c0b8', '#1f1f1f', hatch='xx', weight='heavy'), 'blinding': Material('Blinding layer', '#bdb9b1', '#45433e', hatch='\\\\'), 'rock_fill': Material('Rock fill', '#c9c5bb', '#4a4843', hatch='oo'), 'granular': Material('Granular backfill', '#ddd2b6', '#6f6343', hatch='...'), 'sand': Material('Sand', '#e6d5ad', '#8a7648', hatch='....'), 'subgrade': Material('In-situ seabed', '#cdc0a6', '#6d6243', hatch='////'), 'pavement': Material('Promenade surfacing', '#b8b4ae', '#33322f'), 'water': Material('Water', '#c3dce7', '#4d7f97', weight='thin')}
```

## `use_crisp_style`

```python
def use_crisp_style() -> None
```

```text
Global matplotlib settings for legible technical figures.

Arial throughout as the workspace requires, hairline spines, real black
ink for text, and hatching thin enough to read at 600 dpi rather than
filling in solid. Call it once at the top of a script.
```

## `Section`

```python
class Section
```

```text
A cross-section drawing in real coordinates.

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
```

### `Section.material` (method)

```python
Section.material(self, points, kind: str, label: str | None=None, zorder: float=2.0)
```

```text
Fill a closed polygon with a material.

Parameters
----------
points : sequence of (x, z)
    Polygon vertices in metres. It is closed automatically.
kind : str
    Key into :data:`MATERIALS`.
label : str or False, optional
    Overrides the material name in the key, for a size callout such
    as "Rock armour, Dn50 = 1.45 m". Pass ``False`` to draw the
    polygon but keep it out of the key: a pair of abutments, or a
    row of piers, wants one entry rather than one each.
```

### `Section.line` (method)

```python
Section.line(self, points, weight: str='medium', style: str='-', color: str | None=None, zorder: float=4.0, **kwargs)
```

```text
A construction, ground or hidden line.
```

### `Section.water` (method)

```python
Section.water(self, x0: float, x1: float, level: float, bed=None, label: str | None=None, zorder: float=1.0)
```

```text
Fill water between a level and the bed, with the level symbol.

``bed`` is either a constant level or an (x, z) polyline. Water is
drawn under everything else, so structures sit in it rather than
floating on it.
```

### `Section.dim_h` (method)

```python
Section.dim_h(self, x0: float, x1: float, z: float, text: str | None=None, extend_from: tuple[float, float] | None=None) -> None
```

```text
Horizontal dimension between x0 and x1, drawn at level z.

``extend_from`` gives the two levels the extension lines run back
to, so the dimension ties visibly to the geometry it measures.
```

### `Section.dim_v` (method)

```python
Section.dim_v(self, z0: float, z1: float, x: float, text: str | None=None, extend_from: tuple[float, float] | None=None, side: str='right') -> None
```

```text
Vertical dimension between z0 and z1, drawn at chainage x.
```

### `Section.level` (method)

```python
Section.level(self, x: float, z: float, text: str | None=None, side: str='left', symbol: str='level', run: float=0.0) -> None
```

```text
Levelling triangle and elevation callout at (x, z).

``symbol`` is "level" for the solid surveyor's triangle used on
structure levels, or "water" for the open triangle used on a water
level. ``run`` draws a witness line of that length before the
triangle, to pull the callout clear of the structure.
```

### `Section.slope` (method)

```python
Section.slope(self, apex: tuple[float, float], cot_alpha: float, rise: float, direction: str='left', label: str | None=None) -> None
```

```text
Slope triangle at a point on a face, labelled 1 : cot(alpha).

``apex`` is the upper point of the triangle on the slope face and
``rise`` its vertical leg. ``direction`` says which way the face
falls away, so the triangle sits on the material side.
```

### `Section.note` (method)

```python
Section.note(self, xy: tuple[float, float], text: str, offset: tuple[float, float]=(40, 30), ha: str | None=None) -> None
```

```text
Leader line with a note, the offset given in points.
```

### `Section.detail_bubble` (method)

```python
Section.detail_bubble(self, label: str, title: str, scale: str='', loc: tuple[float, float]=(0.02, -0.06)) -> None
```

```text
The drawing-office detail marker: circled letter, then the title.

``label`` is the single letter or number that a key plan points to,
``title`` the name of the view, and ``scale`` its drawn scale. Placed
in axes coordinates, so it stays put when the geometry changes.
```

### `Section.notes_block` (method)

```python
Section.notes_block(self, lines, title: str='NOTES', loc: tuple[float, float]=(0.015, 0.985), numbered: bool=True, width: int=52, fontsize: float | None=None) -> None
```

```text
Boxed notes, numbered the way a specification note block is.

``lines`` is a sequence of strings, or of (heading, body) pairs for a
note with a bold-looking lead-in. Long lines are wrapped to ``width``
characters so the block keeps a straight right edge.
```

### `Section.scale_bar` (method)

```python
Section.scale_bar(self, length: float, loc: tuple[float, float]=(0.03, 0.06), divisions: int=4, unit: str='m') -> None
```

```text
Chequered scale bar, in data units, placed in axes coordinates.

A drawing without plot axes needs one of these, and a drawing with
plot axes is better with one anyway: it survives being cropped,
pasted into a report, or printed at the wrong size.
```

### `Section.key` (method)

```python
Section.key(self, loc: str='upper left', ncol: int=1)
```

```text
Material key, in drawing order.
```

### `Section.table` (method)

```python
Section.table(self, rows, title: str='Design parameters', loc: tuple[float, float]=(0.985, 0.03), align: str='right', fontsize: float | None=None) -> None
```

```text
Parameter block, as monospaced rows in axes coordinates.

``rows`` is a sequence of (label, value) pairs. Values are already
formatted strings: the drawing shows what the engineer decided, not
a float repr.

A row of ``(None, None)`` draws a rule instead, for separating what
was measured from what was derived from it. A summary that lists
three scour components and then their totals wants the reader to
see at a glance which lines are which.
```

### `Section.auto_exaggeration` (method)

```python
Section.auto_exaggeration(self, xlim, zlim, cap: float=200.0) -> float
```

```text
Stretch the second axis just enough to fill this viewport.

A guessed exaggeration is nearly always wrong, and the cost is not
cosmetic: :meth:`fit_scale` sizes the drawing to whichever axis is
tighter, so an exaggeration a little too large throws the whole view
onto the next scale up and leaves half the paper empty. The viewport
already knows its own proportions, so let it do the arithmetic.

Returns the factor, and sets :attr:`exaggeration` to it.
```

### `Section.fit_scale` (method)

```python
Section.fit_scale(self, xlim, zlim, scales=None, paper: str='', round_vertical: bool=False) -> float
```

```text
Set the view to a true, round drawing scale that fits the extents.

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
```

### `Section.finish` (method)

```python
Section.finish(self, xlim=None, zlim=None, grid: bool=True) -> 'Section'
```

```text
Set limits, titles and the background grid.
```

### `Section.save` (method)

```python
Section.save(self, path, dpi: int=600) -> None
```

```text
Write the drawing as a PNG at print resolution.
```

### `Section.to_dxf` (method)

```python
Section.to_dxf(self, path, scale: float=1.0) -> None
```

```text
Export the geometry as DXF, for import into a CAD package.

Only the material polygons and construction lines are exported,
each on a layer named after its material. Dimensions, notes and the
parameter block are left behind: they are drawing furniture, and a
CAD user will want to place their own, to their own house style.
```

## `PAPER`

```python
PAPER = {'A0': (1189.0, 841.0), 'A1': (841.0, 594.0), 'A2': (594.0, 420.0), 'A3': (420.0, 297.0), 'A4': (297.0, 210.0)}
```

## `TitleBlock`

```python
class TitleBlock
    project: str = ''
    title: str = ''
    organisation: str = ''
    client: str = ''
    scale: str = 'AS SHOWN'
    date: str = ''
    file: str = ''
    sheet: str = '1/1'
    revision: str = 'A'
    drawn_by: str = ''
    checked_by: str = ''
    disclaimer: str = 'Do not scale from this drawing. All dimensions in metres unless noted. Levels to chart datum.'
    status: str = 'PRELIMINARY'
```

```text
What goes in the strip down the right-hand edge of a sheet.

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
```

## `Sheet`

```python
class Sheet
```

```text
A drawing sheet: border, title block strip, and one or more views.

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
```

### `Sheet.viewport` (method)

```python
Sheet.viewport(self, rect: tuple[float, float, float, float]=(0, 0, 1, 1), pad: float=0.02, **kwargs) -> 'Section'
```

```text
Add a drawing view, positioned within the usable area.

``rect`` is (left, bottom, width, height) as fractions of the
drawing area, so (0, 0, 0.5, 1) is the left half of the sheet.
Keyword arguments go to :class:`Section`.
```

### `Sheet.set_scale_from` (method)

```python
Sheet.set_scale_from(self, view: 'Section') -> None
```

```text
Copy a view's fitted scale into the title block and redraw it.

Call it after :meth:`Section.fit_scale` so the strip states the
scale the drawing was actually plotted at.
```

### `Sheet.save` (method)

```python
Sheet.save(self, path, dpi: int | None=None) -> None
```

```text
Write the sheet. No bounding-box trim: the border is the edge.
```

### `Sheet.to_dxf` (method)

```python
Sheet.to_dxf(self, path, scale: float=1.0) -> None
```

```text
Export every view's geometry to one DXF.
```

## `write_dxf`

```python
def write_dxf(path, entities, scale: float=1.0) -> None
```

```text
Write polylines to a minimal DXF R12 file.

``entities`` is a sequence of ``(kind, points, layer)``, where kind is
"POLY" for a closed polygon or "LINE" for an open polyline. R12 LINE
entities are used throughout: the format is ancient, which is exactly
why every CAD package still reads it without complaint.
```

