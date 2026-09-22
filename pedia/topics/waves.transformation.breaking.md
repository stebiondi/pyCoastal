# Breaking

`waves.transformation.breaking` | Wave instability and breaking.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md)

Subtopics: [Breaking criteria](waves.transformation.breaking.criteria.md), [Energy dissipation](waves.transformation.breaking.dissipation.md), [Wave runup](waves.transformation.breaking.runup.md), [Wave setup](waves.transformation.breaking.setup.md), [Breaking-induced turbulence](waves.transformation.breaking.turbulence.md)

Papers: 6. Claims: 5. Equations: 0.

## Synthesis

**Well established.** Surface-gravity waves break when nonlinear crest evolution can no longer remain kinematically and dynamically coherent. Breaking limits wave height, converts organized wave energy into turbulence, currents and heat, and drives setup, runup, sediment suspension and impulsive structural loading.

**Governing physics.** Shoaling raises wave height and steepness as depth decreases, while dispersion, refraction, currents, wind and bathymetry modify crest speed and energy flux. At onset the crest overturns or spills; roller evolution and turbulent transport then redistribute momentum and dissipation through the water column and toward the bed.

**Dimensionless parameters.** Important controls include relative wave height H/h, deep-water or local steepness kH, surf-similarity or Iribarren number, breaker index Hb/hb, crest-speed ratios used in onset criteria, Reynolds and Froude numbers, relative bar or structure geometry, and wind speed normalized by crest propagation speed Uw/C.

**Major equations.** Core descriptions combine conservation of mass and momentum with wave-action or energy-flux balance. Breaking onset is represented by depth-index, steepness, kinematic or crest-energy-flux criteria; phase-averaged models add a dissipation source term, while Navier–Stokes, LES or RANS models resolve or close the post-onset turbulent flow.

**Typical methods.** Breaking is studied with wave flumes and large basins, field pressure/velocity arrays, lidar and georectified video; onset and dissipation are reproduced with spectral, Boussinesq, Serre–Green–Naghdi, potential-flow, RANS, LES and volume-of-fluid models. Validation should distinguish onset location, breaker type, wave-height decay and turbulence.

**Numerical models.** Model fidelity ranges from representative-wave and spectral energy balances with empirical breaking sinks to nonlinear shallow-water/Boussinesq families and interface-resolving Navier–Stokes solvers. Potential-flow models describe pre-onset evolution but require a breaking treatment; turbulence-resolving methods are more expensive and remain sensitive to closure and resolution.

**Experimental datasets.** Reviewed evidence spans field-scale shoaling-soliton experiments with lidar and imagery, Timex-video observations at five Atlantic-coast sites, three laboratory datasets used to compare dissipation models, ten natural-beach campaigns supporting setup/runup parameterization, and large-scale plunging-breaker measurements over a fixed bar.

**Validated ranges.** The Timex methods were tested over roughly 900 records and breaking heights of 0.1–3.8 m, with about 18% average normalized RMSE for the bathymetry-free method. A revised bore-based dissipation formulation had the smallest wave-height error among four models across three datasets; these results remain conditional on their tested beaches and calibrations.

**Recent advances.** Recent advances combine crest-resolved onset diagnostics across arbitrary depth, field-scale lidar and video, machine-learning image segmentation, enhanced fully nonlinear shallow-water solvers, and LES or interface-resolving simulations that expose coherent vortices, energy pathways and structure interaction.

**Disagreements.** No single onset indicator or dissipation closure is uniformly accepted from deep to shallow water and from spilling to plunging breakers. Depth-index and steepness criteria are convenient but site-dependent; crest-based criteria seek broader physics, while operational phase-averaged models still require empirical post-onset dissipation parameters.

**Limitations.** Breaking is intermittent, three-dimensional and aerated, making crest geometry, void fraction and near-bed turbulence difficult to measure. Scale effects, uncertain bathymetry, finite image resolution, breaker-type ambiguity, turbulence closure, grid convergence and calibration transfer can dominate apparent model skill.

**Open questions.** Priorities include a transferable onset-to-dissipation framework, directional and current-modified breaking, wind effects on crest overturning, air entrainment and bubble-mediated dissipation, turbulence transport to the bed, data-assimilative remote sensing, and quantified uncertainty across laboratory-to-field scales.

**Seminal papers.** Classical limiting-wave, breaker-index and surf-similarity studies established depth- and slope-controlled descriptions; radiation-stress and bore analogies connected breaking to mean flow and energy loss. Later crest-kinematic and energy-flux approaches reframed onset as a local dynamical threshold.

## Claims

- **C33.** The model validation in this paper is limited to non-breaking wave propagation because explicit wave-breaking treatment was not implemented. *Regime: All accuracy and efficiency claims reported in the four validation cases..* [direct_finding, numerical] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C1279.** Breaking over 2–8 m deep rocky ridges generated an observed 0.3–0.4 m/s jet, more than four times the maximum tidal current; coupled SWAN–Delft3D simulations captured timing and direction but overpredicted breaking and speed. *Regime: A wave‐driven jet over a rocky shoal.* [direct_finding, mixed] (Ryan P. Mulligan 2010, [doi:10.1029/2009jc006027](https://doi.org/10.1029/2009jc006027))
- **C1539.** Since the 1990s, the modulational instability has commonly been used to explain the occurrence of rogue waves that appear from nowhere in the open ocean. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Francesco Fedele 2016, [doi:10.1038/srep27715](https://doi.org/10.1038/srep27715))
- **C1543.** A concept of wave‐amplitude‐based Reynolds number is suggested which is hypothesised to indicate a transition from laminarity to turbulence for the wave‐induced motion. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Alexander V. Babanin 2006, [doi:10.1029/2006gl027308](https://doi.org/10.1029/2006gl027308))
- **C1546.** The large-scale vortex structures under spilling and plunging breakers are investigated, using a fully three-dimensional large-eddy simulation (LES). *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Yasunori WATANABE 2005, [doi:10.1017/s0022112005006774](https://doi.org/10.1017/s0022112005006774))

## Papers

- Ryan P. Mulligan (2010). A wave‐driven jet over a rocky shoal. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2009jc006027](https://doi.org/10.1029/2009jc006027)
- Abbas Khayyer (2007). Corrected Incompressible SPH method for accurate water-surface tracking in breaking waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.10.001](https://doi.org/10.1016/j.coastaleng.2007.10.001)
- Francesco Fedele (2016). Real world ocean rogue waves explained without the modulational instability. *Scientific Reports*. [doi:10.1038/srep27715](https://doi.org/10.1038/srep27715)
- Alexander V. Babanin (2006). On a wave‐induced turbulence and a wave‐mixed upper ocean layer. *Geophysical Research Letters*. [doi:10.1029/2006gl027308](https://doi.org/10.1029/2006gl027308)
- Yasunori WATANABE (2005). Three-dimensional vortex structures under breaking waves. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112005006774](https://doi.org/10.1017/s0022112005006774)
- Umberto Andriolo (2020). Breaking Wave Height Estimation from Timex Images: Two Methods for Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs12020204](https://doi.org/10.3390/rs12020204)
