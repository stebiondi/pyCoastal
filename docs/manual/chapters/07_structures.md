# Rubble-mound breakwaters {#sec:structures}

*Module:* `pyCoastal.applications.structures`. *Example:*
`examples/breakwater_design.py`. *Browser:* Breakwater.

The module implements armor sizing, wave overtopping and the crown wall.
The sources are Van der Meer (1988) in the form of Van Gent et al. (2003)
for rock, Van der Meer (1988) and the unit design numbers for concrete
armor, Hudson (SPM 1984) as a screening check, the Rock Manual (2007) for
layer geometry, EurOtop (2018) for overtopping and the tolerable discharge
limits, and Pedersen (1996) for the crown wall. Each relation records its source and its
validity range, computes outside that range, and reports the condition.

## The design condition

`DesignConditions(Hm0, Tm10, depth=15.0, storm_duration=6*3600)` carries
the wave and water level at the toe. `DesignConditions.from_peak_period(Hm0,
Tp, ...)` converts with $T_{m-1,0} = T_p/1.1$ for a single-peaked spectrum.
The mean period is $T_m = T_{m-1,0}/1.164$, from $T_p = 1.1\,T_{m-1,0} =
1.28\,T_m$ for a JONSWAP spectrum (Goda 2010). Derived properties are the
wave count $N = t_\mathrm{storm}/T_m$, capped at 7500, the deep and local
wavelengths, and the surf similarity (@eq:structures-1)

