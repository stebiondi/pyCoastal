# Wave loads on piles {#sec:piles}

*Module:* `pyCoastal.applications.piles`. *Example:*
`examples/pile_wave_loads.py`. *Browser:* Monopile.

The wave load on a pile is a distribution along the pile that varies through
the wave cycle. The base shear and the mudline overturning moment reach
their maxima at different phases. The module computes the load
distribution, integrates it, and sweeps the wave phase to locate both
maxima.

## The Morison equation

The Morison equation (Morison et al. 1950) splits the load per unit length
on a slender member into a drag term in phase with the velocity and an
inertia term in phase with the acceleration:

$$ f(z) = \tfrac12\rho C_d D\,u|u| + \rho C_m\frac{\pi D^2}{4}\frac{\partial u}{\partial t}. $$ {#eq:morison}

The slender-member condition is $D/L$ below about 0.2. Above that value the
wave diffracts around the member and the Morison equation does not apply;
the functions report the condition through the returned
`diffraction_ratio` and a warning.

**Kinematics.** `wave_kinematics(H, T, depth, z, phase=0.0,
stretching="wheeler")` returns linear-theory velocity and acceleration.
Linear theory is undefined between the still water level and the crest,
where the load per unit length is largest. Extrapolation of the $\cosh$
profile into that region overestimates the velocity. Wheeler (1970)
stretching maps the still-water profile onto the instantaneous water column
and is the default. The settings `"none"` and `"extrapolate"` are available
for comparison.

**Regime and coefficients.** The Keulegan-Carpenter number
$KC = u_\mathrm{max}T/D$ determines the dominant term: below about 3 the load
is inertia dominated, above about 20 drag dominated.
`drag_inertia_coefficients(KC, rough=True)` returns post-critical values
from DNV-RP-C205: $C_d = 1.05$ for a rough cylinder, which applies to a pile
carrying marine growth, and 0.65 for a clean cylinder. $C_m$ decreases from
the potential-flow value of 2.0 with increasing $KC$. The values are
concept-design defaults; a detailed design takes them from the governing
code for the actual roughness, $KC$ and Reynolds number.

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

The 8 m monopile is inertia dominated. The load follows the fluid
acceleration, which reaches its maximum a quarter cycle ahead of the crest.
Evaluation at the crest phase alone understates the overturning moment by
62% in this case; `phase_sweep` returns both phases and the ratio. The
diameter table gives the transition from drag to inertia dominance with
increasing diameter. At $KC = 6.3$ the wave-induced scour is 0.10 m; the
steady-current value for the same pile is 10.40 m.

![Morison loads on an 8 m monopile: load profiles at the crest and worst phases, and force and moment through the wave cycle.](media/pile_wave_loads.png){#fig:pile-loads}
