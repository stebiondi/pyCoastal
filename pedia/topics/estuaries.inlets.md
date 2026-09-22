# Tidal inlet dynamics

`estuaries.inlets` | Hydraulics and stability of inlets.

Parent: [Estuaries and tidal inlets](estuaries.md)

Papers: 22. Claims: 20. Equations: 1.

## Synthesis

**Well established.** A sandy tidal inlet remains open when current-driven sediment export and scour can balance marine or littoral sediment delivery; closure or cross-sectional adjustment occurs when that balance is persistently shifted.

**Governing physics.** Tidal prism and entrance geometry set exchange velocities, while waves, littoral drift, ebb transport, river flow, storms, and antecedent morphology control sediment import and export; feedback between area, velocity, and transport creates stable, unstable, or closed states.

**Dimensionless parameters.** No universal dimensionless stability parameter is established by this reviewed slice. Tide-wave dominance, transport-capacity ratios, and geometry-normalized relations are regime descriptors whose coefficients depend on inlet population and units.

**Major equations.** Common reduced formulations include the O'Brien prism-area relation, the Escoffier area-velocity stability diagram, Bruun sediment-capacity criteria, and nonlinear attractor equations; the 2004 Frisian formulation adds a physical ebb-transport balance to the Escoffier construction.

**Typical methods.** Methods combine field wave-current-bed observations, coupled morphodynamic simulation, analytical sediment balances, equilibrium/stability diagrams, nonlinear dynamical systems, aerial or chart morphology mapping, hindcast climatologies, and multi-inlet empirical correlation.

**Numerical models.** Wilson Inlet uses coupled cross-shore/longshore morphodynamics to isolate closure mechanisms; reduced engineering tools include O'Brien, Escoffier, Bruun, and an attractor map, each with distinct sediment and hydrodynamic simplifications.

**Experimental datasets.** Key reviewed evidence includes the summer 1995 Wilson Inlet field campaign, historical Frisian Inlet adjustment before and after basin reduction, a Snowy River observed/design case, and an 89-inlet United States database paired with 20-year wave hindcasts.

**Validated ranges.** Evidence is regime-bound: Wilson Inlet is a microtidal wave-dominated seasonal inlet; Frisian results address basin reduction; the attractor comparison uses Snowy River; and morphology correlations span 89 United States inlets but perform poorly in the moderate-wave-exposure group.

**Recent advances.** The 2012 multi-inlet database quantifies limits of classical morphology classification, while the 2018 attractor comparison unifies long-term tidal and river-controlled states and clarifies how reduced tools should support preliminary design.

**Disagreements.** Simple prism-area relations imply a compact equilibrium geometry, whereas the empirical morphology study found limited classification improvement from tidal prism alone. These results address different outputs but jointly warn against treating prism as a sufficient universal predictor.

**Limitations.** The reviewed studies simplify sediment supply, geometry, or transient forcing; two extractions are abstract-limited, field cases are geographically sparse, empirical correlations omit geology and engineering controls, and reduced rules are unsuitable as stand-alone final design models.

**Open questions.** Priorities include transferable stability criteria under nonstationary sea level and wave climate, transient closure/reopening prediction, multi-inlet interaction, uncertainty-aware sediment budgets, and independent validation across geological and engineered inlet classes.

**Seminal papers.** Within this screened branch, Wilson Inlet (1999) supplies a process-resolving closure case and the Frisian Inlet study (2004) gives Escoffier stability a sediment-balance basis; earlier O'Brien, Escoffier, and Bruun works remain seminal but were not directly extracted here.

## Equations

### O'Brien prism-area check

$$
A/P=6.56\times10^{-5}
$$

Regime: The paper's stated calibration and units; not a universal dimensionless constant.

Variables: `A` inlet entrance cross-sectional area; `P` tidal prism

