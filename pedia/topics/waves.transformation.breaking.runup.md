# Wave runup

`waves.transformation.breaking.runup` | Uprush and maximum excursion.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md) > [Breaking](waves.transformation.breaking.md)

Papers: 14. Claims: 9. Equations: 0.

Used by pyCoastal design modules: Storm surge and flooding.

## Synthesis

**Well established.** Wave runup is the time-varying vertical shoreline excursion above the still-water reference and combines mean setup with swash. It is a major component of total water level, overtopping, overwash and erosion, and depends jointly on offshore wave scale, spectral content, water level, beach or structure slope and local geometry.

**Governing physics.** Incident-band waves shoal and break, transferring energy to setup, infragravity motions and swash. Reflection and resonance become more important on steep or structured shores, while dissipation dominates many mild beaches; reefs, bars, permeability and alongshore-variable foreshores alter the energy reaching the shoreline.

**Dimensionless parameters.** Key controls include Iribarren number, foreshore slope, deep-water steepness H0/L0, relative water depth, normalized runup R/H0 or R/sqrt(H0L0), reef or bar freeboard relative to wave height, permeability parameters, directional spread and nondimensional spectral frequency.

**Major equations.** Common predictors scale runup with the deep-water wave length-height product and foreshore slope, often through terms proportional to beta_f sqrt(H0 L0), with separate incident and infragravity swash components. Process models solve nonlinear shallow-water or Boussinesq-family equations with moving shorelines and breaking dissipation.

**Typical methods.** Runup is measured with pressure sensors, resistance staffs, lidar, video and laser transects; empirical formulas use offshore waves and local slope, while phase-resolving Boussinesq, nonhydrostatic and XBeach-family models generate shoreline time series. Hazard work commonly reports mean setup plus exceedance levels such as R2%.

**Numerical models.** Empirical formulations are efficient for screening, Boussinesq and nonhydrostatic models resolve incident and infragravity phases, and XBeach Surfbeat represents grouped-wave forcing at lower cost. Model choice controls whether setup, swash, phase uncertainty, infiltration, overtopping and morphology are explicitly resolved.

**Experimental datasets.** Reviewed evidence includes ten natural-beach campaigns behind the Stockdon parameterization, 180 idealized directional-spectrum simulations over slopes 0.02–0.04, reef-to-island field transects, long-duration irregular plane-beach simulations, a laser-observed gravel-barrier storm and experiments comparing permeable and impermeable slopes.

**Validated ranges.** The directional-spread study was limited to mostly dissipative slopes of 0.02–0.04; its normalized infragravity runup lacked obvious slope dependence within that narrow range. At Loe Bar, XBeach-G reproduced observed overwash hydrodynamics within 5% for the documented storm, but this does not establish universal gravel-barrier skill.

**Recent advances.** Recent work couples dense lidar or laser observations with phase-resolving models, represents infragravity and bimodal spectra more explicitly, uses physics-informed machine learning to emulate higher-fidelity runup, and propagates runup uncertainty through ensemble flood and erosion assessments.

**Disagreements.** Slope dependence differs by regime and response component: local foreshore slope materially improves runup prediction on intermediate and reflective beaches, whereas infragravity runup showed little slope dependence across a narrow dissipative range. These findings are conditional rather than contradictory and should not be merged into one universal formula.

**Limitations.** Uncertain bathymetry and local slope, shoreline-definition choices, sparse extreme observations, phase information absent from spectra, directional spreading, low-frequency boundary conditions, roughness, infiltration and morphology change can dominate error. Empirical coefficients and numerical calibration transfer poorly outside their source regime.

**Open questions.** Needs include phase-aware probabilistic runup, joint tide-surge-wave dependence, transferable rough/permeable/reef formulations, alongshore variability, dynamically evolving morphology, efficient nonhydrostatic ensembles, uncertainty-aware remote sensing and validation during rare overtopping or overwash events.

**Seminal papers.** Classical plane-beach and surf-similarity work linked maximum excursion to wave steepness and slope; later field parameterizations separated setup and swash and established practical exceedance formulas. Moving-shoreline nonlinear-wave benchmarks underpin modern phase-resolving validation.

## Claims

