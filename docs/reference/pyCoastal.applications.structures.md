# `pyCoastal.applications.structures`

Source: [`pyCoastal/applications/structures.py`](../../pyCoastal/applications/structures.py)

Coastal structure design: armour sizing and wave overtopping.

Aimed at design work rather than illustration, so every relation is named,
its source given, and its validity range stated. Where a formula has a
documented range of application the functions say so in their docstrings;
they do not silently extrapolate on your behalf, but neither do they refuse
to compute, since engineering judgement outside a range is your call.

Sources
-------
Van der Meer (1988), "Rock slopes and gravel beaches under wave attack",
    Delft Hydraulics Publication 396. Rock armour stability.

CIRIA/CUR/CETMEF (2007), The Rock Manual, 2nd ed. Armour layer geometry.

Shore Protection Manual (1984), US Army CERC. Hudson formula.

EurOtop (2018), Manual on wave overtopping of sea defences and related
    structures, 2nd ed. Overtopping discharge and tolerable limits.

Conventions
-----------
Wave heights are spectral significant heights Hm0 at the toe. Slopes are
given as cot(alpha), the horizontal run per unit rise, because that is how
they appear on drawings. Discharges are litres per second per metre of
structure, the unit used in the tolerability tables.

## `G`

```python
G = 9.81
```

## `ROUGHNESS_FACTORS`

```python
ROUGHNESS_FACTORS = {'smooth_concrete': 1.0, 'grass': 1.0, 'asphalt': 1.0, 'rock_one_layer_impermeable': 0.6, 'rock_two_layer_impermeable': 0.55, 'rock_two_layer_permeable': 0.4, 'cubes_one_layer_flat': 0.49, 'cubes_two_layer_random': 0.47, 'antifer': 0.47, 'tetrapod': 0.38, 'accropode': 0.46, 'core_loc': 0.44, 'xbloc': 0.45, 'dolos': 0.43}
```

## `TOLERABLE_DISCHARGE`

```python
TOLERABLE_DISCHARGE = {'pedestrians_unaware': (0.03, 'Unaware pedestrians, narrow walkway, clear view of the sea'), 'pedestrians_aware': (0.1, 'Aware pedestrians, able to see and avoid the hazard'), 'trained_staff': (1.0, 'Trained staff, well shod and protected, wide walkway'), 'buildings_structural': (1.0, 'Structural damage to buildings behind the defence'), 'vehicles_low_speed': (10.0, 'Vehicles at low speed on a road behind the crest'), 'vehicles_moderate_speed': (50.0, 'Driving at moderate speed, overtopping by pulsating flows'), 'embankment_seaward': (50.0, 'Damage to a maintained grass or armoured embankment'), 'harbour_quay_equipment': (0.4, 'Damage to equipment set back 5 to 10 m from the crest')}
```

## `DesignConditions`

```python
class DesignConditions
    Hm0: float
    Tm10: float
    depth: float = 15.0
    storm_duration: float = 6 * 3600.0
```

```text
Wave and water-level conditions at the toe of a structure.

Attributes
----------
Hm0 : float
    Spectral significant wave height at the toe [m].
Tm10 : float
    Spectral period Tm-1,0 = m_-1/m_0 [s]. EurOtop is written around this
    period. If you only have Tp, ``from_peak_period`` converts with the
    standard Tm-1,0 = Tp / 1.1 for a single-peaked spectrum.
depth : float
    Water depth at the toe [m].
storm_duration : float
    Duration of the design storm [s]. Used to count waves for armour
    damage progression.
```

### `DesignConditions.from_peak_period` (classmethod)

```python
DesignConditions.from_peak_period(cls, Hm0: float, Tp: float, **kwargs) -> 'DesignConditions'
```

```text
Build from a peak period, using Tm-1,0 = Tp / 1.1.
```

### `DesignConditions.wave_count` (property)

```python
DesignConditions.wave_count(self) -> float
```

```text
Number of waves in the design storm, N = duration / Tm.

Van der Meer's damage relation saturates near N = 7500, so the count
is capped there; a longer storm does not keep eroding the slope at
the same rate.
```

### `DesignConditions.deep_water_wavelength` (method)

```python
DesignConditions.deep_water_wavelength(self) -> float
```

```text
L0 = g T^2 / (2 pi), using Tm-1,0 [m].
```

