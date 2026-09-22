# Physical-model similitude

`laboratory.similitude` | Scaling laws and scale effects.

Parent: [Laboratory experiments](laboratory.md)

Papers: 12. Claims: 11. Equations: 0.

## Synthesis

**Well established.** Coastal hydraulic models normally preserve Froude similarity because gravity controls free-surface motion, but using the same fluid makes simultaneous Reynolds and Weber similarity impossible; viscosity, surface tension, air, turbulence, roughness, impulse duration, sediment and soil can therefore cause scale effects.

**Governing physics.** Dynamic similitude requires matching ratios of inertia to gravity, viscosity, surface tension, elasticity, pressure and body force. Vortices and boundary layers amplify Reynolds mismatch; bubbles, droplets and cushioning add density/viscosity/surface-tension scales; impact peaks depend on compressibility, air and sensor bandwidth.

**Dimensionless parameters.** Key controls are Froude, Reynolds and Weber numbers; relative roughness and depth; density and viscosity ratios; air-content and void-fraction scales; wave steepness; impulse duration relative to structural period and sampling response; Shields and fall-velocity ratios; and centrifuge g level.

**Major equations.** Core relations include Fr=U/sqrt(gL), Re=UL/ν, We=ρU²L/σ, geometric scale λL, Froude time λT=sqrt(λL), velocity sqrt(λL), force ρgλL³, pressure ρgλL, impulse force×time, and centrifuge stress scaling using elevated effective gravity.

**Typical methods.** Methods include paired or multiple geometric scales, prototype/large-scale comparison, repeated-test uncertainty, dimensional analysis, Froude-scaled flumes, aerated-flow probes, high-bandwidth pressure sensing, optical velocity and bore classification, LES scale expansion, and geotechnical centrifuges.

**Numerical models.** Numerical support includes LES comparisons across distorted and undistorted scales, RANS validation against repeated large-scale experiments, lubrication/inviscid air-cushioning regimes, and analytical conversions from model displacement, pressure and velocity to prototype.

**Experimental datasets.** Evidence includes dry/wet tsunami-bore generation, large-scale overtopping and wall impact, repeated shallow-foreshore dike tests, a 1:30 clifftop boulder, a 1:40 tsunami–soil centrifuge, 3× and 10× shallow-flow scaling, and 1:38 downfall-pressure tests.

**Validated ranges.** Reported evidence includes an air-cushioning regime transition near Reynolds number 10^7, 1:30 boulder displacements scaling to 0.15–1.3 m, a 1:40 centrifuge representing 9.6×21×14.6 m, 3× and 10× shallow-flow models, roughly two-thirds quasi-static bore impacts, and downfall pressures of 30–40ρgH.

**Recent advances.** Recent advances use centrifuges to preserve fluid–soil stress, LES to localize scale bias to recirculation, repeated large-scale datasets for uncertainty-aware CFD validation, high-bandwidth downfall pressures, and physically resolved air–water upscaling reviews.

**Disagreements.** Froude similarity is appropriate for gravity waves but insufficient for vortical, viscous, capillary, aerated, porous or sediment processes. Large scale reduces some bias but does not guarantee correct impact physics; numeric agreement can depend on reproducing precursor bore interactions rather than only peak conditions.

**Limitations.** The journal evidence base explicitly comparing multiple coastal scales is sparse; many studies state a scale but do not test scale effects. Prototype data, air and compressibility scaling, roughness, sediment and biological-material similitude, sensor dynamics, and uncertainty propagation remain incomplete.

**Open questions.** Needs include defensible Reynolds/Weber thresholds, aeration and compressibility correction, impulsive-pressure bandwidth, roughness and porous scaling, sediment and morphology distortion, flexible vegetation and debris similitude, multi-hazard soil response, and quantified prototype uncertainty.

**Seminal papers.** The branch connects classical Froude/Reynolds/Weber dimensional analysis to aerated-flow regime studies, large-scale repeated experiments, centrifuge dynamic similitude, numerical scale expansion, and explicit pressure/impulse diagnostics.

