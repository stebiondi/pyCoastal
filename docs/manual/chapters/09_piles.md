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

**Kinematics.** A design wave in intermediate or shallow water is
nonlinear: at $H/h = 0.4$ and an Ursell number of 17 the crest stands about
0.65$H$ above the still water level, not 0.5$H$, and the steep front carries
the largest accelerations. The load is computed on a stream function wave
(`theory="stream"`, the default), Fenton's (1988) Fourier solution of the
full nonlinear free-surface problem with no Eulerian mean current.
`StreamFunctionWave(H, T, depth, N=20)` solves for the wave number,
celerity, surface and the $N$ Fourier coefficients by Newton's method, with
the height raised in six steps from a linear start, and its `kinematics(z,
phase)` returns the horizontal velocity and local acceleration up to the
instantaneous surface. A wave that does not converge is at breaking; the
load then falls back to linear theory with a warning.

`wave_kinematics(H, T, depth, z, phase=0.0, stretching="wheeler")` returns
linear-theory kinematics (`theory="linear"`). Linear theory is undefined
between the still water level and the crest; Wheeler (1970) stretching maps
the still-water profile onto the instantaneous water column and is the
default for that case, with `"none"` and `"extrapolate"` for comparison.
For the design wave above, linear theory understates the mudline moment by
about 30 %.

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
`design_monopile(diameter, H, T, depth, rough=True, phases=181, bed=None,
theory="stream", Hs=None, current=0.0)` returns the worst-phase load, the
scour, and the ratio `crest_underestimate` by which a crest-phase evaluation
would understate the moment.

## Scour at a pile

Scour is driven by the sea state and the current; the design wave governs
the load only.
The Keulegan-Carpenter number for scour is taken at the bed from the
significant wave height (`bed_keulegan_carpenter(Hs, T, depth, diameter)`):
$U_m = \pi H_s/(T\sinh kh)$ and $KC = U_mT/D$. It is several times smaller
than the $KC$ at the surface under the design wave, which sets the Morison
coefficients. $H_s$ defaults to $H/1.86$, the Rayleigh ratio for about 1000
waves.

Sumer and Fredsoe (2001), for combined waves and current (@eq:pile-scour):

$$ \frac{S}{D} = 1.3\left\{1 - \exp\left[-A(KC - B)\right]\right\}\quad (KC > B),\qquad A = 0.03 + 0.75U_{cw}^{2.6},\quad B = 6e^{-4.7U_{cw}}, $$ {#eq:pile-scour}

with $U_{cw} = U_c/(U_c + U_m)$ the current share of the near-bed velocity.
$U_{cw} = 0$ recovers the waves-only relation of Sumer, Fredsoe and
Christiansen (1992), with no scour below $KC = 6$, where the horseshoe
vortex does not form. Under a steady current $S/D = 1.3$ with a standard
deviation of 0.7, which is the `current_only` branch and the limit of the
relation. `scour_depth_pile(diameter, KC, current_only=False, live_bed=True,
bed=None, ..., current_ratio=0.0)` returns the equilibrium depth; pass a bed
to gate it by mobility. `design_monopile` takes the depth-averaged
`current` in m/s and reports when none is given, since a tidal current
dominates the scour at most monopile sites.

```python
from pyCoastal.applications.piles import design_monopile

result = design_monopile(diameter=8.0, H=12.0, T=13.0, depth=30.0, current=1.0)
result["load"].force / 1e3        # kN, at the worst phase
result["load"].moment / 1e6       # MNm about the mudline
result["load"].inertia_fraction   # share carried by the inertia term
result["crest_underestimate"]     # what a crest-phase check would miss
```

## Worked example

<!-- output: pile_wave_loads -->

The 8 m monopile is inertia dominated. On the stream function wave the
largest moment, 111.5 MNm, occurs 28 degrees ahead of the crest, on the
steep front of the wave where the acceleration is largest; evaluation at
the crest phase alone understates it by 53 %. `phase_sweep` returns both
phases and the ratio. The diameter table gives the transition from drag to
inertia dominance with increasing diameter. For scour, the bed $KC$ from the
significant wave is 2.3, below the waves-only threshold, so waves alone
give no scour; a 1.0 m/s tidal current ($U_{cw} = 0.42$) gives 1.47 m, and
a steady current alone 10.40 m.

![Morison loads on an 8 m monopile. (a) Load profile at the governing phase. (b) Load profile at the crest phase. (c) Base shear through the wave cycle. (d) Mudline moment through the wave cycle.](media/pile_wave_loads.png){#fig:pile-loads}
