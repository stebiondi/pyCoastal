# Bedload transport

`sediment.bedload` | Transport in contact with the bed.

Parent: [Sediment transport](sediment.md)

Papers: 9. Claims: 7. Equations: 7.

## Synthesis

**Well established.** Coastal bedload begins above a mobility threshold and responds to the time history of near-bed forcing, not merely bulk wave height; waves, currents, asymmetry, roughness, slope, pressure, breaking, and return flow can change both magnitude and direction.

**Governing physics.** Governing mechanisms include Shields-type mobility, grain-bed friction, oscillatory boundary-layer turbulence, velocity skewness and acceleration asymmetry, gravity on slopes, wave-pressure-induced bed deformation, return currents, breaking transitions, and stochastic variability among waves.

**Dimensionless parameters.** Principal nondimensional controls are Shields parameter theta, critical Shields stress, relative orbital excursion am/ks, wave nonlinearity index Ni, Ursell number S, relative roughness, grain Reynolds number, velocity skewness, acceleration asymmetry, and normalized bedload rate.

**Major equations.** The branch contains practical physics-based formulae for currents and waves, half-cycle random-wave formulations, Bagnold-energetics cross-shore transport, a pressure-coupled porous-bed boundary-layer formulation, and an early wave-bedload law whose coefficients require full-text recovery.

**Typical methods.** Typical methods combine movable-bed wave flumes, full-scale oscillatory water tunnels, turbulence-resolving boundary-layer models, analytical energetics and force balances, stochastic transformation of half-cycle laws, and validation against compiled transport observations.

**Numerical models.** Models span the BSL k-omega boundary-layer closure, practical coastal bedload formula families, half-cycle stochastic transport, Bagnold energetics, and a nonlinear pressure-coupled boundary layer over a poroelastic erodible bed.

**Experimental datasets.** Direct datasets include asymmetric-wave rough-bed cases with Ni=0.58-0.67 and am/ks=35-963, sheet-flow tests using 0.24 and 0.51 mm sand on slopes to 2.5 degrees, and breaking-wave movable-bed tests with D50=0.22 mm.

**Validated ranges.** Reported bounds include conventional bedload from critical Shields stress to theta about 0.8, rough-bed asymmetric waves at Ni=0.58-0.67 and am/ks=35-963, 0.24-0.51 mm sheet-flow sand and slopes to 2.5 degrees, and an energetics formula acceptable for S<=60.

**Recent advances.** Later advances resolve roughness-modified turbulence under asymmetric waves and isolate bed-slope effects in full-scale sheet-flow experiments, improving the process basis for cross-shore morphodynamic prediction.

**Disagreements.** No direct contradiction is established in this small set, but deterministic equivalent-wave calculations underpredict stochastic random-wave estimates, while shear-only practical formulae omit pressure-driven deformation represented in the porous-bed theory.

**Limitations.** Evidence remains dominated by controlled, often unidirectional laboratory forcing. Formula performance is regime dependent, sheet flow lies beyond conventional bedload assumptions, and several historical sources expose insufficient full text to recover coefficients or uncertainty.

**Open questions.** Needs include common validation datasets for combined irregular waves and currents, pressure and seepage effects, graded beds, field-scale direction reversals, sheet-flow transitions, morphology feedback, and uncertainty in threshold and roughness specification.

**Seminal papers.** The 1986 wave-bedload law and 1989 breaking-wave energetics study are early formulations; the 2001 stochastic treatment and 2003 pressure-coupled model broadened the physics, followed by the 2005 practical formula family.

## Equations

