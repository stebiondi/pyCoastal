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
    Delft Hydraulics Publication 396. Rock armour stability, and the cube
    and tetrapod formulae.

Van Gent, M. R. A., Smale, A. J. and Kuiper, C. (2003), "Stability of rock
    slopes with shallow foreshores", Proc. Coastal Structures 2003. The
    form of Van der Meer's rock formula written in Tm-1,0 and H2%, as
    adopted by the Rock Manual (2007).

Pedersen, J. (1996), "Experimental study of wave forces and wave overtopping
    on breakwater crown walls", Series Paper 12, Aalborg University, as
    given in the Coastal Engineering Manual (2011), Table VI-5-61. Crown
    wall loads.

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

## `RHO_W`

```python
RHO_W = 1025.0
```

## `RHO_ROCK`

```python
RHO_ROCK = 2650.0
```

## `RHO_CONCRETE`

```python
RHO_CONCRETE = 2400.0
```

## `SPECTRAL_TO_MEAN_PERIOD`

```python
SPECTRAL_TO_MEAN_PERIOD = 1.28 / 1.1
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

### `DesignConditions.mean_period` (property)

```python
DesignConditions.mean_period(self) -> float
```

```text
Mean period Tm [s], from Tm-1,0 for a JONSWAP spectrum.
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

### `DesignConditions.mean_steepness` (method)

```python
DesignConditions.mean_steepness(self) -> float
```

```text
Fictitious steepness s_om = Hm0 / L_om, with L_om from Tm.
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
def rock_armour_vandermeer(conditions: DesignConditions, cot_alpha: float, Delta: float=1.585, permeability: float=0.4, damage: float=2.0, safety_factor: float=1.0, height_ratio: float=1.4) -> dict
```

```text
Nominal rock diameter Dn50, Van der Meer as modified by Van Gent (2003).

The Rock Manual (2007) form, written in the spectral period Tm-1,0 and
the 2 % wave height, which keeps it valid on shallow foreshores:

plunging (xi < xi_cr)
    Hs / (Delta Dn50) = 8.4 P^0.18 (S / sqrt(N))^0.2 (Hs / H2%) xi^-0.5
surging (xi >= xi_cr)
    Hs / (Delta Dn50) = 1.3 P^-0.13 (S / sqrt(N))^0.2 (Hs / H2%)
                        sqrt(cot a) xi^P

with xi = xi_m-1,0 and xi_cr = (8.4 / 1.3 P^0.31 sqrt(tan a))^(1 / (P + 0.5)).
The original 1988 coefficients (6.2 and 1.0) belong to the mean period
Tm, and using them with Tm-1,0 undersizes surging stone.

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
height_ratio : float
    H2% / Hs. 1.4 is the Rayleigh value for deep water. On a shallow
    foreshore the ratio falls (Battjes and Groenendijk 2000), so 1.4
    is conservative there.

Returns
-------
dict
    ``Dn50`` [m], ``M50`` [kg] for 2650 kg/m3 rock, the regime that
    governed, ``xi``, and ``xi_cr``.
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
def armour_layer(Dn50: float, n_layers: int=2, layer_coefficient: float=1.0, porosity: float=0.37, density: float=RHO_ROCK) -> dict
```

```text
Armour layer thickness and unit count (Rock Manual, 2007).

thickness = n * k_delta * Dn50, and the number of units per unit area is
n * k_delta * (1 - porosity) / Dn50^2.
```

## `CONCRETE_UNITS`

```python
CONCRETE_UNITS = {'cubes_two_layer_random': {'formula': 'cubes', 'layers': 2, 'k': 1.1, 'porosity': 0.47, 'cot': 1.5}, 'cubes_one_layer_flat': {'formula': 'cubes', 'layers': 1, 'k': 1.0, 'porosity': 0.3, 'cot': 1.5}, 'antifer': {'formula': 'cubes', 'layers': 2, 'k': 1.1, 'porosity': 0.46, 'cot': 1.5}, 'tetrapod': {'formula': 'tetrapods', 'layers': 2, 'k': 1.04, 'porosity': 0.5, 'cot': 1.5}, 'accropode': {'formula': 'Ns', 'Ns': 2.7, 'layers': 1, 'k': 1.51, 'porosity': 0.52, 'cot': 1.33}, 'core_loc': {'formula': 'Ns', 'Ns': 2.8, 'layers': 1, 'k': 1.51, 'porosity': 0.6, 'cot': 1.33}, 'xbloc': {'formula': 'Ns', 'Ns': 2.8, 'layers': 1, 'k': 1.4, 'porosity': 0.58, 'cot': 1.33}, 'dolos': {'formula': 'hudson', 'KD': 16.0, 'layers': 2, 'k': 0.94, 'porosity': 0.56, 'cot': 2.0}}
```

## `concrete_armour`

```python
def concrete_armour(conditions: DesignConditions, unit: str, cot_alpha: float, damage: float=0.5, density: float=RHO_CONCRETE, safety_factor: float=1.0) -> dict
```