$$ \xi_{m-1,0} = \frac{\tan\alpha}{\sqrt{H_{m0}/L_{m-1,0}}},\qquad L_{m-1,0} = \frac{gT_{m-1,0}^2}{2\pi}. $$ {#eq:structures-1}

## Armor stability

**Van der Meer, Van Gent form.** Van der Meer's (1988) coefficients 6.2 and
1.0 belong to the mean period $T_m$. The Rock Manual (2007) adopts the form
of Van Gent et al. (2003), written in $T_{m-1,0}$ and the 2 % wave height,
which is used here. Two regimes are selected by the surf similarity against
a critical value ([@eq:vdm-plunging; @eq:vdm-surging; @eq:structures-2]):

$$ \frac{H_s}{\Delta D_{n50}} = 8.4\,P^{0.18}\left(\frac{S}{\sqrt N}\right)^{0.2}\frac{H_s}{H_{2\%}}\,\xi_{m-1,0}^{-0.5}\qquad (\xi < \xi_{cr},\ \text{plunging}), $$ {#eq:vdm-plunging}

$$ \frac{H_s}{\Delta D_{n50}} = 1.3\,P^{-0.13}\left(\frac{S}{\sqrt N}\right)^{0.2}\frac{H_s}{H_{2\%}}\sqrt{\cot\alpha}\,\xi_{m-1,0}^{P}\qquad (\xi \ge \xi_{cr},\ \text{surging}), $$ {#eq:vdm-surging}

$$ \xi_{cr} = \left(\frac{8.4}{1.3}\,P^{0.31}\sqrt{\tan\alpha}\right)^{1/(P + 0.5)}. $$ {#eq:structures-2}

$H_{2\%}/H_s$ is taken as 1.4, the Rayleigh value (`height_ratio`). On a
shallow foreshore the ratio is lower (Battjes and Groenendijk 2000), so the
default is conservative there.

$\Delta = \rho_s/\rho_w - 1$ (1.585 for 2650 kg/m$^3$ rock in seawater), $P$
is the notional permeability (0.1 impermeable core with a filter, 0.4
permeable core, 0.5 homogeneous, 0.6 very permeable), and $S$ the damage
level (`DAMAGE_LEVELS`: 2 start of damage, the design value; 8 and 12 to 17
failure). `rock_armour_vandermeer(conditions, cot_alpha,
Delta=1.585, permeability=0.4, damage=2.0, safety_factor=1.0)` returns
`Dn50`, `M50`, the governing regime, $\xi$, and $\xi_{cr}$.

**Depth at the toe.** `depth_limit_warnings(conditions)` reports
$H_{m0}/h > 0.6$, a wave the toe depth cannot carry, as an inconsistent
input, and $H_{m0}/h > 0.2$ as a shallow toe where the Rayleigh $H_{2\%}$
overstates the load.

**Concrete armor units.** `concrete_armour(conditions, unit, cot_alpha,
damage=0.5, density=2400)` sizes a unit by its own relation, with
$\Delta = \rho_c/\rho_w - 1$, $N_{od}$ the number of displaced units per
strip one $D_n$ wide (0.5 is the start of damage) and
$s_{om} = H_s/L_{om}$ on the mean period:

- cubes, two layers (Van der Meer 1988):
  $H_s/(\Delta D_n) = (6.7N_{od}^{0.4}/N^{0.3} + 1.0)\,s_{om}^{-0.1}$;
- tetrapods, two layers (Van der Meer 1988):
  $H_s/(\Delta D_n) = (3.75N_{od}^{0.5}/N^{0.25} + 0.85)\,s_{om}^{-0.2}$;
- single-layer units: the design stability number $N_s = 2.7$ for
  Accropode and 2.8 for Core-Loc and Xbloc (CEM Table VI-5-37);
- dolos: Hudson with $K_D = 16$ on $H_s$.

`CONCRETE_UNITS` holds the layer count, layer coefficient, porosity and
reference slope of each unit. `design_rubble_mound` selects the relation
from the `armour` argument, reports the unit mass at the concrete density,
and sets the underlayer at a tenth of the unit mass in rock.

**Hudson (SPM 1984).** $H_s/(\Delta D_{n50}) = (K_D\cot\alpha)^{1/3}/1.27$,
where 1.27 converts the SPM's $H_{1/10}$ basis to $H_s$.
`rock_armour_hudson(conditions, cot_alpha, Delta, Kd=4.0)` provides a
screening estimate. The relation has no dependence on wave period, storm
duration, permeability or damage level.

**Layer geometry (Rock Manual).** `armour_layer(Dn50, n_layers=2,
layer_coefficient=1.0, porosity=0.37)` returns the layer thickness
$t = n k_t D_{n50}$ and the number of stones per square meter.

## Overtopping

For a sloping structure, EurOtop (2018) takes the lesser of the breaking
and the maximum expressions ([@eq:eurotop-breaking; @eq:eurotop-max]):

$$ \frac{q}{\sqrt{gH_{m0}^3}} = \frac{0.023}{\sqrt{\tan\alpha}}\gamma_b\xi\exp\left[-\left(2.7\frac{R_c}{\xi H_{m0}\gamma_b\gamma_f\gamma_\beta\gamma_v}\right)^{1.3}\right], $$ {#eq:eurotop-breaking}

$$ \frac{q}{\sqrt{gH_{m0}^3}} = 0.09\exp\left[-\left(1.5\frac{R_c}{H_{m0}\gamma_f\gamma_\beta}\right)^{1.3}\right]. $$ {#eq:eurotop-max}

For a plain vertical wall in non-impulsive conditions (EurOtop eq. 7.1) (@eq:eurotop-vertical):

$$ \frac{q}{\sqrt{gH_{m0}^3}} = 0.047\exp\left[-\left(2.35\frac{R_c}{H_{m0}\gamma_\beta}\right)^{1.3}\right], $$ {#eq:eurotop-vertical}

valid when the impulsiveness parameter
$h_* = 1.35\,(h/H_{m0})(2\pi h/gT_{m-1,0}^2)$ exceeds about 0.23;
`overtopping_vertical` reports `h_star` and `impulsive`.

The factors are roughness $\gamma_f$ (`ROUGHNESS_FACTORS`: 1.0 for smooth
concrete, 0.55 and 0.40 for impermeable and permeable two-layer rock, 0.38
to 0.49 for concrete units), obliquity $\gamma_\beta$
(`obliquity_factor(beta_degrees)`), berm $\gamma_b$, and wave wall
$\gamma_v$. EurOtop reports roughly a factor-of-three scatter about the mean
discharge; `overtopping_with_uncertainty(result, factor=3.0)` returns the
band, and `required_crest_freeboard(conditions, q_allowable, cot_alpha,
...)` inverts the relation by bisection. `assess_overtopping(q)` lists which
uses a discharge is tolerable for (@tbl:tolerable).

: Tolerable mean discharges $q$ in l/s/m (`TOLERABLE_DISCHARGE`, EurOtop 2018). {#tbl:tolerable}

| Key | $q$ | Use |
|-------------------------------|----|-----------------------------------------------------------------|
| `pedestrians_unaware` | 0.03 | unaware pedestrians, narrow walkway, sea in view |
| `pedestrians_aware` | 0.1 | aware pedestrians, able to see and avoid the hazard |
| `harbour_quay_equipment` | 0.4 | equipment set back 5 to 10 m from the crest |
| `trained_staff` | 1 | trained staff, well shod and protected, wide walkway |
| `buildings_structural` | 1 | structural damage to buildings behind the defense |
| `vehicles_low_speed` | 10 | vehicles at low speed on a road behind the crest |
| `vehicles_moderate_speed` | 50 | driving at moderate speed, pulsating overtopping |
| `embankment_seaward` | 50 | damage to a maintained grass or armored embankment |

## Designing a section

`design_rubble_mound(conditions, cot_alpha=2.0,
armour="rock_two_layer_permeable", damage=2.0, permeability=0.4,
Delta=1.585, tolerable_use="trained_staff", safety_factor=1.0,
scatter_factor=3.0)` sizes the stone with Van der Meer and sets the crest so
that the **upper** confidence bound on overtopping meets the limit. The
mean discharge is exceeded in approximately half of the realizations and is
not used for the crest level. The function returns a `BreakwaterDesign`
with `Dn50`, `M50`, `regime`,
`crest_freeboard`, `q_mean`, `q_upper`, `layer`, `governing_limit`,
`section`, and `summary()`.

The rest of the section is built from the design:

- **Toe scour.** `reflection_coefficient(cot_alpha, xi, permeable=True)`
  (Seelig and Ahrens 1981, $K_r = a\xi^2/(b + \xi^2)$ with $a = 0.6$,
  $b = 6.6$ for rubble) and `toe_scour(bed, Hs, T, depth, reflection)`,
  which scales Xie's standing-wave result by $K_r$:
  $S/H_s = 0.4\,K_r/\sinh(kh)^{1.35}$. The scaling is an assumption with the
  correct limits at $K_r = 1$ and $K_r = 0$, and the result carries the flag
  `screening_only`.
  `breakwater_toe_scour(design, depth, bed)` applies it to a design, gated
  by `bed_mobility`.
- **Foundation.** `mound_foundation(design, depth, bed="medium_sand",
  bedding_material="coarse_sand", settlement_allowance=0.0)` returns the
  bedding blanket on a geotextile, carried past each toe by the larger of the
  scour apron and twice the scour depth, with a minimum of 3 m, and a toe
  berm of filter stone. The berm is sized as filter stone; the near-bed
  orbital velocities at its level are lower than at the waterline.
- **Crown wall.** `crown_wall(design, still_water_level, deck_width=7.5,
  parapet_width=2.0, berm_width=None, ...)` places a stepped concrete crown
  block behind an armor berm ($3D_{n50}$ by default) and loads it with
  Pedersen (1996), as given in CEM Table VI-5-61
  (`pedersen_crown_loads`):
  $F_{h,0.1\%} = 0.21\sqrt{L_{om}/B}\,(1.6p_my_\mathrm{eff} + Ap_mh'/2)$,
  $M_{0.1\%} = 0.55(h' + y_\mathrm{eff})F_{h,0.1\%}$ and
  $p_{b,0.1\%} = Ap_m$, with $p_m = \rho_wg(R_{u,0.1\%} - A_c)$,
  $R_{u,0.1\%} = 1.12H_s\xi_m$ ($\xi_m \le 1.5$) or $1.34H_s\xi_m^{0.55}$,
  $y = (R_{u,0.1\%} - A_c)\sin15^\circ/(\sin\alpha\cos(\alpha - 15^\circ))$
  and $y_\mathrm{eff} = \min(y/2, f_c)$. $A = \min(A_2/A_1, 1)$ is taken
  as 1, its upper bound, and the horizontal force and the uplift are
  combined, which is conservative since they do not peak together. The deck
  is widened until sliding reaches 1.2 and overturning about the rear heel
  1.5. Parameters outside Pedersen's tested range are reported.
- **Roundhead.** A head receives wave attack from a wider range of
  directions, and armor on a convex surface has reduced interlock. Design
  practice applies a lower stability coefficient at the head. With a
  ratio $r = K_{D,\mathrm{head}}/K_{D,\mathrm{trunk}}$ from
  `roundhead_kd_ratio(armour, cot_alpha)` (@tbl:roundhead),
  $D_{n50,\mathrm{head}} = D_{n50,\mathrm{trunk}}/r^{1/3}$ and
  $M_{50,\mathrm{head}} = M_{50,\mathrm{trunk}}/r$. `roundhead(design,
  kd_ratio=None, raise_crest=0.0)` returns the head design.

: Head to trunk stability coefficient ratios (`ROUNDHEAD_KD_RATIO`). {#tbl:roundhead}

| Armor family | slope 1:1.5 | 1:2 | 1:3 |
|--------------|-------------|-----|-----|
| rock | 0.95 | 0.80 | 0.65 |
| cubes | 0.85 | 0.75 | 0.60 |
| tetrapod | 0.72 | 0.64 | 0.50 |
| accropode | 0.80 | 0.75 | 0.65 |
| dolos | 0.65 | 0.58 | 0.45 |

```python
from pyCoastal.applications.structures import (
    DesignConditions, design_rubble_mound, roundhead, mound_foundation,
)

conditions = DesignConditions.from_peak_period(
    Hm0=4.0, Tp=11.0, depth=12.0, storm_duration=6 * 3600,
)
design = design_rubble_mound(conditions, cot_alpha=2.0, tolerable_use="trained_staff")
print(design.summary())
head = roundhead(design)                    # heavier armor at the head
base = mound_foundation(design, depth=12.0, bed="medium_sand")
```

## Worked example

<!-- output: breakwater_design -->

![Breakwater design curves. (a) Nominal stone diameter against slope. (b) Mean overtopping discharge against crest freeboard, with the EurOtop scatter band.](media/breakwater_design.png){#fig:breakwater-design}

![The same design issued as a drawing sheet: trunk and head sections with the armor drawn as individual stones at the computed $D_{n50}$, the bedding blanket, toe berms, crown wall, and generated specification notes.](media/breakwater_sheet.png){#fig:breakwater-sheet}
