# Scour at piers and bridges {#sec:scour}

*Module:* `pyCoastal.applications.scour`. *Examples:*
`examples/pier_scour.py`, `examples/bridge_scour.py`.

In an estuary the scour drivers are out of phase. The tidal current
reverses twice a day, the river current is unidirectional, the wave
condition varies with the wind, and the water depth varies with the tide. A
single load case combining a design current with a design wave requires an
assumption about their co-occurrence. The module evaluates the combined
scour at each phase of the tidal cycle and returns the envelope, the
governing phase and the component depths.

## Pier scour in combined waves and current

**Geometry.** A pier is modeled as a stem (`Pier(diameter,
shape="circular", length=None)`) on a base (`PierBase(width, length, height,
top_level, skew)`). A buried pile cap has no effect until the scour hole
reaches its top level. Once exposed, it presents a greater width than the
stem, which increases the scour depth and exposes a further part of the
base. The two elements are reduced to one effective width by weighting each
over the depth of flow it occupies (@eq:equiv-diameter):

$$ D_e = \frac{D_\mathrm{base}h_\mathrm{base} + D_\mathrm{stem}(h - h_\mathrm{base})}{h}, $$ {#eq:equiv-diameter}

where $h_\mathrm{base}$ is the height of the base above the *scoured* bed.
Each element carries the HEC-18 shape factor $K_1$ (`SHAPE_FACTOR`) and the
alignment factor (@eq:k2)

$$ K_2 = \left(\cos\theta + \frac{L}{a}\sin\theta\right)^{0.65},\qquad L/a \le 12. $$ {#eq:k2}

A base aligned with the ebb is skewed to the flood; the flood skew is taken
as the supplement of the ebb skew.

**Combined waves and current.** Sumer and Fredsoe (2001) (@eq:sumer-fredsoe):

$$ \frac{S}{D} = 1.3\left\{1 - \exp\left[-A(KC - B)\right]\right\},\qquad
A = 0.03 + \tfrac34 U_{cw}^{2.6},\qquad B = 6\exp(-4.7U_{cw}), $$ {#eq:sumer-fredsoe}

with $KC = U_mT/D$ on the *near-bed* orbital velocity and
$U_{cw} = U_c/(U_c + U_m)$. At $U_{cw} = 0$ it is exactly the waves-only
relation (@eq:pile-scour); at $U_{cw} = 1$ the threshold vanishes and
$S/D \to 1.3$ as $KC$ grows.

**The steady-current floor.** $KC$ is defined on the wave orbital velocity.
A strong current with small waves therefore gives a high $U_{cw}$ and a low
$KC$ simultaneously, and @eq:sumer-fredsoe returns a scour ratio approaching
zero. The steady-current case is the $KC \to \infty$ limit of an oscillatory
flow, and a current above the threshold of motion generates a horseshoe
vortex independently of the wave condition. The implementation therefore
limits the ratio from below at the steady-current value when the approach
current alone is live-bed. This limit is an addition to the published
relation and is reported as `current_governs` (`scour_ratio_combined(KC,
Ucw, current_live_bed=...)`; `None` disables it).

**Depth limitation and time scale.** `depth_limitation(depth, diameter)`
applies $\tanh(h/D)$ (Breusers et al. 1977). The factor is 0.995 at
$h/D = 3$ and 0.76 at $h/D = 1$. The skin-friction Shields
parameter under the current uses $u_* = U\kappa/\ln(11h/k_s)$ with
$k_s = 2.5d_{50}$, and the time scale (Sumer, Christiansen and Fredsoe 1992)
is given by @eq:scour-time,

$$ T^* = \frac{1}{2000}\frac{h}{D}\theta^{-2.2},\qquad T = T^*\frac{D^2}{\sqrt{g(s-1)d_{50}^3}},\qquad S(t) = S_\mathrm{eq}\left[1 - e^{-t/T}\right]. $$ {#eq:scour-time}

For a pier of order 2 m width, $T$ is of order 20 hours, against a tidal
half cycle of about 6 hours.

**Feedback.** `equilibrium_scour(pier, base, depth, current, Um, period,
...)` solves the coupling between scour depth and effective diameter by
bisection and returns the *deepest* self-consistent root. A scour hole does
not refill, and the shallow root corresponds to a transient state.

**Protection.** `riprap_size(velocity)` follows HEC-23 guideline 12,
$d_{50} = 0.692(KV)^2/[2g(s-1)]$ with $K = 1.5$ for round-nosed and 1.7 for
rectangular piers, and `scour_protection(pier, base, velocity, scour)` sizes
a falling apron reaching two obstacle widths from the face, at least three
stones thick, with a launch allowance. An apron relocates the scour hole to
its perimeter; it does not remove it.

**The tidal cycle.** `EstuaryConditions(mean_depth, tidal_amplitude,
tidal_current, river_current, Hs, Tp, tidal_period=M2, current_phase=90,
bed="medium_sand", wave_follows_tide=False)` takes positive as ebb. The
river current adds to the tidal current on the ebb and opposes it on the
flood, so the peak combined current occurs on the ebb. `current_phase` sets
the lead of
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

![Pier scour assessment sheet. View A is the predicted scour without protection. View B is the proposed apron on an intact bed. The two states are drawn separately.](media/pier_scour_sheet.png){#fig:pier-sheet}

![Scour through the tidal cycle and against the burial depth of the base.](media/pier_scour_tide.png){#fig:pier-tide}

Two results follow from the phase sweep. **The governing phase differs from
the phase of peak current.** The effective diameter is weighted over the
depth of flow,
so an exposed base contributes more at low water. The governing phase in
this case occurs after peak ebb, at a current of 0.78 m/s against a peak of
1.50 m/s. **The response to burial depth is discontinuous.** With the base
buried deeper than the scour depth of the bare stem, the scour is that of
the stem. With the base 1 m shallower, the feedback of @eq:equiv-diameter
raises the equilibrium scour to approximately twice that depth.

## Total bridge scour

HEC-18 divides total scour at a crossing into contraction scour, local
scour at the pier and abutment scour. On a contracted crossing the pier
component is frequently the smallest of the three. The module implements all
three and evaluates each over the tidal cycle.

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
(1960) (@eq:laursen):

$$ \frac{y_2}{y_1} = \left(\frac{Q_2}{Q_1}\right)^{6/7}\left(\frac{W_1}{W_2}\right)^{k_1}, $$ {#eq:laursen}

with $k_1$ = 0.59, 0.64, or 0.69 as $V_*/w$ is below 0.5, between 0.5 and 2,
or above 2 (`transport_exponent`). Clear water (HEC-18 eq. 6.4) (@eq:clear-water):

$$ y_2 = \left[\frac{0.025\,Q_2^2}{D_m^{2/3}W_2^2}\right]^{3/7}. $$ {#eq:clear-water}

The live-bed relation is a sediment balance: faster water carries more but
delivers more, and the two cancel, leaving the width ratio. The two
relations were fitted separately and do not meet at the threshold;
`contraction_scour(..., regime="live" | "clear")` computes either on
demand so the step can be seen.

**Abutment scour.** Froehlich (1989) for $L'/y < 25$ and HIRE for longer
abutments (@eq:abutment):

$$ \frac{y_s}{y_a} = 2.27K_1K_2\left(\frac{L'}{y_a}\right)^{0.43}Fr^{0.61} + 1,\qquad
\frac{y_s}{y_a} = 4Fr^{0.33}\frac{K_1}{0.55}K_2, $$ {#eq:abutment}

with $K_1$ from `ABUTMENT_SHAPE` (1.0 vertical, 0.82 wing wall, 0.55 spill
through). The `+1` in Froehlich is a factor of safety HEC-18 added, not
physics, and it is often more than half the answer; it is reported as
`safety_margin`. These are the fourth-edition HEC-18 relations, the edition
the pier scour also comes from.

**Sequential evaluation.** `bridge_scour_state` computes the components in
the order the flow encounters them. Contraction scour is computed from the
approach flow. Local scour at the pier is then computed from the flow *in
the contracted opening*, which has a higher velocity and a greater depth.
Abutment scour is computed from the approach flow. The components are summed
only where they coexist: contraction plus pier scour at a pier, contraction
plus abutment scour at an abutment. `design_bridge_scour(opening,
conditions, pier, base)` envelopes each component over the cycle and returns
a `BridgeScourDesign` with `contraction`, `pier_local`, `abutment`,
`total_at_pier`, `total_at_abutment`, `component(name)` and notes. A total
exceeding the water depth is reported in the notes and indicates application
of the relations outside their fitted range.

Continuing from the pier above, with the same `estuary`, `pier` and `base`:

```python
from pyCoastal.applications.scour import BridgeOpening, design_bridge_scour

opening = BridgeOpening(approach_width=140, opening_width=80, pier_blockage=5,
                        abutment_length=22, abutment_shape="spill_through")
design = design_bridge_scour(opening, estuary, pier, base)
design.total_at_pier, design.total_at_abutment, design.component("pier")
```

### Worked example: bridge scour

<!-- output: bridge_scour -->

![Bridge scour assessment sheet. The three components are drawn on a single bed line, which gives the deepest point at each location.](media/bridge_scour_sheet.png){#fig:bridge-sheet}

![Scour components through the tidal cycle. The components reach their maxima at different phases and are enveloped separately.](media/bridge_scour_components.png){#fig:bridge-components}

## Limitations

A pile cap at bed level can act as a collar and reduce the scour depth. This
effect is not credited in the computed depth. Cohesive beds are not
supported. Long-term degradation of the reach and channel migration are
outside the scope of the module; HEC-18 adds both to the totals computed
here.
