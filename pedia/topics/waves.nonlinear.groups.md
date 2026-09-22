# Wave groups and infragravity waves

`waves.nonlinear.groups` | Group forcing and low-frequency response.

Parent: [Waves and wave transformation](waves.md) > [Nonlinear wave dynamics](waves.nonlinear.md)

Papers: 16. Claims: 16. Equations: 0.

## Synthesis

**Well established.** Amplitude modulation of short waves forces difference-frequency long waves that are bound to groups offshore; shoaling, breaking and changing group speed can amplify, phase-shift and release free infragravity waves.

**Governing physics.** Gradients in short-wave radiation stress force long-wave setup and oscillation. The response approaches resonance when group velocity matches shallow-water long-wave speed; bathymetry, breaking, directional spreading, reflection and edge-wave trapping control subsequent evolution.

**Dimensionless parameters.** Controls include group frequency, modulation depth, relative depth, beach slope, wave steepness, group-to-long-wave speed ratio, directional spread, normalized breakpoint excursion, reflection coefficient, reef width/depth and infragravity frequency bands.

**Major equations.** Core descriptions are forced shallow-water continuity and momentum at group scale, radiation-stress source terms, free/bound Green-function solutions, spectral energy and flux balances, and nonlinear or nonhydrostatic equations for coupled short/long waves.

**Typical methods.** Methods include bichromatic and random-wave flumes, high-resolution cross-shore arrays, directional spectral reconstruction, bispectral/phase analysis, field swash and reef transects, SurfBeat/group-scale models, phase-resolving models and regional spectral infragravity sources.

**Numerical models.** Models include Delft3D-SurfBeat, WAVEWATCH III with an infragravity source, InWave coupled to ocean–wave–sediment dynamics, unstructured group-scale hydrodynamics, linear forced-wave models, dissipative edge-wave models and Green-function solutions.

**Experimental datasets.** Key evidence comes from barred- and plane-beach flumes, Delft experiments, the Delilah field campaign, dissipative-beach swash observations, a five-month Roi-Namur reef record, bichromatic 1:100-slope tests and directional coastal arrays.

**Validated ranges.** The corpus covers unbroken shoaling and surf-zone breaking, plane and barred beaches, gentle dissipative slopes, reefs, shore-oblique forcing, regional/global propagation and frequencies from conventional infragravity below about 0.05 Hz to reef VLF bands of 0.001–0.005 Hz.

**Recent advances.** Recent advances unify free and forced components analytically, reconstruct directional spectra, drive coupled morphology models with infragravity waves, extend computation to unstructured meshes and represent free infragravity propagation at regional-to-global scales.

**Disagreements.** Bound-wave release at breaking, breakpoint forcing and continuous free-wave radiation are competing but not mutually exclusive descriptions; inferred contributions depend on phase convention, directionality, decomposition method and the treatment of dissipation and reflection.

**Limitations.** Directional long-wave observations are sparse; shoreline reflection and dissipation are difficult to separate; frequency-band definitions vary; laboratory scales and one-dimensional bathymetry simplify natural systems; empirical regional sources omit event-specific phase.

**Open questions.** Open issues include nonlinear resonance saturation, directional and alongshore coupling, wave-group statistics in broad spectra, free/bound separation through breaking, shoreline and reef dissipation, interaction with currents and tides, and extreme-runup predictability.

**Seminal papers.** Early field and laboratory work established group-bound long waves and competing release/breakpoint mechanisms; energy-budget and phase-lag studies then quantified shoaling, reflection and dissipation.

## Claims

