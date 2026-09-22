# Wave-structure interaction

`wave_structure` | Hydrodynamic interaction between waves and built elements.

Subtopics: [Floating structures](wave_structure.floating.md), [Wave loads](wave_structure.loads.md), [Porous structures](wave_structure.porous.md), [Transmission and reflection](wave_structure.transmission.md)

Papers: 6. Claims: 4. Equations: 0.

## Synthesis

**Well established.** Built coastal elements reflect, transmit, diffract and radiate waves; movable or energy-absorbing structures also exchange energy through body motion, air chambers, moorings and power take-off. Response is governed jointly by the incident climate, geometry, spacing and structural dynamics.

**Governing physics.** Fluid inertia, gravity, pressure and viscosity couple to fixed-boundary scattering or rigid/flexible-body motion. Resonance and array interference can amplify response, while damping, radiation, porous losses, breaking and power take-off remove or redistribute energy.

**Dimensionless parameters.** Important controls include wave steepness and relative depth, wavelength-to-structure scale, draft and submergence ratios, spacing-to-wavelength, blockage, Keulegan–Carpenter and Reynolds numbers, mass and damping ratios, capture width and power or reflection coefficients.

**Major equations.** Common models combine potential-flow boundary-value problems and eigenfunction matching with radiation–diffraction theory and motion equations containing mass, added mass, damping, restoring and forcing. More nonlinear regimes require Navier–Stokes, free-surface and structural equations.

**Typical methods.** Methods include analytical eigenfunction solutions, boundary-element and CFD models, wave-basin tests, load and motion measurements, field deployments, array studies, response-amplitude operators, power curves and environmental monitoring.

**Numerical models.** Linear potential-flow models efficiently resolve diffraction, radiation and array coupling; time-domain and CFD approaches address nonlinear free surfaces, impacts and viscous losses. Device models couple hydrodynamics to air compressibility, turbine, generator, mooring or control dynamics.

**Experimental datasets.** Root evidence includes the monitored Lysekil point-absorber site, theoretical coast-integrated oscillating-water-column arrays, comparative low-energy-sea converter literature and a broad coastal-engineering wave–structure process review.

**Validated ranges.** The reviewed evidence spans a deployed heaving point absorber, planned multi-device field expansion, coast-integrated OWC arrays with variable chamber dimensions and spacing, and low-energy regional wave climates. Exact quantitative ranges remain source-specific.

**Recent advances.** Recent advances integrate devices into coasts and ports, exploit constructive array effects, tailor smaller converters to low-energy seas, couple hydrodynamics with control and electrical systems, and expand field and environmental monitoring.

**Disagreements.** Linear models isolate interference and resonance but cannot represent all breaking, viscous, impact or extreme-load behavior. Wave-energy devices may protect coasts in some configurations yet alter sediment or ecosystems, and resource potential does not by itself establish economic performance.

**Limitations.** Scale effects, incomplete coupled structural models, uncertain damping and power take-off, idealized waves and geometry, sparse long-duration field data, survivability, maintenance, grid integration and environmental impacts limit transfer from model or prototype to arrays.

**Open questions.** Priorities include nonlinear array interaction, extreme and fatigue loads, flexible and porous response, optimized geometry and control, multi-use coastal protection, climate robustness, field-scale validation and cumulative ecological effects.

**Seminal papers.** Classical diffraction and radiation theory established wave loading, added mass and damping for fixed and floating bodies; subsequent laboratory and numerical work extended these foundations to breakwaters, offshore structures and energy converters.

## Claims

- **C1269.** A linear-potential-flow and eigenfunction-matching model shows that coast-integrated oscillating-water-column arrays can enhance power extraction over a range of waves through constructive array and coast effects controlled by direction, chamber geometry, spacing and array size. *Regime: Wave power extraction from multiple oscillating water columns along a straight coast.* [direct_finding, analytical] (Siming Zheng 2019, [doi:10.1017/jfm.2019.656](https://doi.org/10.1017/jfm.2019.656))
- **C1272.** Coastal wave–structure interaction is a complex fluid–structure problem spanning multiple engineering configurations and requires process-specific analysis rather than a single transferable response model. *Regime: Wave-Structure Interaction Processes in Coastal Engineering.* [literature_review_statement, review] (Aristodemo 2021, [doi:10.3390/w13060831](https://doi.org/10.3390/w13060831))
- **C1623.** An OpenFOAM numerical wave tank with generation and relaxation-zone absorption reproduced measured nonlinear loading on a vertical cylinder through fourth-order harmonics; linear theory could miss up to 50% of total wave load, and converged cases used roughly L/70 horizontal and H/8 vertical resolution. *Regime: Nonlinear regular and focused wave groups interacting with a vertical cylinder in the tested numerical and laboratory configurations..* [direct_finding, mixed] (Lifen Chen 2014, [doi:10.1016/j.oceaneng.2014.06.003](https://doi.org/10.1016/j.oceaneng.2014.06.003))
- **C1754.** Adding a density-aware buoyancy-production term to the k-omega SST turbulence-energy equation suppresses nonphysical air-water-interface turbulence and excessive wave damping, enabling stable RANS-VOF propagation and credible regular-wave run-up predictions around a monopile. *Regime: Regular waves propagating in a three-dimensional numerical flume and interacting with a vertical circular monopile under the tested relatively deep-water conditions..* [direct_finding, mixed] (Brecht Devolder 2017, [doi:10.1016/j.coastaleng.2017.04.004](https://doi.org/10.1016/j.coastaleng.2017.04.004))

## Papers

- Lifen Chen (2014). Numerical investigation of wave–structure interaction using OpenFOAM. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2014.06.003](https://doi.org/10.1016/j.oceaneng.2014.06.003)
- Siming Zheng (2019). Wave power extraction from multiple oscillating water columns along a straight coast. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2019.656](https://doi.org/10.1017/jfm.2019.656)
- Brecht Devolder (2017). Application of a buoyancy-modified k-ω SST turbulence model to simulate wave run-up around a monopile subjected to regular waves using OpenFOAM ®. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.04.004](https://doi.org/10.1016/j.coastaleng.2017.04.004)
- Aristodemo (2021). Wave-Structure Interaction Processes in Coastal Engineering. *Water*. [doi:10.3390/w13060831](https://doi.org/10.3390/w13060831)
- Spyros Foteinis (2022). Wave energy converters in low energy seas: Current state and opportunities. *Renewable and Sustainable Energy Reviews*. [doi:10.1016/j.rser.2022.112448](https://doi.org/10.1016/j.rser.2022.112448)
- Mats Leijon (2008). Wave Energy from the North Sea: Experiences from the Lysekil Research Site. *Surveys in Geophysics*. [doi:10.1007/s10712-008-9047-x](https://doi.org/10.1007/s10712-008-9047-x)