### `DesignConditions.wavelength` (method)

```python
DesignConditions.wavelength(self) -> float
```

```text
Local wavelength at the toe from the dispersion relation [m].
```

### `DesignConditions.breaker_parameter` (method)

```python
DesignConditions.breaker_parameter(self, cot_alpha: float) -> float
```

```text
Surf similarity parameter xi_m-1,0 = tan(alpha) / sqrt(Hm0 / L0).
```

## `DAMAGE_LEVELS`

```python
DAMAGE_LEVELS = {'start_of_damage': 2.0, 'intermediate': 5.0, 'failure_1_in_1.5': 8.0, 'failure_1_in_2': 8.0, 'failure_1_in_3': 12.0, 'failure_1_in_4': 17.0}
```

## `rock_armour_vandermeer`

```python
def rock_armour_vandermeer(conditions: DesignConditions, cot_alpha: float, Delta: float=1.585, permeability: float=0.4, damage: float=2.0, safety_factor: float=1.0) -> dict
```

```text
Nominal rock diameter Dn50 from Van der Meer (1988).

Two regimes, selected by the surf similarity parameter against a critical
value ``xi_cr``:

plunging (xi < xi_cr)
    Hs / (Delta Dn50) = 6.2 P^0.18 (S / sqrt(N))^0.2 xi^-0.5
surging (xi >= xi_cr)
    Hs / (Delta Dn50) = 1.0 P^-0.13 (S / sqrt(N))^0.2 sqrt(cot a) xi^P

with xi_cr = (6.2 P^0.31 sqrt(tan a))^(1 / (P + 0.5)).

Parameters
----------
cot_alpha : float
    Slope, horizontal per vertical. Valid range roughly 1.5 to 6.
Delta : float
    Relative buoyant density (rho_s / rho_w - 1). 1.585 corresponds to
    2650 kg/m3 rock in seawater of 1025 kg/m3.
permeability : float
    Notional permeability P (Van der Meer 1988, Figure 8):
    0.1 impermeable core with a filter layer, 0.4 permeable core,
    0.5 homogeneous structure, 0.6 very permeable core.
damage : float
    Damage level S. See ``DAMAGE_LEVELS``. 2 is start of damage and is
    the usual design condition.
safety_factor : float
    Divides the stability coefficients, so values above 1 give larger
    stone. Apply your own code's partial factors here.

Returns
-------
dict
    ``Dn50`` [m], ``M50`` [kg] for 2650 kg/m3 rock, the regime that
    governed, ``xi``, and ``xi_cr``.

Notes
-----
Valid for deep-water conditions at the toe and non-depth-limited waves.
For depth-limited surf, Van der Meer's shallow-water modification or the
Rock Manual's H2% form should be used instead; this function does not
apply it.
```

## `rock_armour_hudson`

```python
def rock_armour_hudson(conditions: DesignConditions, cot_alpha: float, Delta: float=1.585, Kd: float=4.0) -> dict
```

```text
Nominal rock diameter from the Hudson formula (SPM 1984).

Hs / (Delta Dn50) = (Kd cot a)^(1/3) / 1.27, where the 1.27 converts the
SPM's H1/10 basis to a significant wave height.

``Kd`` is the stability coefficient: 4.0 for rough angular rock in two
layers on a trunk with breaking waves, 2.0 for a head. Hudson carries no
dependence on wave period, storm duration, permeability or damage level,
so it is a first estimate. Prefer ``rock_armour_vandermeer`` for design
and use Hudson as a cross-check.
```

## `armour_layer`

```python
def armour_layer(Dn50: float, n_layers: int=2, layer_coefficient: float=1.0, porosity: float=0.37) -> dict
```

```text
Armour layer thickness and stone count (Rock Manual, 2007).

thickness = n * k_delta * Dn50, and the number of stones per unit area is
n * k_delta * (1 - porosity) / Dn50^2.
```

## `overtopping_sloped`

```python
def overtopping_sloped(conditions: DesignConditions, crest_freeboard: float, cot_alpha: float, gamma_f: float=1.0, gamma_beta: float=1.0, gamma_b: float=1.0, gamma_v: float=1.0) -> dict
```

