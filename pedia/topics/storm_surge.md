# Storm surge and coastal flooding

`storm_surge` | Meteorologically forced coastal water levels and flooding.

Subtopics: [Compound flooding](storm_surge.compound.md), [Wave-surge-tide coupling](storm_surge.coupling.md), [Surge forcing](storm_surge.forcing.md), [Tropical cyclone flooding](storm_surge.hurricanes.md)

Papers: 6. Claims: 1. Equations: 0.

## Synthesis

**Well established.** Storm surge is the meteorologically forced departure of coastal water level from the astronomical tide. Wind stress, atmospheric pressure, storm track and translation interact with shelf and basin geometry; waves, tides, rivers and rainfall can substantially alter total flooding.

**Governing physics.** Wind transfers momentum to the water column, pressure gradients drive inverse-barometer response, rotation and bathymetry shape propagation, and nonlinear tide–surge interaction changes timing and amplitude. Waves add setup and overtopping; discharge encounters surge-driven backwater in estuaries and deltas.

**Dimensionless parameters.** Controls include storm size-to-shelf scale, translation-to-wave speed, Rossby and Froude numbers, drag coefficient, surge-to-tidal range, wave setup-to-surge ratio, discharge-to-tidal prism, coastal slope, return period and joint dependence measures.

**Major equations.** Depth-integrated or three-dimensional mass and momentum equations include wind and pressure forcing, Coriolis, bottom stress and wetting/drying. Spectral wave equations supply radiation stresses; hydrologic and hydraulic equations supply runoff, while extreme-value or event-set methods estimate probabilities.

**Typical methods.** Studies use tide gauges, wave buoys, reanalyses and post-event maps; synthetic or historical cyclone ensembles; SLOSH, ADCIRC, WW3, D-Flow and hydraulic models; nested inundation grids; peaks-over-threshold analysis; attribution and climate perturbation experiments.

**Numerical models.** Model chains range from statistical hurricane generation plus SLOSH to global routing bounded by dynamic tide-surge levels, regional surge–wave models, and NWM–D-Flow/HEC-RAS–ADCIRC/WW3 compound systems with wetting and drying.

**Experimental datasets.** Evidence includes synthetic New York hurricanes, 3,433 global river mouths, Storm Gloria, Hurricanes Isabel, Irene and Sandy in Delaware, 21 U.S. hurricanes from 2000–2013, and Liverpool Bay and wider European surge-wave applications.

**Validated ranges.** Reported values include up to 1 m surge and 8 m significant waves during Gloria, 0.79–0.91 Delaware peak-level skill, surge effects at 64% of global delta mouths, and average end-century U.S. hurricane inundation increases of 36% by volume and 25% by extent.

**Recent advances.** Recent work dynamically couples ocean, wave, river and floodplain models, uses large synthetic event sets, resolves deltas globally, perturbs historical cyclones under future climates and attributes flood response to interacting drivers and geography.

**Disagreements.** Surge-only models can omit wave and discharge contributions, while fully coupled systems add uncertain boundaries and parameters. Climate-modified storm characteristics do not map monotonically to inundation because track, timing and local geography interact nonlinearly.

**Limitations.** Cyclone sampling, wind and pressure bias, drag at extreme winds, bathymetric and topographic resolution, levees and drainage, wave setup and overtopping, river boundaries, dependence assumptions and nonstationarity limit transferable hazard estimates.

**Open questions.** Priorities include compound-driver dependence, changing cyclone tracks and structure, rapid coupled forecasts, urban drainage and defenses, uncertainty partitioning, equitable exposure and consistent global-to-local downscaling.

**Seminal papers.** Classical wind setup and inverse-barometer theory established surge forcing; numerical shallow-water models enabled operational prediction, and later tide–surge interaction, wave coupling and statistical event methods established modern hazard assessment.

## Claims

- **C1324.** Coastal storm-flood assessment should treat storm surge, astronomical tide, wind waves and their mean-circulation interactions as a coupled system whenever their combined water-level and overtopping effects are material. *Regime: Marine-storm flooding where surge, tide and wind-wave processes jointly affect coastal water level or impacts..* [literature_review_statement, review] (Judith Wolf 2008, [doi:10.5194/adgeo-17-19-2008](https://doi.org/10.5194/adgeo-17-19-2008))

## Papers

- Ning Lin (2010). Risk assessment of hurricane storm surge for New York City. *Journal of Geophysical Research: Atmospheres*. [doi:10.1029/2009jd013630](https://doi.org/10.1029/2009jd013630)
- Angel Amores (2020). Coastal impacts of Storm Gloria (January 2020) over the north-western Mediterranean. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-20-1955-2020](https://doi.org/10.5194/nhess-20-1955-2020)
- Dirk Eilander (2020). The effect of surge on riverine flood hazard and impact in deltas globally. *Environmental Research Letters*. [doi:10.1088/1748-9326/ab8ca6](https://doi.org/10.1088/1748-9326/ab8ca6)
- R. Bakhtyar (2020). A New 1D/2D Coupled Modeling Approach for a Riverine‐Estuarine System Under Storm Events: Application to Delaware River Basin. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2019jc015822](https://doi.org/10.1029/2019jc015822)
- Jeane Camelo (2020). Projected Climate Change Impacts on Hurricane Storm Surge Inundation in the Coastal United States. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2020.588049](https://doi.org/10.3389/fbuil.2020.588049)
- Judith Wolf (2008). Coupled wave and surge modelling and implications for coastal flooding. *Advances in Geosciences*. [doi:10.5194/adgeo-17-19-2008](https://doi.org/10.5194/adgeo-17-19-2008)
