# `pyCoastal.applications.sections`

Source: [`pyCoastal/applications/sections.py`](../../pyCoastal/applications/sections.py)

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

## `MoundProfile`

```python
class MoundProfile
    x_sea: float
    x_land: float
    crest: float
    cot_sea: float
    cot_land: float
```

```text
A trapezoidal mound, described by its crest and its two slopes.

Attributes
----------
x_sea, x_land : float
    Chainage of the seaward and landward crest edges [m].
crest : float
    Crest level [m].
cot_sea, cot_land : float
    Slopes as horizontal run per unit rise.
```

### `MoundProfile.points` (method)

```python
MoundProfile.points(self, bed: float) -> np.ndarray
```

```text
Closed polygon from the seaward toe round to the landward toe.
```

### `MoundProfile.offset` (method)

```python
MoundProfile.offset(self, thickness: float) -> 'MoundProfile'
```

```text
The profile a uniform layer of ``thickness`` inside this one.

The offset is perpendicular to each face, which is how a layer
thickness is specified and measured on site. Lowering the crest by
the thickness and pulling the crest edges in by
``t (sqrt(1 + cot^2) - cot)`` is the exact perpendicular offset of a
trapezoid, not an approximation.
```

### `MoundProfile.band` (method)

```python
MoundProfile.band(self, inner: 'MoundProfile', bed: float) -> np.ndarray
```

```text
Closed polygon of the layer between this profile and ``inner``.
```

### `MoundProfile.area` (method)

```python
MoundProfile.area(self, bed: float) -> float
```

```text
Cross-sectional area above the bed [m2 per metre run].
```

## `mound_layer_volumes`

```python
def mound_layer_volumes(profiles, bed: float) -> list[float]
```

```text
Area of each layer, from a list of profiles outermost first.

Each entry is the area between one profile and the next, in m2 per metre
run, with the innermost profile taken as solid. Multiply by the length of
the trunk for a volume.
```

## `draw_seawall`

```python
def draw_seawall(dwg: Section, design, sea_extent: float=22.0, land_extent: float=8.0, show_scour: bool=True, annotate: bool=True) -> tuple[tuple, tuple]
```

```text
Put a designed seawall into an open :class:`Section`.

Returns the (xlim, zlim) the section needs, so the caller can either set
them directly or hand them to
:meth:`~pyCoastal.drafting.Section.fit_scale`.
```

## `seawall_notes`

```python
def seawall_notes(design) -> list[str]
```

```text
Specification notes generated from a seawall design.

The numbers come from the calculation; the material clauses are the
generic ones a coastal designer would expect to see and still has to
confirm for the project. Nothing here is a substitute for a
specification.
```

## `seawall_section`

```python
def seawall_section(design, title: str='Vertical seawall, typical cross-section', sea_extent: float=22.0, land_extent: float=8.0, figsize: tuple[float, float]=(14.5, 8.5), show_scour: bool=True, ax=None) -> Section
```

```text
A standalone figure of a designed seawall, with plot axes.

Returns the :class:`~pyCoastal.drafting.Section` still open, so you can
add project notes before saving.
```

## `seawall_sheet`

```python
def seawall_sheet(design, project: str='Coastal protection works', title: str='Seawall typical cross-section', size: str='A3', sea_extent: float=22.0, land_extent: float=8.0, file: str='seawall_sheet.py', **titleblock) -> Sheet
```

```text
A full drawing sheet of a designed seawall, at a true stated scale.

The view is fitted to a standard scale, the title block records that
scale, and the specification notes are generated from the design. Extra
keyword arguments go to the :class:`~pyCoastal.drafting.TitleBlock`.
```

## `draw_rubble_mound`

```python
def draw_rubble_mound(dwg: Section, design, still_water_level: float, seabed_level: float, cot_land: float | None=None, crest_width: float | None=None, margin: float=12.0, annotate: bool=True, foundation: dict | None=None, crown: dict | None=None, bed='medium_sand', show_foundation: bool=True) -> tuple[tuple, tuple]
```