- **C99.** On intermediate and reflective beaches with complex foreshores, substituting an alongshore-averaged slope can introduce substantial runup error relative to the locally measured slope. *Regime: Intermediate and reflective beaches with alongshore-variable foreshore topography..* [direct_finding, field] (Stockdon 2006, [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005))
- **C1553.** Waves observed in the inner surf and swash zones of a fine grained, gently sloping beach are modeled accurately with the nonlinear shallow water equations. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Britt Raubenheimer 1995, [doi:10.1029/95jc00232](https://doi.org/10.1029/95jc00232))
- **C1556.** Vertical flow structure and turbulent dissipation in the swash zone are estimated using cross‐shore fluid velocities observed on a low‐sloped, fine‐grained sandy beach [ Raubenheimer, 2002 ] with two stacks of three current meters located about 2, 5, and 8 cm above the bed. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Britt Raubenheimer 2004, [doi:10.1029/2003jc001877](https://doi.org/10.1029/2003jc001877))
- **C1561.** Abstract. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Diana Di Luccio 2018, [doi:10.5194/nhess-18-2841-2018](https://doi.org/10.5194/nhess-18-2841-2018))
- **C1564.** Abstract The present study uses nine machine learning (ML) methods to predict wave runup in an innovative and comprehensive methodology. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Durap 2023, [doi:10.1007/s44218-023-00033-7](https://doi.org/10.1007/s44218-023-00033-7))
- **C1568.** Abstract Observations on a mildly sloping beach suggest that the largest runup events are related to bore‐bore capture (BBC). *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Gabriel García‐Medina 2017, [doi:10.1002/2017jc012862](https://doi.org/10.1002/2017jc012862))
- **C1569.** A field experiment was conducted at a tropical microtidal intermediate sandy beach with a low tide terrace (Nha Trang, Vietnam) to investigate the short-term swash-zone hydrodynamics and morphodynamics under variable wave conditions. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Luís Pedro Almeida 2020, [doi:10.3390/jmse8050302](https://doi.org/10.3390/jmse8050302))
- **C1574.** Abstract The propagation of bichromatic wave groups with differences in the wave‐group structure and its influence in long‐wave generation are investigated. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Enrique M. Padilla 2018, [doi:10.1029/2018jc014213](https://doi.org/10.1029/2018jc014213))
- **C1640.** Focused-wave flume tests and a calibrated Boussinesq–nonlinear-shallow-water model show extreme runup depends jointly on focus amplitude, location and phase rather than spectral parameters alone; second-order wavemaker correction removed about 60% of subharmonic error that otherwise inflated runup. *Regime: Focused wave groups on the tested plane beach, amplitudes, phases and focus locations..* [direct_finding, mixed] (Colin Whittaker 2017, [doi:10.1016/j.coastaleng.2016.12.001](https://doi.org/10.1016/j.coastaleng.2016.12.001))

## Papers

- Colin Whittaker (2017). Optimisation of focused wave group runup on a plane beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.12.001](https://doi.org/10.1016/j.coastaleng.2016.12.001) [accepted manuscript, read only](https://api.research-repository.uwa.edu.au/ws/files/150932115/Whittaker_et_al_2017_Optimisation_focused_wave_group_runup_CEng_AAM.pdf)
- Stockdon (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005)
- Britt Raubenheimer (1995). Swash on a gently sloping beach. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/95jc00232](https://doi.org/10.1029/95jc00232) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/95JC00232)
- Denys Dutykh (2011). Finite volume schemes for dispersive wave propagation and runup. *Journal of Computational Physics*. [doi:10.1016/j.jcp.2011.01.003](https://doi.org/10.1016/j.jcp.2011.01.003) [preprint, read only](https://arxiv.org/pdf/1004.1950)
- Britt Raubenheimer (2004). Observations of swash zone velocities: A note on friction coefficients. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2003jc001877](https://doi.org/10.1029/2003jc001877) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2003JC001877)
- Diana Di Luccio (2018). Wave run-up prediction and observation in a micro-tidal beach. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-18-2841-2018](https://doi.org/10.5194/nhess-18-2841-2018) [published version, CC BY](https://nhess.copernicus.org/articles/18/2841/2018/nhess-18-2841-2018.pdf)
- Durap (2023). A comparative analysis of machine learning algorithms for predicting wave runup. *Anthropocene Coasts*. [doi:10.1007/s44218-023-00033-7](https://doi.org/10.1007/s44218-023-00033-7) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s44218-023-00033-7.pdf)
- Leont'yev (1996). Numerical modelling of beach erosion during storm event. *Coastal Engineering*. [doi:10.1016/s0378-3839(96)00029-4](https://doi.org/10.1016/s0378-3839(96)00029-4)
- Gabriel García‐Medina (2017). Large runup controls on a gently sloping dissipative beach. *Journal of Geophysical Research Oceans*. [doi:10.1002/2017jc012862](https://doi.org/10.1002/2017jc012862) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2017JC012862)
- Luís Pedro Almeida (2020). Lidar Observations of the Swash Zone of a Low-Tide Terraced Tropical Beach under Variable Wave Conditions: The Nha Trang (Vietnam) COASTVAR Experiment. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8050302](https://doi.org/10.3390/jmse8050302) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-08-00302/article_deploy/jmse-08-00302-v2.pdf)
- Enrique M. Padilla (2018). Long Wave Generation Induced by Differences in the Wave‐Group Structure. *Journal of Geophysical Research Oceans*. [doi:10.1029/2018jc014213](https://doi.org/10.1029/2018jc014213) [published version, CC BY](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2018JC014213)
- Rafaël Almar (2018). A new remote predictor of wave reflection based on runup asymmetry. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2018.10.018](https://doi.org/10.1016/j.ecss.2018.10.018) [accepted manuscript, read only](https://purehost.bath.ac.uk/ws/portalfiles/portal/189538102/Manuscript_20181011.pdf)
- Han-Jing Dai (2016). Entrained air in bore-driven swash on an impermeable rough slope. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.10.002](https://doi.org/10.1016/j.coastaleng.2016.10.002) [accepted manuscript, CC BY-NC-ND](https://aura.abdn.ac.uk/bitstream/2164/9830/1/Revised_Manuscript_R2.pdf)
- Hallin (2025). RoadRAT – A new framework to assess the probability of inundation, wave runup, and erosion impacting coastal roads. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104741](https://doi.org/10.1016/j.coastaleng.2025.104741) [published version, CC BY](https://curis.ku.dk/ws/files/437990286/RoadRAT.pdf)
