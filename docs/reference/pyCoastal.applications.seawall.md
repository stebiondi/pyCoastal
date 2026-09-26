# `pyCoastal.applications.seawall`

Source: [`pyCoastal/applications/seawall.py`](../../pyCoastal/applications/seawall.py)

Vertical seawall design: wave pressures, stability, scour and toe protection.

This is the design half of the seawall product. Give it a design condition
and a set of choices, and it returns a fully dimensioned section: crest
level set by overtopping, base width set by sliding, overturning and bearing
in two load cases, stem and base thickness set by bending and shear, toe
level set by scour, and toe stone sized for stability.
:mod:`pyCoastal.applications.sections` turns the result into a drawing and a
bill of quantities.

Sources
-------
Goda, Y. (1974, 2010), Random Seas and Design of Maritime Structures.
    Wave pressure distribution on a vertical wall, the breaker index used to
    cap the design wave, and the extension to impulsive conditions by
    Takahashi et al. (1994).

EurOtop (2018), Manual on wave overtopping of sea defences, 2nd ed.
    Crest level for a tolerable mean discharge.

Xie, S. L. (1981), Scouring patterns in front of vertical breakwaters,
    Delft University of Technology. Scour depth at a vertical wall.

Tanimoto, K., Yagyu, T. and Goda, Y. (1982), Irregular wave tests for
    composite breakwater foundations, Proc. 18th ICCE, with the extension
    by Takahashi (2002). Toe berm stone in front of a vertical wall.

EN 1992-1-1 (2004), Eurocode 2. Bending and shear resistance of the stem.

Conventions
-----------
Levels are metres above chart datum and increase upward, matching the
package's z convention. Distances are metres landward from the seaward face
of the wall unless stated. Forces are kN per metre run of wall.

Stability is computed on a free body of the wall and the fill standing on
its heel, with total unit weights and every water pressure applied
explicitly: on the seaward face, on the virtual back plane through the rear
of the heel, and under the base. Buoyant weights are not used, because they
assume one water level on both sides of the wall, which is exactly the
condition a seawall does not see.

## `G`

```python
G = 9.81
```

## `RHO_W`

```python
RHO_W = 1025.0
```

## `RHO_C`

```python
RHO_C = 2400.0
```

## `RHO_S`

```python
RHO_S = 2650.0
```

## `GAMMA_W`

```python
GAMMA_W = RHO_W * G / 1000.0
```

## `GAMMA_C`

```python
GAMMA_C = RHO_C * G / 1000.0
```

## `F_CK`

```python
F_CK = 35.0
```

## `F_YK`

```python
F_YK = 500.0
```

## `REINFORCEMENT_RATIO`

```python
REINFORCEMENT_RATIO = 0.01
```

## `COVER_TO_STEEL`

```python
COVER_TO_STEEL = 0.1
```

## `ULS_FACTOR`

```python
ULS_FACTOR = 1.35
```

## `L_WALL_PRACTICAL_HEIGHT`

```python
L_WALL_PRACTICAL_HEIGHT = 8.0
```

## `goda_breaking_height`

```python
def goda_breaking_height(T: float, depth: float, slope: float, coefficient: float=0.17) -> float
```

```text
Height of the largest wave a depth can carry, Goda's breaker index.

    Hb = A L0 [1 - exp(-1.5 pi h / L0 (1 + 15 tan^(4/3) theta))]

with L0 = g T^2 / (2 pi) and A = 0.17 (Goda 2010). Used to cap Hmax at
the depth five significant wave heights seaward of the wall, where Goda
sets the breaking point for the design wave.
```

## `goda_pressures`

```python
def goda_pressures(Hm0: float, T: float, depth: float, wall_toe_depth: float, berm_depth: float | None=None, crest_freeboard: float=5.0, beta_degrees: float=0.0, slope: float=1 / 30, Hmax_factor: float=1.8, depth_limit: bool=True) -> dict
```