```text
Put a designed rubble mound into an open :class:`Section`.

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
```

## `fmt`

```python
def fmt(value: float) -> str
```

```text
Signed level, the way a drawing writes one.
```

## `rubble_mound_notes`

```python
def rubble_mound_notes(design, still_water_level, seabed_level, cot_land=None, crest_width=None, foundation=None, crown=None) -> list[str]
```

```text
Specification notes generated from a rubble-mound design.
```

## `rubble_mound_section`

```python
def rubble_mound_section(design, still_water_level: float, seabed_level: float, cot_land: float | None=None, crest_width: float | None=None, title: str='Rubble-mound breakwater, typical cross-section', figsize: tuple[float, float]=(14.5, 8.0), margin: float=12.0, ax=None) -> Section
```

```text
A standalone figure of a designed rubble mound, with plot axes.

Notes
-----
The underlayer follows the Rock Manual rule of a tenth of the armour
mass, so Dn50 falls by 10^(1/3), about 2.15. The layers drawn are the
ones the stability calculation assumes are there; a filter check against
the core grading is a separate exercise.
```

## `rubble_mound_sheet`

```python
def rubble_mound_sheet(design, still_water_level: float, seabed_level: float, cot_land: float | None=None, crest_width: float | None=None, project: str='Harbour protection works', title: str='Breakwater typical sections', size: str='A3', margin: float=12.0, file: str='breakwater_sheet.py', bed='medium_sand', show_head: bool=True, head_kd_ratio: float | None=None, **titleblock) -> Sheet
```

```text
A drawing sheet of a designed rubble mound, trunk and head.

Two sections, as a real set carries them: the trunk, and the roundhead
with the heavier armour its exposure needs. Set ``show_head`` False for
a trunk-only sheet.
```

## `vessel_outline`

```python
def vessel_outline(beam: float, draught: float, freeboard: float, bilge: float=0.18, centre: float=0.0) -> np.ndarray
```

```text
Midship section of a hull, as a closed polygon.

A box with chamfered bilges and a little flare. Enough to read as a ship
at the scale a channel section is drawn at, and deliberately not more:
the hull form is not what the drawing is about.
```

## `draw_channel`

```python
def draw_channel(dwg: Section, design, margin: float=60.0, show_vessel: bool=True, annotate: bool=True, show_depth_chain: bool=True, seabed_extent: float | None=None) -> tuple[tuple, tuple]
```

```text
Put a designed navigation channel into an open :class:`Section`.

Draws the dredged prism, the existing bed, the design vessel at her
static draught, and the underkeel clearance stack as a dimension chain,
so every allowance can be read off the paper.
```

## `channel_notes`

```python
def channel_notes(design) -> list[str]
```

```text
Specification notes generated from a channel design.
```

## `channel_section`

```python
def channel_section(design, title: str='Navigation channel, typical cross-section', figsize: tuple[float, float]=(14.5, 8.0), margin: float=60.0, exaggeration: float=8.0, ax=None) -> Section
```

```text
A standalone figure of a designed navigation channel.

Drawn with vertical exaggeration by default. A channel several hundred
metres wide and twenty deep is unreadable at a true scale, which is why
dredging drawings have always been exaggerated; the factor is stated on
the drawing rather than left for the reader to infer.
```

## `channel_sheet`

```python
def channel_sheet(design, project: str='Port approach works', title: str='Navigation channel typical section', size: str='A3', margin: float=60.0, exaggeration: float=8.0, file: str='channel_sheet.py', **titleblock) -> Sheet
```

```text
A full drawing sheet of a designed navigation channel.

Vertically exaggerated by default, with the factor stated beside the
detail title and in the notes.
```

## `draw_channel_detail`

```python
def draw_channel_detail(dwg: Section, design, width_in_beams: float=0.35, hull_shown: float=1.3, annotate: bool=True) -> tuple[tuple, tuple]
```