```text
Mean overtopping discharge for a sloping structure (EurOtop 2018).

Takes the lesser of the breaking-wave and non-breaking expressions,

breaking (eq. 5.10)
    q / sqrt(g Hm0^3) = (0.023 / sqrt(tan a)) gamma_b xi
                        exp[-(2.7 Rc / (xi Hm0 gamma_b gamma_f gamma_beta gamma_v))^1.3]
maximum (eq. 5.11)
    q / sqrt(g Hm0^3) = 0.09 exp[-(1.5 Rc / (Hm0 gamma_f gamma_beta))^1.3]

Parameters
----------
crest_freeboard : float
    Rc, crest height above the still water level [m]. Zero or negative
    freeboard is outside these formulae and raises.
gamma_f : float
    Roughness factor, see ``ROUGHNESS_FACTORS``.
gamma_beta : float
    Oblique wave attack factor. 1.0 for normal incidence; use
    ``obliquity_factor``.
gamma_b : float
    Berm factor, 1.0 for no berm.
gamma_v : float
    Wave wall factor, 1.0 for no crest wall.

Returns
-------
dict
    ``q`` in l/s per m, the dimensionless discharge, and which branch
    governed.

Notes
-----
These are mean values. EurOtop reports roughly a factor-of-three scatter
about the mean discharge, so a design check should consider the upper
confidence band, not the mean alone. ``overtopping_with_uncertainty``
returns that band.
```

## `overtopping_vertical`

```python
def overtopping_vertical(conditions: DesignConditions, crest_freeboard: float, gamma_beta: float=1.0) -> dict
```

```text
Mean overtopping for a plain vertical wall, non-impulsive conditions.

EurOtop (2018) eq. 7.1:

    q / sqrt(g Hm0^3) = 0.047 exp[-(2.35 Rc / (Hm0 gamma_beta))^1.3]

Notes
-----
Valid for non-impulsive (pulsating) conditions, roughly when the
impulsiveness parameter h* = 1.35 (h / Hm0) (2 pi h / (g Tm10^2)) exceeds
about 0.23. Impulsive conditions give far larger discharges and need the
separate impulsive formulae, which are not implemented here. The returned
dict reports ``h_star`` and ``impulsive`` so the caller can tell.
```

## `obliquity_factor`

```python
def obliquity_factor(beta_degrees: float, kind: str='overtopping') -> float
```

```text
Oblique wave attack factor gamma_beta (EurOtop 2018, section 5.4.4).

For overtopping of a sloping structure,
gamma_beta = 1 - 0.0063 |beta| for |beta| <= 80 degrees, and the value at
80 degrees beyond that.
```

## `overtopping_with_uncertainty`

```python
def overtopping_with_uncertainty(result: dict, factor: float=3.0) -> dict
```

```text
Bracket a mean discharge with EurOtop's reported scatter.

EurOtop notes roughly a factor of three about the mean for the sloping
formulae. Design against the upper bound, not the mean.
```

## `required_crest_freeboard`

```python
def required_crest_freeboard(conditions: DesignConditions, q_allowable: float, cot_alpha: float, gamma_f: float=1.0, gamma_beta: float=1.0, gamma_b: float=1.0, gamma_v: float=1.0, vertical: bool=False, tolerance: float=0.0001) -> float
```

```text
Crest freeboard Rc that limits mean overtopping to ``q_allowable``.

Inverts the relevant EurOtop expression by bisection, since the two
branches make an analytic inverse awkward. ``q_allowable`` is in l/s per m.
```

## `assess_overtopping`

```python
def assess_overtopping(q: float) -> dict
```

```text
Which uses a given mean discharge is tolerable for.

``q`` is in l/s per m. Returns each limit in ``TOLERABLE_DISCHARGE`` with
whether it is satisfied, sorted from strictest to most permissive.
```

## `BreakwaterDesign`

```python
class BreakwaterDesign
    conditions: DesignConditions
    cot_alpha: float
    Dn50: float
    M50: float
    regime: str
    crest_freeboard: float
    q_mean: float
    q_upper: float
    layer: dict
    armour_type: str
    governing_limit: str | None
    section: str = 'trunk'
    kd_ratio: float | None = None
```

```text
A rubble-mound cross-section sized against a design condition.
```

### `BreakwaterDesign.summary` (method)

```python
BreakwaterDesign.summary(self) -> str
```

