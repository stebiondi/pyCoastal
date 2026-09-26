# Wave-flume experiments

`laboratory.flumes` | Two-dimensional physical modeling.

Parent: [Laboratory experiments](laboratory.md)

Papers: 19. Claims: 9. Equations: 5.

## Synthesis

**Well established.** Wave flumes isolate coastal processes under repeatable forcing and support direct measurement, empirical relation development, and numerical-model validation, but results remain conditional on scale, geometry, boundary reflections, wave generation, material similarity, and instrumentation.

**Governing physics.** Across reviewed experiments the governing processes include wave shoaling, breaking, runup, overtopping and transmission; air-water resonance; groundwater exchange; sediment thresholds and phase lag; vegetation drag; wave impact and erosion; and nonlinear structural loading.

**Dimensionless parameters.** Key controls include Froude and Reynolds similarity, relative depth and freeboard, wave steepness and Ursell number, mobility and Shields-type numbers, settling-time factor, relative vegetation submergence and density, Keulegan-Carpenter number, and normalized transmission, runup, pressure, and force.

**Major equations.** The evidence uses mobility and Ursell threshold relations, ripple-migration transport and settling-time factors, overtopping transmission normalized by theoretical runup, RANS-VOF and groundwater equations, impact and erosion formulae, vegetation-drag attenuation, and harmonic force decomposition.

**Typical methods.** Methods include regular and irregular wave generation, large-scale profile tests, movable and permeable beds, pressure and force sensing, water-level and groundwater measurement, bed surveys, vegetation mimics, phase manipulation, empirical regression, and coupled model-data comparison.

**Numerical models.** Models tested against flume data include RANS-VOF hydrodynamics coupled to SEAWAT-2000, a process-oriented sea-dike breach model, empirical ripple thresholds, Ribberink bedload comparison, overtopping transmission relations, cliff-notch force formulae, vegetation attenuation closures, and harmonic load reconstructions.

**Experimental datasets.** The branch now links OWC, permeable-beach, dike-cover erosion, ripple onset and migration, overtopping transmission, cliff-notch pressure, storm beach-dune erosion, vegetation attenuation, higher-harmonic cylinder loading, and classic setup/runup flume datasets.

**Validated ranges.** Explicit regimes include a smooth impermeable 1:4 overtopped breakwater under regular waves, three imposed sand-bed perturbation classes, regular-wave migrating ripples, fresh-water large-scale permeable-beach tests, grass and clay cover under breaking impacts, flexible vegetation mimics, and phase-controlled cylinder waves.

**Recent advances.** Recent experiments increasingly combine dense measurements with process-based models, isolate higher harmonics through phase manipulation, decompose vegetation components, couple groundwater and sediment response, and distinguish sustained from impulsive coastal-cliff loads.

**Disagreements.** Laboratory relations can diverge from field transport or prototype impacts because phase lag, scale effects, sediment and vegetation similarity, three-dimensionality, irregularity, and material failure are incompletely represented. Larger scale is valuable but does not eliminate all distortion.

**Limitations.** Common limitations are reflection and finite-length effects, wavemaker fidelity, sensor bandwidth, repeatability, scale-dependent air compressibility and impulsive pressure, imperfect sediment and vegetation similitude, two-dimensional geometry, short duration, and restricted forcing ranges.

**Open questions.** Needed advances include uncertainty-standardized benchmark datasets, quantified scale effects for impacts and OWC pneumatics, reproducible irregular and multidirectional forcing, full measurement metadata, sediment and ecological similitude criteria, and stronger field-to-flume validation.

**Seminal papers.** Within this screened set, the 1982 storm beach-dune and overtopping-transmission papers and the 1992 OWC tests established enduring large-flume and device-testing evidence; later work added process-resolving measurements and coupled validation.

## Equations

### Flat-bed ripple threshold

$$
M=17-14.5e^{-0.03U}
$$

Regime: The tested well-sorted sands, three imposed bed perturbations, and oscillatory-flow Ursell-number range.

Variables: `M` mobility number; `U` Ursell number