## Claims

- **C735.** Aerated free-surface flows require measurement and modelling of bubbles, droplets, turbulence, and surface-tension breakup, making direct prototype transfer difficult. *Regime: Hydraulics of aerated flows:<i>qui pro quo</i>?.* [literature_review_statement, review] (Chanson 2013, [doi:10.1080/00221686.2013.795917](https://doi.org/10.1080/00221686.2013.795917))
- **C736.** Air cushioning changes regime near a wall: lubrication coupling applies below a global Reynolds number of order 10^7 for air–water, transitions near that scale, and becomes formally inviscid above it. *Regime: Air cushioning with a lubrication/inviscid balance.* [direct_finding, analytical] (F. T. Smith 2003, [doi:10.1017/s0022112003004063](https://doi.org/10.1017/s0022112003004063))
- **C737.** A vertical-release generator reproduced classical dry-bed surges and wet-bed bores while preserving Froude number, momentum, front celerity, and velocity-profile behavior needed for tsunami-load tests. *Regime: Experimental Study of Tsunami-Like Waves Generated with a Vertical Release Technique on Dry and Wet Beds.* [direct_finding, experimental] (Davide Wüthrich 2018, [doi:10.1061/(asce)ww.1943-5460.0000447](https://doi.org/10.1061/(asce)ww.1943-5460.0000447))
- **C738.** Prototype prediction of aerated high-Froude flows remains limited by instrumentation, multiphase modelling, and upscaling from controlled hydraulic experiments. *Regime: Air–water flows.* [literature_review_statement, review] (Daniel Valero 2024, [doi:10.1080/00221686.2024.2379482](https://doi.org/10.1080/00221686.2024.2379482))
- **C739.** Large-scale overtopping tests distinguished five bore-interaction patterns and three wall-impact types; roughly two-thirds of impacts were quasi-static. *Regime: Classification of bore patterns induced by storm waves overtopping a dike crest and their impact types on dike mounted vertical walls – a large-scale model study.* [direct_finding, experimental] (Maximilian Streicher 2019, [doi:10.1080/21664250.2019.1589635](https://doi.org/10.1080/21664250.2019.1589635))
- **C740.** Repeated large-scale dike tests quantified experimental uncertainty and showed that accurate force and pressure prediction depends on reproducing the preceding bore interactions. *Regime: Validation of RANS Modelling for Wave Interactions with Sea Dikes on Shallow Foreshores Using a Large-Scale Experimental Dataset.* [direct_finding, mixed] (Vincent Gruwez 2020, [doi:10.3390/jmse8090650](https://doi.org/10.3390/jmse8090650))
- **C741.** A 1:30 Froude-scaled clifftop-boulder experiment produced prototype-equivalent displacement of 0.15–1.3 m, with maximum displacement requiring both high pressure and long impact duration. *Regime: Breaking-wave induced pressure and acceleration on a clifftop boulder.* [direct_finding, experimental] (James N. Steer 2021, [doi:10.1017/jfm.2021.841](https://doi.org/10.1017/jfm.2021.841))
- **C742.** A 1:40 geotechnical centrifuge reduced fluid–soil dynamic-similitude mismatch and produced prototype-identical pressure and velocity for a 9.6 m deep, 21 m long, 14.6 m wide soil field. *Regime: Simulating Tsunami Inundation and Soil Response in a Large Centrifuge.* [direct_finding, experimental] (Margaret Exton 2019, [doi:10.1038/s41598-019-47512-x](https://doi.org/10.1038/s41598-019-47512-x))
- **C743.** Froude-scaled 3× and 10× models could not simultaneously match Reynolds and Weber numbers; scale effects were strong in recirculating vortices and energy loss but weak in upstream non-vortical velocity. *Regime: Scale Effects Investigation in Physical Modeling of Recirculating Shallow Flow Using Large Eddy Simulation Technique.* [direct_finding, numerical] (Ravi Anthony Tartandyo 2023, [doi:10.47176/jafm.17.1.1980](https://doi.org/10.47176/jafm.17.1.1980))
- **C744.** At 1:38 scale, violent seawall downfall impacts regularly reached 30–40ρgH and showed shorter impulse duration at higher pressure, exposing a scaling-sensitive impulsive-load regime. *Regime: Shore-Side Downfall Pressures Due to Waves Impacting a Vertical Seawall: An Experimental Study.* [direct_finding, experimental] (Annelie Baines 2024, [doi:10.3390/jmse12122149](https://doi.org/10.3390/jmse12122149))
- **C1748.** Froude-scaled laboratory models of subaerial landslide impulse waves underpredict relative wave amplitude when water depth is too small because surface tension alters impact-crater and air-entrainment dynamics while viscosity and dispersion increase propagation damping. *Regime: Two-dimensional granular subaerial landslides entering water and generating nonlinear intermediate-depth impulse waves in Froude-scaled laboratory channels..* [direct_finding, experimental] (Valentin Heller 2007, [doi:10.1007/s00348-007-0427-7](https://doi.org/10.1007/s00348-007-0427-7))

## Papers

- Valentin Heller (2007). Scale effects in subaerial landslide generated impulse waves. *Experiments in Fluids*. [doi:10.1007/s00348-007-0427-7](https://doi.org/10.1007/s00348-007-0427-7)
- Chanson (2013). Hydraulics of aerated flows:<i>qui pro quo</i>?. *Journal of Hydraulic Research*. [doi:10.1080/00221686.2013.795917](https://doi.org/10.1080/00221686.2013.795917)
- F. T. Smith (2003). Air cushioning with a lubrication/inviscid balance. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112003004063](https://doi.org/10.1017/s0022112003004063)
- Davide Wüthrich (2018). Experimental Study of Tsunami-Like Waves Generated with a Vertical Release Technique on Dry and Wet Beds. *Journal of Waterway Port Coastal and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000447](https://doi.org/10.1061/(asce)ww.1943-5460.0000447)
- Daniel Valero (2024). Air–water flows. *Journal of Hydraulic Research*. [doi:10.1080/00221686.2024.2379482](https://doi.org/10.1080/00221686.2024.2379482)
- Maximilian Streicher (2019). Classification of bore patterns induced by storm waves overtopping a dike crest and their impact types on dike mounted vertical walls – a large-scale model study. *Coastal Engineering Journal*. [doi:10.1080/21664250.2019.1589635](https://doi.org/10.1080/21664250.2019.1589635)
- Vincent Gruwez (2020). Validation of RANS Modelling for Wave Interactions with Sea Dikes on Shallow Foreshores Using a Large-Scale Experimental Dataset. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8090650](https://doi.org/10.3390/jmse8090650)
- James N. Steer (2021). Breaking-wave induced pressure and acceleration on a clifftop boulder. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2021.841](https://doi.org/10.1017/jfm.2021.841)
- Margaret Exton (2019). Simulating Tsunami Inundation and Soil Response in a Large Centrifuge. *Scientific Reports*. [doi:10.1038/s41598-019-47512-x](https://doi.org/10.1038/s41598-019-47512-x)
- Ravi Anthony Tartandyo (2023). Scale Effects Investigation in Physical Modeling of Recirculating Shallow Flow Using Large Eddy Simulation Technique. *Journal of Applied Fluid Mechanics*. [doi:10.47176/jafm.17.1.1980](https://doi.org/10.47176/jafm.17.1.1980)
- Annelie Baines (2024). Shore-Side Downfall Pressures Due to Waves Impacting a Vertical Seawall: An Experimental Study. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse12122149](https://doi.org/10.3390/jmse12122149)
- Helge Fuchs (2010). Impulse wave run-over: experimental benchmark study for numerical modelling. *Experiments in Fluids*. [doi:10.1007/s00348-010-0836-x](https://doi.org/10.1007/s00348-010-0836-x)
