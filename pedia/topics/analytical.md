# Analytical methods

`analytical` | Closed-form and asymptotic coastal-process analysis.

Subtopics: [Linear wave theory](analytical.linear.md), [Nonlinear and asymptotic theory](analytical.nonlinear.md), [Similarity and scaling analysis](analytical.similarity.md)

Papers: 18. Claims: 10. Equations: 0.

## Synthesis

**Well established.** Analytical coastal models reduce conservation laws and boundary conditions to exact, approximate, asymptotic, similarity, perturbation, spectral, or reduced-order relations whose assumptions remain visible and testable.

**Governing physics.** Mass, momentum, energy and sediment conservation are closed with gravity, pressure, dispersion, nonlinearity, friction, turbulence or transport parameterizations and boundary conditions for the bed, shoreline, free surface, currents and structures.

**Dimensionless parameters.** Regime selection depends on relative depth, wave steepness, Ursell and Froude numbers, surf similarity, current-to-wave speed, relative bathymetric or boundary amplitude, bandwidth, sediment mobility and fall-velocity scaling, and ratios among forcing, dissipation and adjustment scales.

**Major equations.** Core families include potential-flow and free-surface boundary conditions, shallow-water and Boussinesq-type equations, wave-action and spectral balances, radiation-stress or momentum balances, Exner continuity, transport energetics, eigenvalue/scattering systems and perturbation expansions.

**Typical methods.** Methods nondimensionalize the governing problem, identify small or large parameters, impose idealized initial and boundary conditions, derive exact or asymptotic solutions, test limiting behavior, and compare with laboratory, field or converged numerical evidence.

**Numerical models.** Analytical solutions serve as standalone reduced-order models and verification benchmarks for spectral wave, shallow-water, Boussinesq, morphodynamic, scattering, wave-current and fluid-structure solvers.

**Experimental datasets.** The reviewed evidence connects theory to finite-depth crest and setup measurements, truncated-beach overtopping experiments, estuarine fetch/depth wave observations, and coastal wave or morphology datasets used to constrain asymptotic regimes.

**Validated ranges.** Examples span weakly nonlinear finite-depth waves, fetch- and depth-limited basins, long waves over gently varying or corrugated beds, idealized planar beaches, partial reflection, deformable boundaries and energetics-based sandy shoreface adjustment.

**Recent advances.** Recent analytical work increasingly couples currents, complex or compliant boundaries, partial reflections and morphology, and uses observations plus high-fidelity computation to map validity rather than presenting a closed form without an error regime.

**Disagreements.** Alternative closures can share conservation laws yet predict different asymptotes; exactness under idealized boundaries does not imply field accuracy; fitted empirical coefficients can outperform theory locally while transferring less reliably; formally higher order is not always better outside its scaling regime.

**Limitations.** Tractability usually requires simplified geometry, weak nonlinearity or dispersion, scale separation, prescribed closures, narrow spectra, uniform sediment or currents, and idealized boundaries; breaking, turbulence, three-dimensionality and stochastic forcing often enter indirectly.

**Open questions.** Priorities are analytical hierarchies for compound forcing, irregular directional waves, nonlinear breaking, mixed sediments, porous and deformable boundaries, coupled morphology, nonstationarity, uncertainty propagation and explicit transition criteria between model orders.

**Seminal papers.** Classical linear and nonlinear wave theories, shallow-water characteristics, perturbation and multiple-scale methods, radiation stress, spectral balances and sediment-continuity reductions established the analytical vocabulary used by coastal engineering.

## Claims

