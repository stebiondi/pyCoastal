# Flood mapping and inundation

`inundation` | Prediction and representation of flood extent and depth.

Subtopics: [Inundation modeling](inundation.models.md), [Topographic and bathymetric controls](inundation.topography.md), [Flood-map uncertainty](inundation.uncertainty.md)

Papers: 14. Claims: 1. Equations: 0.

## Synthesis

**Well established.** Inundation is controlled by conservation of water across connected terrain, with wetting and drying, storage, friction, drainage, defenses and boundary forcing determining extent, depth, velocity and arrival time. Reliable maps require both hydraulic realism and defensible terrain and forcing data.

**Governing physics.** Flood waves spread according to pressure gradients, inertia, friction and topographic connectivity; rainfall, runoff, river discharge, tide, surge, waves and failures can interact. Small elevation errors can open or close flow paths, while defenses and drainage create thresholds and discontinuities.

**Dimensionless parameters.** Useful controls include Froude number, relative depth, friction and slope ratios, Courant number, grid spacing relative to hydraulic controls, DEM error relative to flood depth, compound-driver dependence, validation overlap and depth-error metrics, and computational speedup.

**Major equations.** Models solve shallow-water or diffusion-wave mass and momentum equations, sometimes coupled to rainfall–runoff and coastal boundary models. Reduced approaches use HAND or storage/connectivity rules; surrogates emulate depth and extent, while probabilistic maps integrate hazard frequency and uncertain inputs.

**Typical methods.** Workflows assemble conditioned terrain, roughness, drainage and defenses; generate rainfall, river and coastal boundaries; solve 1D/2D hydraulics or surrogates; validate against satellite extent, lidar, gauges, water marks and arrival times; and propagate forcing, parameter, DEM and model-structure uncertainty.

**Numerical models.** Representations include coupled rainfall–runoff–inundation diffusion waves, full shallow-water solvers on structured or unstructured grids, HAND, MIKE11 GIS, MSN_Flood, Gaussian-process/EOF surrogates and physics-aware classifiers. Model choice trades process fidelity, data needs and forecast speed.

**Experimental datasets.** Reviewed evidence includes the 2010 Kabul flood, historical dam-break test cases, MERIT/SRTM ensembles benchmarked against lidar, the 2016 Brazos Landsat extent, southwest Florida climate ensembles, Cork compound scenarios, the 2000 Langat flood and sparse-observation mapping applications.

**Validated ranges.** Reported performance is case-specific: Brazos extent overlap ranged 56–70%, Langat sampled-map agreement was 70%, and one hybrid surrogate was 12 times faster than its high-resolution model. These metrics use different observations and cannot be directly ranked as universal skill.

**Recent advances.** Recent advances simulate spatial DEM error, learn physics-aware maps from sparse data, emulate unstructured high-resolution models, integrate pluvial–fluvial–coastal drivers and translate climate ensembles into changing inundation magnitude and recurrence.

**Disagreements.** Fast terrain-based or learned models can support large-domain warning but may miss momentum, inter-catchment exchange or compound pathways; high-resolution hydrodynamics represents these processes but costs more and remains sensitive to terrain and friction. Extent-only agreement can conceal depth or timing error.

**Limitations.** DEM bias, unresolved buildings and defenses, uncertain roughness and drainage, sparse extreme observations, boundary dependence, climate and downscaling spread, numerical wetting/drying choices and inconsistent validation metrics limit confidence. Static maps do not demonstrate event forecasting skill.

**Open questions.** Priorities include dynamic defense and drainage failure, compound dependence, urban microtopography, transparent DEM ensembles, rapid depth-and-velocity surrogates, transfer under nonstationarity, observation assimilation and common multi-variable validation benchmarks.

**Seminal papers.** Early storage-cell and shallow-water models established dynamic floodplain routing; GIS and DEM methods enabled regional mapping, and satellite observations supported extent validation. Modern work combines high-resolution solvers, ensembles and emulators for operational and climate-scale analysis.

