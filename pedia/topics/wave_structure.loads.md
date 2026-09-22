# Wave loads

`wave_structure.loads` | Forces, pressures, and moments.

Parent: [Wave-structure interaction](wave_structure.md)

Subtopics: [Loads on coastal buildings](wave_structure.loads.buildings.md), [Impact and impulsive loads](wave_structure.loads.impact.md)

Papers: 23. Claims: 13. Equations: 7.

Used by pyCoastal design modules: Pile wave loads.

## Synthesis

**Well established.** Wave-load prediction must distinguish distributed non-impact loading from breaking, slamming, and green-water impact, and must convert local pressure into the force and overturning moment relevant to the structural failure mode.

**Governing physics.** Load physics include inertia and drag, nonlinear diffraction and higher harmonics, runup and breaking, porous transmission, hydrostatics, wave excitation and radiation, air-gap closure, diffraction-driven focusing, and water retained above decks.

**Dimensionless parameters.** Relevant nondimensional controls include Keulegan-Carpenter number, wave steepness, relative depth, relative cylinder diameter, relative freeboard or air gap, wave direction, geometric scale, and normalized force, moment, and pressure coefficients.

**Major equations.** The reviewed methods use VARANS momentum and porous-resistance equations, distributed time-domain force balance, Stokes-like harmonic power models, and moment relations in which each force harmonic is multiplied by a harmonic-specific effective arm derived from its depth distribution.

**Typical methods.** Typical studies combine scaled pressure/load measurements with wave gauges, harmonic or spectral decomposition, CFD or potential-flow simulation, integration to global force and moment, and comparison with semi-empirical design expressions or reduced-order models.

**Numerical models.** Models include COBRAS-UC VARANS-VOF with porous media, fully nonlinear potential flow, Stokes-like reduced-order harmonic reconstruction, coupled Simo-Riflex finite elements with ReaTHM forcing, and OpenFOAM monopile CFD.

**Experimental datasets.** The reviewed evidence includes two 1:20 breakwater sections, a 76 m flume campaign on a 0.315 m cylinder, a 1:30 hybrid 5 MW semi-submersible test at five hull sections, and a 1:20 jacket deck tested across three orientations and water-level states.

**Validated ranges.** Validation is heterogeneous: 1:20 breakwater and jacket tests, a 0.315 m cylinder in 1.8 m depth under non-breaking low-KC focused groups, and a 1:30 floating-wind model under three operational regimes. Reported jacket maxima use source-specific normalizations and must not be transferred as universal coefficients.

**Recent advances.** Recent advances isolate load harmonics experimentally, reconstruct moments from harmonic force arms, validate distributed internal loads under combined wind and waves, and quantify extreme vertical deck-impact configurations rather than relying only on total inline force.

**Disagreements.** Simple harmonic moment-arm models perform well for most non-breaking inertia-load components but show marked triple-frequency discrepancies, while green-water impact is dominated by impulsive vertical force and localized pressure. These findings describe different regimes rather than competing universal models.

**Limitations.** Key limitations are scale and air-compressibility effects, two-dimensional approximations, uncertain pressure integration during impact, site-specific porous properties, omitted hydroelasticity and vibration, third-harmonic model error, and numerical rather than experimental validation of recent closed-form moment arms.

**Open questions.** Needs include common benchmarks spanning non-impact to slamming regimes, pressure-impulse and structural-response coupling, compressible multiphase validation, directional and current effects, uncertainty propagation to failure probability, and experimental validation of harmonic moment arms.

**Seminal papers.** Within this screened slice, the 2009 COBRAS-UC study is an early end-to-end validation of CFD pressure, force, and moment for porous breakwaters; the broader classical force literature remains a discovery gap for this initial branch.

## Equations

### Harmonic-specific effective moment arm

$$
z_n=\frac{\int_{-h}^{0}(z+h)f_n(z)\,dz}{\int_{-h}^{0}f_n(z)\,dz}
$$

Regime: Inertia-dominated non-breaking monopile loading integrated to still-water level.

Variables: `z_n` effective moment arm for harmonic n; `h` water depth; `f_n` depth distribution of nth-harmonic inertia force; `z` vertical coordinate

