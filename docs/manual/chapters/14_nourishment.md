# Beach nourishment {#sec:nourishment}

*Module:* `pyCoastal.applications.nourishment`. *Examples:*
`examples/nourishment_design.py`, `examples/nourishment_profile.py`.
*Browser:* Nourishment.

A beach fill is designed in two directions. Alongshore, the fill is a
perturbation to a straight shoreline; it spreads and the placed volume
leaves the project area over time. Cross-shore, the equilibrium profile is
set by the grain size of the fill, which determines the dry beach width
obtained from a given placed volume.

## The planform: how long a fill lasts

Under small wave angles the one-line model (@eq:oneline) reduces to a
diffusion equation. With the CERC transport in the solid-volume SI form this
model needs (@eq:cerc),

$$ Q = K_\mathrm{cerc}H_b^{5/2}\sin 2\alpha,\qquad K_\mathrm{cerc} = \frac{K\sqrt{g/\gamma_b}}{16(s - 1)}, $$ {#eq:cerc}

(`cerc_coefficient(K=0.39, s=2.65, gamma_b=0.78)`; the solver divides by
$1 - p$ itself, so a bulk-volume coefficient would double-count porosity),
linearization gives @eq:diffusivity,

$$ \frac{\partial y}{\partial t} = \varepsilon\frac{\partial^2y}{\partial x^2},\qquad \varepsilon = \frac{2K_\mathrm{cerc}H_b^{5/2}}{(1 - p)(D + B)}, $$ {#eq:diffusivity}

(`longshore_diffusivity`). For an initially rectangular fill of width $W$
and length $L = 2a$, Pelnard-Considere (1956) gives @eq:pelnard,

$$ y(x, t) = \frac{W}{2}\left[\operatorname{erf}\left(\frac{a - x'}{2\sqrt{\varepsilon t}}\right) + \operatorname{erf}\left(\frac{a + x'}{2\sqrt{\varepsilon t}}\right)\right], $$ {#eq:pelnard}

with $x'$ measured from the fill center (`pelnard_considere`). The center
width $W\operatorname{erf}(a/2\sqrt{\varepsilon t})$ halves when the
argument reaches $\operatorname{erf}^{-1}(1/2) = 0.4769$. This defines the
spreading half-life returned by `sections.spreading_half_life`, which sets
the time scale of the planform evolution.

`NourishmentDesign(length=1000, berm_width=30, taper=100, center=None, D=8,
B=2, porosity=0.4)` is the fill: full-width length, shoreline advance at
placement, linear tapers at each end, closure depth $D$, and berm height $B$.
`WaveClimate(Hb=1.0, T=8.0, alpha0=0.0, Kcerc=KCERC_DEFAULT)` drives it; a
zero angle means the fill diffuses symmetrically without migrating.
`simulate_nourishment(design, climate, duration, domain_length=None,
dx=10.0, n_outputs=25, bc="fixed_ends", cfl=0.9)` evolves the tapered
planform with `tools.shoreline` on a domain five times the fill footprint and
returns a `NourishmentResult` with `planforms`, `volume_retained`,
`retained_fraction`, `berm_width`, and `design_life(threshold=0.5)`.
`renourishment_schedule(design, climate, horizon, threshold=0.5)` returns the
interval, the number of renourishments, the placement times, and the total
volume over a planning horizon. The analytical solution verifies the solver
in the test suite.

<!-- output: nourishment_design -->

![Nourishment planform. (a) Shoreline offset alongshore at the output times, against the Pelnard-Considere solution. (b) Volume retained in the project area against time, with the renourishment threshold.](media/nourishment_design.png){#fig:nourishment-design}

## The profile: borrow material and shoreline advance

Dean's equilibrium profile is $h = Ay^{2/3}$ (`equilibrium_profile`), with
the scale parameter tied to the fall velocity (Kriebel, Kraus and Larson
1991) (@eq:dean-A),

$$ A = 0.067\,w^{0.44}\quad (w \text{ in cm/s}), $$ {#eq:dean-A}

so a sediment cannot have one settling velocity for scour and another for
its profile (`dean_scale`; fine sand at 0.19 mm gives 0.094 and medium sand
at 0.38 mm gives 0.141, against Dean's tabulated 0.10 and 0.14).

A fill with scale $A_f$ placed on a native beach with scale $A_n$ pushes the
profile seaward at each depth by
$\Delta(h) = a + (h/A_f)^{3/2} - (h/A_n)^{3/2}$, where $a$ is the shoreline
advance. The active profile is bounded by the closure contour, so the
integration runs over *depth* from the waterline to closure and gives
@eq:fill-volume,

$$ V = Ba + ah_L + 0.4\,h_L^{5/2}\left(A_f^{-3/2} - A_n^{-3/2}\right), $$ {#eq:fill-volume}

where $h_L$ is the closure depth, or the depth at which the profiles
intersect for a fill coarser than the native sand
(`fill_volume_for_advance`). For matched sand the expression reduces to
$V = (B + h_*)a$. Three cases follow. A coarser fill **intersects** the
native profile and yields a larger advance per unit volume. A finer fill is
**non-intersecting**. Below a **critical volume** (`critical_volume`) a
finer fill yields no dry beach: the placed volume is contained in the
flattening of the submerged profile.
`shoreline_advance(A_native, A_fill, volume, berm_height, closure_depth)`
solves for the advance by bisection over the volume, which is monotonic in
the advance, and returns the case. `profile_overfill_factor(native, borrow,
...)` returns the ratio of borrow to native volume for the same advance.
This quantity is distinct from James's (1975) textural overfill ratio. `grain_compatibility(native, borrow)`
compares the phi means and sortings
($\delta = (\phi_b - \phi_n)/\sigma_n$) and gives a verdict; `phi_size` and
`size_from_phi` convert grain sizes.

<!-- output: nourishment_profile -->

![Profiles for borrow sources from very fine sand to fine gravel on a medium sand beach.](media/nourishment_profile.png){#fig:nourishment-profile}

![Borrow material. (a) Dry beach gained against placed volume, by borrow source. (b) Equilibrium profiles of the native beach and of each borrow source.](media/nourishment_borrow.png){#fig:nourishment-borrow}

![Planform spreading alongshore from the analytical solution, at times taken from the fill's own half-life. The cross-shore axis is stretched to fill the sheet and the factor is stated on the drawing.](media/nourishment_plan.png){#fig:nourishment-plan}

![Nourishment drawing sheet with the design profile and the planform on one sheet, each at its own standard scale.](media/nourishment_sheet.png){#fig:nourishment-sheet}

## Limits

The analytical planform is for a rectangular fill with constant diffusivity;
the numerical solver handles tapers but still uses one wave climate. The
profile method assumes both profiles reach equilibrium and ignores
winnowing of fines, which the compatibility check addresses separately.
