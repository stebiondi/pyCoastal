# Open-channel hydraulics and backwater {#sec:river}

*Module:* `pyCoastal.applications.river`. *Example:*
`examples/backwater.py`.

The module provides the open-channel hydraulics of a river crossing. A
bridge contracts the flow, which raises the upstream water level and
produces a backwater profile extending upstream from the structure. The
module also supplies one input to the scour chain: the fraction of the
discharge passing through the bridge opening, computed from conveyance.

## The channel

`Channel(width=30.0, side_slope=2.0, roughness="natural_clean")` is a
trapezoidal prismatic section (zero width is triangular, zero side slope
rectangular). Roughness is a Manning $n$ or a key into `MANNING`: 0.013 and
0.017 for smooth and rough concrete, 0.022 and 0.030 for clean and weedy
earth, 0.028 gravel, 0.035 cobbles, 0.030 and 0.045 for clean and weedy
natural channels, and 0.035, 0.07, 0.10 for pasture, brush, and wooded
floodplains. The section provides `area`, `perimeter`, `top_width`,
`hydraulic_radius`, `velocity`, and the conveyance (@eq:conveyance)

$$ K = \frac{A R^{2/3}}{n},\qquad Q = K\sqrt{S}. $$ {#eq:conveyance}

## Two depths

**Normal depth** is where friction balances the bed slope,
$Q = K(y_n)\sqrt{S_0}$ (`normal_depth`, which raises on a horizontal or
adverse slope, where uniform flow does not exist). **Critical depth** is
where the specific energy $E = y + V^2/2g$ is least and the Froude number is
one, $Q^2T/(gA^3) = 1$ (`critical_depth`), with
$Fr = V/\sqrt{gA/T}$ (`froude_number`), the form that is right for any
section. `classify_slope(channel, discharge, slope)` compares them: mild,
steep, critical, horizontal, or adverse. The classification belongs to the
channel and the discharge together, so the same reach can be mild in flood
and steep at low flow. `profile_type(depth, classification)` names the
profile in Chow's notation: M1 behind a bridge on a mild reach, M2 a
drawdown to a free overfall, S1 behind a structure on a steep reach.

## Gradually varied flow

`gvf_profile(channel, discharge, slope, control_depth, steps=200,
approach=0.99)` integrates the direct step method (@eq:direct-step),

$$ \Delta x = \frac{\Delta E}{S_0 - S_f},\qquad S_f = \left(\frac{Qn}{AR^{2/3}}\right)^2, $$ {#eq:direct-step}

away from the control. Depths are prescribed and distances computed, which
is exact for a prismatic channel and requires no iteration. The profile
approaches normal depth asymptotically, so the integration terminates at a
prescribed fraction of the approach to normal depth. `approach` sets that
fraction, default 0.99; a value of 0.95 returns a shorter reach. The
criterion used is recorded in the notes of the returned `BackwaterResult`,
which also carries `distance`, `depth`, `water_surface`, `bed_level`,
`profile`, `reach` and `depth_at(distance)`.

## Afflux at bridge piers

Yarnell (1934) (@eq:yarnell):

$$ \Delta H = K(K + 5Fr^2 - 0.6)(a + 15a^4)Fr^2\,y, $$ {#eq:yarnell}

with $a$ the fraction of the area blocked by the piers, $Fr$ the downstream
Froude number, and $K$ the pier shape coefficient (`PIER_SHAPE`: 0.9
semicircular nose to 2.5 for a ten-pile trestle). The fourth power on the
blockage gives a strongly nonlinear dependence on pier area. Yarnell's tests
were in a rectangular flume at blockages up to about 0.4 with the flow class
unchanged through the bridge. Where a bridge chokes the flow to critical,
the energy or momentum methods of HEC-RAS apply.
`yarnell_afflux(channel, discharge, downstream_depth, blockage,
shape="semicircular_nose")` returns the afflux and the upstream depth.

## Flow distribution

`flow_distribution(main, main_depth, slope, floodplains=[(Channel,
depth), ...])` splits the discharge by conveyance (@eq:flow-split),

$$ \frac{Q_i}{Q} = \frac{K_i}{\sum_j K_j}. $$ {#eq:flow-split}

The result is the `flow_fraction` input of `scour.BridgeOpening`. Conveyance
depends on the roughness and the hydraulic radius, so a wooded floodplain
occupying half the section width can carry a tenth of the discharge. An
assumed flow fraction propagates directly into the contraction scour
depth.

```python
from pyCoastal.applications.river import (
    Channel, classify_slope, flow_distribution, gvf_profile, yarnell_afflux,
)

channel = Channel(width=30.0, side_slope=2.0, roughness="natural_clean")
plain = Channel(width=120.0, side_slope=3.0, roughness="floodplain_trees")

state = classify_slope(channel, 250.0, 0.0008)      # normal, critical, mild
afflux = yarnell_afflux(channel, 250.0, state["normal"], blockage=0.18)
profile = gvf_profile(channel, 250.0, 0.0008, afflux["upstream_depth"])
profile.profile, profile.reach, profile.depth_at(1500.0)

split = flow_distribution(channel, state["normal"], 0.0008, [(plain, 1.2)])
split["main_fraction"]
```

## Worked example

<!-- output: backwater -->

![Backwater at the crossing. (a) Depth along the reach upstream of the bridge, against normal depth; the plotted variable is depth, since the bed rises 4 m over the reach while the depth changes by 7 cm. (b) Quoted extent of backwater against the termination criterion.](media/backwater.png){#fig:backwater}

In the example the channel occupies 26% of the section width and carries
84% of the discharge. The computed fraction gives a contraction scour of
1.08 m in `contraction_scour`; a flow fraction of 1.0 gives 1.81 m.
