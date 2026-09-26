# Vertical seawalls {#sec:seawall}

*Module:* `pyCoastal.applications.seawall`. *Example:*
`examples/seawall_section.py`. *Browser:* Seawall.

The module sizes an L-shaped gravity seawall: crest level from EurOtop,
founding level from the scour allowance, toe stone from Tanimoto, Goda wave
pressures on the wetted face, earth and water pressure from the backfill,
stem and base thickness from the bending and shear at the foot of the stem,
and a base width incremented until sliding, overturning, the middle third
and the allowable bearing pressure are satisfied under each load case.
`applications.sections` converts the result into a drawing and a bill of
quantities (@sec:drafting).

## Goda pressures

Goda's method (1974, 2010) gives a trapezoidal pressure distribution on the
face of a vertical wall. The design wave is $H_\mathrm{max} = 1.8H_{m0}$,
capped at the breaking height of Goda's breaker index at the depth $h_b$
five significant wave heights seaward (`depth_limit=True`,
`goda_breaking_height(T, depth, slope)`):

$$ H_b = 0.17L_0\left\{1 - \exp\left[-1.5\pi\frac{h_b}{L_0}\left(1 + 15\tan^{4/3}\theta\right)\right]\right\},\qquad L_0 = \frac{gT^2}{2\pi}. $$ {#eq:goda-breaker}

The pressure at the still water level, the elevation of the distribution
above it, and the pressure at the base of the upright are given by
@eq:goda:

$$ p_1 = \tfrac12(1 + \cos\beta)(\alpha_1 + \alpha_2\cos^2\beta)\rho g H_\mathrm{max},\qquad
\eta^* = 0.75(1 + \cos\beta)H_\mathrm{max},\qquad p_3 = \alpha_3 p_1, $$ {#eq:goda}

with the pressure at the crest $p_4$ interpolated where the crest is below
$\eta^*$, and a triangular uplift $p_u = \tfrac12(1 + \cos\beta)\alpha_1\alpha_3\rho g H_\mathrm{max}$
at the seaward edge. The coefficients in @eq:goda are given by @eq:seawall-1:

$$ \begin{aligned}
\alpha_1 &= 0.6 + \frac12\left(\frac{4\pi h/L}{\sinh 4\pi h/L}\right)^2,\\
\alpha_2 &= \min\left[\frac{h_b - d}{3h_b}\left(\frac{H_\mathrm{max}}{d}\right)^2, \frac{2d}{H_\mathrm{max}}\right],\\
\alpha_3 &= 1 - \frac{h'}{h}\left[1 - \frac{1}{\cosh 2\pi h/L}\right],
\end{aligned} $$ {#eq:seawall-1}

where $d$ is the depth over the berm and $h'$ the depth to the underside of
the upright. `goda_pressures(Hm0, T, depth, wall_toe_depth, berm_depth=None,
crest_freeboard=5.0, beta_degrees=0.0, slope=1/30, Hmax_factor=1.8,
depth_limit=True)` returns the pressures, `eta_star`, the force `F`, its
lever arm, and the uplift. The pressures are in excess of hydrostatic about
the still water level; the still-water pressure is applied separately in
the stability calculation. This is the standard non-impulsive distribution;
Takahashi's impulsive coefficient is not applied, so a wall on a high mound
needs a separate check.

## Scour, toe, and stability relations

- `scour_depth_vertical_wall(Hm0, T, depth, coefficient=0.4)`: Xie (1981),
  $S/H = 0.4/\sinh(kh)^{1.35}$, the equilibrium depth a quarter wavelength
  from the wall, used as a scour allowance for the founding level.
- `toe_stone_tanimoto(Hs, T, berm_depth, berm_width, Delta=1.585,
  beta_degrees=0.0)`: Tanimoto et al. (1982) with Takahashi (2002), the
  berm in front of a vertical wall (@eq:tanimoto):

  $$ \frac{H_s}{\Delta D_{n50}} = \max\left\{1.8,\ 1.3\frac{1 - \kappa}{\kappa^{1/3}}\frac{h'}{H_s} + 1.8\exp\left[-1.5\frac{(1 - \kappa)^2}{\kappa^{1/3}}\frac{h'}{H_s}\right]\right\}, $$ {#eq:tanimoto}

  with $\kappa = \kappa_1\kappa_2$, $\kappa_1 = (4\pi h'/L')/\sinh(4\pi h'/L')$
  and $\kappa_2 = \max\{0.45\sin^2\beta\cos^2(2\pi B_M\cos\beta/L'),
  \cos^2\beta\sin^2(2\pi B_M\cos\beta/L')\}$, $h'$ the depth over the berm,
  $B_M$ its width and $L'$ the wavelength at $h'$. $\kappa_2$ carries the
  standing-wave velocity at the berm: a narrow berm close to the face sits
  near a velocity node and takes small stone. The design reports when the
  berm does not reach the quarter-wavelength scour zone.
- `toe_stone_size(Hm0, toe_depth, water_depth, Delta=1.585, damage=0.5)`:
  Van der Meer's toe formula for a sloping structure, kept for that use.
- `bearing_pressures(normal, base_width, net_moment)`: $p_\mathrm{max}$,
  $p_\mathrm{min}$, the eccentricity, and `middle_third`; outside the middle
  third the no-tension triangular distribution is used. The moment may be
  taken about either edge.
- `hydrostatic_force(depth)`: $\tfrac12\gamma h^2$ at $h/3$.
- `stem_section(moment, shear)`: the thickness a reinforced concrete
  cantilever needs to EN 1992-1-1 at concept level, per meter width: bending
  $d_M = \sqrt{M_{Ed}/(0.9\rho f_{yd})}$ with $\rho = 1\%$, and shear without
  links $d_V = V_{Ed}/v_{Rd,c}$ with
  $v_{Rd,c} = \max[0.12k(100\rho f_{ck})^{1/3},\ 0.035k^{1.5}f_{ck}^{1/2}]$,
  C35/45 and B500, plus 100 mm to the bar centroid.
- `sliding_safety` and `overturning_safety` remain as general relations for
  a single block under a single water level.

## The free body

Stability is computed on the wall and the fill standing on its heel, with
total unit weights (2400 kg/m$^3$ concrete; the backfill's dry unit weight
above its water table and saturated unit weight below it) and every water
pressure applied explicitly:

- on the seaward face, hydrostatic from the sea level of the load case down
  to the founding level;
- on the virtual back plane through the rear of the heel, the backfill pore
  pressure from its water table, inside the earth pressure of
  `lateral_earth_force`;
- under the base, a linear uplift from the sea-level head at the seaward
  edge to the water-table head at the heel.

Buoyant weights are not used. They imply one water level on both sides of
the wall, and a seawall with a saturated backfill has two. The backfill
water table is never taken below the still water level, since the sea
feeds it.

## Designing a wall

`design_seawall(conditions, still_water_level, seabed_level,
tolerable_use="pedestrians_aware", allowable_bearing=300.0, ...)` follows
the chain a design office follows:

1. **Crest level** from EurOtop, set so the upper bound of the overtopping
   scatter meets the tolerable limit.
2. **Founding level** from the scour allowance, bounded by
   `minimum_embedment` and `maximum_embedment`.
3. **Toe stone** from @eq:tanimoto, iterated: the berm thickness changes the
   depth over the berm and the stone sets the thickness and width.
4. **Goda pressures** on the wetted face, from the still water level down to
   the seabed.
5. **Stem and base thickness** from the characteristic moment and shear at
   the foot of the stem, factored by 1.35. The stem is bent seaward by the
   at-rest backfill at the trough and landward by the wave and the still
   water less the active backfill. `stem_thickness` and `base_thickness`
   are minimums, and the base is never thinner than the stem.
6. **Base width** grown in `step` increments until both load cases pass
   sliding (1.2), overturning (1.5), the middle third and
   `allowable_bearing`:
   - *wave crest*: Goda pressure and uplift plus the still water in front,
     against the active backfill, overturning about the rear heel;
   - *drawdown*: the at-rest backfill and its pore water pushing seaward,
     the sea at the trough ($\mathrm{SWL} - H_{m0}/2$, `drawdown_level`),
     overturning about the seaward toe.

Full Goda uplift is applied under the base including the embedded part, and
passive resistance in front of the embedment is ignored; both are
conservative. The default allowable bearing of 300 kPa is a presumptive
value for a medium dense sand and is replaced by the geotechnical
designer's figure. A retained height above 8 m is reported, since a
cantilever L-wall is normally limited to about that height. The result is a `SeawallDesign`
with every level and dimension, the pressures and forces, both load cases
with their bearing, the `stem` demand, `governing_case`, the overtopping,
`warnings`, `summary()`, and `quantities()`.

## Worked example

<!-- output: seawall_section -->

The drawdown case governs this wall: the base width is set by the saturated
backfill acting seaward at the wave trough, with the resultant close to the
edge of the middle third. Pore water accounts for 64% of the pressure on
the back of the wall, and a drain holding the water table at the still
water level would reduce the total from 548 to 403 kN/m. The retained
height of 8.4 m is at the upper limit for a cantilever L-wall, which is
reflected in the 1.0 m stem. The conditions are impulsive ($h^* = 0.10$),
so the crest and the load both need the impulsive check before the section
is fixed.

![The seawall drawing sheet: typical section at a true stated scale, an enlarged toe detail, the design parameter block, and specification notes generated from the design.](media/seawall_sheet.png){#fig:seawall-sheet}

![Standalone seawall section with plot axes, for a report.](media/seawall_section.png){#fig:seawall-section width=85%}
