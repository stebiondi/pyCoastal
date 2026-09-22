# Part IV. Drawings and deliverables {.part .unnumbered}

# Drawings, sections, and sheets {#sec:drafting}

*Modules:* `pyCoastal.drafting`, `pyCoastal.applications.sections`,
`pyCoastal.plotting`. Needs the `plots` extra.

A coastal cross-section is not a plot. It is a scaled drawing: the geometry
is in real meters, line weights carry meaning, materials are hatched rather
than colored by value, and every dimension that governs the design is called
out on the paper. `pyCoastal.drafting` gives the small set of primitives that
takes matplotlib from plotting to drafting, and `applications.sections`
turns each design object into a drawing and a take-off.

## Drafting primitives

**`Section(title="", subtitle="", figsize=(13, 7), ax=None, caps=False,
dim_style="arrow", frame=True, exaggeration=1.0)`** is a drawing in real
coordinates ($x$ cross-shore, $z$ elevation), locked to equal aspect so a 1:2
slope looks like a 1:2 slope. Text is sized in points and placed with
offsets in points, so annotation stays readable when the section is rescaled;
only the geometry scales. Its methods are the vocabulary of a drawing
office:

- `material(points, kind, label=None)` fills a closed polygon with a
  material from the library (@tbl:materials);
- `line(points, weight="medium", style="-")` draws construction, ground, or
  hidden lines with the line weights in `WEIGHTS` (thin 0.5, medium 1.0,
  heavy 1.8, extra 2.4);
- `water(x0, x1, level, bed=None, label=None)` fills water between a level
  and the bed, with the level symbol;
- `dim_h(x0, x1, z, text=None, extend_from=None)` and
  `dim_v(z0, z1, x, text=None, side="right")` draw dimension lines with
  extension lines and terminators;
- `level(x, z, text=None, side="left", symbol="level")` draws the levelling
  triangle and elevation callout;
- `slope(apex, cot_alpha, rise, direction="left")` draws the slope
  triangle, labelled $1 : \cot\alpha$;
- `note(xy, text, offset=(40, 30))` places a leader line and note;
- `detail_bubble(label, title, scale="")` places the circled detail marker;
- `notes_block(lines, title="NOTES", numbered=True)` places numbered
  specification notes;
- `table(rows, title="Design parameters")` places the parameter block (a
  drawing that does not carry its design inputs is not a deliverable);
- `scale_bar(length, divisions=4)` and `key(loc="upper left")` add a
  checkered scale bar and a material key;
- `fit_scale(xlim, zlim, scales=None, paper="")` sets the view to a true,
  round drawing scale that fits the extents, and
  `auto_exaggeration(xlim, zlim, cap=200)` stretches the second axis just
  enough to fill the viewport when a true scale is unreadable;
- `finish(xlim=None, zlim=None, grid=True)`, `save(path, dpi=600)`, and
  `to_dxf(path, scale=1.0)`.