### Bagnold energetics cross-shore bedload model

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Movable-bed flume with D50=0.22 mm sand; derived formula reported acceptable for Ursell number S<=60, especially short waves and beds with at most one submerged bar.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Pruszak 1989, [doi:10.1016/0378-3839(89)90053-7](https://doi.org/10.1016/0378-3839(89)90053-7))

### Soulsby-van Rijn coastal bedload framework

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Coarse sand and gravel bedload; conventional bedload from critical Shields stress to about theta=0.8, with sheet flow above about theta=0.8.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Soulsby 2005, [doi:10.1016/j.coastaleng.2005.04.003](https://doi.org/10.1016/j.coastaleng.2005.04.003))

### BSL k-omega boundary-layer model

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Wave nonlinearity index Ni=0.58-0.67 and orbital-excursion-to-roughness ratio am/ks=35-963.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Suntoyo 2009, [doi:10.1016/j.coastaleng.2009.06.005](https://doi.org/10.1016/j.coastaleng.2009.06.005))

### half-cycle sheet-flow interpretation

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Sediment diameters 0.24 and 0.51 mm and bed slopes from horizontal to 2.5 degrees under matched first-harmonic velocity and period.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Tan 2019, [doi:10.1016/j.coastaleng.2019.01.002](https://doi.org/10.1016/j.coastaleng.2019.01.002))

### Tsuchiya wave-bedload law

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Wave-driven bedload; accessible metadata does not expose coefficients or a validation range.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Tsuchiya 1986, [doi:10.1080/05785634.1986.11924433](https://doi.org/10.1080/05785634.1986.11924433))

### stochastic nonlinear random-wave bedload model

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Narrow-band second-order random waves using a regular-wave half-cycle bedload formula.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Myrhaug 2001, [doi:10.1142/s0578563401000311](https://doi.org/10.1142/s0578563401000311))

### deformable porous-bed boundary-layer model

$$
q_b=f(\theta,\,u(t),\,k_s,\,D_{50},\,\beta)
$$

Regime: Wave loading over a deformable, erodible porous seabed represented with an extended Saffman slip condition and Coulomb failure criterion.

Variables: `q_b` bedload transport rate; `theta` Shields parameter; `u(t)` near-bed velocity history; `k_s` bed roughness; `D50` median sediment diameter; `beta` bed slope; generic normalized dependency list, not a recovered source coefficient equation

Source: (Foda 2003, [doi:10.1061/(asce)0733-950x(2003)129:6(243)](https://doi.org/10.1061/(asce)0733-950x(2003)129:6(243)))

## Claims

- **C236.** For reviewed coastal datasets spanning currents, symmetric or asymmetric waves, and combined forcing, the physics-based bedload formulae predicted 47%-91% of observations within a factor of two; their stated conventional-bedload range extends from critical Shields stress to approximately theta=0.8. *Regime: Coarse sand and gravel bedload; conventional bedload from critical Shields stress to about theta=0.8, with sheet flow above about theta=0.8..* [direct_finding, analytical] (Soulsby 2005, [doi:10.1016/j.coastaleng.2005.04.003](https://doi.org/10.1016/j.coastaleng.2005.04.003))
- **C237.** For asymmetric-wave boundary layers with Ni=0.58-0.67 and am/ks=35-963, increasing roughness raised turbulent kinetic energy and bottom shear stress, reduced inner-layer mean velocity, and increased potential net sediment transport, with direction and magnitude also strongly controlled by wave nonlinearity. *Regime: Wave nonlinearity index Ni=0.58-0.67 and orbital-excursion-to-roughness ratio am/ks=35-963..* [direct_finding, mixed] (Suntoyo 2009, [doi:10.1016/j.coastaleng.2009.06.005](https://doi.org/10.1016/j.coastaleng.2009.06.005))
- **C238.** Full-scale oscillatory-tunnel tests isolated bed-slope effects on sheet-flow transport for 0.24 and 0.51 mm sand over slopes up to 2.5 degrees under skewed and asymmetric flows with matched first-harmonic velocity and period. *Regime: Sediment diameters 0.24 and 0.51 mm and bed slopes from horizontal to 2.5 degrees under matched first-harmonic velocity and period..* [direct_finding, experimental] (Tan 2019, [doi:10.1016/j.coastaleng.2019.01.002](https://doi.org/10.1016/j.coastaleng.2019.01.002))
- **C239.** A nonlinear boundary-layer formulation predicts coastal bedload by coupling wave shear with pressure-driven poroelastic bed deformation and a Coulomb failure criterion; its applicability is limited to the assumed deformable porous-bed and viscoelastic-sediment representation. *Regime: Wave loading over a deformable, erodible porous seabed represented with an extended Saffman slip condition and Coulomb failure criterion..* [direct_finding, analytical] (Foda 2003, [doi:10.1061/(asce)0733-950x(2003)129:6(243)](https://doi.org/10.1061/(asce)0733-950x(2003)129:6(243)))
- **C240.** For narrow-band second-order random waves modeled with a regular-wave half-cycle transport law, stochastic averaging predicts larger mean bedload than applying the same law to an equivalent deterministic sinusoidal wave. *Regime: Narrow-band second-order random waves using a regular-wave half-cycle bedload formula..* [direct_finding, analytical] (Myrhaug 2001, [doi:10.1142/s0578563401000311](https://doi.org/10.1142/s0578563401000311))
- **C241.** In movable-bed flume tests with D50=0.22 mm sand, single breaking produced shoreward bedload in the surf zone and offshore transport seaward of breaking, whereas repeated breaking over multiple bars produced multiple direction reversals; the derived energetics formula was acceptable for S<=60. *Regime: Movable-bed flume with D50=0.22 mm sand; derived formula reported acceptable for Ursell number S<=60, especially short waves and beds with at most one submerged bar..* [direct_finding, mixed] (Pruszak 1989, [doi:10.1016/0378-3839(89)90053-7](https://doi.org/10.1016/0378-3839(89)90053-7))
- **C242.** Tsuchiya (1986) proposed a law for wave-driven sediment transport in the bedload regime; available metadata does not support a quantitative coefficient set or validated parameter range. *Regime: Wave-driven bedload; accessible metadata does not expose coefficients or a validation range..* [proposed_hypothesis, author_hypothesis] (Tsuchiya 1986, [doi:10.1080/05785634.1986.11924433](https://doi.org/10.1080/05785634.1986.11924433))

## Papers

- Soulsby (2005). Bedload sediment transport in coastal waters. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.04.003](https://doi.org/10.1016/j.coastaleng.2005.04.003)
- Suntoyo (2009). Effect of bed roughness on turbulent boundary layer and net sediment transport under asymmetric waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2009.06.005](https://doi.org/10.1016/j.coastaleng.2009.06.005)
- Tan (2019). Experimental study of sheet-flow sediment transport under nonlinear oscillatory flow over a sloping bed. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.01.002](https://doi.org/10.1016/j.coastaleng.2019.01.002) [preprint, read only](https://yuanj2021.github.io/yuanjLab/pdf/CE_2018_slope.pdf)
- Foda (2003). Role of Wave Pressure in Bedload Sediment Transport. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)0733-950x(2003)129:6(243)](https://doi.org/10.1061/(asce)0733-950x(2003)129:6(243))
- Myrhaug (2001). Bedload Sediment Transport Rate by Nonlinear Random Waves. *Coastal Engineering Journal*. [doi:10.1142/s0578563401000311](https://doi.org/10.1142/s0578563401000311)
- Pruszak (1989). On-Offshore bed-load sediment transport in the coastal zone. *Coastal Engineering*. [doi:10.1016/0378-3839(89)90053-7](https://doi.org/10.1016/0378-3839(89)90053-7)
- Tsuchiya (1986). A Law for Sediment Transport by Waves in a Bed Load. *Coastal Engineering in Japan*. [doi:10.1080/05785634.1986.11924433](https://doi.org/10.1080/05785634.1986.11924433)
- van de Kreeke (2004). Equilibrium and cross-sectional stability of tidal inlets: application to the Frisian Inlet before and after basin reduction. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.05.002](https://doi.org/10.1016/j.coastaleng.2004.05.002)
- Kılar (2025). Wave storm impacts on shoreline evolution: A case study of Iztuzu beach. *Ocean &amp; Coastal Management*. [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748) [published version, read only](https://acikerisim.uludag.edu.tr/bitstreams/c85bd685-4a66-457d-88b3-ab395a726911/download)