- **C999.** Reanalysis of fully developed wind seas relates asymptotic integral spectral limits to the source-term balances used to validate operational wave models. *Regime: Revisiting the Pierson–Moskowitz Asymptotic Limits for Fully Developed Wind Waves.* [direct_finding, analytical] (Jose-Henrique Alves 2003, [doi:10.1175/1520-0485(2003)033<1301:rtpalf>2.0.co;2](https://doi.org/10.1175/1520-0485(2003)033<1301:rtpalf>2.0.co;2))
- **C1000.** An energetics-based cross-shore sediment-transport formulation yields a mechanistic morphodynamic depth of closure rather than prescribing one solely from wave statistics. *Regime: Exploring shoreface dynamics and a mechanistic explanation for a morphodynamic depth of closure.* [direct_finding, analytical] (Alejandra C. Ortiz 2016, [doi:10.1002/2015jf003699](https://doi.org/10.1002/2015jf003699))
- **C1001.** Second-order three-dimensional finite-depth theory explains setup and surface-elevation and crest statistics when evaluated against controlled experimental data. *Regime: Second-Order Theory and Setup in Surface Gravity Waves: A Comparison with Experimental Data.* [direct_finding, mixed] (Alessandro Toffoli 2007, [doi:10.1175/2007jpo3634.1](https://doi.org/10.1175/2007jpo3634.1))
- **C1002.** Fetch- and depth-limited estuarine wind waves can be organized by nondimensional scaling that distinguishes growth constrained by basin geometry and water depth. *Regime: Wind Wave Behavior in Fetch and Depth Limited Estuaries.* [direct_finding, mixed] (Arash Karimpour 2017, [doi:10.1038/srep40654](https://doi.org/10.1038/srep40654))
- **C1003.** Weakly dispersive surface and internal waves admit reduced analytical descriptions of interacting long-wave structures, with applicability bounded by the asymptotic assumptions. *Regime: Analytical behavior of weakly dispersive surface and internal waves in the ocean.* [direct_finding, analytical] (Mohammad Asif Arefin 2021, [doi:10.1016/j.joes.2021.08.012](https://doi.org/10.1016/j.joes.2021.08.012))
- **C1004.** Theory and experiments for a truncated planar beach relate an individual incident wave to overtopped volume and identify the limits of idealized run-up representations. *Regime: Overtopping a truncated planar beach.* [direct_finding, mixed] (Andrew J. Hogg 2010, [doi:10.1017/s0022112010004325](https://doi.org/10.1017/s0022112010004325))
- **C1005.** An asymptotic solution describes Bragg scattering by variable bathymetry with a uniform current and floating membrane, exposing how current, depth variation, and compliance modify resonance. *Regime: Bragg scattering of gravity waves by a sea bed of varying depth in the presence of uniform current covered by a floating membrane.* [direct_finding, analytical] (Koushik Kanti Barman 2024, [doi:10.1063/5.0183629](https://doi.org/10.1063/5.0183629))
- **C1006.** A nonlinear shallow-water formulation coupled to an elastic sheet on a viscoelastic foundation describes wave propagation over a deformable seabed. *Regime: Nonlinear waves propagating over a deformable seafloor.* [direct_finding, analytical] (Vasily Kostikov 2024, [doi:10.1063/5.0227362](https://doi.org/10.1063/5.0227362))
- **C1007.** A free-long-wave framework with partial reflections resolves nearshore transformation relevant to inundation and shoreline or dune erosion. *Regime: Free Long-Wave Transformation in the Nearshore Zone through Partial Reflections.* [direct_finding, analytical] (Stephanie Contardo 2022, [doi:10.1175/jpo-d-22-0109.1](https://doi.org/10.1175/jpo-d-22-0109.1))
- **C1008.** Perturbation analysis shows how a wavy bed modifies currents induced by long waves approaching a beach, including nearshore and swash-zone circulation effects. *Regime: Currents induced by long waves propagating towards a beach over a wavy bed.* [direct_finding, analytical] (Harumichi Kyotoh 2000, [doi:10.1017/s0022112000008545](https://doi.org/10.1017/s0022112000008545))

## Papers

- Jose-Henrique Alves (2003). Revisiting the Pierson–Moskowitz Asymptotic Limits for Fully Developed Wind Waves. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(2003)033<1301:rtpalf>2.0.co;2](https://doi.org/10.1175/1520-0485(2003)033<1301:rtpalf>2.0.co;2) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/33/7/1520-0485_2003_033_1301_rtpalf_2.0.co_2.pdf)
- Alejandra C. Ortiz (2016). Exploring shoreface dynamics and a mechanistic explanation for a morphodynamic depth of closure. *Journal of Geophysical Research Earth Surface*. [doi:10.1002/2015jf003699](https://doi.org/10.1002/2015jf003699) [published version, read only](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015JF003699)
- Alessandro Toffoli (2007). Second-Order Theory and Setup in Surface Gravity Waves: A Comparison with Experimental Data. *Journal of Physical Oceanography*. [doi:10.1175/2007jpo3634.1](https://doi.org/10.1175/2007jpo3634.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/37/11/2007jpo3634.1.pdf)
- Arash Karimpour (2017). Wind Wave Behavior in Fetch and Depth Limited Estuaries. *Scientific Reports*. [doi:10.1038/srep40654](https://doi.org/10.1038/srep40654) [published version, CC BY](https://www.nature.com/articles/srep40654.pdf)
- Mohammad Asif Arefin (2021). Analytical behavior of weakly dispersive surface and internal waves in the ocean. *Journal of Ocean Engineering and Science*. [doi:10.1016/j.joes.2021.08.012](https://doi.org/10.1016/j.joes.2021.08.012) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S2468013321000802/pdf)
- Andrew J. Hogg (2010). Overtopping a truncated planar beach. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112010004325](https://doi.org/10.1017/s0022112010004325) [submitted manuscript, read only](https://strathprints.strath.ac.uk/29110/1/download.pdf)
- Koushik Kanti Barman (2024). Bragg scattering of gravity waves by a sea bed of varying depth in the presence of uniform current covered by a floating membrane. *Physics of Fluids*. [doi:10.1063/5.0183629](https://doi.org/10.1063/5.0183629) [published version, read only](https://pubs.aip.org/aip/pof/article-pdf/doi/10.1063/5.0183629/18340231/012118_1_5.0183629.pdf)
- Vasily Kostikov (2024). Nonlinear waves propagating over a deformable seafloor. *Physics of Fluids*. [doi:10.1063/5.0227362](https://doi.org/10.1063/5.0227362) [accepted manuscript, read only](https://discovery.dundee.ac.uk/ws/files/141975236/KHE_PoF_2024_ACCEPTED.pdf)
- Stephanie Contardo (2022). Free Long-Wave Transformation in the Nearshore Zone through Partial Reflections. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-22-0109.1](https://doi.org/10.1175/jpo-d-22-0109.1) [submitted manuscript, read only](https://archimer.ifremer.fr/doc/00823/93491/100238.pdf)
- Harumichi Kyotoh (2000). Currents induced by long waves propagating towards a beach over a wavy bed. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112000008545](https://doi.org/10.1017/s0022112000008545) [submitted manuscript, read only](https://tsukuba.repo.nii.ac.jp/record/7563/files/JFM_413.pdf)
- Gourlay (2005). Wave-generated flow on coral reefs—an analysis for two-dimensional horizontal reef-tops with steep faces. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.11.007](https://doi.org/10.1016/j.coastaleng.2004.11.007)
- van Veelen (2021). Modelling wave attenuation by quasi-flexible coastal vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103820](https://doi.org/10.1016/j.coastaleng.2020.103820) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383920305068?httpAccept=text/xml)
- Liu (2019). Characterization and prediction of tropical cyclone forerunner surge. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.01.005](https://doi.org/10.1016/j.coastaleng.2019.01.005) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383918301224?httpAccept=text/xml)
- Hinwood (2018). Tidal inlets and estuaries: Comparison of Bruun, Escoffier, O'Brien and attractors. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.12.008](https://doi.org/10.1016/j.coastaleng.2017.12.008) [preprint, read only](https://www.researchgate.net/publication/323489746_Tidal_inlets_and_estuaries_Comparison_of_Bruun_Escoffier_O%27Brien_and_attractors)
- Liu (2024). A theoretical model for wave attenuation by vegetation considering current effects. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104508](https://doi.org/10.1016/j.coastaleng.2024.104508)
- Hlophe (2026). Wave-induced overturning moments, moment arms, and associated forces on monopile foundations. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105055](https://doi.org/10.1016/j.coastaleng.2026.105055) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383926001092?httpAccept=text/xml)
- Alipour (2026). Characterization of tropical cyclone surge evolution. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105086](https://doi.org/10.1016/j.coastaleng.2026.105086)
- van Veelen (2022). Corrigendum to “Modelling wave attenuation by quasi-flexible coastal vegetation” [Coast. Eng. 164 (2021) 103820]. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104165](https://doi.org/10.1016/j.coastaleng.2022.104165) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383922000801?httpAccept=text/xml)
