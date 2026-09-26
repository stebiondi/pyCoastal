# Wave generation

`waves.generation` | Wind-wave generation and source processes.

Parent: [Waves and wave transformation](waves.md)

Subtopics: [Extreme wave climates](waves.generation.extremes.md), [Wind-wave growth](waves.generation.wind.md)

Papers: 14. Claims: 13. Equations: 0.

## Synthesis

**Well established.** Surface waves are generated when pressure or moving boundaries do work on the free surface; their spectra then evolve through propagation, bathymetric refraction/focusing, nonlinear resonant transfer, currents, breaking and dissipation.

**Governing physics.** Generation requires kinematic and dynamic free-surface compatibility. Linear sources radiate dispersive modes; finite amplitude creates bound harmonics and resonant energy exchange; shear currents modify dispersion and modulation stability; absorption suppresses reflected contamination.

**Dimensionless parameters.** Controls include relative depth kh, wave steepness ka, Ursell and Benjamin–Feir indices, bandwidth and directional spread, current-to-phase-speed ratio, source or paddle stroke, sponge length/wavelength, Courant and grid resolution, and target focus distance/time.

**Major equations.** Core formulations include linear potential-flow free-surface conditions with applied pressure or wavemaker motion, Boussinesq and Navier–Stokes wave tanks, spectral action balance with nonlinear source terms, Hasselmann interaction integrals, and nonlinear Schrödinger/Alber modulation equations.

**Typical methods.** Methods use analytical source solutions, perturbation theory, spectral interaction approximations, flap/piston/bottom-tilting wavemakers, internal or pressure sources, active or sponge absorption, Boussinesq/RANS/VOF/DNS tanks, phase focusing and spectral validation.

**Numerical models.** Represented approaches include potential-flow pressure forcing, Hasselmann and discrete four-wave source terms, Boussinesq generating–absorbing layers, OpenFOAM free-surface solvers, RANS bottom-tilting wavemakers, DNS breaking waves and Alber stochastic spectral dynamics.

**Experimental datasets.** Evidence includes controlled oscillating-pressure and wavemaker configurations, level-bottom breaking-wave tanks, irregular runup generation with second-order corrections, focusing-wave spectra and bottom-tilting long-wave generation.

**Validated ranges.** The branch spans linear to breaking waves, gravity–capillary and gravity regimes, shallow through intermediate depth, monochromatic, irregular, focused and random spectra, quiescent and shear-current cases, and physical plus numerical wave tanks.

**Recent advances.** Recent work improves generating–absorbing layers, alternative OpenFOAM solvers, DNS of generated breaking waves, spectrum-aware focusing, RANS bottom-tilting long-wave makers and stochastic modulation over shear currents.

**Disagreements.** Different generators can match surface elevation while differing in bound harmonics, velocity, pressure or reflected energy; approximate nonlinear source terms trade accuracy for speed; VOF, level-set and alternative interface solvers differ in conservation and numerical dissipation.

**Limitations.** Broad directional seas and long runs expose reflection, phase and mass-conservation errors; high-order corrections are bandwidth- and depth-limited; breaking is resolution sensitive; spectral closures omit phase; controlled generation is not identical to natural wind input.

**Open questions.** Needs include reflection-free broadband directional generation, coupled current/source design, consistent higher-order kinematics, automatic calibration across solvers, uncertainty in nonlinear transfer, and efficient phase-aware generation from field spectra.

**Seminal papers.** Perturbation theory and nonlinear interaction parameterizations established spectral redistribution, while linear pressure and boundary radiation solutions established controlled free-surface generation.

## Claims