: The material library in `pyCoastal.drafting`. {#tbl:materials}

| Key | Drawn as |
|-----|----------|
| `armour`, `secondary`, `underlayer`, `toe` | individual stones at the layer's stone size |
| `core` | quarry run, dotted hatch |
| `concrete`, `reinforced` | mass and reinforced concrete, diagonal and cross hatch, heavy edge |
| `blinding` | blinding layer |
| `rock_fill`, `granular`, `sand` | fills, circle and dot hatches |
| `subgrade` | in-situ seabed, dense diagonal hatch |
| `pavement` | promenade surfacing |
| `water` | water, thin edge |

`Material(name, face, edge, hatch=None, weight="medium", stones=0.0)`
defines a new one, and `use_crisp_style()` sets global matplotlib settings
for legible technical figures.

**`Sheet(titleblock, size="A3", dpi=400, margin=8.0, strip=52.0)`** is a
drawing sheet with a border and a title block strip down the right edge, in
any of `PAPER` (A0 to A4). `viewport(rect)` adds a `Section` view within the
usable area, `set_scale_from(view)` copies a view's fitted scale into the
title block, `save(path)` writes the sheet with no trimming (the border is
the edge), and `to_dxf(path)` exports every view to one DXF.
**`TitleBlock`** holds `project`, `title`, `organisation`, `client`,
`scale`, `date`, `file`, `sheet`, `revision`, `drawn_by`, `checked_by`,
`status`, and a standard disclaimer.

**DXF.** `write_dxf(path, entities, scale=1.0)` writes polylines on named
layers to a minimal DXF R12 file that any CAD package opens.

## Sections for each design

Every structure in `applications.sections` has three entry points, and all
three take a design object rather than loose numbers:

- `draw_*` puts the geometry and annotation into an open `Section` and
  returns the extents it needs;
- `*_section` is a standalone figure with plot axes, for a report or slide;
- `*_sheet` is a full drawing sheet with border, title block, and notes, at
  a true stated scale; extra keyword arguments go to the `TitleBlock`.

: Drawing functions in `pyCoastal.applications.sections`. {#tbl:sections}

| Structure | draw | section | sheet | notes |
|-----------|------|---------|-------|-------|
| Seawall | `draw_seawall`, `draw_seawall_toe_detail` | `seawall_section` | `seawall_sheet` | `seawall_notes` |
| Rubble mound | `draw_rubble_mound` | `rubble_mound_section` | `rubble_mound_sheet` (trunk and head) | `rubble_mound_notes` |
| Channel | `draw_channel`, `draw_channel_detail` | `channel_section` | `channel_sheet` | `channel_notes` |
| Nourishment profile | `draw_nourishment` | `nourishment_section` | `nourishment_sheet` | `nourishment_notes` |
| Nourishment plan | `draw_nourishment_plan` | `nourishment_plan_section` | via `nourishment_sheet(plan_design=...)` | |
| Pier scour | `draw_pier_scour` | `pier_scour_section` | `pier_scour_sheet` | `pier_scour_notes` |
| Bridge scour | `draw_bridge_scour` | `bridge_scour_section` | `bridge_scour_sheet` | `bridge_scour_notes` |

Supporting geometry: `MoundProfile(x_sea, x_land, crest, cot_sea, cot_land)`
describes a trapezoidal mound, with `offset(thickness)` giving the exact
perpendicular offset of a layer (the crest edges move by
$t(\sqrt{1 + \cot^2\alpha} - \cot\alpha)$), `band`, and `area`;
`mound_layer_volumes(profiles, bed)` takes off the layer quantities. The
underlayer follows the Rock Manual rule of a tenth of the armor mass, so its
$D_{n50}$ falls by $10^{1/3} \approx 2.15$. `vessel_outline` draws a midship
section, `scour_hole_profile` a hole whose faces stand at the angle of
repose (`REPOSE_ANGLE = 32` degrees), `bridge_bed_profile` the scoured bed
across the whole waterway as one line, and `plan_margin` and
`spreading_half_life` set the extents and times of a planform.

### Scale and exaggeration

Sections are drawn at a true scale by default, fitted to a round standard
scale that the title block then states. Where a true scale is unreadable, as
for a channel 600 m wide and 20 m deep or a beach profile hundreds of meters
long and a few meters deep, the exaggeration is applied deliberately and
printed on the drawing next to the scale. A drawing set then carries a
second view at true scale where the detail matters: the channel keel and
underkeel allowances, and the seawall toe.

## The drawing sheets

The worked examples of Part III issue these sheets; they are collected here
as the deliverables of the design chain.

![Seawall typical cross-section with toe detail (`seawall_sheet`).](media/seawall_sheet.png){#fig:sheet-seawall}

![Breakwater trunk and head sections (`rubble_mound_sheet`).](media/breakwater_sheet.png){#fig:sheet-breakwater}

![Navigation channel with true-scale keel detail (`channel_sheet`).](media/navigation_channel_sheet.png){#fig:sheet-channel}

![Nourishment design profile and planform (`nourishment_sheet`).](media/nourishment_sheet.png){#fig:sheet-nourishment}

![Pier scour, unprotected and protected (`pier_scour_sheet`).](media/pier_scour_sheet.png){#fig:sheet-pier}

![Bridge scour, all three components on one bed line (`bridge_scour_sheet`).](media/bridge_scour_sheet.png){#fig:sheet-bridge}

The examples also write DXF files of the geometry
(`media/seawall_section.dxf`, `media/breakwater_section.dxf`,
`media/navigation_channel.dxf`), with each material on its own layer.

## Plot helpers

`pyCoastal.plotting` holds the color maps and helpers shared by the
examples: `water_colormap()`, a diverging map for the instantaneous surface
built to look like water; `agitation_colormap()`, a sequential map for wave
height or disturbance coefficient; `surface_norm(snapshots, percentile=99.5)`,
a symmetric color scale centered on still water; `land_overlay(land)`, a
float array that is 1 on structures and NaN on water; and `LAND_COLOR`. For
quantitative fields use `agitation_colormap` or a standard scientific map,
and keep `water_colormap` for reading the wave pattern at a glance.