```text
Nominal size of a concrete armour unit.

cubes, two layers (Van der Meer 1988)
    Hs / (Delta Dn) = (6.7 Nod^0.4 / N^0.3 + 1.0) s_om^-0.1
tetrapods, two layers (Van der Meer 1988)
    Hs / (Delta Dn) = (3.75 Nod^0.5 / N^0.25 + 0.85) s_om^-0.2
single-layer interlocking units
    Hs / (Delta Dn) = Ns, the design stability number: 2.7 for
    Accropode, 2.8 for Core-Loc and Xbloc (CEM Table VI-5-37 and the
    suppliers' guidance), which already carries a margin on the
    start-of-damage value.
dolos
    Hudson with KD = 16 on Hs.

Parameters
----------
damage : float
    Nod, units displaced per strip one Dn wide. 0.5 is the start of
    damage and the usual design value.
density : float
    Concrete density [kg/m3].

Notes
-----
The cube and tetrapod formulae were fitted on a 1:1.5 slope and the
single-layer design numbers assume about 3:4. The returned
``slope_note`` says so when the section departs from that.
```

## `layer_for`

```python
def layer_for(armour: str, Dn50: float, density: float) -> dict
```

```text
The armour layer of an armour type, from its unit size.
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
    density: float = RHO_ROCK
    warnings: list[str] = field(default_factory=list)
```

```text
A rubble-mound cross-section sized against a design condition.
```

### `BreakwaterDesign.concrete` (property)

```python
BreakwaterDesign.concrete(self) -> bool
```

```text
True when the armour is a concrete unit rather than rock.
```

### `BreakwaterDesign.underlayer_Dn50` (property)

```python
BreakwaterDesign.underlayer_Dn50(self) -> float
```

```text
Underlayer rock, a tenth of the armour unit mass (Rock Manual).
```

### `BreakwaterDesign.summary` (method)

```python
BreakwaterDesign.summary(self) -> str
```

```text
A short design report.
```

## `depth_limit_warnings`

```python
def depth_limit_warnings(conditions: DesignConditions) -> list[str]
```

```text
Flags for a wave height the toe depth cannot carry or barely can.
```

## `design_rubble_mound`

```python
def design_rubble_mound(conditions: DesignConditions, cot_alpha: float=2.0, armour: str='rock_two_layer_permeable', damage: float=2.0, permeability: float=0.4, Delta: float=1.585, tolerable_use: str='trained_staff', safety_factor: float=1.0, scatter_factor: float=3.0, unit_damage: float=0.5, concrete_density: float=RHO_CONCRETE) -> BreakwaterDesign
```

```text
Size armour and crest level for a rubble-mound section.

Rock is sized with Van der Meer in the Van Gent (2003) form; concrete
units with their own relations (:func:`concrete_armour`). The crest is
set so that the *upper* confidence bound on overtopping, not the mean,
meets the limit for ``tolerable_use``. Designing to the mean would be
exceeded about half the time.

Parameters
----------
damage : float
    Damage level S for rock.
unit_damage : float
    Damage number Nod for concrete units.
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

## `pedersen_crown_loads`

```python
def pedersen_crown_loads(conditions: DesignConditions, cot_alpha: float, armour_freeboard: float, berm_width: float, protected_height: float, unprotected_height: float) -> dict
```

```text
Wave loads on a crown wall behind an armour berm, Pedersen (1996).

As given in the Coastal Engineering Manual, Table VI-5-61::

    F_h,0.1% = 0.21 sqrt(L_om / B) (1.6 p_m y_eff + A p_m / 2 h')
    M_0.1%   = 0.55 (h' + y_eff) F_h,0.1%
    p_b,0.1% = 1.00 A p_m

with p_m = rho_w g (R_u,0.1% - A_c), the run-up
R_u,0.1% = 1.12 Hs xi_m (xi_m <= 1.5) or 1.34 Hs xi_m^0.55, xi_m on the
mean period, the wedge thickness
y = (R_u,0.1% - A_c) / sin(a) * sin(15 deg) / cos(a - 15 deg), and
y_eff = min(y / 2, f_c).

Parameters
----------
armour_freeboard : float
    A_c, armour crest above still water [m].
berm_width : float
    B, width of the armour berm in front of the wall [m].
protected_height : float
    h', height of the wall face below the armour crest [m].
unprotected_height : float
    f_c, height of the wall face above the armour crest [m].

Notes
-----
A = min(A2 / A1, 1) compares the run-up wedge with the berm cross
section; it is taken as 1, its upper bound. The horizontal force and
the uplift do not peak together, so combining them is conservative.
Pedersen's tests cover xi_m 1.1 to 5.2, Hm0/Ac 0.5 to 1.5, Ac/B 1 to
2.6, cot a 1.5 to 3.5 and Hm0/h 0.16 to 0.35; ``outside`` lists the
ranges this section leaves. Norgaard et al. (2013) show the formulae
overpredict in shallow water, so they err on the safe side there.
```

## `crown_wall`

```python
def crown_wall(design, still_water_level: float, deck_width: float=7.5, parapet_width: float=2.0, parapet_height: float | None=None, base_below_crest: float | None=None, berm_width: float | None=None, friction: float=0.6, target_sliding: float=1.2, target_overturning: float=1.5, max_deck_width: float=25.0, step: float=0.25) -> dict
```

```text
A concrete crown block on the crest, checked for stability.

A parapet on the seaward side to take the run-up, a deck behind it wide
enough to drive a lorry along for maintenance, and a base bedded into
the underlayer below the armour crest. The armour runs on in front of
the parapet as a berm ``berm_width`` wide.

The block is loaded with Pedersen's horizontal force and uplift
(:func:`pedersen_crown_loads`), taken together, and the deck is widened
until sliding and overturning about the rear heel meet their targets.

Returns
-------
dict
    Levels and widths for the block, its concrete volume per metre run
    at 2400 kg/m3, the loads, both factors of safety and any warnings.
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