```text
A short design report.
```

## `design_rubble_mound`

```python
def design_rubble_mound(conditions: DesignConditions, cot_alpha: float=2.0, armour: str='rock_two_layer_permeable', damage: float=2.0, permeability: float=0.4, Delta: float=1.585, tolerable_use: str='trained_staff', safety_factor: float=1.0, scatter_factor: float=3.0) -> BreakwaterDesign
```

```text
Size armour and crest level for a rubble-mound section.

Sizes the stone with Van der Meer, then sets the crest so that the
*upper* confidence bound on overtopping, not the mean, meets the limit
for ``tolerable_use``. Designing to the mean would be exceeded about half
the time.
```

## `reflection_coefficient`

```python
def reflection_coefficient(cot_alpha: float, surf_similarity: float, permeable: bool=True) -> float
```

```text
Reflection coefficient of a rough slope, Seelig and Ahrens (1981).

    Kr = a xi^2 / (b + xi^2)

with a = 0.6 and b = 6.6 for a permeable rubble mound, and a = 1.0,
b = 5.5 for a smooth impermeable slope. A vertical wall reflects almost
everything; a rubble mound dissipates most of it, which is why the
scour in front of the two is not the same problem.
```

## `toe_scour`

```python
def toe_scour(bed, Hs: float, T: float, depth: float, reflection: float=1.0, coefficient: float=0.4, exponent: float=1.35) -> dict
```

```text
Equilibrium scour depth at the toe of a marine structure [m].

The standing-wave form, as for a vertical wall::

    S / Hs = coefficient * Kr / sinh(k h) ** exponent

Parameters
----------
bed : Sediment or str
    What the bed is made of. This decides whether there is any scour to
    compute: a bed below its threshold of motion in the approach waves
    is in the clear-water regime, where a live-bed relation overstates
    the hole, and a cohesive bed is not governed by this at all.
reflection : float
    Reflection coefficient Kr of the structure. 1.0 for a vertical
    wall, which recovers Xie (1981) exactly; roughly 0.2 to 0.5 for a
    rubble mound, from :func:`reflection_coefficient`.
coefficient : float
    0.4 is Xie's value for fine sand under regular waves at a fully
    reflecting wall, and is the usual design number.
exponent : float
    1.35, from the same work.

Returns
-------
dict
    The ``depth``, the mobility state of the bed, and whether the
    relation is being applied inside the regime it came from.

Notes
-----
Scaling Xie's fully reflecting result by the reflection coefficient is
an engineering assumption, not a calibrated relation: it has the right
limits, going to Xie at a vertical wall and to nothing at a perfect
absorber, and it puts a rubble mound sensibly below a caisson. It is a
screening number. A scheme whose toe design turns on it wants a mobile
bed model or a physical model, and the returned dict says as much
through ``screening_only``.
```

## `breakwater_toe_scour`

```python
def breakwater_toe_scour(design, depth: float, bed='medium_sand', permeable: bool=True) -> dict
```

```text
Toe scour in front of a designed rubble mound.

Takes the reflection from the slope and the surf similarity of the
design condition, so a flatter, rougher, more permeable mound is
correctly predicted to scour its own toe less than a steep one.
```

## `mound_foundation`

```python
def mound_foundation(design, depth: float, bed='medium_sand', permeable: bool=True, bedding_material='coarse_sand', settlement_allowance: float=0.0) -> dict
```

```text
Bedding blanket, toe berm and geotextile under a rubble mound.

A trapezoid of rock does not sit straight on the seabed. Under it goes a
levelling blanket of graded sand and gravel, on a geotextile, carried
well past both toes so the scour hole forms in the apron rather than
under the structure. At the foot of the armour sits a berm of the same
stone as the filter layer, which is what stops the bottom of the
mantle unravelling.

Parameters
----------
design : BreakwaterDesign
    The sized mound.
depth : float
    Water depth at the toe [m].
bed : Sediment or str
    The natural seabed. Decides the scour, and therefore how far the
    blanket has to reach.
bedding_material : Sediment or str
    The blanket itself, normally a well graded sand and gravel.
settlement_allowance : float
    Extra blanket thickness for consolidation of a soft seabed [m].

Returns
-------
dict
    Every dimension the section needs, and the scour result behind it.

Notes
-----
Two rules are doing the work.

The toe berm takes the same stone as the filter layer rather than the
armour. It sits low, where the orbital velocities are much smaller than
at the waterline, and sizing it as armour is expensive without being
safer. This follows normal Italian and Rock Manual practice.

The blanket reaches past the toe by whichever is larger of the computed
scour apron and twice the predicted scour depth, with a floor of three
metres for something a dredger can actually place. Its job is to keep
the edge of the hole away from the toe, so it has to be wider than the
hole is deep.
```