```text
Goda wave pressures on a vertical wall.

Parameters
----------
Hm0 : float
    Significant wave height at the structure [m].
T : float
    Period used for the pressure distribution [s]. Goda's method is
    written around the significant period; use Tp or T_1/3, not Tm-1,0.
depth : float
    Water depth in front of the structure, seaward of the mound [m].
wall_toe_depth : float
    Depth from the still water level to the underside of the upright
    section, Goda's h' [m].
berm_depth : float, optional
    Depth over the toe berm, Goda's d [m]. Defaults to ``wall_toe_depth``,
    that is, no berm in front of the wall.
crest_freeboard : float
    Crest level above the still water level, Rc [m]. Caps the pressure
    distribution at the crest: a wall lower than the run-up wedge is not
    loaded above its own crest.
beta_degrees : float
    Angle of wave attack from the wall normal [deg].
slope : float
    Seabed slope in front of the structure, used for the depth at five
    wave heights seaward and for the breaker index.
Hmax_factor : float
    Hmax / Hm0 for the design wave. Goda uses 1.8 for non-breaking
    conditions.
depth_limit : bool
    Cap Hmax at the breaking height from :func:`goda_breaking_height`,
    evaluated at the depth h_b five significant wave heights seaward.

Returns
-------
dict
    Pressures p1, p3, p4 and uplift pu [kPa], the elevation of the
    pressure distribution above the still water level ``eta_star`` [m],
    the horizontal force ``F`` and its lever arm ``arm`` about the
    underside of the wall, and the uplift force ``U`` per metre of base
    width.

Notes
-----
These are the pressures in excess of hydrostatic about the still water
level. The still-water pressure on the face and under the base is added
by the caller. This is the standard (non-impulsive) Goda distribution.
Takahashi's impulsive pressure coefficient alpha_I, which governs when a
steep mound throws a breaking wave at the wall, is not applied: check
the mound geometry independently before relying on these numbers for a
wall on a high berm.
```

## `scour_depth_vertical_wall`

```python
def scour_depth_vertical_wall(Hm0: float, T: float, depth: float, coefficient: float=0.4) -> float
```

```text
Equilibrium scour depth at the toe of a vertical wall [m].

Xie (1981), for fine sediment under a standing wave in front of a
reflecting wall::

    S / H = coefficient / sinh(k h) ** 1.35

The scour hole sits a quarter wavelength from the wall, where the
standing-wave node drives the largest near-bed velocity.

Parameters
----------
T : float
    Peak period [s], which sets the standing-wave pattern.
coefficient : float
    0.4 is Xie's value for regular waves on fine sand, and is the usual
    design value. Irregular waves smear the nodal structure and give a
    smaller, wider hole, so a lower coefficient is defensible; coarse
    sediment reduces it further. Set it deliberately rather than
    trusting the default.

Notes
-----
This is the equilibrium depth after a long exposure, not the depth
after one storm. It is a scour *allowance* for setting the founding
level, and does not replace a check that the toe protection stays in
place.
```

## `toe_stone_size`

```python
def toe_stone_size(Hm0: float, toe_depth: float, water_depth: float, Delta: float=1.585, damage: float=0.5) -> dict
```

```text
Toe berm stone size from the Van der Meer toe formula.

    Hs / (Delta Dn50) = (2 + 6.2 (ht/h)^2.7) Nod^0.15

This is the toe of a *sloping* rubble structure. For the berm in front
of a vertical wall use :func:`toe_stone_tanimoto`, which is what
:func:`design_seawall` does.

Parameters
----------
toe_depth : float
    Water depth over the toe berm, ht [m].
water_depth : float
    Water depth at the structure, h [m].
damage : float
    Damage number Nod, stones displaced out of the berm per Dn50 width.
    0.5 is effectively no damage, 2 is acceptable damage, 4 is severe.

Notes
-----
The formula is calibrated for 0.4 < ht/h < 0.9. A toe set very deep or
very shallow relative to the water depth falls outside it, and the
returned dict says so rather than silently extrapolating.
```

## `toe_stone_tanimoto`

```python
def toe_stone_tanimoto(Hs: float, T: float, berm_depth: float, berm_width: float, Delta: float=1.585, beta_degrees: float=0.0, alpha_s: float=0.45) -> dict
```

```text
Stone on the toe berm in front of a vertical wall.

Tanimoto et al. (1982) as extended by Takahashi (2002)::

    Dn50 = Hs / (Delta Ns)
    Ns = max{1.8, 1.3 (1 - kappa) / kappa^(1/3) h'/Hs
                  + 1.8 exp[-1.5 (1 - kappa)^2 / kappa^(1/3) h'/Hs]}
    kappa  = kappa1 kappa2
    kappa1 = (4 pi h'/L') / sinh(4 pi h'/L')
    kappa2 = max{alpha_s sin^2(beta) cos^2(2 pi B/L' cos beta),
                 cos^2(beta) sin^2(2 pi B/L' cos beta)}

Parameters
----------
Hs : float
    Significant wave height at the wall [m].
T : float
    Significant wave period [s]; Tp is a close enough stand-in.
berm_depth : float
    Water depth over the top of the berm armour, h' [m].
berm_width : float
    Width of the berm in front of the wall, B_M [m].
alpha_s : float
    0.45, Takahashi's coefficient for oblique attack.

Notes
-----
Unlike the Van der Meer toe formula this one knows it is in front of a
wall: kappa2 carries the standing-wave velocity at the berm, which is
why the berm width appears.
```

