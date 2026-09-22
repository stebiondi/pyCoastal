# Vertical seawalls {#sec:seawall}

*Module:* `pyCoastal.applications.seawall`. *Example:*
`examples/seawall_section.py`. *Browser:* Seawall.

The full chain for an L-shaped gravity seawall: crest level from EurOtop,
founding level from scour, Goda wave pressures on the wetted face, earth and
water pressure from the backfill, then the base width grown until sliding,
overturning, and the base pressure all pass under every load case.
`applications.sections` turns the result into a drawing and a bill of
quantities (@sec:drafting).

## Goda pressures

Goda's method (1974, 2010) gives a trapezoidal pressure distribution on the
face of a vertical wall. With the design wave $H_\mathrm{max} = 1.8H_{m0}$,
limited to $\gamma_b d$ in shallow water (`breaker_index=0.78`), the
pressure at the still water level, the elevation of the distribution above
it, and the pressure at the base of the upright are

$$ p_1 = \tfrac12(1 + \cos\beta)(\alpha_1 + \alpha_2\cos^2\beta)\rho g H_\mathrm{max},\qquad
\eta^* = 0.75(1 + \cos\beta)H_\mathrm{max},\qquad p_3 = \alpha_3 p_1, $$ {#eq:goda}

with the pressure at the crest $p_4$ interpolated where the crest is below
$\eta^*$, and a triangular uplift $p_u = \tfrac12(1 + \cos\beta)\alpha_1\alpha_3\rho g H_\mathrm{max}$
at the seaward edge. The coefficients are

$$ \alpha_1 = 0.6 + \frac12\left(\frac{4\pi h/L}{\sinh 4\pi h/L}\right)^2,\quad
\alpha_2 = \min\left[\frac{h_b - d}{3h_b}\left(\frac{H_\mathrm{max}}{d}\right)^2, \frac{2d}{H_\mathrm{max}}\right],\quad
\alpha_3 = 1 - \frac{h'}{h}\left[1 - \frac{1}{\cosh 2\pi h/L}\right], $$

where $h_b$ is the depth five wave heights seaward (from the seabed slope),
$d$ the depth over the berm, and $h'$ the depth to the underside of the
upright. `goda_pressures(Hm0, T, depth, wall_toe_depth, berm_depth=None,
crest_freeboard=5.0, beta_degrees=0.0, slope=1/30, Hmax_factor=1.8,
breaker_index=0.78)` returns the pressures, `eta_star`, the force `F`, its
lever arm, and the uplift. This is the standard non-impulsive distribution;
Takahashi's impulsive coefficient is not applied, so a wall on a high mound
needs a separate check.

## Scour, toe, and stability relations

- `scour_depth_vertical_wall(Hm0, T, depth, coefficient=0.4)`: Xie (1981),
  $S/H = 0.4/\sinh(kh)^{1.35}$, the equilibrium depth a quarter wavelength
  from the wall, used as a scour allowance for the founding level.
- `toe_stone_size(Hm0, toe_depth, water_depth, Delta=1.585, damage=0.5)`:
  Van der Meer's toe formula,
  $H_s/(\Delta D_{n50}) = (2 + 6.2(h_t/h)^{2.7})N_{od}^{0.15}$, calibrated
  for $0.4 < h_t/h < 0.9$ and flagged outside it.
- `sliding_safety(F, weight, uplift, friction=0.6)`:
  $\mathrm{FoS} = \mu(W - U)/F$, zero when uplift exceeds weight
  (flotation).
- `overturning_safety(F, arm, restoring_moment, uplift, base_width)`: about
  the rear heel, with the triangular uplift centroid at two thirds of the
  base width.
- `bearing_pressures(normal, base_width, net_moment)`: $p_\mathrm{max}$,
  $p_\mathrm{min}$, the eccentricity, and `middle_third`; outside the middle
  third the no-tension triangular distribution is used.
- `hydrostatic_force(depth)`: $\tfrac12\gamma h^2$ at $h/3$, for the water
  standing in front of the wall when the trough passes.

## Designing a wall

`design_seawall(conditions, still_water_level, seabed_level,
tolerable_use="pedestrians_aware", ...)` follows the chain a design office
follows:

1. **Crest level** from EurOtop, set so the upper bound of the overtopping
   scatter meets the tolerable limit.
2. **Founding level** from the scour allowance, bracketed by
   `minimum_embedment` and `maximum_embedment` (deeper is a piling question,
   not a gravity-wall one).
3. **Goda pressures** on the wetted face, from the still water level down to
   the seabed.
4. **Earth pressure** from the backfill (`backfill="medium_sand"`,
   `water_table`, `surcharge`, `earth_pressure_driving="at_rest"`), with the
   pore water apart.
5. **Base width** grown in `step` increments until sliding, overturning,
   and, with `require_middle_third`, the bearing check pass under both load
   cases: the wave crest pushing landward, and the trough with the
   saturated backfill pushing seaward against only the water left in front
   (the drawdown case, `drawdown_level`).
6. **Toe stone** from the Van der Meer toe formula, iterated because the
   berm thickness changes the depth over the berm.

Full Goda uplift is applied under the base even when it is embedded, which
is deliberately on the safe side. The result is a `SeawallDesign` with
every level and dimension, the pressures and forces, both load cases,
`governing_case`, the overtopping, `warnings`, `summary()`, and
`quantities()` (concrete, backfill, toe rock, excavation per meter run).

## Worked example

<!-- output: seawall_section -->

Two warnings in this output are the point of the example. Pore water is 66%
of the pressure on the back of the wall, and the drawdown case governs,
not the wave: the wall is sized by the saturated backfill pushing it
seaward at the trough, so the backfill grading and the drainage detail
matter more than the design wave. The toe depth ratio is also just outside
the calibration range of the toe formula, and the output says so.

![The seawall drawing sheet: typical section at a true stated scale, an enlarged toe detail, the design parameter block, and specification notes generated from the design.](media/seawall_sheet.png){#fig:seawall-sheet}

![Standalone seawall section with plot axes, for a report.](media/seawall_section.png){#fig:seawall-section width=85%}