## `crown_wall`

```python
def crown_wall(design, still_water_level: float, deck_width: float=7.5, parapet_width: float=2.0, parapet_height: float | None=None, base_below_crest: float | None=None) -> dict
```

```text
A concrete crown block on the crest, in the usual stepped form.

A parapet on the seaward side to take the run-up, a deck behind it wide
enough to drive a lorry along for maintenance, and a base bedded into
the core below the armour crest.

Returns
-------
dict
    Levels and widths for the block, and its concrete volume per metre
    run at 2400 kg/m3.

Notes
-----
The block is proportioned here, not designed. Sliding and overturning
of a crown wall under wave impact are a separate calculation, and a
real one also has to survive the uplift that gets under it when the
core does not drain fast enough.
```

## `ROUNDHEAD_KD_RATIO`

```python
ROUNDHEAD_KD_RATIO = {'rock': {1.5: 0.95, 2.0: 0.8, 3.0: 0.65}, 'cubes': {1.5: 0.85, 2.0: 0.75, 3.0: 0.6}, 'tetrapod': {1.5: 0.72, 2.0: 0.64, 3.0: 0.5}, 'accropode': {1.5: 0.8, 2.0: 0.75, 3.0: 0.65}, 'dolos': {1.5: 0.65, 2.0: 0.58, 3.0: 0.45}}
```

## `ARMOUR_FAMILY`

```python
ARMOUR_FAMILY = {'rock_one_layer_impermeable': 'rock', 'rock_two_layer_impermeable': 'rock', 'rock_two_layer_permeable': 'rock', 'cubes_one_layer_flat': 'cubes', 'cubes_two_layer_random': 'cubes', 'antifer': 'cubes', 'tetrapod': 'tetrapod', 'accropode': 'accropode', 'core_loc': 'accropode', 'xbloc': 'accropode', 'dolos': 'dolos', 'smooth_concrete': 'rock', 'grass': 'rock', 'asphalt': 'rock'}
```

## `roundhead_kd_ratio`

```python
def roundhead_kd_ratio(armour: str, cot_alpha: float) -> float
```

```text
KD_head / KD_trunk for an armour type on a given slope.

Linear in cot(alpha) between the tabulated slopes, and held flat outside
them rather than extrapolated into values nobody has measured.
```

## `roundhead`

```python
def roundhead(design, kd_ratio: float | None=None, raise_crest: float=0.0) -> 'BreakwaterDesign'
```

```text
The head section of a breakwater, armoured for its exposure.

A roundhead is attacked from a wider range of directions than the trunk,
the armour on a convex surface gets less support from its neighbours,
and the run-down concentrates where the flow turns the corner. Practice
handles all three by using a lower stability coefficient at the head.

Since Hudson makes the nominal diameter go as KD to the power minus a
third, a KD ratio of r gives::

    Dn50_head = Dn50_trunk / r^(1/3)
    M50_head  = M50_trunk  / r

so a ratio of 0.8 means a quarter more stone by mass, which is the step
from sixteen to twenty tonne units that a real scheme ends up with.

Parameters
----------
kd_ratio : float, optional
    KD_head / KD_trunk. Taken from :func:`roundhead_kd_ratio` for the
    design's own armour and slope when not given.
raise_crest : float
    Extra crest freeboard at the head [m]. Heads are often built higher
    than the trunk, because the overtopping there lands on the part of
    the structure people stand on and the navigation light sits on.

Returns
-------
BreakwaterDesign
    The same design with head armour, its layer recomputed, and
    ``section`` set to "head".

Notes
-----
Only the armour is rescaled. The filter follows it, because the layer
is recomputed from the new diameter, but the core grading, the crest
width and the overtopping are left as the trunk's. A real head is also
usually widened to give the plant somewhere to work and the light
somewhere to stand.
```