Source: (Hlophe 2026, [doi:10.1016/j.coastaleng.2026.105055](https://doi.org/10.1016/j.coastaleng.2026.105055))

### Stokes-like nth-harmonic load model

$$
F_n(t)=\Gamma_n[\widehat{F}_1(t)]^n\cos(n\phi(t)-\psi_n)
$$

Regime: Non-breaking focused waves on a low-KC slender vertical cylinder.

Variables: `F_n` nth force harmonic; `Gamma_n` harmonic scale coefficient; `F_1` linear-force envelope; `phi` linear phase; `psi_n` harmonic phase coefficient

Source: (Feng 2020, [doi:10.1016/j.coastaleng.2020.103747](https://doi.org/10.1016/j.coastaleng.2020.103747))

### Harmonic moment-arm approximation

$$
M_n(t)=z_n F_n(t)
$$

Regime: Tested non-breaking inertia-dominated focused-wave cases.

Variables: `M_n` nth moment harmonic about the base; `z_n` harmonic-specific constant moment arm; `F_n` nth force harmonic

Source: (Feng 2020, [doi:10.1016/j.coastaleng.2020.103747](https://doi.org/10.1016/j.coastaleng.2020.103747))

### time-domain higher-order boundary element model

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: 1:20 dual-chamber OWC in 1.0 m water; d/h=0.125, 0.2, 0.25 and chamber-width ratios 1:3, 1:1, 3:1.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Rongquan Wang 2020, [doi:10.1016/j.coastaleng.2020.103744](https://doi.org/10.1016/j.coastaleng.2020.103744))

### first-principles cylinder force model

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Vertical surface-piercing cylinder under matched nominal North Sea sea states with opposing, following, and no current.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Ghadirian 2021, [doi:10.1016/j.coastaleng.2020.103832](https://doi.org/10.1016/j.coastaleng.2020.103832))

### fast second-order Morison load model

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Slender monopiles/spars; example 8 m pile in 33 m depth, with diffraction limit near T=5.1 s and KCmax=2.2; 10 s example D/L=0.057 and KCmax=7.7.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Henrik Bredmose 2021, [doi:10.1016/j.coastaleng.2021.103952](https://doi.org/10.1016/j.coastaleng.2021.103952))

### current-modified Morison equation

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Narrowband weakly nonlinear irregular waves with arbitrary depth-dependent subsurface current acting on a bottom-fixed slender cylinder.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Xin 2023, [doi:10.1016/j.coastaleng.2023.104304](https://doi.org/10.1016/j.coastaleng.2023.104304))

## Claims

- **C162.** For 1:20 low-mound and rubble-mound crown-wall tests under regular and irregular waves, COBRAS-UC reproduced pressure, force, and moment behavior sufficiently to complement semi-empirical stability formulae, but the prototype applications were not field validations. *Regime: The two tested two-dimensional breakwater cross-sections, wave cases, porous formulation, and grid rules..* [direct_finding, mixed] (Guanche 2009, [doi:10.1016/j.coastaleng.2008.11.003](https://doi.org/10.1016/j.coastaleng.2008.11.003))
- **C163.** In non-breaking, inertia-dominated focused-wave tests on a 0.315 m vertical cylinder, a Stokes-like model and constant harmonic-specific moment arms represented most force and moment harmonics well, but the triple-frequency component showed significant discrepancies. *Regime: Low-KC focused groups, 1.8 m depth, slender surface-piercing cylinder; not breaking-wave impact loading..* [direct_finding, mixed] (Feng 2020, [doi:10.1016/j.coastaleng.2020.103747](https://doi.org/10.1016/j.coastaleng.2020.103747))
- **C164.** For a 1:30 braceless 5 MW semi-submersible under three operational wind-wave regimes, time-domain simulations agreed closely with hybrid-test motions and sectional loads, while identifying the pontoon-central-column interface and combined low- and wave-frequency bending as design-critical. *Regime: The tested semi-submersible, calibrated operational conditions, and models excluding hull hydroelasticity and structural vibration..* [direct_finding, mixed] (Luan 2018, [doi:10.1016/j.engstruct.2018.08.021](https://doi.org/10.1016/j.engstruct.2018.08.021))
- **C165.** In 1:20 random-wave jacket tests, zero air gap produced normalized peak vertical force 42 and under-deck peak pressures 13.2 at the leading side and 21.5 at the trailing side; vertical force dominated partial and full green-water cases. *Regime: The tested jacket-deck geometry, random-wave energy levels, orientations, and water levels; normalization definitions are source-specific..* [direct_finding, experimental] (AlMashan 2021, [doi:10.1016/j.oceaneng.2021.109324](https://doi.org/10.1016/j.oceaneng.2021.109324))
- **C166.** For inertia-dominated non-breaking monopile loading, closed-form harmonic-specific moment arms with modest corrections reproduced OpenFOAM total overturning moments accurately, but validation used simulated rather than measured force harmonics. *Regime: Inertia-dominated monopiles and compatible higher-order Stokes-type force harmonics; not breaking or drag-dominated loading..* [direct_finding, mixed] (Hlophe 2026, [doi:10.1016/j.coastaleng.2026.105055](https://doi.org/10.1016/j.coastaleng.2026.105055))
- **C282.** For the tested 1:20 dual-chamber OWC, horizontal curtain-wall loads dominated, the seaside wall governed, and increasing draft raised dominant force and moment; moving the inner wall toward the seaside wall reduced peak loads. *Regime: 1:20 dual-chamber OWC in 1.0 m water; d/h=0.125, 0.2, 0.25 and chamber-width ratios 1:3, 1:1, 3:1..* [direct_finding, mixed] (Rongquan Wang 2020, [doi:10.1016/j.coastaleng.2020.103744](https://doi.org/10.1016/j.coastaleng.2020.103744))
- **C283.** For matched North Sea-type sea states on a vertical cylinder, fitted force coefficients were consistently smaller with current than without, and opposing-current peak force shifted toward the free surface. *Regime: Vertical surface-piercing cylinder under matched nominal North Sea sea states with opposing, following, and no current..* [direct_finding, experimental] (Ghadirian 2021, [doi:10.1016/j.coastaleng.2020.103832](https://doi.org/10.1016/j.coastaleng.2020.103832))
- **C284.** For narrowband weakly nonlinear waves and depth-dependent currents, slender-cylinder load extremes changed materially even when surface-elevation extreme statistics changed little, so current direction and vertical profile must be coupled in the load model. *Regime: Narrowband weakly nonlinear irregular waves with arbitrary depth-dependent subsurface current acting on a bottom-fixed slender cylinder..* [direct_finding, analytical] (Xin 2023, [doi:10.1016/j.coastaleng.2023.104304](https://doi.org/10.1016/j.coastaleng.2023.104304))
- **C287.** For slender monopiles, regrouping second-order spectral interactions permits Morison-type wave loads to be evaluated at O(N log N), with demonstrated field-scale regimes including an 8 m pile in 33 m depth. *Regime: Slender monopiles/spars; example 8 m pile in 33 m depth, with diffraction limit near T=5.1 s and KCmax=2.2; 10 s example D/L=0.057 and KCmax=7.7..* [direct_finding, analytical] (Henrik Bredmose 2021, [doi:10.1016/j.coastaleng.2021.103952](https://doi.org/10.1016/j.coastaleng.2021.103952))
- **C1274.** A validated three-dimensional poroelastic model shows that monopile diffraction and reflection materially alter seabed pore pressure and displacement; pile motion increases with wave height and decreases with seabed Young's modulus. *Regime: Three-dimensional numerical model for wave-induced seabed response around mono-pile.* [direct_finding, mixed] (Titi Sui 2016, [doi:10.1080/17445302.2015.1051312](https://doi.org/10.1080/17445302.2015.1051312))
- **C1674.** Air trapped between coastal-bridge girders substantially amplifies uplift; venting reduces pressure and vertical force, while AASHTO horizontal-force estimates are reasonable but vertical estimates shift from conservative for large waves to underprediction for smaller waves. *Regime: Girder-deck coastal bridge superstructures subjected to the modeled wave heights, periods, clearances and vent configurations..* [direct_finding, numerical] (Mohsen Azadbakht 2016, [doi:10.1007/s40722-016-0043-9](https://doi.org/10.1007/s40722-016-0043-9))
- **C1683.** A one-way SPH–FEM wave-flume framework converts uncertain wave-load and structural inputs into probability distributions of structural acceleration and displacement, exposing nonlinear wave-height response and parameter sensitivities that deterministic runs cannot represent. *Regime: HyTOFU/Tokyo numerical wave-flume geometry with a single idealized flexible structure under the tested breaking and non-breaking wave conditions..* [direct_finding, numerical] (Xiaoyuan Luo 2025, [doi:10.1007/s40571-025-00967-4](https://doi.org/10.1007/s40571-025-00967-4))
- **C1701.** For a 1:30 coastal-bridge model under solitary waves, girders and trapped air amplify and destabilize deck loading; two-dimensional CFD is adequate mainly for decks without girders, whereas three-dimensional CFD better reproduces complex force histories. *Regime: The tested elevated coastal-bridge decks, solitary-wave heights, water depths and submergence conditions at 1:30 scale..* [direct_finding, mixed] (Deming Zhu 2020, [doi:10.1016/j.oceaneng.2020.107499](https://doi.org/10.1016/j.oceaneng.2020.107499))

## Papers

- Titi Sui (2016). Three-dimensional numerical model for wave-induced seabed response around mono-pile. *Ships and Offshore Structures*. [doi:10.1080/17445302.2015.1051312](https://doi.org/10.1080/17445302.2015.1051312)
- Guanche (2009). Numerical analysis of wave loads for coastal structure stability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2008.11.003](https://doi.org/10.1016/j.coastaleng.2008.11.003)
- Deming Zhu (2020). Experimental and 3D numerical investigation of solitary wave forces on coastal bridges. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2020.107499](https://doi.org/10.1016/j.oceaneng.2020.107499)
- Rongquan Wang (2020). Wave loads on a land-based dual-chamber Oscillating Water Column wave energy device. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103744](https://doi.org/10.1016/j.coastaleng.2020.103744)
- Mohsen Azadbakht (2016). Effect of trapped air on wave forces on coastal bridge superstructures. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-016-0043-9](https://doi.org/10.1007/s40722-016-0043-9)
- Feng (2020). Experimental investigation of higher harmonic wave loads and moments on a vertical cylinder by a phase-manipulation method. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103747](https://doi.org/10.1016/j.coastaleng.2020.103747)
- Ghadirian (2021). Wave-current interaction effects on waves and their loads on a vertical cylinder. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103832](https://doi.org/10.1016/j.coastaleng.2020.103832)
- Luan (2018). Comparative analysis of numerically simulated and experimentally measured motions and sectional forces and moments in a floating wind turbine hull structure subjected to combined wind and wave loads. *Engineering Structures*. [doi:10.1016/j.engstruct.2018.08.021](https://doi.org/10.1016/j.engstruct.2018.08.021)
- Xin (2023). Coupled effects of wave and depth-dependent current interaction on loads on a bottom-fixed vertical slender cylinder. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104304](https://doi.org/10.1016/j.coastaleng.2023.104304)
- Henrik Bredmose (2021). Second-order monopile wave loads at linear cost. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103952](https://doi.org/10.1016/j.coastaleng.2021.103952)
- AlMashan (2021). Experimental investigations on wave impact pressures under the deck and global wave forces and moments on offshore jacket platform for partial and full green water conditions. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.109324](https://doi.org/10.1016/j.oceaneng.2021.109324)
- Xiaoyuan Luo (2025). Framework for uncertainty quantification of wave–structure interaction in a flume. *Computational Particle Mechanics*. [doi:10.1007/s40571-025-00967-4](https://doi.org/10.1007/s40571-025-00967-4)
- Hlophe (2026). Wave-induced overturning moments, moment arms, and associated forces on monopile foundations. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105055](https://doi.org/10.1016/j.coastaleng.2026.105055)
- Markel Peñalba (2017). Mathematical modelling of wave energy converters: A review of nonlinear approaches. *Renewable and Sustainable Energy Reviews*. [doi:10.1016/j.rser.2016.11.137](https://doi.org/10.1016/j.rser.2016.11.137)
- Higuera (2014). Three-dimensional interaction of waves and porous coastal structures using OpenFOAM®. Part I: Formulation and validation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.010](https://doi.org/10.1016/j.coastaleng.2013.08.010)
- Brecht Devolder (2017). Application of a buoyancy-modified k-ω SST turbulence model to simulate wave run-up around a monopile subjected to regular waves using OpenFOAM ®. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.04.004](https://doi.org/10.1016/j.coastaleng.2017.04.004)
- Ming He (2023). Wave interactions with multi-float structures: SPH model, experimental validation, and parametric study. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104333](https://doi.org/10.1016/j.coastaleng.2023.104333)
- Peng Jin (2023). Optimization and evaluation of a semi-submersible wind turbine and oscillating body wave energy converters hybrid system. *Energy*. [doi:10.1016/j.energy.2023.128889](https://doi.org/10.1016/j.energy.2023.128889)
- Blanca Peña (2021). Wave-GAN: A deep learning approach for the prediction of nonlinear regular wave loads and run-up on a fixed cylinder. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103902](https://doi.org/10.1016/j.coastaleng.2021.103902)
- Dirk P. Rijnsdorp (2016). Simulating waves and their interactions with a restrained ship using a non-hydrostatic wave-flow model. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.018](https://doi.org/10.1016/j.coastaleng.2016.04.018)
- Arefeh Emami (2024). Further development of offshore floating solar and its design requirements. *Marine Structures*. [doi:10.1016/j.marstruc.2024.103730](https://doi.org/10.1016/j.marstruc.2024.103730)
- Hongbin Hao (2022). Wind turbine model-test method for achieving similarity of both model- and full-scale thrusts and torques. *Applied Ocean Research*. [doi:10.1016/j.apor.2022.103444](https://doi.org/10.1016/j.apor.2022.103444)
- Al-Towayti (2024). Hydrodynamic Performance Assessment of Emerged, Alternatively Submerged and Submerged Semicircular Breakwater: An Experimental and Computational Study. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105)
