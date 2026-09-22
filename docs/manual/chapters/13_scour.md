# Scour at piers and bridges {#sec:scour}

*Module:* `pyCoastal.applications.scour`. *Examples:*
`examples/pier_scour.py`, `examples/bridge_scour.py`.

The hard part of estuarine scour is not any single relation. It is that the
drivers do not peak together and do not even point the same way. The tide
reverses twice a day, the river does not, the waves come and go with the
wind, and the water depth changes under all of it. A calculation done at
"the design current" and "the design wave" without asking whether they can
occur at the same moment is either optimistic or absurd, and it is usually
not obvious which. So this module works a tidal cycle rather than a load
case: it evaluates the scour at every phase and reports the envelope, which
phase governs, and by how much.

## Pier scour in combined waves and current

**Geometry.** A pier is a stem (`Pier(diameter, shape="circular",
length=None)`) on a base (`PierBase(width, length, height, top_level,
skew)`), because that is what piers are, and the base is where the
interesting failure lives. A buried pile cap does nothing until the scour
hole reaches it; then it is exposed, it is wider than the stem, and the
scour deepens because of it, which exposes more of it. The obstacle is
reduced to one width by weighting each element over the depth of flow it
occupies:

$$ D_e = \frac{D_\mathrm{base}h_\mathrm{base} + D_\mathrm{stem}(h - h_\mathrm{base})}{h}, $$ {#eq:equiv-diameter}

where $h_\mathrm{base}$ is how much of the base stands proud of the
*scoured* bed. Each element carries the HEC-18 shape factor $K_1$
(`SHAPE_FACTOR`) and the alignment factor

$$ K_2 = \left(\cos\theta + \frac{L}{a}\sin\theta\right)^{0.65},\qquad L/a \le 12. $$ {#eq:k2}

A base set square to the ebb is skewed to the flood (the flood skew is taken
as the supplement), which is what makes a tidal estuary awkward.

**Combined waves and current.** Sumer and Fredsoe (2001):

$$ \frac{S}{D} = 1.3\left\{1 - \exp\left[-A(KC - B)\right]\right\},\qquad
A = 0.03 + \tfrac34 U_{cw}^{2.6},\qquad B = 6\exp(-4.7U_{cw}), $$ {#eq:sumer-fredsoe}

with $KC = U_mT/D$ on the *near-bed* orbital velocity and
$U_{cw} = U_c/(U_c + U_m)$. At $U_{cw} = 0$ it is exactly the waves-only
relation (@eq:pile-scour); at $U_{cw} = 1$ the threshold vanishes and
$S/D \to 1.3$ as $KC$ grows.

**The steady-current floor.** $KC$ is built on the wave orbital velocity, so
a strong current under small waves has a high $U_{cw}$ and a low $KC$ at the
same time, and the bare formula returns almost no scour: a pier in a
1.5 m/s current would scour less than in still water with a ripple on it. A
steady current is the $KC \to \infty$ limit of an oscillatory flow, not the
$KC \to 0$ one, and a current that moves the bed digs its own horseshoe
vortex. So when the approach current alone is live-bed, the ratio is floored
at the steady-current value. This is an addition to the published relation
and is flagged as `current_governs` (`scour_ratio_combined(KC, Ucw,
current_live_bed=...)`; `None` disables it).

**Depth limitation and time scale.** `depth_limitation(depth, diameter)`
applies $\tanh(h/D)$ (Breusers et al. 1977), worth nothing above
$h/D = 3$ and a quarter below $h/D = 1$. The skin-friction Shields
parameter under the current uses $u_* = U\kappa/\ln(11h/k_s)$ with
$k_s = 2.5d_{50}$, and the time scale (Sumer, Christiansen and Fredsoe 1992)
is

$$ T^* = \frac{1}{2000}\frac{h}{D}\theta^{-2.2},\qquad T = T^*\frac{D^2}{\sqrt{g(s-1)d_{50}^3}},\qquad S(t) = S_\mathrm{eq}\left[1 - e^{-t/T}\right]. $$ {#eq:scour-time}

For a pier a couple of meters across $T$ is typically most of a day, while
the tide reverses every six hours.

**Feedback.** `equilibrium_scour(pier, base, depth, current, Um, period,
...)` solves the coupling between scour and effective diameter for its
*deepest* self-consistent root by bisection, because a scour hole does not
refill and the shallow root is not an outcome the pier can stay at.

**Protection.** `riprap_size(velocity)` follows HEC-23 guideline 12,
$d_{50} = 0.692(KV)^2/[2g(s-1)]$ with $K = 1.5$ for round-nosed and 1.7 for
rectangular piers, and `scour_protection(pier, base, velocity, scour)` sizes
a falling apron reaching two obstacle widths from the face, at least three
stones thick, with a launch allowance: an apron relocates the scour to its
edge rather than removing it.

**The tidal cycle.** `EstuaryConditions(mean_depth, tidal_amplitude,
tidal_current, river_current, Hs, Tp, tidal_period=M2, current_phase=90,
bed="medium_sand", wave_follows_tide=False)` uses positive for ebb: the
river adds to the tide on the ebb and opposes it on the flood, which is why
estuarine scour is usually an ebb problem. `current_phase` sets the lead of
the current over the elevation (90 degrees for a standing tide, 0 for a
progressive one). `design_pier_scour(pier, conditions, base, samples=73,
protection_factor=1.0)` evaluates every phase and returns a
`PierScourDesign` with the `equilibrium` scour (for protection and the
long-term foundation check), the `tidal_limited` scour one half cycle can
cut, `base_exposed`, `undermined`, the `envelope`, and the `protection`.

```python
from pyCoastal.applications.scour import (
    Pier, PierBase, EstuaryConditions, design_pier_scour,
)

pier = Pier(diameter=2.5, shape="circular")
base = PierBase(width=7.0, length=12.0, height=2.5, top_level=-1.5, skew=20.0)
estuary = EstuaryConditions(mean_depth=9.0, tidal_amplitude=2.2,
                            tidal_current=1.1, river_current=0.4,
                            Hs=1.2, Tp=5.5, bed="medium_sand")
design = design_pier_scour(pier, estuary, base)
design.equilibrium, design.tidal_limited, design.undermined, design.protection
```

### Worked example: pier scour

<!-- output: pier_scour -->

![Pier scour assessment sheet. View A is the prediction if nothing is done; view B is the proposed apron on an intact bed. An apron and a fully developed hole cannot share one section, because the apron exists to stop that hole.](media/pier_scour_sheet.png){#fig:pier-sheet}

![Scour through the tidal cycle and against the burial depth of the base.](media/pier_scour_tide.png){#fig:pier-tide}

Two findings fall out of working the cycle. **The worst phase is not peak
current**: once the footing is exposed, a wide base counts for more in
shallow water, so the governing phase here is well after peak ebb, at
0.78 m/s rather than the 1.50 m/s peak. **Burial depth is a cliff**: bury
the base deeper than the bare stem would scour and nothing happens; a meter
shallower and the hole runs away to nearly twice the depth.

## Total bridge scour

Local scour at a pier is the component everyone computes, and on a
contracted crossing it is routinely the smallest of the three. HEC-18 splits
total scour into contraction, local, and abutment scour; all three are here
and all three are worked over the tidal cycle.

**The opening.** `BridgeOpening(approach_width, opening_width,
pier_blockage=0, abutment_length=25, abutment_shape="spill_through",
abutment_skew=90, slope=5e-4, flow_fraction=1.0,
abutment_depth_fraction=0.4)` gives the contraction ratio $W_1/W_2$ with the
piers subtracted from the gross opening. `flow_fraction` is $Q_2/Q_1$, best
computed with `river.flow_distribution` (@sec:river).
`abutment_depth_fraction` sets Froehlich's $y_a$, the depth where the
embankment actually stands; feeding it a mid-channel depth in a deep
estuary returns a hole deeper than the water.

**Contraction scour.** Two modes, switched by the critical velocity
$V_c = 6.19\,y^{1/6}D_{50}^{1/3}$ (HEC-18 eq. 6.1). Live bed, Laursen
(1960):

$$ \frac{y_2}{y_1} = \left(\frac{Q_2}{Q_1}\right)^{6/7}\left(\frac{W_1}{W_2}\right)^{k_1}, $$ {#eq:laursen}

with $k_1$ = 0.59, 0.64, or 0.69 as $V_*/w$ is below 0.5, between 0.5 and 2,
or above 2 (`transport_exponent`). Clear water (HEC-18 eq. 6.4):

$$ y_2 = \left[\frac{0.025\,Q_2^2}{D_m^{2/3}W_2^2}\right]^{3/7}. $$ {#eq:clear-water}

The live-bed relation is a sediment balance: faster water carries more but
delivers more, and the two cancel, leaving the width ratio. The two
relations were fitted separately and do not meet at the threshold;
`contraction_scour(..., regime="live" | "clear")` computes either on
demand so the step can be seen.

**Abutment scour.** Froehlich (1989) for $L'/y < 25$ and HIRE for longer
abutments:

$$ \frac{y_s}{y_a} = 2.27K_1K_2\left(\frac{L'}{y_a}\right)^{0.43}Fr^{0.61} + 1,\qquad
\frac{y_s}{y_a} = 4Fr^{0.33}\frac{K_1}{0.55}K_2, $$ {#eq:abutment}

with $K_1$ from `ABUTMENT_SHAPE` (1.0 vertical, 0.82 wing wall, 0.55 spill
through). The `+1` in Froehlich is a factor of safety HEC-18 added, not
physics, and it is often more than half the answer; it is reported as
`safety_margin`. These are the fourth-edition HEC-18 relations, the edition
the pier scour also comes from.

**Chained, not parallel.** `bridge_scour_state` computes the components in
the order the water meets them: contraction from the approach flow, then
local scour from the flow *in the contracted opening*, which is faster and
deeper, and abutment scour from the approach flow it turns. They are added
only where they coexist: contraction plus pier at a pier, contraction plus
abutment at an abutment. `design_bridge_scour(opening, conditions, pier,
base)` envelopes each component over the cycle and returns a
`BridgeScourDesign` with `contraction`, `pier_local`, `abutment`,
`total_at_pier`, `total_at_abutment`, `component(name)`, and notes. When a
total exceeds the water depth the result says so: that is a signal the
relations have been pushed past their fitted range, not a foundation level.

```python
from pyCoastal.applications.scour import BridgeOpening, design_bridge_scour

opening = BridgeOpening(approach_width=140, opening_width=80, pier_blockage=5,
                        abutment_length=22, abutment_shape="spill_through")
design = design_bridge_scour(opening, estuary, pier, base)
design.total_at_pier, design.total_at_abutment, design.component("pier")
```

### Worked example: bridge scour

<!-- output: bridge_scour -->

![Bridge scour assessment sheet. The three components are drawn on one bed line so that the deepest point reads as one hole at one place, not the sum of three numbers.](media/bridge_scour_sheet.png){#fig:bridge-sheet}

![Scour components through the tidal cycle. They peak at different phases, so each has its own envelope.](media/bridge_scour_components.png){#fig:bridge-components}

## What is not modeled

A pile cap at bed level can act as a collar and reduce scour; crediting it
would be unconservative, so it is not credited. Cohesive beds are refused
rather than guessed at. Long-term degradation of the reach and channel
migration are separate studies that HEC-18 adds to these totals.
