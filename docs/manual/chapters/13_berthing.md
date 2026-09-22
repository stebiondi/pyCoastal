# Berthing energy and fenders {#sec:berthing}

*Module:* `pyCoastal.applications.berthing`. *Example:*
`examples/berth_fenders.py`.

A ship comes alongside carrying kinetic energy, and something has to absorb
it. A berth fails in three different ways and only one of them is about
energy. The fender can be too small, and the ship reaches the quay. The
panel can be too small, and the reaction dents the side shell even though
the energy was absorbed perfectly. The fenders can be too far apart, and the
hull touches the structure between them. All three are checked.

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
ships), covers the berthing that goes wrong: a parted tug line, an engine
that does not go astern. It is reported separately because it is frequently
the largest single term.

**Velocity** is squared and is the least well known quantity.
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

A fender chosen to absorb twice the energy pushes back only about 1.6 times
as hard. `FenderFamily` holds a reference size (the default `CONE_FENDER` is
a mid-grade cone fender, 1.0 m, 500 kNm, 1000 kN, in standard heights from
0.3 to 2.5 m) and `select_fender(energy, family)` returns the smallest
standard size that absorbs the energy and how much of its capacity is used.
This is a scaling model, not a catalogue: size the fender you are asking for
here, then select against the manufacturer's tested curves.

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
about $0.15L_{pp}$. Without a bow radius the contact is on the straight
parallel midbody, so the geometric check cannot bind and the length rule
governs; the rule uses the *smallest* vessel, not the design one.

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

Three of the four PIANC factors reduce the energy and the abnormal allowance
puts most of it back: the design energy of 2360 kNm is close to the
2018 kNm the ship arrived with, which makes it easy to conclude wrongly that
the factors did not matter.

![The berthing energy chain and the design levers.](media/berth_energy.png){#fig:berth-energy}
