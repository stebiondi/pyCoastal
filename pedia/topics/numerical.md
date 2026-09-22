# Numerical modeling

`numerical` | Computational representation of coastal systems.

Subtopics: [Computational fluid dynamics](numerical.cfd.md), [Model coupling and nesting](numerical.coupling.md), [Hydrodynamic circulation models](numerical.hydro.md), [Morphodynamic models](numerical.morpho.md), [Phase-averaged wave models](numerical.phase_averaged.md), [Phase-resolving wave models](numerical.phase_resolving.md)

Papers: 14. Claims: 3. Equations: 0.

## Synthesis

**Well established.** Coastal numerical models discretize conservation laws and process closures to represent waves, circulation, sediment, morphology and structures. Credible use requires equations and resolution appropriate to scale plus calibration, validation, sensitivity and uncertainty evidence matched to the decision.

**Governing physics.** Models conserve mass, momentum and tracers while representing pressure, gravity, turbulence, viscosity, free surfaces, wave dispersion and breaking, bottom stress, porous or structural forces and sediment exchange; coupled systems pass forcing and feedback among components.

**Dimensionless parameters.** Resolution and regime depend on Courant, Reynolds, Froude, Keulegan–Carpenter, relative-depth, steepness, Ursell, Shields, grid-to-feature and time-step ratios, plus error, skill, convergence and sensitivity measures.

**Major equations.** Common frameworks include depth-averaged and three-dimensional Reynolds-averaged Navier–Stokes equations, LES, volume-of-fluid and particle methods, nonhydrostatic and Boussinesq systems, spectral wave-action balance, sediment advection–diffusion and Exner bed evolution.

**Typical methods.** Workflows define purpose and conceptual model, assemble bathymetry and boundaries, generate meshes, choose closures, calibrate limited parameters, verify numerics, validate independent variables, quantify sensitivity and uncertainty, and document applicability and reproducibility.

**Numerical models.** Reviewed approaches include OpenFOAM LES, COAWST wave–tide coupling, RANS–VOF, SPH, nonhydrostatic phase-resolving reef flow, REEF3D scour and MIKE21 FM coupled waves and hydrodynamics, alongside general model-assurance guidance.

**Experimental datasets.** Evidence includes ultrasonic dune winds and LiDAR terrain, British shelf wave climates, dam-break swash, large-scale barred-beach breaking, rough and smooth reef flumes, pile-scour benchmarks and Iraqi coastal water-level, wind and wave observations.

**Validated ranges.** Examples report swash r² above 0.97 and stress error within 20%, reef geometry from a 1:5 fore-reef to 500 m prototype flat, 49–93% oblique wave occurrence at tidal sites and 46.8% wave-height bias when Iraqi wind forcing is omitted.

**Recent advances.** Recent advances apply particle and nonhydrostatic methods at near-natural scales, couple wave and tide resources, resolve reef roughness, use LiDAR-derived complex terrain, quantify field-linked model skill and emphasize fit-for-purpose uncertainty documentation.

**Disagreements.** Higher-fidelity models expose vortices, aeration and three-dimensional response but cost more and still require closures; simpler phase-averaged or depth-averaged systems support regional prediction yet can omit process-scale dynamics. Agreement in one variable does not guarantee all fluxes are correct.

**Limitations.** Uncertain boundary data and bathymetry, grid and time-step dependence, turbulence and breaking closures, scale effects, sparse validation, parameter compensation, one-way coupling, computational cost and incomplete uncertainty reporting constrain confidence.

**Open questions.** Priorities include coupled atmosphere–wave–ocean–sediment prediction, differentiable and adjoint methods, adaptive meshes, hybrid physics–ML, reproducible benchmarks, probabilistic calibration, extreme-event validation and decision-relevant error propagation.

**Seminal papers.** Finite-difference shallow-water and spectral wave models established regional simulation; RANS, Boussinesq, boundary-element and morphodynamic approaches expanded process coverage, while formal verification and validation established numerical credibility practice.

## Claims

