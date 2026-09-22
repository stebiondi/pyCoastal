# Berthing energy and fenders {#sec:berthing}

*Module:* `pyCoastal.applications.berthing`. *Example:*
`examples/berth_fenders.py`.

A berthing ship delivers kinetic energy to the fender system. The module
checks three limit states. Insufficient fender energy capacity allows
contact between the ship and the quay. Insufficient panel area transfers a
contact pressure above the limit for the hull. Excessive fender spacing
allows hull contact with the structure between fenders. All three are
evaluated and reported.

## The energy chain

PIANC (2002, Working Group 33) writes the normal berthing energy as the
kinetic energy times four factors (@eq:pianc):

$$ E_N = \tfrac12 MV^2\,C_mC_eC_sC_c. $$ {#eq:pianc}

- **Added mass** (Vasco Costa 1964), $C_m = 1 + 2T/B$, the water the ship
  drags sideways. It is the only factor that makes the energy larger. Below
  about 1.1 draughts of water depth the form starts to understate it, and
  `added_mass_factor(vessel, depth)` warns.
- **Eccentricity**, $C_e = (K^2 + R^2\cos^2\gamma)/(K^2 + R^2)$ with the
  radius of gyration $K = (0.19C_b + 0.11)L_{pp}$, $R$ the distance from the
  contact point to the center of mass along the berth (default $L_{pp}/4$,
  the quarter point), and $\gamma$ the angle between the velocity and that
  line (default 90 degrees). The rotation carries away energy the fender
  never sees.
- **Softness** $C_s$: 1.0 for a soft fender, 0.9 where it is stiff enough
  that the hull deflects with it.
- **Configuration** $C_c$ (`BERTH_CONFIGURATION`): 0.8 solid quay, 0.9
  semi-solid, 1.0 open piled.

The **abnormal factor**, applied afterwards (`ABNORMAL_FACTOR`: 1.25 for a
large tanker up to 2.0 for ro-ro, ferries and tugs, 1.5 for container
ships), covers abnormal berthing conditions such as a parted tug line or a
propulsion failure. It is applied after the four factors and is reported
separately in the result.

**Velocity** enters as a square and is the dominant term in the energy.
`BERTHING_VELOCITY` holds the Brolsma et al. (1977) style table
(@tbl:velocity); `berthing_velocity(vessel, condition)` picks the size class
from the displacement.

: Indicative design berthing velocities (m/s), `BERTHING_VELOCITY`. {#tbl:velocity}

| Condition | small | medium | large |
|-----------|-------|--------|-------|
| `easy_sheltered` | 0.20 | 0.15 | 0.10 |
| `difficult_sheltered` | 0.30 | 0.20 | 0.15 |
| `easy_exposed` | 0.40 | 0.30 | 0.20 |
| `good_exposed` | 0.50 | 0.40 | 0.25 |
| `difficult_exposed` | 0.80 | 0.60 | 0.40 |

## Fender, panel, and spacing

**Fender family.** Within one family and rubber grade, performance scales
with size: energy with the volume of rubber, reaction with the section (@eq:fender-scaling),

$$ E = E_0\left(\frac{H}{H_0}\right)^3,\qquad R = R_0\left(\frac{H}{H_0}\right)^2. $$ {#eq:fender-scaling}

A fender sized for twice the energy returns a reaction larger by a factor of
approximately 1.6. `FenderFamily` holds a reference size; the default
`CONE_FENDER` is a mid-grade cone fender of 1.0 m, 500 kNm and 1000 kN, with
standard heights from 0.3 to 2.5 m. `select_fender(energy, family)` returns
the smallest standard size that absorbs the energy and the fraction of its
rated capacity used. The routine performs fender scaling.
Manufacturer-specific product selection, against tested energy and reaction
curves at the design temperature, angle and velocity, is outside its
scope.

**Hull pressure.** `hull_pressure(reaction, panel_width, panel_height,
vessel_class)` checks the panel against `HULL_PRESSURE_LIMIT` (150 kN/m$^2$
for large tankers, 200 for small tankers and bulk carriers, 400 for container
ships and general cargo, 700 for tugs).

**Spacing.** `fender_spacing(vessel, spacing, projection, bow_radius=None,
smallest_vessel=None, clearance=0.15)` applies two checks. Geometric: with
the fenders compressed, the standoff must exceed the sagitta of the hull
across the gap (@eq:spacing),

$$ s \le 2\sqrt{R_b^2 - (R_b - p + c)^2}. $$ {#eq:spacing}

Practical: the smallest ship using the berth must reach two fenders at once,
about $0.15L_{pp}$ of that ship. Without a bow radius the contact point is
taken on the parallel midbody, which is straight, and the geometric check is
inactive; the length rule then governs. The length rule is evaluated on the
*smallest* vessel using the berth, supplied as `smallest_vessel`.

`design_berth(vessel, velocity=None, condition="easy_sheltered",
vessel_class="container", configuration="open_piled", ...,
smallest_vessel=None, panel_aspect=(1.2, 2.0), family=CONE_FENDER)` runs the
whole chain and returns a `BerthDesign` with `normal`, `abnormal`, `energy`,
`fender`, `panel`, `pressure`, `spacing`, `adequate`, and notes.

```python
from pyCoastal.applications.berthing import design_berth
from pyCoastal.applications.channel import Vessel

ship = Vessel(name="Post-Panamax container", length=366, beam=48.2,
              draught=15.2, block_coefficient=0.68)
feeder = Vessel(name="Feeder", length=140, beam=22.0, draught=8.5,
                block_coefficient=0.68)
design = design_berth(ship, velocity=0.15, vessel_class="container",
                      configuration="open_piled", depth=17.0,
                      smallest_vessel=feeder)
design.energy, design.fender["height"], design.pressure["pressure"], design.adequate
```

## Worked example

<!-- output: berth_fenders -->

Three of the four PIANC factors reduce the energy and the abnormal factor
increases it. The design energy of 2360 kNm is of the same order as the
kinetic energy of 2018 kNm at contact. The intermediate values are reported
at each step of the chain.

![The berthing energy chain and the sensitivity to each input.](media/berth_energy.png){#fig:berth-energy}