```text
True-scale detail of the keel, the allowances and the dredge level.

The overall channel section has to be exaggerated to be readable, which
stretches the vessel into a tower and makes every slope a lie. This is
the companion view a drawing set always carries: the part that matters,
at a true scale, cropped to the keel, where the underkeel clearance can
be read as a real thickness rather than as a band on a distorted
picture.
```

## `draw_seawall_toe_detail`

```python
def draw_seawall_toe_detail(dwg: Section, design, annotate: bool=True) -> tuple[tuple, tuple]
```

```text
Enlarged detail of the toe, where the section is actually decided.

The typical section shows where everything is. This shows what the toe
is made of: the blinding under the heel, the founding level against the
scour allowance, the rock berm and its geotextile, and the seabed the
whole thing is sitting on. It is the part of a seawall that fails first
and the part a typical section is always too small to explain.
```

## `draw_nourishment`

```python
def draw_nourishment(dwg: Section, result, native, borrow, berm_height: float, closure_depth: float, water_level: float=0.0, annotate: bool=True, landward: float=40.0) -> tuple[tuple, tuple]
```

```text
Put a nourishment cross-section into an open :class:`Section`.

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
```

## `nourishment_notes`

```python
def nourishment_notes(result, native, borrow, berm_height: float, closure_depth: float, design=None) -> list[str]
```

```text
Specification notes generated from a nourishment design.
```

## `nourishment_section`

```python
def nourishment_section(result, native, borrow, berm_height: float, closure_depth: float, water_level: float=0.0, title: str='Beach nourishment, design profile', figsize: tuple[float, float]=(14.0, 7.0), exaggeration: float | None=None, ax=None) -> Section
```

```text
A standalone figure of a nourishment profile.

Vertically exaggerated, because a beach profile is hundreds of metres
long and a few metres deep and at a true scale it is a line. Left to
itself the exaggeration is chosen so the profile fills the sheet, which
is what makes it readable; pass a number to fix it instead.
```

## `nourishment_sheet`

```python
def nourishment_sheet(result, native, borrow, berm_height: float, closure_depth: float, water_level: float=0.0, project: str='Beach management scheme', title: str='Nourishment design profile', size: str='A3', exaggeration: float=6.0, plan_design=None, plan_climate=None, plan_years=None, file: str='nourishment_sheet.py', **titleblock) -> Sheet
```

```text
A drawing sheet of a nourishment profile, with its borrow notes.

Pass ``plan_design`` and ``plan_climate`` to add a second view below the
section: the planform spreading alongshore, from the same
Pelnard-Considere solution the app plots. A fill is designed in two
directions at once, and a sheet that shows only the profile leaves the
reader to imagine how long it stays there.
```

## `plan_margin`

```python
def plan_margin(design, climate, years) -> float
```

```text
How far past the fill a planform has to be drawn, in metres.

Enough to show the sand that has left: 1.4 spreading lengths at the
latest time, and never less than the fill is long. Split out from the
drawing so a sheet can ask for the extents before it commits to a
scale, and trim them to hold a rung of the scale ladder.
```

## `spreading_half_life`

```python
def spreading_half_life(design, climate) -> float
```

```text
Time for the centre of a fill to lose half its width [s].

From the Pelnard-Considere solution: the centre width is
``W erf(a / (2 sqrt(eps t)))``, which is halved when the argument
reaches erfinv(1/2) = 0.476936... It is the natural clock of a fill, and the right basis
for choosing what times to draw: a plan at ten years tells you nothing
about a fill whose half-life is seven months.
```

## `draw_nourishment_plan`

```python
def draw_nourishment_plan(dwg: Section, design, climate, years=(0, 1, 2, 5, 10), annotate: bool=True, samples: int=601, margin: float | None=None) -> tuple[tuple, tuple]
```

```text
Plan view of a fill spreading alongshore, from the analytical solution.

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
```

## `nourishment_plan_section`