- **C363.** A 2018 coastal-modeling workshop identified common benchmarks, grid and validation standards, standardized I/O and reporting, and stronger parameter estimation and uncertainty quantification as central requirements for reducing subjectivity and improving reproducibility. *Regime: Findings of a 2018 United States workshop on physical coastal and estuarine modeling..* [literature_review_statement, review] (Oliver B. Fringer 2019, [doi:10.1016/j.ocemod.2019.101458](https://doi.org/10.1016/j.ocemod.2019.101458))
- **C1298.** Fit-for-purpose shelf and estuary modeling requires explicit setup, input-data, calibration, validation, error, uncertainty and performance-metric documentation rather than model execution alone. *Regime: Guidance on Setup, Calibration, and Validation of Hydrodynamic, Wave, and Sediment Models for Shelf Seas and Estuaries.* [literature_review_statement, review] (Jon J. Williams 2017, [doi:10.1155/2017/5251902](https://doi.org/10.1155/2017/5251902))
- **C1303.** A coastal-hydrodynamics review identifies tidal and wave modeling foundations and emerging SPH fluid–solid interaction, adjoint prediction, renewable-energy and large-scale morphodynamic applications. *Regime: Coastal hydrodynamics – present and future.* [literature_review_statement, review] (Peter Stansby 2013, [doi:10.1080/00221686.2013.821678](https://doi.org/10.1080/00221686.2013.821678))

## Papers

- Oliver B. Fringer (2019). The future of coastal and estuarine modeling: Findings from a workshop. *Ocean Modelling*. [doi:10.1016/j.ocemod.2019.101458](https://doi.org/10.1016/j.ocemod.2019.101458)
- Jon J. Williams (2017). Guidance on Setup, Calibration, and Validation of Hydrodynamic, Wave, and Sediment Models for Shelf Seas and Estuaries. *Advances in Civil Engineering*. [doi:10.1155/2017/5251902](https://doi.org/10.1155/2017/5251902)
- Peter Stansby (2013). Coastal hydrodynamics – present and future. *Journal of Hydraulic Research*. [doi:10.1080/00221686.2013.821678](https://doi.org/10.1080/00221686.2013.821678)
- Abbas Khayyer (2007). Corrected Incompressible SPH method for accurate water-surface tracking in breaking waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.10.001](https://doi.org/10.1016/j.coastaleng.2007.10.001)
- Derek Jackson (2011). Investigation of three‐dimensional wind flow behaviour over coastal dune morphology under offshore winds using computational fluid dynamics (CFD) and ultrasonic anemometry. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.2139](https://doi.org/10.1002/esp.2139)
- Matthew Lewis (2014). Realistic wave conditions and their influence on quantifying the tidal stream energy resource. *Applied Energy*. [doi:10.1016/j.apenergy.2014.09.061](https://doi.org/10.1016/j.apenergy.2014.09.061)
- Colin Whittaker (2017). Optimisation of focused wave group runup on a plane beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.12.001](https://doi.org/10.1016/j.coastaleng.2016.12.001)
- Gioele Ruffini (2019). Numerical modelling of landslide-tsunami propagation in a wide range of idealised water body geometries. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103518](https://doi.org/10.1016/j.coastaleng.2019.103518)
- Alec Torres‐Freyermuth (2013). Modeling swash‐zone hydrodynamics and shear stresses on planar slopes using Reynolds‐Averaged Navier–Stokes equations. *Journal of Geophysical Research Oceans*. [doi:10.1002/jgrc.20074](https://doi.org/10.1002/jgrc.20074)
- Corrado Altomare (2023). Large-scale wave breaking over a barred beach: SPH numerical simulation and comparison with experiments. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104362](https://doi.org/10.1016/j.coastaleng.2023.104362)
- Mark L. Buckley (2022). Wave‐Driven Hydrodynamic Processes Over Fringing Reefs With Varying Slopes, Depths, and Roughness: Implications for Coastal Protection. *Journal of Geophysical Research Oceans*. [doi:10.1029/2022jc018857](https://doi.org/10.1029/2022jc018857)
- Matías Quezada (2019). Numerical Study of the Hydrodynamics of Waves and Currents and Their Effects in Pier Scouring. *Water*. [doi:10.3390/w11112256](https://doi.org/10.3390/w11112256)
- Luan (2018). Comparative analysis of numerically simulated and experimentally measured motions and sectional forces and moments in a floating wind turbine hull structure subjected to combined wind and wave loads. *Engineering Structures*. [doi:10.1016/j.engstruct.2018.08.021](https://doi.org/10.1016/j.engstruct.2018.08.021)
- Majid Al-Rammahi (2025). Numerical Simulation of Hydrodynamic and Spectral Model of Iraqi Coastal Water at the Northern Arabian Gulf. *CFD Letters*. [doi:10.37934/cfdl.17.9.194211](https://doi.org/10.37934/cfdl.17.9.194211)
