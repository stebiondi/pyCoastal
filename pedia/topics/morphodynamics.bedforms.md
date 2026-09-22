# Bedforms

`morphodynamics.bedforms` | Ripples, dunes, and bed roughness.

Parent: [Coastal morphodynamics](morphodynamics.md)

Papers: 15. Claims: 14. Equations: 0.

## Synthesis

**Well established.** Subaqueous ripples and dunes emerge from sediment-transport feedback under waves, currents, and combined flow. Their geometry, orientation, migration, and state alter hydraulic roughness, turbulence, suspension, and net sediment flux.

**Governing physics.** Controls include bed shear and Shields stress, oscillatory asymmetry, acceleration skewness, wave-current angle, vortex shedding, phase lag, avalanching, grain sorting and armouring, cohesion and EPS, and lagged adjustment to changing forcing.

**Dimensionless parameters.** Important groups include Shields parameter, mobility and suspension numbers, wave orbital excursion relative to grain and ripple scale, wave-current angle, velocity and acceleration asymmetry, relative roughness, clay volume fraction, and normalized adjustment time.

**Major equations.** Core frameworks include Exner sediment continuity, Shields-based mobility, logistic ripple evolution, semi-unsteady half-cycle transport, Euler-Lagrange particle dynamics, Eulerian two-phase RANS, LES boundary layers, and equilibrium-size roughness relations.

**Typical methods.** Evidence uses oscillatory tunnels and wave flumes, ripple profiling and spectral analysis, dual-station seabed imaging, spring-neap intertidal surveys, regression and phase diagrams, practical formula databases, particle models, two-phase RANS, and LES.

**Numerical models.** Models range from empirical and logistic closures to grain-resolving Euler-Lagrange, Eulerian two-phase sediment-fluid equations, and coupled far-field/LES calculations that explicitly resolve vortex and suspension processes.

**Experimental datasets.** Datasets include 226 large-scale transport measurements, mixed-flat spring-neap observations, Sand Engine records at 60-66 m station spacing, four weeks of MEGAPEX imaging, and vortex-ripple and sheet-flow validation experiments.

**Validated ranges.** Explicit evidence spans 0.13-0.54 mm sands; cohesion shutdown above 2.8 vol% clay and 0.05 wt% EPS; wavelengths from 0.14 to over 2 m; heights 0.02-0.40 m; migration to 3.6 m/h; and flux to 1.7 m3/m/day.

**Recent advances.** Recent advances quantify rapid field transformation, cohesion thresholds, phase diagrams across near-orthogonal wave-current angles, grain-scale sorting, ripple-resolved two-phase transport, and multiscale flux contributions to sandbar evolution.

**Disagreements.** Equilibrium geometry can predict roughness in some variable intertidal settings, yet individual bedforms may be out of equilibrium half the time and transform over 20 minutes to 6 hours. Instantaneous equilibrium is therefore a useful closure, not a universal state description.

**Limitations.** Most evidence is two-dimensional or site-specific; mixtures, biology, three-dimensional defect dynamics, broad grading, storm reversals, instrument resolution, scale effects, and feedback to larger morphology constrain transfer.

**Open questions.** Priorities are unified transient phase diagrams, mixed-grain and cohesive biology, three-dimensional vortex-bed coupling, bedform-sheet-flow transitions, uncertainty-aware roughness, and upscaling ripple flux to bars and shorelines.

**Seminal papers.** The branch links classic Shields mobility, Exner continuity, ripple-equilibrium and roughness concepts to transient logistic evolution and modern phase-resolving particle and two-phase models; detailed historical attribution awaits full text.

## Claims