## Claims

- **C1173.** Coastal inundation assessment must jointly represent changing storm forcing, sea-level rise, precipitation and their probabilistic dependence because their combined effects can alter both flood magnitude and recurrence nonlinearly. *Regime: Large southwest Florida coastal floodplain and the study's climate/downscaling scenarios..* [direct_finding, numerical] (Y. Peter Sheng 2022, [doi:10.1038/s41598-022-07010-z](https://doi.org/10.1038/s41598-022-07010-z))

## Papers

- Takahiro Sayama (2012). Rainfall–runoff–inundation analysis of the 2010 Pakistan flood in the Kabul River basin. *Hydrological Sciences Journal*. [doi:10.1080/02626667.2011.644245](https://doi.org/10.1080/02626667.2011.644245)
- Francesca Aureli (2021). Review of Historical Dam-Break Events and Laboratory Tests on Real Topography for the Validation of Numerical Models. *Water*. [doi:10.3390/w13141968](https://doi.org/10.3390/w13141968)
- Laurence Hawker (2018). Implications of Simulating Global Digital Elevation Models for Flood Inundation Studies. *Water Resources Research*. [doi:10.1029/2018wr023279](https://doi.org/10.1029/2018wr023279)
- Karim I. Abdrabo (2020). Integrated Methodology for Urban Flood Risk Mapping at the Microscale in Ungauged Regions: A Case Study of Hurghada, Egypt. *Remote Sensing*. [doi:10.3390/rs12213548](https://doi.org/10.3390/rs12213548)
- Percival (2019). A methodology for urban micro-scale coastal flood vulnerability and risk assessment and mapping. *Natural Hazards*. [doi:10.1007/s11069-019-03648-7](https://doi.org/10.1007/s11069-019-03648-7)
- Niels Fraehr (2023). Development of a Fast and Accurate Hybrid Model for Floodplain Inundation Simulations. *Water Resources Research*. [doi:10.1029/2022wr033836](https://doi.org/10.1029/2022wr033836)
- Dedekorkut-Howes (2021). Planning for a different kind of sea change: lessons from Australia for sea level rise and coastal flooding. *Climate Policy*. [doi:10.1080/14693062.2020.1819766](https://doi.org/10.1080/14693062.2020.1819766)
- Jiaqi Zhang (2018). Comparative Analysis of Inundation Mapping Approaches for the 2016 Flood in the Brazos River, Texas. *JAWRA Journal of the American Water Resources Association*. [doi:10.1111/1752-1688.12623](https://doi.org/10.1111/1752-1688.12623)
- Y. Peter Sheng (2022). A sensitivity study of rising compound coastal inundation over large flood plains in a changing climate. *Scientific Reports*. [doi:10.1038/s41598-022-07010-z](https://doi.org/10.1038/s41598-022-07010-z)
- Jennifer Isabel Munro Kirkpatrick (2020). Modelling the effects of climate change on urban coastal-fluvial flooding. *Journal of Water and Climate Change*. [doi:10.2166/wcc.2020.166](https://doi.org/10.2166/wcc.2020.166)
- Billa (2011). Pre‐flood inundation mapping for flood early warning. *Journal of Flood Risk Management*. [doi:10.1111/j.1753-318x.2011.01115.x](https://doi.org/10.1111/j.1753-318x.2011.01115.x)
- Sainju (2021). Flood Inundation Mapping with Limited Observations Based on Physics-Aware Topography Constraint. *Frontiers in Big Data*. [doi:10.3389/fdata.2021.707951](https://doi.org/10.3389/fdata.2021.707951)
- Hallin (2025). RoadRAT – A new framework to assess the probability of inundation, wave runup, and erosion impacting coastal roads. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104741](https://doi.org/10.1016/j.coastaleng.2025.104741)
- MIMURA (2010). Effectivity of Storm Surge - Wave Hindcasting Coupling Model on Estimation of Storm Surge at T7010. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.66.216](https://doi.org/10.2208/kaigan.66.216)