Source: (Sekiguchi 2004, [doi:10.1016/j.coastaleng.2003.11.002](https://doi.org/10.1016/j.coastaleng.2003.11.002))

### Notched-bed ripple threshold

$$
M=5.0-2.5e^{-0.1U}
$$

Regime: The tested well-sorted sands, three imposed bed perturbations, and oscillatory-flow Ursell-number range.

Variables: `M` mobility number; `U` Ursell number

Source: (Sekiguchi 2004, [doi:10.1016/j.coastaleng.2003.11.002](https://doi.org/10.1016/j.coastaleng.2003.11.002))

### Settling-time factor

$$
\Omega_s=\eta/(w_0T)
$$

Regime: The tested migrating-ripple regular-wave conditions and settling-time factor Omega_s=eta/(w0 T).

Variables: `eta` ripple height; `w_0` settling velocity; `T` wave period

Source: (Yamaguchi 2011, [doi:10.1016/j.coastaleng.2011.03.001](https://doi.org/10.1016/j.coastaleng.2011.03.001))

### Ripple migration transport

$$
\langle q_r\rangle=(1-\epsilon)f_s\eta v
$$

Regime: The tested migrating-ripple regular-wave conditions and settling-time factor Omega_s=eta/(w0 T).

Variables: `epsilon` porosity; `f_s` shape factor; `eta` ripple height; `v` migration rate

Source: (Yamaguchi 2011, [doi:10.1016/j.coastaleng.2011.03.001](https://doi.org/10.1016/j.coastaleng.2011.03.001))

### superposition and stretching wave-velocity approximations

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: Controlled waves over a 1:40 beach measured by an acoustic meter on a servo-hydraulic surface follower.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Doering 1997, [doi:10.1016/s0378-3839(97)00030-6](https://doi.org/10.1016/s0378-3839(97)00030-6))

## Claims

- **C222.** Controlled wave-flume experiments were used to characterize a two-dimensional oscillating-water-column wave-energy device; quantitative transfer requires the source-specific geometry and wave regime. *Regime: The specific two-dimensional OWC and wave-flume configurations reported in the source..* [direct_finding, experimental] (Sarmento 1992, [doi:10.1007/bf00187307](https://doi.org/10.1007/bf00187307))
- **C223.** In large-scale permeable-beach tests, the coupled RANS-VOF and SEAWAT model reproduced wave-driven water-table behavior, and tested low water tables tended toward accretion whereas high water tables tended toward erosion. *Regime: The large-scale permeable-beach experiment and modeled fresh-water, wave, sediment, and aquifer conditions..* [direct_finding, experimental] (Bakhtyar 2011, [doi:10.1016/j.coastaleng.2010.08.004](https://doi.org/10.1016/j.coastaleng.2010.08.004))
- **C224.** Laboratory and model analysis indicated that erosion of grass and clay cover accounted for more than 85% of total modeled sea-dike breach time under seaward breaking-wave impact. *Regime: Grass- and clay-reveted sea dikes exposed to seaward breaking-wave impacts comparable to the laboratory and tentative validation cases..* [direct_finding, experimental] (Stanczak 2012, [doi:10.1016/j.coastaleng.2011.07.001](https://doi.org/10.1016/j.coastaleng.2011.07.001))
- **C225.** Ripple-onset mobility decreased as imposed bed perturbation increased; the fitted threshold changed from M=17-14.5 exp(-0.03U) on a flat bed to M=2.5 independent of U on a notch-mounded bed. *Regime: The tested well-sorted sands, three imposed bed perturbations, and oscillatory-flow Ursell-number range..* [direct_finding, experimental] (Sekiguchi 2004, [doi:10.1016/j.coastaleng.2003.11.002](https://doi.org/10.1016/j.coastaleng.2003.11.002))
- **C226.** Cliff-notch experiments separated sustained forces, estimable from buoyancy at low velocity, from impulsive forces that were more likely to mobilize cliff-top boulders; scale effects on impulses remain unresolved. *Regime: The tested cliff-notch geometry and observed/simulated wave-height and velocity range; impulsive scaling remains unresolved..* [direct_finding, experimental] (Watanabe 2023, [doi:10.1016/j.oceaneng.2023.113656](https://doi.org/10.1016/j.oceaneng.2023.113656))
- **C227.** For a smooth impermeable 1:4 breakwater under regular waves, overtopping transmission was correlated with crest height above mean sea level normalized by theoretical wave-runup height. *Regime: Regular waves overtopping the tested smooth impermeable 1:4 breakwater..* [direct_finding, experimental] (Hamer 1982, [doi:10.1016/0378-3839(82)90019-9](https://doi.org/10.1016/0378-3839(82)90019-9))
- **C228.** Deviation between Ribberink bedload predictions and ripple-migration transport increased systematically with settling-time factor Omega_s=eta/(w0 T), supporting a phase-lag mechanism. *Regime: The tested migrating-ripple regular-wave conditions and settling-time factor Omega_s=eta/(w0 T)..* [direct_finding, experimental] (Yamaguchi 2011, [doi:10.1016/j.coastaleng.2011.03.001](https://doi.org/10.1016/j.coastaleng.2011.03.001))
- **C264.** For shoaling waves over a 1:40 beach, surface-following acoustic velocities agreed with superposition and stretching adaptations of linear theory before and near breaking; after breaking, air entrainment contaminated crest measurements while trough velocities remained relatively well predicted. *Regime: Controlled waves over a 1:40 beach measured by an acoustic meter on a servo-hydraulic surface follower..* [direct_finding, experimental] (Doering 1997, [doi:10.1016/s0378-3839(97)00030-6](https://doi.org/10.1016/s0378-3839(97)00030-6))
- **C1752.** Controlled two-dimensional granular-slide experiments provide a reproducible benchmark for nonlinear impulse-wave run-over: wave gauges, photography, and PIV resolve bore-like, cnoidal-like, and Stokes-like cases over a trapezoidal breakwater for calibrating and validating numerical models. *Regime: Two-dimensional subaerial granular landslides entering still water in a rectangular laboratory channel and producing nonlinear impulse waves that cross a trapezoidal breakwater..* [direct_finding, experimental] (Helge Fuchs 2010, [doi:10.1007/s00348-010-0836-x](https://doi.org/10.1007/s00348-010-0836-x))

## Papers

- Sarmento (1992). Wave flume experiments on two-dimensional oscillating water column wave energy devices. *Experiments in Fluids*. [doi:10.1007/bf00187307](https://doi.org/10.1007/bf00187307)
- Bakhtyar (2011). Wave-induced water table fluctuations, sediment transport and beach profile change: Modeling and comparison with large-scale laboratory experiments. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2010.08.004](https://doi.org/10.1016/j.coastaleng.2010.08.004) [submitted manuscript, CC BY-NC-ND](https://infoscience.epfl.ch/record/149207)
- Stanczak (2012). Modeling sea dike breaching induced by breaking wave impact-laboratory experiments and computational model. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2011.07.001](https://doi.org/10.1016/j.coastaleng.2011.07.001)
- Sekiguchi (2004). Effects of bed perturbation and velocity asymmetry on ripple initiation: wave-flume experiments. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2003.11.002](https://doi.org/10.1016/j.coastaleng.2003.11.002)
- Helge Fuchs (2010). Impulse wave run-over: experimental benchmark study for numerical modelling. *Experiments in Fluids*. [doi:10.1007/s00348-010-0836-x](https://doi.org/10.1007/s00348-010-0836-x) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-010-0836-x.pdf)
- Watanabe (2023). Elucidation of wave pressure acting on a wave-cut notch beneath a coastal cliff based on laboratory experiments and numerical modeling. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2023.113656](https://doi.org/10.1016/j.oceaneng.2023.113656) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0029801823000409?httpAccept=text/xml)
- Hamer (1982). Laboratory experiments on wave transmission by overtopping. *Coastal Engineering*. [doi:10.1016/0378-3839(82)90019-9](https://doi.org/10.1016/0378-3839(82)90019-9)
- Yamaguchi (2011). Variability of wave-induced ripple migration in wave-flume experiments and its implications for sediment transport. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2011.03.001](https://doi.org/10.1016/j.coastaleng.2011.03.001)
- Doering (1997). Acoustic measurements of the velocity field beneath shoaling and breaking waves. *Coastal Engineering*. [doi:10.1016/s0378-3839(97)00030-6](https://doi.org/10.1016/s0378-3839(97)00030-6) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0378383997000306?httpAccept=text/xml)
- Anderson (2014). Wave attenuation by flexible, idealized salt marsh vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.10.004](https://doi.org/10.1016/j.coastaleng.2013.10.004)
- Hermann M. Fritz (2003). Landslide generated impulse waves.. *Experiments in Fluids*. [doi:10.1007/s00348-003-0659-0](https://doi.org/10.1007/s00348-003-0659-0) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-003-0659-0.pdf)
- Valentin Heller (2007). Scale effects in subaerial landslide generated impulse waves. *Experiments in Fluids*. [doi:10.1007/s00348-007-0427-7](https://doi.org/10.1007/s00348-007-0427-7) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-007-0427-7.pdf)
- Vellinga (1982). Beach and dune erosion during storm surges. *Coastal Engineering*. [doi:10.1016/0378-3839(82)90007-2](https://doi.org/10.1016/0378-3839(82)90007-2) [published version, read only](https://publications.deltares.nl/Pub276.pdf)
- Paul (2016). Plant stiffness and biomass as drivers for drag forces under extreme wave loading: A flume study on mimics. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.07.004](https://doi.org/10.1016/j.coastaleng.2016.07.004) [accepted manuscript, read only](https://repo.uni-hannover.de/bitstreams/37f190ea-bec4-4452-bc3f-fc33514272dd/download)
- He (2019). Surface wave attenuation by vegetation with the stem, root and canopy. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103509](https://doi.org/10.1016/j.coastaleng.2019.103509)
- Colin Whittaker (2017). Optimisation of focused wave group runup on a plane beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.12.001](https://doi.org/10.1016/j.coastaleng.2016.12.001) [accepted manuscript, read only](https://api.research-repository.uwa.edu.au/ws/files/150932115/Whittaker_et_al_2017_Optimisation_focused_wave_group_runup_CEng_AAM.pdf)
- M. Salauddin (2021). Eco-Engineering of Seawalls—An Opportunity for Enhanced Climate Resilience From Increased Topographic Complexity. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.674630](https://doi.org/10.3389/fmars.2021.674630) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2021.674630/pdf)
- Feng (2020). Experimental investigation of higher harmonic wave loads and moments on a vertical cylinder by a phase-manipulation method. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103747](https://doi.org/10.1016/j.coastaleng.2020.103747) [accepted manuscript, read only](https://strathprints.strath.ac.uk/73305/1/Feng_etal_CE_2020_Experimental_investigation_to_higher_harmonic_wave_loads_and_moments.pdf)
- William G. Van Dorn (1976). SET-UP AND RUN-UP IN SHOALING BREAKERS. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41) [published version, CC BY](https://journals.tdl.org/icce/index.php/icce/article/download/3090/2755)