```python
def nourishment_plan_section(design, climate, years=None, title: str='Beach nourishment, planform evolution', figsize: tuple[float, float]=(14.0, 6.5), exaggeration: float | None=None, ax=None) -> Section
```

```text
A standalone plan-view figure of a fill spreading alongshore.

Left to themselves the times come from the fill's own half-life, so the
plan always shows the part of the evolution that is worth looking at,
and the cross-shore exaggeration is chosen to fill the sheet and printed
on it.
```

## `REPOSE_ANGLE`

```python
REPOSE_ANGLE = 32.0
```

## `scour_hole_profile`

```python
def scour_hole_profile(scour: float, radius: float, repose: float=REPOSE_ANGLE, samples: int=2)
```

```text
Points tracing one side of the scour hole, from the pier face out.

The hole is drawn as a straight face at the angle of repose, because
that is what a scour hole in sand is: it deepens until the sides stand
at their limiting slope, and then widens. Anything smoother would be an
invention.
```

## `draw_pier_scour`

```python
def draw_pier_scour(dwg: Section, design, annotate: bool=True, protected: bool=False)
```

```text
Section through a pier, either scoured or protected.

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
```

## `pier_scour_notes`

```python
def pier_scour_notes(design) -> list[str]
```

```text
Drawing notes for a pier scour assessment.
```

## `pier_scour_section`

```python
def pier_scour_section(design, title: str='Pier scour, estuary', figsize: tuple[float, float]=(11.0, 7.0), protected: bool=False, exaggeration: float=1.0, ax=None) -> Section
```

```text
A standalone section of the pier and its scour hole.

Drawn true to scale by default. A scour section is one of the few
drawings in coastal work whose horizontal and vertical extents are
comparable, so there is no reason to distort it, and the angle of
repose then reads as the angle it actually is.
```

## `pier_scour_sheet`

```python
def pier_scour_sheet(design, project: str='Estuary crossing', title: str='Pier scour assessment', size: str='A3', show_protection: bool=True, file: str='pier_scour_sheet.py', **titleblock) -> Sheet
```

```text
A drawing sheet of the pier, its scour hole and its protection.
```

## `bridge_bed_profile`

```python
def bridge_bed_profile(design, repose: float=REPOSE_ANGLE)
```

```text
The scoured bed across the whole waterway, left bank to right.

Traces, in order: the untouched bed on the left bank, down the left
abutment hole, up to the contracted bed, down into the pier hole and
back out, then the mirror image. Every face stands at the angle of
repose, because that is the steepest a hole in sand can be.

Returning one polyline rather than three separate holes is deliberate.
The components are computed apart and they are drawn together, and
seeing them in one line is what stops anyone adding the pier hole to
the abutment hole.
```

## `draw_bridge_scour`

```python
def draw_bridge_scour(dwg: Section, design, annotate: bool=True, freeboard: float=2.0)
```

```text
Elevation through a bridge opening, with all three scour components.

Looking downstream: the abutments at each end, the pier between them,
and one bed line carrying the contraction across the whole opening with
the local holes cut into it at the pier and at each abutment toe.

Drawing them on one line is the point. The three components are
computed separately and are often quoted separately, and a reader who
sees them apart will add them. Here it is visible that the deepest
point is one hole at one place, not the sum of three.
```

## `bridge_scour_notes`

```python
def bridge_scour_notes(design) -> list[str]
```

```text
Drawing notes for a bridge scour assessment.
```

## `bridge_scour_section`

```python
def bridge_scour_section(design, title: str='Bridge scour, total', figsize: tuple[float, float]=(13.0, 7.0), exaggeration: float | None=None, ax=None) -> Section
```

```text
A standalone elevation of the crossing and its scour.
```

## `bridge_scour_sheet`

```python
def bridge_scour_sheet(design, project: str='Estuary crossing', title: str='Bridge scour assessment', size: str='A3', file: str='bridge_scour_sheet.py', **titleblock) -> Sheet
```

```text
A drawing sheet of the crossing, its scour and its protection.
```