## `sliding_safety`

```python
def sliding_safety(F: float, weight: float, uplift: float, friction: float=0.6) -> float
```

```text
Factor of safety against sliding on the base.

FoS = friction * (W - U) / F, all forces per metre run. 0.6 is the usual
design friction coefficient between concrete and a rubble bedding layer,
and 1.2 the conventional requirement under the design wave. Returns 0
when the uplift exceeds the weight, which is failure by flotation and
not a sliding problem at all.
```

## `overturning_safety`

```python
def overturning_safety(F: float, arm: float, restoring_moment: float, uplift: float, base_width: float) -> float
```

```text
Factor of safety against overturning about the rear heel.

The wave pushes shoreward, so the wall tips about its landward heel.
Goda uplift is triangular with its peak at the seaward edge, putting its
centroid two thirds of the base width from the rear heel.

Parameters
----------
F, arm : float
    Horizontal wave force [kN/m] and its lever arm above the base [m].
restoring_moment : float
    Sum of W_i * (B - x_i) for every weight component, taken about the
    rear heel [kNm/m]. For a single uniform block this is W * B / 2.
```

## `bearing_pressures`

```python
def bearing_pressures(normal: float, base_width: float, net_moment: float) -> dict
```

```text
Base pressure distribution under a gravity wall.

Parameters
----------
normal : float
    Net vertical force on the base, weight less uplift [kN/m].
base_width : float
    Base width B [m].
net_moment : float
    Net moment about one edge of the base, restoring less overturning
    [kNm/m]. Its ratio to the normal force locates the resultant from
    that edge. Either edge works: the distribution is symmetric in the
    eccentricity.

Returns
-------
dict
    ``p_max``, ``p_min`` [kPa], the eccentricity ``e`` from the centre
    of the base, and ``middle_third``, which is False when the
    resultant falls outside the middle third of the base and the heel
    goes into tension. Outside the middle third the no-tension
    distribution is used, so p_max is the triangular peak.
```

## `hydrostatic_force`

```python
def hydrostatic_force(depth: float, unit_weight: float=GAMMA_W) -> dict
```

```text
Hydrostatic force on a vertical face and its lever arm [kN/m, m].

F = 0.5 gamma h^2, acting at h/3 above the bottom of the face.
```

## `stem_section`

```python
def stem_section(moment: float, shear: float, fck: float=F_CK, fyk: float=F_YK, rho: float=REINFORCEMENT_RATIO, cover: float=COVER_TO_STEEL) -> dict
```

```text
Thickness a reinforced concrete cantilever needs for M and V.

Concept design to EN 1992-1-1, per metre width:

bending
    M_Ed <= 0.9 d rho d f_yd, so d_M = sqrt(M_Ed / (0.9 rho f_yd))
shear, no links
    V_Ed <= v_Rd,c d with v_Rd,c = max(0.12 k (100 rho f_ck)^(1/3),
    0.035 k^1.5 f_ck^0.5), k = min(1 + sqrt(200 / d[mm]), 2)

Parameters
----------
moment, shear : float
    Design (factored) values at the critical section [kNm/m, kN/m].
rho : float
    Tension reinforcement ratio. 1 % is a practical ceiling for a wall
    that has to be built and to crack acceptably.

Returns
-------
dict
    Effective depths for bending and shear and the ``thickness`` that
    satisfies both, rounded up to 50 mm.
```

## `SeawallDesign`

```python
class SeawallDesign
    conditions: DesignConditions
    still_water_level: float
    seabed_level: float
    crest_level: float
    crest_freeboard: float
    promenade_level: float
    base_width: float
    stem_thickness: float
    base_thickness: float
    founding_level: float
    embedment: float
    scour_depth: float
    toe_berm_width: float
    toe_berm_thickness: float
    toe_Dn50: float
    toe_M50: float
    toe_stability_number: float
    pressures: dict
    wave_force: float
    wave_arm: float
    weight: float
    uplift: float
    static_uplift: float
    sliding_FoS: float
    overturning_FoS: float
    bearing: dict
    allowable_bearing: float | None
    backfill: Sediment
    retained_height: float
    water_table: float
    back_water_level: float
    surcharge: float
    earth_driving: dict
    earth_resisting: dict
    drawdown: dict
    governing_case: str
    stem: dict
    q_mean: float
    q_upper: float
    governing_limit: str
    impulsive: bool
    iterations: int = 0
    warnings: list[str] = field(default_factory=list)
```