Source: (Hinwood 2018, [doi:10.1016/j.coastaleng.2017.12.008](https://doi.org/10.1016/j.coastaleng.2017.12.008))

## Claims

- **C125.** At Wilson Inlet, persistent summer swell drove onshore sediment transport that exceeded removal by weak inlet currents and formed the entrance bar responsible for seasonal closure. *Regime: Wilson Inlet and comparable microtidal, wave-dominated, seasonally open sandy inlets under persistent summer swell..* [direct_finding, mixed] (Ranasinghe 1999, [doi:10.1016/s0378-3839(99)00007-1](https://doi.org/10.1016/s0378-3839(99)00007-1))
- **C126.** The influence of summer streamflow and storm events on inlet open duration depended on both event intensity and timing. *Regime: The Wilson Inlet model scenarios; event-response direction is not universal outside the modeled sequence and sediment state..* [direct_finding, numerical] (Ranasinghe 1999, [doi:10.1016/s0378-3839(99)00007-1](https://doi.org/10.1016/s0378-3839(99)00007-1))
- **C127.** For the Frisian Inlet framework, annual-mean entrance area is an equilibrium in which ebb currents restore cross-section losses caused by seasonal storm deposition. *Regime: The paper's sandy inlet schematization with annually averaged littoral input and separable entrance/interior sections..* [direct_finding, analytical] (van de Kreeke 2004, [doi:10.1016/j.coastaleng.2004.05.002](https://doi.org/10.1016/j.coastaleng.2004.05.002))
- **C128.** An inlet equilibrium is stable only when a perturbation in cross-sectional area drives the section back toward its equilibrium value; the allowable reduction before closure measures its stability margin. *Regime: The extended Escoffier construction applied to basin reduction..* [direct_finding, analytical] (van de Kreeke 2004, [doi:10.1016/j.coastaleng.2004.05.002](https://doi.org/10.1016/j.coastaleng.2004.05.002))
- **C129.** O'Brien, Escoffier, Bruun, and attractor methods can provide rapid preliminary stability checks, but the authors advise that final inlet design use more sophisticated models. *Regime: Sandy barrier estuaries and tidal inlets consistent with each reduced method's assumptions..* [direct_finding, review] (Hinwood 2018, [doi:10.1016/j.coastaleng.2017.12.008](https://doi.org/10.1016/j.coastaleng.2017.12.008))
- **C130.** The attractor formulation generalizes prism-area, Escoffier, and Bruun concepts by representing long-term tidal and river-controlled entrance states within one nonlinear dynamical framework. *Regime: Barrier estuaries with erodible entrances and the model's reduced sediment and hydrodynamic balances..* [direct_finding, analytical] (Hinwood 2018, [doi:10.1016/j.coastaleng.2017.12.008](https://doi.org/10.1016/j.coastaleng.2017.12.008))
- **C131.** Across 89 United States tidal inlets, the Hayes tide-range/wave-height diagram had limited applicability, and replacing tide range with tidal prism did not materially improve morphology classification. *Regime: The sampled Atlantic, Gulf, and Pacific United States inlets and available morphology classifications..* [direct_finding, field] (Anon. 2012, [doi:10.2112/jcoastres-d-11-00124.1](https://doi.org/10.2112/jcoastres-d-11-00124.1))
- **C365.** In idealized COAWST inlet simulations, ebb-shoal bathymetry was the dominant control on outflow-jet structure, while incident waves increased lateral spreading and limited seaward reach through momentum conversion, friction, and Stokes-drift interaction, with regime-dependent return-current effects. *Regime: Idealized tidal-inlet configurations varying ebb shoal, outflow, incident waves, and channel geometry..* [direct_finding, numerical] (Maitane Olabarrieta 2014, [doi:10.1002/2014jc010191](https://doi.org/10.1002/2014jc010191))
- **C1345.** At shallow inlets, maximum ebb and flood balances are dominated by advection, pressure and bottom friction alongstream and centrifugal-pressure balance cross-stream; near slack, local acceleration and pressure dominate. *Regime: Transient Tidal Circulation and Momentum Balances at a Shallow Inlet.* [direct_finding, numerical] (James L. Hench 2003, [doi:10.1175/1520-0485(2003)33<913:ttcamb>2.0.co;2](https://doi.org/10.1175/1520-0485(2003)33<913:ttcamb>2.0.co;2))
- **C1488.** Stability analysis and morphodynamic modeling relate tidal-basin channel number and spacing to bed slope, Shields parameter, and mean water depth. *Regime: Modeling of channel patterns in short tidal basins.* [direct_finding, analytical] (Raffaele Marciano 2005, [doi:10.1029/2003jf000092](https://doi.org/10.1029/2003jf000092))
- **C1489.** Field measurements at a wave-dominated tidal inlet show currents modify wave propagation and create systematic spatial and temporal variations in wave height and water level. *Regime: Wave‐current interactions in a wave‐dominated tidal inlet.* [direct_finding, field] (Guillaume Dodet 2013, [doi:10.1002/jgrc.20146](https://doi.org/10.1002/jgrc.20146))
- **C1490.** Analysis of short unvegetated tidal flats identifies geometric and hydraulic controls on funnel-shaped tidal-channel equilibrium morphology. *Regime: On funneling of tidal channels.* [direct_finding, analytical] (Stefano Lanzoni 2015, [doi:10.1002/2014jf003203](https://doi.org/10.1002/2014jf003203))
- **C1491.** Delft3D–SWAN experiments show oblique waves drive tidal-inlet migration through coupled channel, shoal, and alongshore sediment-transport mechanisms. *Regime: Mechanics and rates of tidal inlet migration: Modeling and application to natural examples.* [direct_finding, numerical] (Jaap H. Nienhuis 2016, [doi:10.1002/2016jf004035](https://doi.org/10.1002/2016jf004035))
- **C1492.** Field reconstruction of New Inlet links barrier narrowing, storm surge, astronomical tide, restricted exchange, and tidal phase differences to breach formation and sediment bypassing. *Regime: Inlet Formation and Evolution of the Sediment Bypassing System: New Inlet, Cape Cod, Massachusetts.* [direct_finding, field] (Duncan M. FitzGerald 2002, [doi:10.2112/1551-5036-36.sp1.290](https://doi.org/10.2112/1551-5036-36.sp1.290))
- **C1493.** A Vietnamese inlet study relates seasonal monsoon waves and microtidal forcing to sand-spit evolution and recurring entrance-morphology change. *Regime: Comprehensive Study of the Sand Spit Evolution at Tidal Inlets in the Central Coast of Vietnam.* [direct_finding, mixed] (Nguyen Quang Duc Anh 2020, [doi:10.3390/jmse8090722](https://doi.org/10.3390/jmse8090722))
- **C1593.** Across 35 estuaries and 190 tidal bars, summed bar width approximately follows channel excess width and bar dimensions scale with channel width or tidal prism. *Regime: Topographic forcing of tidal sandbar patterns for irregular estuary planforms.* [direct_finding, mixed] (Jasper R. F. W. Leuven 2017, [doi:10.1002/esp.4166](https://doi.org/10.1002/esp.4166))
- **C1699.** In a 110-year Delft3D analogue of Ameland Inlet, increasing relative sea-level rise strengthens flood dominance, erodes the ebb-tidal delta and accretes the basin; tidal flats persist near the 0.2 m scenario but drown under 0.7 m sea-level rise plus subsidence. *Regime: Highly schematized large tidal-inlet/basin morphology representing Ameland Inlet under the specified relative-sea-level scenarios..* [direct_finding, numerical] (D.M.P.K. Dissanayake 2012, [doi:10.1007/s10584-012-0402-z](https://doi.org/10.1007/s10584-012-0402-z))
- **C1704.** At Nagatsura-ura Lagoon, tidal-inlet depth controls lagoon water-level response and the magnitude of salinity intrusion: spectral observations and three-dimensional simulations show deeper channels strengthen tidal coherence and salt exchange. *Regime: Nagatsura-ura Lagoon and its shallow connection to Oppa Bay under the observed tidal response and tested inlet-depth cases..* [direct_finding, mixed] (WATANABE 2009, [doi:10.2208/kaigan.65.416](https://doi.org/10.2208/kaigan.65.416))
- **C1778.** Analysis of 89 U.S. tidal inlets using tidal prism and a 20-year wave hindcast found limited support for the Hayes tide-range/wave-height morphology classification; ebb-delta seaward and downdrift extents correlate best after stratifying by wave exposure, remaining nearly constant below an approximately 10^8 m3 tidal-prism threshold and increasing roughly linearly above it. *Regime: Structured and unstructured tidal inlets on the Atlantic, Gulf of Mexico, and Pacific coasts of the United States, grouped into mild, moderate, and high wave-exposure classes..* [direct_finding, mixed] (Anon. 2012, [doi:10.2112/jcoastres-d-11-00124.1](https://doi.org/10.2112/jcoastres-d-11-00124.1))
- **C1779.** Microstructure and velocity transects in a curved, weakly stratified Wadden Sea inlet show that differential advection creates a lateral buoyancy gradient which reinforces curvature-driven single-cell circulation and late-flood stratification during flood, suppresses cross-channel exchange during ebb, and thereby drives a residual longitudinal estuarine exchange flow. *Regime: Well-mixed to weakly stratified, curved tidal channel in the German Wadden Sea, with channel-shoal bathymetry and reversing flood-ebb currents..* [direct_finding, field] (Becherer 2015, [doi:10.1175/jpo-d-14-0001.1](https://doi.org/10.1175/jpo-d-14-0001.1))

## Papers

- Raffaele Marciano (2005). Modeling of channel patterns in short tidal basins. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2003jf000092](https://doi.org/10.1029/2003jf000092)
- Guillaume Dodet (2013). Wave‐current interactions in a wave‐dominated tidal inlet. *Journal of Geophysical Research Oceans*. [doi:10.1002/jgrc.20146](https://doi.org/10.1002/jgrc.20146)
- D.M.P.K. Dissanayake (2012). The morphological response of large tidal inlet/basin systems to relative sea level rise. *Climatic Change*. [doi:10.1007/s10584-012-0402-z](https://doi.org/10.1007/s10584-012-0402-z)
- James L. Hench (2003). Transient Tidal Circulation and Momentum Balances at a Shallow Inlet. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(2003)33<913:ttcamb>2.0.co;2](https://doi.org/10.1175/1520-0485(2003)33<913:ttcamb>2.0.co;2)
- Maitane Olabarrieta (2014). The role of morphology and wave‐current interaction at tidal inlets: An idealized modeling analysis. *Journal of Geophysical Research Oceans*. [doi:10.1002/2014jc010191](https://doi.org/10.1002/2014jc010191)
- Stefano Lanzoni (2015). On funneling of tidal channels. *Journal of Geophysical Research Earth Surface*. [doi:10.1002/2014jf003203](https://doi.org/10.1002/2014jf003203)
- Jasper R. F. W. Leuven (2017). Topographic forcing of tidal sandbar patterns for irregular estuary planforms. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.4166](https://doi.org/10.1002/esp.4166)
- Ranasinghe (1999). The seasonal closure of tidal inlets: Wilson Inlet—a case study. *Coastal Engineering*. [doi:10.1016/s0378-3839(99)00007-1](https://doi.org/10.1016/s0378-3839(99)00007-1)
- Jaap H. Nienhuis (2016). Mechanics and rates of tidal inlet migration: Modeling and application to natural examples. *Journal of Geophysical Research Earth Surface*. [doi:10.1002/2016jf004035](https://doi.org/10.1002/2016jf004035)
- Becherer (2015). Lateral Circulation Generates Flood Tide Stratification and Estuarine Exchange Flow in a Curved Tidal Inlet. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-14-0001.1](https://doi.org/10.1175/jpo-d-14-0001.1)
- Duncan M. FitzGerald (2002). Inlet Formation and Evolution of the Sediment Bypassing System: New Inlet, Cape Cod, Massachusetts. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.290](https://doi.org/10.2112/1551-5036-36.sp1.290)
- van de Kreeke (2004). Equilibrium and cross-sectional stability of tidal inlets: application to the Frisian Inlet before and after basin reduction. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.05.002](https://doi.org/10.1016/j.coastaleng.2004.05.002)
- Nguyen Quang Duc Anh (2020). Comprehensive Study of the Sand Spit Evolution at Tidal Inlets in the Central Coast of Vietnam. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8090722](https://doi.org/10.3390/jmse8090722)
- Hinwood (2018). Tidal inlets and estuaries: Comparison of Bruun, Escoffier, O'Brien and attractors. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.12.008](https://doi.org/10.1016/j.coastaleng.2017.12.008)
- Anon. (2012). Tidal Inlet Morphology Classification and Empirical Determination of Seaward and Down-Drift Extents of Tidal Inlets. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00124.1](https://doi.org/10.2112/jcoastres-d-11-00124.1)
- WATANABE (2009). Influence of Tidal Inlet Depth on Water Level Response and Salinity Intrusion in A Lagoon. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.65.416](https://doi.org/10.2208/kaigan.65.416)
- Bonnie C. Ludka (2018). Nourishment evolution and impacts at four southern California beaches: A sand volume analysis. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2018.02.003](https://doi.org/10.1016/j.coastaleng.2018.02.003)
- Laura Lavaud (2020). The contribution of short-wave breaking to storm surges: The case Klaus in the Southern Bay of Biscay. *Ocean Modelling*. [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710)
- Kabir Suara (2017). Relative dispersion of clustered drifters in a small micro-tidal estuary. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2017.05.001](https://doi.org/10.1016/j.ecss.2017.05.001)
- Cai (2016). An Analytical Approach to Determining Resonance in Semi-Closed Convergent Tidal Channels. *Coastal Engineering Journal*. [doi:10.1142/s0578563416500091](https://doi.org/10.1142/s0578563416500091)
- Weathers (2013). Evaluation of Beach Nourishment Evolution Models Using Data from Two South Carolina, USA Beaches: Folly Beach and Hunting Island. *Journal of Coastal Research*. [doi:10.2112/si_69_7](https://doi.org/10.2112/si_69_7)
- Marcus Silva-Santana (2026). Automated detection of river mouth opening and closure using cloud-based processing of Sentinel-2 imagery. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110052](https://doi.org/10.1016/j.ecss.2026.110052)
