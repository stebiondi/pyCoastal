# Navigation channels {#sec:channel}

*Module:* `pyCoastal.applications.channel`. *Example:*
`examples/navigation_channel.py`. *Browser:* Channel.

How deep and how wide does the approach channel have to be? The answer is a
stack of allowances, each small, each defensible, and together often several
meters. This module builds that stack explicitly so it can be argued over
line by line, which is how a dredging budget actually gets agreed. It
follows the concept-design method of PIANC (2014), Report 121. The width
and lane tables are exposed as editable dictionaries rather than buried,
because the governing edition of the guideline, and the pilots on the day,
decide the numbers on a real scheme; a real channel is confirmed by
simulation.

## The vessel

`Vessel(name, length, beam, draught, block_coefficient=0.75,
length_pp=None)` is the design ship. $L_{pp}$ defaults to $0.96L_{oa}$.
`displaced_volume` is $C_bL_{pp}BT$ and `displacement` is in tonnes at
1025 kg/m$^3$. The same class is used by the berthing module.

## The depth chain

Start at the design water level, subtract the static draught, then in turn
the squat as the ship moves, its vertical response to waves, the net
clearance over the bed, and the tolerances the dredger and the survey cannot
beat. What is left is the dredge level.

**Squat.** ICORELS (1980), as given by PIANC:

$$ S = C_s\frac{\nabla}{L_{pp}^2}\frac{F_{nh}^2}{\sqrt{1 - F_{nh}^2}},\qquad F_{nh} = \frac{V}{\sqrt{gh}}, $$ {#eq:icorels}

with $C_s = 2.4$ for an open or wide channel. It blows up as $F_{nh} \to 1$
and is normally kept to $F_{nh} < 0.7$; the function flags speeds where it is
unusable. Barrass (1979) is the back-of-envelope check,
$S_\mathrm{max} = C_bV_k^2/100$ in open water and $/50$ in a confined
channel, with the speed in knots (`squat_icorels`, `squat_barrass`).

**Wave response.** `wave_response_allowance(Hs, factor=0.5, period=None,
vessel=None)` takes a fraction of $H_s$ as keel motion: about 0.3 for a
long vessel in short head seas up to about 0.7 for a short vessel in long
beam seas. With any swell this is the single largest judgement in the depth
chain. Given the period and vessel, it also reports the ratio of wavelength
to ship length, which governs whether the ship contours or bridges the wave.

**Clearance stack.** `underkeel_clearance(vessel, squat, wave_allowance,
net_clearance=0.6, water_level_allowance=0.0, dredging_tolerance=0.3,
survey_tolerance=0.2, siltation_allowance=0.2, density_allowance=0.0)`
returns each allowance, the gross total below the keel, and the required
depth. Leaving out the dredging and survey tolerances is the most common way
a channel ends up shallower than its drawing.

Because the squat depends on the depth and the depth depends on the squat,
`design_channel` solves the depth by a short fixed-point iteration.

## The width chain

`channel_width(vessel, manoeuvrability="moderate", section="outer",
two_way=False, speed_class="moderate", bank="sloping_channel_edges",
conditions=None)` builds the PIANC width: a basic maneuvering lane
(`MANOEUVRING_LANE`: 1.3, 1.5, 1.8 beams for good, moderate, poor
maneuverability), plus additional widths from `WIDTH_COMPONENTS` for vessel
speed, crosswind, crosscurrent, longitudinal current, waves, aids to
navigation, bottom surface, depth of waterway, and cargo hazard (with
separate outer and inner-channel columns), plus a bank clearance each side
(`BANK_CLEARANCE`), plus a passing distance for two-way traffic
(`PASSING_DISTANCE`). **Components you do not specify are taken at their
most benign class and reported as assumed**, because a silent default is how
a channel ends up too narrow on paper.

## Side slopes, volumes, and turning basins

`dredged_side_slope(bed, factor=2.0)` gives $\cot\beta = f/\tan\phi'$; the
factor of 2 covers both the partial factor on a submerged granular slope and
the overcut and slumping of dredging, landing near 1:2.6 in gravel and 1:3.8
in silt. `turning_basin_diameter(vessel, assisted=True, current=False)`
gives 1.5 $L_{oa}$ with tugs, 2.0 unassisted, plus half a length where a
current runs through.

`design_channel(vessel, speed, design_water_level, Hs=0, Tp=None,
wave_factor=0.5, net_clearance=0.6, ..., bed="medium_sand",
existing_bed=None, **width_kwargs)` returns a `ChannelDesign` with the
`dredge_level`, `required_depth`, the clearance stack, squat and wave
details, `width`, `top_width`, `side_slope`, `dredge_volume(length)`,
`warnings`, and `summary()`.

```python
from pyCoastal.applications.channel import Vessel, design_channel

vessel = Vessel(name="Post-Panamax container ship", length=336, beam=48.2,
                draught=14.5, block_coefficient=0.68)
channel = design_channel(vessel, speed=8.0, design_water_level=1.20,
                         Hs=1.8, Tp=9.0, existing_bed=-11.5, two_way=True,
                         conditions={"crosswind": "moderate", "waves": "moderate"})
channel.dredge_level, channel.width, channel.dredge_volume(1000)
```

## Worked example

<!-- output: navigation_channel -->

The sensitivity table at the end is the lesson: one judgement call, the
fraction of the wave height taken as vertical vessel motion, moves the
dredge level by 0.35 m either way, more than the dredging and survey
tolerances together.

![Navigation channel drawing sheet: the whole channel with a stated vertical exaggeration, and the underkeel clearance at a true scale where the allowances read as real thicknesses.](media/navigation_channel_sheet.png){#fig:channel-sheet}

![The depth chain and its sensitivity to each judgement.](media/channel_depth_chain.png){#fig:channel-chain}