- **C942.** For the idealized two-dimensional oscillating-water-column device, linear surface-wave theory shows that air compressibility can materially affect performance, phase-shifted turbine response can reduce chamber and turbine size with little loss of regular-wave extraction, and the two tested strongly nonlinear take-off laws retain peak efficiencies close to the linear optimum. *Regime: Regular waves acting on a simple two-dimensional oscillating-water-column in uniform depth, with shallow structural draught except for the optional vertical wall..* [direct_finding, analytical] (Sarmento 1985, [doi:10.1017/s0022112085000234](https://doi.org/10.1017/s0022112085000234))
- **C943.** Hasselmann perturbation theory shows gravity–capillary spectra exchange energy through second-order resonant interactions with higher-order redistribution. *Regime: Nonlinear energy transfer in gravity–capillary wave spectra, with applications.* [direct_finding, analytical] (Valenzuela 1972, [doi:10.1017/s0022112072000849](https://doi.org/10.1017/s0022112072000849))
- **C944.** Direct numerical simulations quantify statistics, kinematics and dissipation of shallow-water breaking waves generated by a wave plate at constant depth. *Regime: Wave statistics and energy dissipation of shallow-water breaking waves in a tank with a level bottom.* [direct_finding, numerical] (Shuo Liu 2023, [doi:10.1017/jfm.2023.876](https://doi.org/10.1017/jfm.2023.876))
- **C945.** Alternative OpenFOAM free-surface solvers provide numerical-wave-tank generation and propagation options beyond conventional VOF interFoam practice. *Regime: Beyond VoF: alternative OpenFOAM solvers for numerical wave tanks.* [direct_finding, numerical] (Pál Schmitt 2020, [doi:10.1007/s40722-020-00173-9](https://doi.org/10.1007/s40722-020-00173-9))
- **C946.** Quasi-coherent stochastic theory represents interference and refractive focusing of swell over variable depth that radiative-transfer models cannot resolve. *Regime: Stochastic Modeling of Coherent Wave Fields over Variable Depth.* [direct_finding, analytical] (Pieter Smit 2015, [doi:10.1175/jpo-d-14-0219.1](https://doi.org/10.1175/jpo-d-14-0219.1))
- **C947.** A Boussinesq model combines a generating–absorbing sponge layer with second-order irregular-wave generation to support long-duration runup simulations. *Regime: Irregular wave runup statistics on plane beaches: Application of a Boussinesq-type model incorporating a generating–absorbing sponge layer and second-order wave generation.* [direct_finding, numerical] (Colm J. Fitzgerald 2016, [doi:10.1016/j.coastaleng.2016.04.019](https://doi.org/10.1016/j.coastaleng.2016.04.019))
- **C948.** Four-wave nonlinear interaction source terms materially shape modeled ocean-wave spectra and their redistribution across frequency. *Regime: Role of Nonlinear Four-Wave Interactions Source Term on the Spectral Shape.* [literature_review_statement, review] (Ponce de León 2020, [doi:10.3390/jmse8040251](https://doi.org/10.3390/jmse8040251))
- **C949.** Three-wave theory gives sufficient conditions and amplitude bounds for unidirectional nonlinear energy transfer into one wave from two interacting waves. *Regime: Unidirectional energy transfer in nonlinear wave-wave interactions.* [direct_finding, analytical] (Wang 1973, [doi:10.1063/1.1666416](https://doi.org/10.1063/1.1666416))
- **C950.** Numerical experiments show input amplitude spectra control the accuracy and evolution of prescribed focusing-wave generation. *Regime: Numerical investigation of wave amplitude spectra effects on focusing wave generation.* [direct_finding, numerical] (Guochun Xu 2022, [doi:10.1016/j.oceaneng.2022.112550](https://doi.org/10.1016/j.oceaneng.2022.112550))
- **C951.** RANS simulations characterize the generation mechanism and wave forms produced by a bottom-tilting flume wavemaker designed for long waves. *Regime: Numerical Investigation of Wave Generation Characteristics of Bottom-Tilting Flume Wavemaker.* [direct_finding, numerical] (Hsin-Erh Wang 2020, [doi:10.3390/jmse8100769](https://doi.org/10.3390/jmse8100769))
- **C952.** A fourth-order nonlinear Schrödinger/Alber framework predicts modulation stability of random surface-wave spectra over linear shear currents. *Regime: NONLINEAR MODULATION OF RANDOM WAVE SPECTRA FOR SURFACE-GRAVITY WAVES WITH LINEAR SHEAR CURRENTS.* [direct_finding, analytical] (MUKHERJEE 2024, [doi:10.1017/s1446181124000269](https://doi.org/10.1017/s1446181124000269))
- **C1275.** ECMWF hindcasts and MIKE21 SW propagation estimate mean wave power of 15.25 kW/m offshore and 11.43 kW/m at the 20 m isobath on the north-central Santa Catarina coast, dominated by southeastern waves. *Regime: Wave Energy Resource along the Coast of Santa Catarina (Brazil).* [direct_finding, numerical] (Pasquale Contestabile 2015, [doi:10.3390/en81212423](https://doi.org/10.3390/en81212423))
- **C1427.** Sea-surface roughness scales with wave height and steepness across tanks, lakes, and coastal seas, while shoaling and swell systematically alter the effective roughness. *Regime: The Dependence of Sea Surface Roughness on the Height and Steepness of the Waves.* [direct_finding, mixed] (Peter K. Taylor 2001, [doi:10.1175/1520-0485(2001)031<0572:tdossr>2.0.co;2](https://doi.org/10.1175/1520-0485(2001)031<0572:tdossr>2.0.co;2))

## Papers

- Peter K. Taylor (2001). The Dependence of Sea Surface Roughness on the Height and Steepness of the Waves. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(2001)031<0572:tdossr>2.0.co;2](https://doi.org/10.1175/1520-0485(2001)031<0572:tdossr>2.0.co;2) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/31/2/1520-0485_2001_031_0572_tdossr_2.0.co_2.pdf)
- Sarmento (1985). Wave generation by an oscillating surface-pressure and its application in wave-energy extraction. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112085000234](https://doi.org/10.1017/s0022112085000234) [accepted manuscript, read only](https://www.researchgate.net/publication/231844373_Wave_generation_by_an_oscillating_surface-pressure_and_its_application_in_wave-energy_extraction)
- Pasquale Contestabile (2015). Wave Energy Resource along the Coast of Santa Catarina (Brazil). *Energies*. [doi:10.3390/en81212423](https://doi.org/10.3390/en81212423) [published version, CC BY](https://mdpi-res.com/d_attachment/energies/energies-08-12423/article_deploy/energies-08-12423.pdf)
- Valenzuela (1972). Nonlinear energy transfer in gravity–capillary wave spectra, with applications. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112072000849](https://doi.org/10.1017/s0022112072000849)
- Shuo Liu (2023). Wave statistics and energy dissipation of shallow-water breaking waves in a tank with a level bottom. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2023.876](https://doi.org/10.1017/jfm.2023.876) [published version, CC BY](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A85C764857124B9D6EE12EE0A3F660BE/S0022112023008765a.pdf/div-class-title-wave-statistics-and-energy-dissipation-of-shallow-water-breaking-waves-in-a-tank-with-a-level-bottom-div.pdf)
- Pál Schmitt (2020). Beyond VoF: alternative OpenFOAM solvers for numerical wave tanks. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-020-00173-9](https://doi.org/10.1007/s40722-020-00173-9) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s40722-020-00173-9.pdf)
- Pieter Smit (2015). Stochastic Modeling of Coherent Wave Fields over Variable Depth. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-14-0219.1](https://doi.org/10.1175/jpo-d-14-0219.1) [published version, public domain](https://journals.ametsoc.org/downloadpdf/journals/phoc/45/4/jpo-d-14-0219.1.pdf)
- Colm J. Fitzgerald (2016). Irregular wave runup statistics on plane beaches: Application of a Boussinesq-type model incorporating a generating–absorbing sponge layer and second-order wave generation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.019](https://doi.org/10.1016/j.coastaleng.2016.04.019) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0378383916300667/pdf)
- Ponce de León (2020). Role of Nonlinear Four-Wave Interactions Source Term on the Spectral Shape. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8040251](https://doi.org/10.3390/jmse8040251) [published version, CC BY](https://doi.org/10.3390/jmse8040251)
- Wang (1973). Unidirectional energy transfer in nonlinear wave-wave interactions. *Journal of Mathematical Physics*. [doi:10.1063/1.1666416](https://doi.org/10.1063/1.1666416)
- Guochun Xu (2022). Numerical investigation of wave amplitude spectra effects on focusing wave generation. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2022.112550](https://doi.org/10.1016/j.oceaneng.2022.112550) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0029801822018339/pdf)
- Hsin-Erh Wang (2020). Numerical Investigation of Wave Generation Characteristics of Bottom-Tilting Flume Wavemaker. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8100769](https://doi.org/10.3390/jmse8100769) [published version, CC BY](https://www.mdpi.com/2077-1312/8/10/769/pdf?version=1603175678)
- MUKHERJEE (2024). NONLINEAR MODULATION OF RANDOM WAVE SPECTRA FOR SURFACE-GRAVITY WAVES WITH LINEAR SHEAR CURRENTS. *The ANZIAM Journal*. [doi:10.1017/s1446181124000269](https://doi.org/10.1017/s1446181124000269) [published version, read only](https://www.researchgate.net/publication/387917502_NONLINEAR_MODULATION_OF_RANDOM_WAVE_SPECTRA_FOR_SURFACE-GRAVITY_WAVES_WITH_LINEAR_SHEAR_CURRENTS)
- Luigi Cavaleri (2007). Wave modelling – The state of the art. *Progress In Oceanography*. [doi:10.1016/j.pocean.2007.05.005](https://doi.org/10.1016/j.pocean.2007.05.005) [accepted manuscript, read only](http://nora.nerc.ac.uk/id/eprint/2732/1/WISE_the_state_of_the_art.pdf)
