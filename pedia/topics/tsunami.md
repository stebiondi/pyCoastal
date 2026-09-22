# Tsunamis and long waves

`tsunami` | Generation, propagation, inundation, and loading by long waves.

Subtopics: [Tsunami generation](tsunami.generation.md), [Tsunami inundation](tsunami.inundation.md), [Tsunami loads and debris](tsunami.loads.md), [Tsunami propagation](tsunami.propagation.md)

Papers: 19. Claims: 2. Equations: 0.

## Synthesis

**Well established.** Tsunamis arise from rapid water-column displacement, propagate predominantly as long waves, and amplify through shoaling, focusing and interaction with coastal topography. Earthquake rupture dominates global hazard, while landslides and volcanic collapse can create especially severe near-field waves.

**Governing physics.** Generation maps seafloor or mass-motion kinematics into free-surface displacement and momentum. Propagation is controlled by gravity, depth, dispersion and bathymetric refraction; near shore, nonlinearity, breaking, friction, buildings and terrain control runup and inundation.

**Dimensionless parameters.** Key controls include wave amplitude-to-depth ratio, wavelength-to-depth ratio, Froude and Reynolds numbers, relative slide thickness and density, slope, dispersion measures, roughness and blockage ratios, and source probability or return period.

**Major equations.** Linear long-wave and shallow-water equations describe much basin propagation; nonlinear shallow-water and Boussinesq systems add finite amplitude and dispersion. Navier–Stokes or multiphase models resolve energetic slide generation, while probabilistic hazard integrates source occurrence and conditional inundation response.

**Typical methods.** The literature combines post-event surveys, gauges, geodesy, seismic and marine mapping, laboratory long-wave experiments, source inversion, shallow-water/Boussinesq/Navier–Stokes simulation, benchmark suites, probabilistic ensembles and emerging image or neural-network forecasts.

**Numerical models.** Operational and research systems range from depth-averaged nonlinear shallow-water solvers such as Tsunami-HySEA to dispersive Boussinesq propagation and three-dimensional Navier–Stokes source models. Ensembles represent slip, fault, landslide and model uncertainty.

**Experimental datasets.** Root evidence includes the 1993 Hokkaido, 1998 Papua New Guinea, 2011 Tohoku and 2018 Anak Krakatau events; Oregon and New Zealand hazard scenarios; NTHMP benchmarks; controlled runup experiments; and coastal CCTV-derived shoreline observations.

**Validated ranges.** The reviewed cases span laboratory runup, local landslide and volcanic sources, regional earthquake inundation and basin propagation. Reported examples include 10–18 m/s inferred overland flow and near-30 m runup at Hokkaido and locally about 13 m runup after Anak Krakatau.

**Recent advances.** Recent work uses heterogeneous rupture ensembles, coupled high-fidelity source and efficient propagation models, benchmarked GPU solvers, neural-network inundation forecasts and automated coastal imagery to shorten the path from observation to actionable warning.

**Disagreements.** Source attribution can remain contested where earthquake and landslide mechanisms overlap. Efficient depth-averaged models enable ensembles but may omit dispersive or three-dimensional generation physics; deterministic reconstructions can fit observations without uniquely identifying the source.

**Limitations.** Sparse near-source observations, uncertain rupture or slide kinematics, bathymetric and topographic resolution, friction and building representation, breaking treatment, uncertain event rates and limited validation of extreme regimes constrain transferable predictions.

**Open questions.** Priorities include faster source characterization, reliable near-field warning, compound and cascading sources, probabilistic treatment of rare landslides, urban-scale inundation and loads, real-time assimilation, explainable machine learning, and climate-conditioned exposure.

**Seminal papers.** Classical long-wave and shallow-water theory established propagation and runup foundations; later benchmark programs standardized model verification, while post-event surveys connected observed runup and damage to source reconstruction and inundation physics.

## Claims

