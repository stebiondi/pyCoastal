# Wave loads on piles {#sec:piles}

*Module:* `pyCoastal.applications.piles`. *Example:*
`examples/pile_wave_loads.py`. *Browser:* Monopile.

The load on a pile is not one number. It is a distribution up the pile that
changes through the wave cycle, and the two things a designer needs from it,
the base shear and the overturning moment at the mudline, peak at different
phases. This module computes the distribution, integrates it, and sweeps the
phase, rather than evaluating a formula at the crest.

## The Morison equation

The Morison equation (Morison et al. 1950) splits the load per unit length
on a slender member into a drag term in phase with the velocity and an
inertia term in phase with the acceleration:

$$ f(z) = \tfrac12\rho C_d D\,u|u| + \rho C_m\frac{\pi D^2}{4}\frac{\partial u}{\partial t}. $$ {#eq:morison}

Slender means $D/L$ below about 0.2; above that the wave diffracts around
the member and the functions warn rather than return a number.

**Kinematics.** `wave_kinematics(H, T, depth, z, phase=0.0,
stretching="wheeler")` gives linear-theory velocity and acceleration.
Linear theory says nothing about the water between the still water level
and the crest, which is exactly where the load is largest, and
extrapolating the $\cosh$ profile there overstates the velocity badly.
Wheeler (1970) stretching maps the still-water profile onto the
instantaneous water column and is the default; `"none"` and
`"extrapolate"` are available for comparison.

**Regime and coefficients.** The Keulegan-Carpenter number
$KC = u_\mathrm{max}T/D$ sets which term dominates: below about 3 the load is
almost all inertia, above about 20 drag governs. `drag_inertia_coefficients(KC,
rough=True)` returns post-critical values from DNV-RP-C205: $C_d = 1.05$ for
a rough cylinder (any pile with marine growth) and 0.65 for a clean one,
with $C_m$ falling from the potential-flow value of 2.0 as $KC$ rises.
These are concept-design starting values.

**Integration and sweep.** `morison_load_profile` evaluates @eq:morison up
the pile, `integrate_load(z, load, mudline)` integrates the force and the
mudline moment, and `morison_pile_load(diameter, H, T, depth, phase=0.0,
...)` returns a `PileLoad` at one phase. `phase_sweep(diameter, H, T, depth,
phases=181)` sweeps the cycle and reports where each peaks.
`design_monopile(diameter, H, T, depth, rough=True, stretching="wheeler",
phases=181, bed=None)` returns the worst-phase load, the scour, and the
ratio `crest_underestimate` by which a crest-phase evaluation would
understate the moment.

## Scour at a pile

Sumer, Fredsoe and Christiansen (1992), for waves:

$$ \frac{S}{D} = 1.3\left[1 - e^{-0.03(KC - 6)}\right]\quad (KC > 6), $$ {#eq:pile-scour}

with no scour below $KC = 6$, where the horseshoe vortex does not form.
Under a steady current $S/D = 1.3$ with a standard deviation of 0.7, which is
the `current_only` branch and the limit of the wave relation.
`scour_depth_pile(diameter, KC, current_only=False, live_bed=True, bed=None,
...)` returns the equilibrium depth; pass a bed to gate it by mobility.

```python
from pyCoastal.applications.piles import design_monopile

result = design_monopile(diameter=8.0, H=12.0, T=13.0, depth=30.0)
result["load"].force / 1e3        # kN, at the worst phase
result["load"].moment / 1e6       # MNm about the mudline
result["load"].inertia_fraction   # share carried by the inertia term
result["crest_underestimate"]     # what a crest-phase check would miss
```

## Worked example

<!-- output: pile_wave_loads -->

A large monopile is inertia dominated, so the load follows the fluid
acceleration, which peaks a quarter cycle before the crest. Evaluating the
load under the crest, because that is where the water is highest,
understates the overturning moment by 62% here. That is what the phase
sweep exists to catch. The diameter table shows the transition from drag to
inertia dominance as the pile grows, and the scour result shows that waves
alone barely scour a pile this large because $KC$ is small; current is what
governs.

![Morison loads on an 8 m monopile: load profiles at the crest and worst phases, and force and moment through the wave cycle.](media/pile_wave_loads.png){#fig:pile-loads}