- **C902.** A laboratory energy budget over a barred beach shows how group-induced subharmonic waves shoal, exchange energy, and dissipate across the nearshore. *Regime: Shoaling of subharmonic gravity waves.* [direct_finding, experimental] (J.A. Battjes 2004, [doi:10.1029/2003jc001863](https://doi.org/10.1029/2003jc001863))
- **C903.** Flume observations and Delft3D-SurfBeat quantify low-frequency-wave shoaling growth, shoreline reflection, and dissipation. *Regime: Shoaling and shoreline dissipation of low‐frequency waves.* [direct_finding, mixed] (Ap van Dongeren 2007, [doi:10.1029/2006jc003701](https://doi.org/10.1029/2006jc003701))
- **C904.** WAVEWATCH III extended with a shoreline source represents free infragravity waves at regional and global scales using offshore wave height and mean period. *Regime: A numerical model for free infragravity waves: Definition and validation at regional and global scales.* [direct_finding, numerical] (Fabrice Ardhuin 2014, [doi:10.1016/j.ocemod.2014.02.006](https://doi.org/10.1016/j.ocemod.2014.02.006))
- **C905.** Field observations on a gently sloping dissipative beach show infragravity swash saturation can occur even under mild offshore energy, especially above roughly 0.025–0.035 Hz. *Regime: Observations of wave energy fluxes and swash motions on a low-sloping, dissipative beach.* [direct_finding, field] (Rafael M.C. Guedes 2013, [doi:10.1002/jgrc.20267](https://doi.org/10.1002/jgrc.20267))
- **C906.** Linear modelling of the Delilah data evaluates bound-wave release and breakpoint forcing by directionally spread short waves on an alongshore-uniform beach. *Regime: Linear modeling of infragravity waves during Delilah.* [direct_finding, mixed] (Ad Reniers 2002, [doi:10.1029/2001jc001083](https://doi.org/10.1029/2001jc001083))
- **C907.** Five months of reef-flat observations classify very-low-frequency waves and show resonance can drive large runup and overwash on low-lying reef islands. *Regime: Identification and classification of very low frequency waves on a coral reef flat.* [direct_finding, field] (Matthijs Gawehn 2016, [doi:10.1002/2016jc011834](https://doi.org/10.1002/2016jc011834))
- **C908.** Bichromatic groups on a 1:100 slope show group frequency strongly controls nonlinear transfer toward both low- and high-frequency components. *Regime: Transfer and dissipation of energy during wave group propagation on a gentle beach slope.* [direct_finding, experimental] (Enrique M. Padilla 2017, [doi:10.1002/2017jc012703](https://doi.org/10.1002/2017jc012703))
- **C909.** An analytical shallow-water solution decomposes free and forced long-wave components generated as short-wave groups shoal without breaking. *Regime: Free and Forced Components of Shoaling Long Waves in the Absence of Short-Wave Breaking.* [direct_finding, analytical] (Stephanie Contardo 2021, [doi:10.1175/jpo-d-20-0214.1](https://doi.org/10.1175/jpo-d-20-0214.1))
- **C910.** A reconstruction method separates directional spectra of free and bound infragravity components beyond conventional linear-wave assumptions. *Regime: Reconstruction of Directional Spectra of Infragravity Waves.* [direct_finding, mixed] (Yoshinao Matsuba 2022, [doi:10.1029/2021jc018273](https://doi.org/10.1029/2021jc018273))
- **C911.** The InWave driver supplies infragravity forcing to a coupled ocean–wave–sediment model for erosion and breaching simulations. *Regime: Development and Application of an Infragravity Wave (InWave) Driver to Simulate Nearshore Processes.* [direct_finding, numerical] (Maitane Olabarrieta 2023, [doi:10.1029/2022ms003205](https://doi.org/10.1029/2022ms003205))
- **C912.** An unstructured-grid hydrodynamic model with a nonstationary directionally spread wave driver resolves two-dimensional nearshore flow at wave-group scale. *Regime: Modelling wave group-scale hydrodynamics on orthogonal unstructured meshes.* [direct_finding, numerical] (Johan Reyns 2023, [doi:10.1016/j.envsoft.2023.105655](https://doi.org/10.1016/j.envsoft.2023.105655))
- **C913.** A forced dissipative shallow-water model explains cross-shore propagation and trapping of shore-oblique infragravity and edge waves. *Regime: Simulations of Dissipative, Shore-Oblique Infragravity Waves.* [direct_finding, numerical] (Stephen M. Henderson 2003, [doi:10.1175/2398.1](https://doi.org/10.1175/2398.1))
- **C914.** Higher-order theory explains the growing phase lag between bound infragravity waves and forcing short-wave groups during shoaling. *Regime: On the Bound Wave Phase Lag.* [direct_finding, analytical] (Thomas Guérin 2019, [doi:10.3390/fluids4030152](https://doi.org/10.3390/fluids4030152))
- **C915.** A Green-function solution unifies free and bound group-induced infragravity waves and captures the near-resonant response where group and shallow-water wave speeds match. *Regime: Unified analytical solution for group-induced infragravity waves based on Green's function.* [direct_finding, analytical] (Zhiling Liao 2023, [doi:10.1017/jfm.2023.475](https://doi.org/10.1017/jfm.2023.475))
- **C916.** Conceptual and numerical analysis shows that shoaling forced infragravity waves can radiate free long waves, with outcomes depending on phase and generation assumptions. *Regime: The Influence of Free Long Wave Generation on the Shoaling of Forced Infragravity Waves.* [direct_finding, numerical] (Moura 2019, [doi:10.3390/jmse7090305](https://doi.org/10.3390/jmse7090305))
- **C1746.** Short-wave groups generate infragravity waves through bound-wave forcing, breakpoint modulation, and bore merging; their subsequent shoaling, nonlinear transfer, breaking, friction, and reflection make them important controls on runup, sediment transport, overwash, reef hydrodynamics, and harbor resonance. *Regime: Group-forced surface waves typically below 0.04 Hz propagating from deep water through surf zones, beaches, tidal inlets, reef flats and lagoons, harbors, and the open ocean..* [literature_review_statement, review] (Xavier Bertin 2018, [doi:10.1016/j.earscirev.2018.01.002](https://doi.org/10.1016/j.earscirev.2018.01.002))

## Papers

- Xavier Bertin (2018). Infragravity waves: From driving mechanisms to impacts. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2018.01.002](https://doi.org/10.1016/j.earscirev.2018.01.002)
- J.A. Battjes (2004). Shoaling of subharmonic gravity waves. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2003jc001863](https://doi.org/10.1029/2003jc001863)
- Ap van Dongeren (2007). Shoaling and shoreline dissipation of low‐frequency waves. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2006jc003701](https://doi.org/10.1029/2006jc003701)
- Fabrice Ardhuin (2014). A numerical model for free infragravity waves: Definition and validation at regional and global scales. *Ocean Modelling*. [doi:10.1016/j.ocemod.2014.02.006](https://doi.org/10.1016/j.ocemod.2014.02.006)
- Rafael M.C. Guedes (2013). Observations of wave energy fluxes and swash motions on a low-sloping, dissipative beach. *Journal of Geophysical Research: Oceans*. [doi:10.1002/jgrc.20267](https://doi.org/10.1002/jgrc.20267)
- Ad Reniers (2002). Linear modeling of infragravity waves during Delilah. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2001jc001083](https://doi.org/10.1029/2001jc001083)
- Matthijs Gawehn (2016). Identification and classification of very low frequency waves on a coral reef flat. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2016jc011834](https://doi.org/10.1002/2016jc011834)
- Enrique M. Padilla (2017). Transfer and dissipation of energy during wave group propagation on a gentle beach slope. *Journal of Geophysical Research Oceans*. [doi:10.1002/2017jc012703](https://doi.org/10.1002/2017jc012703)
- Stephanie Contardo (2021). Free and Forced Components of Shoaling Long Waves in the Absence of Short-Wave Breaking. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-20-0214.1](https://doi.org/10.1175/jpo-d-20-0214.1)
- Yoshinao Matsuba (2022). Reconstruction of Directional Spectra of Infragravity Waves. *Journal of Geophysical Research Oceans*. [doi:10.1029/2021jc018273](https://doi.org/10.1029/2021jc018273)
- Maitane Olabarrieta (2023). Development and Application of an Infragravity Wave (InWave) Driver to Simulate Nearshore Processes. *Journal of Advances in Modeling Earth Systems*. [doi:10.1029/2022ms003205](https://doi.org/10.1029/2022ms003205)
- Johan Reyns (2023). Modelling wave group-scale hydrodynamics on orthogonal unstructured meshes. *Environmental Modelling &amp; Software*. [doi:10.1016/j.envsoft.2023.105655](https://doi.org/10.1016/j.envsoft.2023.105655)
- Stephen M. Henderson (2003). Simulations of Dissipative, Shore-Oblique Infragravity Waves. *Journal of Physical Oceanography*. [doi:10.1175/2398.1](https://doi.org/10.1175/2398.1)
- Thomas Guérin (2019). On the Bound Wave Phase Lag. *Fluids*. [doi:10.3390/fluids4030152](https://doi.org/10.3390/fluids4030152)
- Zhiling Liao (2023). Unified analytical solution for group-induced infragravity waves based on Green's function. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2023.475](https://doi.org/10.1017/jfm.2023.475)
- Moura (2019). The Influence of Free Long Wave Generation on the Shoaling of Forced Infragravity Waves. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7090305](https://doi.org/10.3390/jmse7090305)