- **C1258.** Tsunami hazard assessment must explicitly distinguish earthquake, landslide and volcanic-collapse sources because their characteristic kinematics, directionality and near-field uncertainty require different source and modeling assumptions. *Regime: Multi-source tsunami hazard assessment, especially where submarine or volcanic mass movements are plausible..* [literature_review_statement, review] (Finn Løvholt 2015, [doi:10.1098/rsta.2014.0376](https://doi.org/10.1098/rsta.2014.0376))
- **C1631.** At Palaikastro, Crete, an erosional, chaotic deposit containing Santorini ash intraclasts, marine shells and microfauna, imbricated beach pebbles, building stones, ceramics and bones provides convergent geoarchaeological evidence for a tsunami coeval with the Late Minoan Santorini eruption. *Regime: Late Minoan IA coastal settlement deposits at Palaikastro, northeastern Crete..* [direct_finding, field] (Hendrik J. Bruins 2007, [doi:10.1016/j.jas.2007.08.017](https://doi.org/10.1016/j.jas.2007.08.017))

## Papers

- Hendrik J. Bruins (2007). Geoarchaeological tsunami deposits at Palaikastro (Crete) and the Late Minoan IA eruption of Santorini. *Journal of Archaeological Science*. [doi:10.1016/j.jas.2007.08.017](https://doi.org/10.1016/j.jas.2007.08.017)
- Philip Watts (2003). Landslide tsunami case studies using a Boussinesq model and a fully nonlinear tsunami generation model. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-3-391-2003](https://doi.org/10.5194/nhess-3-391-2003)
- Stéphan T. Grilli (2019). Modelling of the tsunami from the December 22, 2018 lateral collapse of Anak Krakatau volcano in the Sunda Straits, Indonesia. *Scientific Reports*. [doi:10.1038/s41598-019-48327-6](https://doi.org/10.1038/s41598-019-48327-6)
- David R. Tappin (2014). Did a submarine landslide contribute to the 2011 Tohoku tsunami?. *Marine Geology*. [doi:10.1016/j.margeo.2014.09.043](https://doi.org/10.1016/j.margeo.2014.09.043)
- David R. Tappin (2008). The Papua New Guinea tsunami of 17 July 1998: anatomy of a catastrophic event. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-8-243-2008](https://doi.org/10.5194/nhess-8-243-2008)
- Anawat Suppasri (2013). Lessons Learned from the 2011 Great East Japan Tsunami: Performance of Tsunami Countermeasures, Coastal Buildings, and Tsunami Evacuation in Japan. *Pure and Applied Geophysics*. [doi:10.1007/s00024-012-0511-7](https://doi.org/10.1007/s00024-012-0511-7)
- Junliang Gao (2020). Numerical investigation of harbor oscillations induced by focused transient wave groups. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103670](https://doi.org/10.1016/j.coastaleng.2020.103670)
- Finn Løvholt (2015). On the characteristics of landslide tsunamis. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences*. [doi:10.1098/rsta.2014.0376](https://doi.org/10.1098/rsta.2014.0376)
- Stéphane Abadie (2012). Numerical modeling of tsunami waves generated by the flank collapse of the Cumbre Vieja Volcano (La Palma, Canary Islands): Tsunami source and near field effects. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2011jc007646](https://doi.org/10.1029/2011jc007646)
- González (2009). Probabilistic tsunami hazard assessment at Seaside, Oregon, for near‐ and far‐field seismic sources. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2008jc005132](https://doi.org/10.1029/2008jc005132)
- В. В. Титов (1997). Extreme inundation flows during the Hokkaido‐Nansei‐Oki Tsunami. *Geophysical Research Letters*. [doi:10.1029/97gl01128](https://doi.org/10.1029/97gl01128)
- Katsuichiro Goda (2014). Sensitivity of tsunami wave profiles and inundation simulations to earthquake slip and fault geometry for the 2011 Tohoku earthquake. *Earth, Planets and Space*. [doi:10.1186/1880-5981-66-105](https://doi.org/10.1186/1880-5981-66-105)
- Fumiyasu Makinoshima (2021). Early forecasting of tsunami inundation from tsunami and geodetic observation data with convolutional neural networks. *Nature Communications*. [doi:10.1038/s41467-021-22348-0](https://doi.org/10.1038/s41467-021-22348-0)
- Christof Mueller (2015). Effects of rupture complexity on local tsunami inundation: Implications for probabilistic tsunami hazard assessment by example. *Journal of Geophysical Research: Solid Earth*. [doi:10.1002/2014jb011301](https://doi.org/10.1002/2014jb011301)
- Jorge Macı́as (2017). Performance Benchmarking of Tsunami-HySEA Model for NTHMP’s Inundation Mapping Activities. *Pure and Applied Geophysics*. [doi:10.1007/s00024-017-1583-1](https://doi.org/10.1007/s00024-017-1583-1)
- Finn Løvholt (2012). Stochastic analysis of tsunami runup due to heterogeneous coseismic slip and dispersion. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2011jc007616](https://doi.org/10.1029/2011jc007616)
- Finn Løvholt (2012). Modeling propagation and inundation of the 11 March 2011 Tohoku tsunami. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-12-1017-2012](https://doi.org/10.5194/nhess-12-1017-2012)
- Ingrid Charvet (2013). New tsunami runup relationships based on long wave experiments. *Ocean Modelling*. [doi:10.1016/j.ocemod.2013.05.009](https://doi.org/10.1016/j.ocemod.2013.05.009)
- Shirai (2025). Automated wave runup monitoring using coastal CCTV cameras for tsunami detection. *Scientific Reports*. [doi:10.1038/s41598-025-28874-x](https://doi.org/10.1038/s41598-025-28874-x)