- **C445.** A semi-unsteady transport formula using bed stress, phase lag, acceleration skewness, streaming, and advection placed 78% of 226 measured rates within a factor two and captured both rippled-bed and sheet-flow trends. *Regime: large oscillatory tunnels and wave flume; 0.13-0.54 mm sand.* [direct_finding, mixed] (Dominic van der A 2013, [doi:10.1016/j.coastaleng.2013.01.007](https://doi.org/10.1016/j.coastaleng.2013.01.007))
- **C446.** An Euler-Lagrange natural-sand model reproduced vortex-ripple and sheet-flow velocity and concentration and revealed dynamic coarse-over-fine armouring, size-selective pickup, and delayed settling of finer grains. *Regime: asymmetric oscillatory vortex-ripple and sheet-flow conditions with natural sand.* [direct_finding, numerical] (Justin Finn 2016, [doi:10.1017/jfm.2016.246](https://doi.org/10.1017/jfm.2016.246))
- **C447.** On a mixed sand-mud intertidal flat, bedform transport decreased with cohesive clay and EPS and became undetectable above 2.8 vol% clay and 0.05 wt% EPS despite that clay level often being classed as clean sand. *Regime: biologically active mixed sand-mud flat with clay below 2 to 5.4 vol%.* [direct_finding, field] (Ian D. Lichtman 2018, [doi:10.1016/j.geomorph.2018.04.016](https://doi.org/10.1016/j.geomorph.2018.04.016))
- **C448.** Wave-ripple growth and transition experiments were represented by one logistic evolution law whose rate depends on Shields parameter, enabling time-dependent bottom-roughness estimation after sea-state changes. *Regime: wave-formed ripples evolving between equilibrium states after wave change.* [direct_finding, mixed] (Joseph P. Davis 2004, [doi:10.1029/2004jc002307](https://doi.org/10.1029/2004jc002307))
- **C449.** A spring-neap field phase diagram integrated wave-, current-, and combined-flow bedforms, and an equilibrium-size equation predicted roughness even though observed forms were in equilibrium only about half the time. *Regime: mixed sand-clay intertidal flat across wave-current angles.* [direct_finding, field] (Jaco H. Baas 2021, [doi:10.3389/feart.2021.747567](https://doi.org/10.3389/feart.2021.747567))
- **C450.** A two-phase model matched measured onshore ripple migration by resolving onshore near-bed transport and lee-flank avalanching, while asymmetric ripple vortices drove offshore suspended flux. *Regime: orbital ripples under skewed second-order and symmetric sinusoidal oscillation.* [direct_finding, numerical] (Ali Salimi-Tarazouj 2020, [doi:10.1029/2020jc016773](https://doi.org/10.1029/2020jc016773))
- **C451.** At the Sand Engine, bedforms 0.14 to over 2 m long transformed within 20 minutes to 6 hours, and their volume change followed integrated sediment transport over the lagged development interval. *Regime: two Sand Engine locations 60 m apart under waves and currents.* [direct_finding, field] (M. E. Wengrove 2018, [doi:10.1029/2018jc014357](https://doi.org/10.1029/2018jc014357))
- **C452.** A coupled far-field/LES model accurately predicted mean velocity and suspended sediment over full-scale vortex ripples, with surface roughness exerting a significant control on the result. *Regime: full-scale vortex ripples under oscillatory wave forcing.* [direct_finding, numerical] (Jeffrey C. Harris 2014, [doi:10.5194/npg-21-1169-2014](https://doi.org/10.5194/npg-21-1169-2014))
- **C453.** Four-week surf-zone observations found 0.02-0.40 m high ripples migrating up to 3.6 m/h and carrying mean and maximum volume fluxes of 0.22 and 1.7 m3/m/day, sufficient to contribute to larger sandbar evolution. *Regime: 2014 MEGAPEX Sand Engine transect with stations 66 m apart.* [direct_finding, field] (M. E. Wengrove 2022, [doi:10.1016/j.geomorph.2022.108246](https://doi.org/10.1016/j.geomorph.2022.108246))
- **C1183.** Multibeam and seismic evidence indicates Llobregat prodelta undulations on 0.2–3° slopes are sediment waves formed by hyperpycnal bottom-current interaction with regional circulation, not progressive slope deformation. *Regime: Sediment undulations on the Llobregat prodelta: Signs of early slope instability or sedimentary bedforms?.* [direct_finding, mixed] (Roger Úrgeles 2007, [doi:10.1029/2005jb003929](https://doi.org/10.1029/2005jb003929))
- **C1188.** A hybrid sorted-bedform model using genetic-programming predictors for suspended-sediment reference concentration and oscillatory ripples captured two observed pattern modes absent from the prior model. *Regime: Data-driven components in a model of inner-shelf sorted bedforms: a new hybrid model.* [direct_finding, mixed] (Evan B. Goldstein 2014, [doi:10.5194/esurf-2-67-2014](https://doi.org/10.5194/esurf-2-67-2014))
- **C1452.** Delft3D sensitivity analysis shows that ripple and megaripple roughness choices materially affect modeled hydrodynamics and sediment transport on an ebb-tidal delta. *Regime: From Ripples to Large-Scale Sand Transport: The Effects of Bedform-Related Roughness on Hydrodynamics and Sediment Transport Patterns in Delft3D.* [direct_finding, numerical] (Laura Brakenhoff 2020, [doi:10.3390/jmse8110892](https://doi.org/10.3390/jmse8110892))
- **C1453.** Morphodynamic stability analysis links increased bed roughness to a shift from dune-scale toward megaripple-scale bed instability on sandy beds. *Regime: Influence of bed roughness on dune and megaripple generation.* [direct_finding, numerical] (Déborah Idier 2004, [doi:10.1029/2004gl019969](https://doi.org/10.1029/2004gl019969))
- **C1707.** Process-based morphodynamic simulations show that tidal sand-wave recovery is slower after swiping than topping, and that larger dredged volumes lengthen recovery; maintenance intervals also evolve because recovery depends on bedform shape as well as height. *Regime: Fully developed modeled tidal sand waves under topping, swiping, multiple dredging depths, and repeated navigation-channel maintenance..* [direct_finding, numerical] (Campmans 2021, [doi:10.1016/j.coastaleng.2021.103862](https://doi.org/10.1016/j.coastaleng.2021.103862))

## Papers

- Dominic van der A (2013). Practical sand transport formula for non-breaking waves and currents. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.01.007](https://doi.org/10.1016/j.coastaleng.2013.01.007)
- Justin Finn (2016). Particle based modelling and simulation of natural sand dynamics in the wave bottom boundary layer. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2016.246](https://doi.org/10.1017/jfm.2016.246)
- Laura Brakenhoff (2020). From Ripples to Large-Scale Sand Transport: The Effects of Bedform-Related Roughness on Hydrodynamics and Sediment Transport Patterns in Delft3D. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8110892](https://doi.org/10.3390/jmse8110892)
- Roger Úrgeles (2007). Sediment undulations on the Llobregat prodelta: Signs of early slope instability or sedimentary bedforms?. *Journal of Geophysical Research: Solid Earth*. [doi:10.1029/2005jb003929](https://doi.org/10.1029/2005jb003929)
- Déborah Idier (2004). Influence of bed roughness on dune and megaripple generation. *Geophysical Research Letters*. [doi:10.1029/2004gl019969](https://doi.org/10.1029/2004gl019969)
- Joseph P. Davis (2004). Wave‐formed sediment ripples: Transient analysis of ripple spectral development. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2004jc002307](https://doi.org/10.1029/2004jc002307)
- Ian D. Lichtman (2018). Bedform migration in a mixed sand and cohesive clay intertidal environment and implications for bed material transport predictions. *Geomorphology*. [doi:10.1016/j.geomorph.2018.04.016](https://doi.org/10.1016/j.geomorph.2018.04.016)
- Jaco H. Baas (2021). Current- and Wave-Generated Bedforms on Mixed Sand–Clay Intertidal Flats: A New Bedform Phase Diagram and Implications for Bed Roughness and Preservation Potential. *Frontiers in Earth Science*. [doi:10.3389/feart.2021.747567](https://doi.org/10.3389/feart.2021.747567)
- Ali Salimi-Tarazouj (2020). A Numerical Study of Onshore Ripple Migration Using a Eulerian Two‐phase Model. *Journal of Geophysical Research Oceans*. [doi:10.1029/2020jc016773](https://doi.org/10.1029/2020jc016773)
- M. E. Wengrove (2018). Observations of Time‐Dependent Bedform Transformation in Combined Wave‐Current Flows. *Journal of Geophysical Research Oceans*. [doi:10.1029/2018jc014357](https://doi.org/10.1029/2018jc014357)
- Evan B. Goldstein (2014). Data-driven components in a model of inner-shelf sorted bedforms: a new hybrid model. *Earth Surface Dynamics*. [doi:10.5194/esurf-2-67-2014](https://doi.org/10.5194/esurf-2-67-2014)
- Campmans (2021). Modeling tidal sand wave recovery after dredging: effect of different types of dredging strategies. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103862](https://doi.org/10.1016/j.coastaleng.2021.103862)
- Jeffrey C. Harris (2014). Large eddy simulation of sediment transport over rippled beds. *Nonlinear processes in geophysics*. [doi:10.5194/npg-21-1169-2014](https://doi.org/10.5194/npg-21-1169-2014)
- M. E. Wengrove (2022). Surfzone bedform migration and sediment flux implications to large scale morphologic evolution. *Geomorphology*. [doi:10.1016/j.geomorph.2022.108246](https://doi.org/10.1016/j.geomorph.2022.108246)
- Klervi Hamon-Kerivel (2020). Shoreface mesoscale morphodynamics: A review. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2020.103330](https://doi.org/10.1016/j.earscirev.2020.103330)
