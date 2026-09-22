# Open-channel hydraulics and backwater {#sec:river}

*Module:* `pyCoastal.applications.river`. *Example:*
`examples/backwater.py`.

The foundation the fluvial side of a crossing stands on. Everything a bridge
does to a river it does by changing the depth: it squeezes the flow, the
water backs up, and that backwater reaches upstream for a distance nobody
guesses correctly by eye. The module also exists for one number in the
scour chain: the fraction of the discharge that actually goes through a
bridge opening, which is a conveyance calculation, not a guess.

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

away from the control. The depths are chosen and the distances computed,
which is exact for a prismatic channel and never iterates. The integration
stops as the depth approaches normal depth, because it gets there only
asymptotically: a backwater curve has no end, and the extent of backwater
is always a convention. `approach` sets the one used (0.99 of the way to
normal depth by default; 0.95 gives a noticeably shorter and equally
defensible reach), and the notes of the returned `BackwaterResult` say
which. The result carries `distance`, `depth`, `water_surface`,
`bed_level`, `profile`, `reach`, and `depth_at(distance)`.

## Afflux at bridge piers

Yarnell (1934) (@eq:yarnell):

$$ \Delta H = K(K + 5Fr^2 - 0.6)(a + 15a^4)Fr^2\,y, $$ {#eq:yarnell}

with $a$ the fraction of the area blocked by the piers, $Fr$ the downstream
Froude number, and $K$ the pier shape coefficient (`PIER_SHAPE`: 0.9
semicircular nose to 2.5 for a ten-pile trestle). The fourth power on the
blockage is what makes it bite. Yarnell's tests were in a rectangular flume
at blockages up to about 0.4 with the flow class unchanged; where a bridge
chokes the flow to critical, use the HEC-RAS energy or momentum methods.
`yarnell_afflux(channel, discharge, downstream_depth, blockage,
shape="semicircular_nose")` returns the afflux and the upstream depth.

## Flow distribution

`flow_distribution(main, main_depth, slope, floodplains=[(Channel,
depth), ...])` splits the discharge by conveyance (@eq:flow-split),

$$ \frac{Q_i}{Q} = \frac{K_i}{\sum_j K_j}. $$ {#eq:flow-split}

This is the number `scour.BridgeOpening` calls `flow_fraction`. A wooded
floodplain can be half the width of the section and carry a tenth of the
flow; guessing the fraction is the largest assumption in a contraction
scour calculation, and it hides behind the most precise-looking number in
the output.

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

![The backwater profile and the extent convention. Depth, not level, is plotted, because the bed rises 4 m over the reach while the depth changes by 7 cm.](media/backwater.png){#fig:backwater}

In the example the channel is 26% of the section and carries 84% of the
flow, because conveyance goes as the roughness and the hydraulic radius, not
the area. Feeding the computed fraction into `contraction_scour` gives
1.08 m, where assuming all the flow goes through the opening gives 1.81 m.