```text
A dimensioned L-shaped gravity seawall.

Levels are metres above chart datum. Distances are metres landward from
the seaward face of the stem, which is the origin of the section.
Everything is per metre run of wall.
```

### `SeawallDesign.wall_height` (property)

```python
SeawallDesign.wall_height(self) -> float
```

```text
Founding level to crest.
```

### `SeawallDesign.heel_width` (property)

```python
SeawallDesign.heel_width(self) -> float
```

```text
Landward projection of the base beyond the stem.
```

### `SeawallDesign.water_depth` (property)

```python
SeawallDesign.water_depth(self) -> float
```

```text
Depth at the wall under the design still water level.
```

### `SeawallDesign.quantities` (method)

```python
SeawallDesign.quantities(self) -> dict
```

```text
Take-off per metre run of wall.

Rock tonnage uses a 0.37 layer porosity, so it is placed tonnage
rather than solid volume times density.
```

### `SeawallDesign.summary` (method)

```python
SeawallDesign.summary(self) -> str
```

```text
A short design report, in the order an engineer checks it.
```

## `design_seawall`

```python
def design_seawall(conditions: DesignConditions, still_water_level: float, seabed_level: float, tolerable_use: str='pedestrians_aware', beta_degrees: float=0.0, friction: float=0.6, target_sliding: float=1.2, target_overturning: float=1.5, require_middle_third: bool=True, allowable_bearing: float | None=300.0, scour_coefficient: float=0.4, minimum_embedment: float=1.0, maximum_embedment: float=3.0, stem_thickness: float=0.5, base_thickness: float=0.6, promenade_freeboard: float=1.0, toe_berm_width: float | None=None, seabed_slope: float=1 / 30, scatter_factor: float=3.0, max_base_width: float=30.0, step: float=0.1, backfill: 'Sediment | str'='medium_sand', water_table: float=0.0, surcharge: float=10.0, earth_pressure_driving: str='at_rest', earth_pressure_resisting: str='active', credit_earth_pressure: bool=True, drawdown_level: float | None=None) -> SeawallDesign
```

```text
Size an L-shaped gravity seawall against a design condition.

The chain is the one a design office follows.

1. Crest level from EurOtop, set so the *upper* bound of the overtopping
   scatter band meets the limit for ``tolerable_use``, not the mean.
2. Founding level from the scour allowance, bracketed by
   ``minimum_embedment`` and ``maximum_embedment``. Deeper embedment is
   a piling question, not a gravity-wall one.
3. Toe stone from Tanimoto's formula for a berm in front of a vertical
   wall, iterated because the berm thickness changes the depth over it.
4. Goda pressures on the wetted face, from the still water level down to
   the seabed, with Hmax capped by Goda's breaker index.
5. Stem and base thickness from the bending and shear at the foot of the
   stem, as a reinforced concrete cantilever. The inputs are minimums.
6. Base width grown in ``step`` increments until both load cases pass
   sliding, overturning, the middle third (if ``require_middle_third``)
   and the ``allowable_bearing`` pressure:

   * wave crest: Goda pressure and uplift plus the still water in
     front, against the active backfill behind;
   * drawdown: the at-rest backfill and its pore water pushing seaward,
     with the sea down at the trough in front.

Every water pressure is applied explicitly: on the face, on the virtual
back plane through the rear of the heel, and under the base, where it
varies linearly from the sea level in front to the water table behind.
Weights are total weights. The backfill water table is never taken
below the still water level, since the sea feeds it.

Parameters
----------
allowable_bearing : float or None
    Allowable base pressure [kPa]. 300 kPa is a presumptive value for a
    medium dense sand bearing stratum and must be replaced by the
    geotechnical designer's figure. None skips the check.
stem_thickness, base_thickness : float
    Minimum thicknesses [m]. Both grow if the stem needs more; the base
    is never thinner than the stem.

Notes
-----
Full Goda uplift is applied under the base even when the base is
embedded, where wave pressure would in reality be attenuated through
the soil. That is deliberately on the safe side. Passive resistance in
front of the embedment and the vertical component of wall friction are
both ignored, also on the safe side.

Returns
-------
SeawallDesign
    Fully dimensioned, with ``summary()`` and ``quantities()``.
```

