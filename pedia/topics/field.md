# Field measurements

`field` | In-situ observations of coastal processes.

Subtopics: [Extreme-event observations](field.extreme.md), [Sediment and morphology observations](field.sediment.md), [Tracer and drifter studies](field.tracers.md), [Wave and current observations](field.waves.md)

Papers: 24. Claims: 10. Equations: 0.

## Synthesis

**Well established.** Coastal field measurement requires simultaneous attention to the process, decision variable, spatial and temporal scales, platform response, calibration, datum, sampling design, uncertainty, metadata and survivability; a sensor record is not automatically a representative observation.

**Governing physics.** Instruments sample coupled waves, currents, water levels, turbulence, sediment, bathymetry and morphology through mechanical, pressure, acoustic, optical, electromagnetic or satellite interactions, each filtered by platform motion, geometry, propagation, scattering and environmental interference.

**Dimensionless parameters.** Observational adequacy depends on sampling-to-process frequency, record-length-to-event scale, spatial spacing relative to wavelength or morphology, signal-to-noise ratio, platform speed and footprint, relative water depth, wave and current regime, sediment size, calibration range, data return and uncertainty ratios.

**Major equations.** Core relations include sensor transfer and calibration functions, wave spectra and directional moments, velocity and discharge transformations, acoustic or optical backscatter inversion, sediment and volume budgets, datum and coordinate transformations, sampling and aliasing criteria, and uncertainty propagation or data-assimilation observation operators.

**Typical methods.** Methods combine fixed gauges and profilers, pressure and velocity arrays, tide gauges, GNSS and survey control, lidar and photogrammetry, multibeam and sidescan acoustics, sediment traps and optical sensors, drifters, autonomous vehicles, satellites, repeat topobathymetry and coordinated multi-platform campaigns.

**Numerical models.** Field data support retrieval and inversion algorithms, quality-control systems, spectral and directional estimators, observation operators, data assimilation, process-model calibration and validation, uncertainty models, adaptive sampling and digital observing-system design.

**Experimental datasets.** The reviewed evidence includes a nine-station barred-beach array, multi-site European storm morphology, Willapa Bay wave–current observations, reef-to-island flooding transects, barrier-reef networks, autonomous sandbank plume surveys, multibeam sediment calibration and satellite wind-wave-current products.

**Validated ranges.** Examples span beaches, tidal bays, coral and barrier reefs, shallow sandbanks and regional-to-global satellite coverage, from intra-wave sensing through tidal and storm campaigns to multi-year morphology; each dataset remains bounded by its platform and site regime.

**Recent advances.** Recent advances integrate satellite winds, waves and currents; autonomous underwater and surface vehicles; calibrated multibeam concentration mapping; dense cross-shore arrays; rapid repeat topobathymetry; cloud-ready standards; and observation-model fusion with explicit uncertainty.

**Disagreements.** Point instruments resolve time but may miss spatial structure; remote sensors resolve area but infer rather than directly sample variables; Eulerian and Lagrangian views differ; proxy shorelines and concentrations are algorithm-dependent; denser sampling can still be biased if placement or duration misses the governing process.

**Limitations.** Energetic events cause sensor loss and saturation; biofouling, bubbles, turbidity and bed mobility corrupt signals; datums and clocks drift; platforms disturb or move with the flow; calibration may not span field conditions; short records alias extremes and morphology; access and maintenance constrain continuity.

**Open questions.** Priorities include event-resilient and low-cost sustained arrays, seamless land–water topobathymetry, direct sediment-flux sensing, uncertainty covariance across platforms, compound-hazard measurements, adaptive sampling, autonomous calibration, reproducible retrievals and equitable long-term observing networks.

**Seminal papers.** Early coastal field programs established pressure and current arrays, sediment concentration sampling, profile surveys, spectral analysis and wave–current boundary-layer observations; satellite altimetry, imaging, acoustics and autonomous platforms later expanded coverage and repeatability.

## Claims

- **C1014.** A review shows that autonomous underwater vehicles extend marine geoscience observations through repeatable, high-resolution, spatially continuous surveys while imposing navigation, endurance, payload, calibration, and data-management constraints. *Regime: Autonomous Underwater Vehicles (AUVs): Their past, present and future contributions to the advancement of marine geoscience.* [literature_review_statement, review] (Russell B. Wynn 2014, [doi:10.1016/j.margeo.2014.03.012](https://doi.org/10.1016/j.margeo.2014.03.012))
- **C1015.** A two-month nine-station cross-shore array jointly measured waves, currents, and seabed position to resolve natural sandbar evolution rather than inferring morphology from hydrodynamics alone. *Regime: Observations of sand bar evolution on a natural beach.* [direct_finding, field] (Edith L. Gallagher 1998, [doi:10.1029/97jc02765](https://doi.org/10.1029/97jc02765))
- **C1016.** A coordinated Atlantic European dataset links the exceptional 2013/2014 winter wave climate to spatially variable beach morphological impacts across multiple sites. *Regime: Extreme wave activity during 2013/2014 winter and morphological impacts along the Atlantic coast of Europe.* [direct_finding, field] (Gerd Masselink 2016, [doi:10.1002/2015gl067492](https://doi.org/10.1002/2015gl067492))
- **C1017.** Field observations in Willapa Bay resolve wave–current interaction in a tidal coastal system and demonstrate that wave and circulation measurements must be interpreted jointly. *Regime: Wave-current interaction in Willapa Bay.* [direct_finding, field] (Maitane Olabarrieta 2011, [doi:10.1029/2011jc007387](https://doi.org/10.1029/2011jc007387))
- **C1018.** A reef-to-island observational transect connects offshore water levels and low-frequency wave transformation to runup, overwash, and coastal flooding. *Regime: Observations of wave transformation over a fringing coral reef and the importance of low‐frequency waves and offshore water levels to runup, overwash, and coastal flooding.* [direct_finding, field] (Olivia M. Cheriton 2016, [doi:10.1002/2015jc011231](https://doi.org/10.1002/2015jc011231))
- **C1019.** A review of satellite surface winds, waves, and currents identifies complementary observables, retrieval limitations, calibration needs, and scientific and operational uses. *Regime: Satellite Remote Sensing of Surface Winds, Waves, and Currents: Where are we Now?.* [literature_review_statement, review] (Danièle Hauser 2023, [doi:10.1007/s10712-023-09771-2](https://doi.org/10.1007/s10712-023-09771-2))
- **C1020.** A cross-shore field-instrument network combined with numerical analysis resolves wave transformation over a barrier reef and provides a process-consistent observational benchmark. *Regime: Wave transformation over a barrier reef.* [direct_finding, mixed] (Damien Sous 2019, [doi:10.1016/j.csr.2019.07.010](https://doi.org/10.1016/j.csr.2019.07.010))
- **C1021.** Wave-glider monitoring demonstrates an autonomous approach for mapping sediment transport and dredge plumes in a shallow marine sandbank environment. *Regime: Wave Glider Monitoring of Sediment Transport and Dredge Plumes in a Shallow Marine Sandbank Environment.* [direct_finding, field] (V. Van Lancker 2015, [doi:10.1371/journal.pone.0128948](https://doi.org/10.1371/journal.pone.0128948))
- **C1022.** Calibration of multibeam acoustic backscatter provides spatially resolved suspended-sediment concentration fields while making inversion and calibration assumptions explicit. *Regime: Suspended sediment concentration field quantified from a calibrated MultiBeam EchoSounder.* [direct_finding, mixed] (Guillaume Fromant 2021, [doi:10.1016/j.apacoust.2021.108107](https://doi.org/10.1016/j.apacoust.2021.108107))
- **C1344.** A coastal-observing review provides ten recommendations for sustaining mooring networks, including stakeholder-led requirements, complementary technologies, standardized open data, performance metrics and routine network-design assessment. *Regime: Coastal Mooring Observing Networks and Their Data Products: Recommendations for the Next Decade.* [literature_review_statement, review] (Kathleen Bailey 2019, [doi:10.3389/fmars.2019.00180](https://doi.org/10.3389/fmars.2019.00180))

## Papers

- Russell B. Wynn (2014). Autonomous Underwater Vehicles (AUVs): Their past, present and future contributions to the advancement of marine geoscience. *Marine Geology*. [doi:10.1016/j.margeo.2014.03.012](https://doi.org/10.1016/j.margeo.2014.03.012)
- Edith L. Gallagher (1998). Observations of sand bar evolution on a natural beach. *Journal of Geophysical Research: Oceans*. [doi:10.1029/97jc02765](https://doi.org/10.1029/97jc02765)
- Gerd Masselink (2016). Extreme wave activity during 2013/2014 winter and morphological impacts along the Atlantic coast of Europe. *Geophysical Research Letters*. [doi:10.1002/2015gl067492](https://doi.org/10.1002/2015gl067492)
- Maitane Olabarrieta (2011). Wave-current interaction in Willapa Bay. *Journal of Geophysical Research*. [doi:10.1029/2011jc007387](https://doi.org/10.1029/2011jc007387)
- Olivia M. Cheriton (2016). Observations of wave transformation over a fringing coral reef and the importance of low‐frequency waves and offshore water levels to runup, overwash, and coastal flooding. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2015jc011231](https://doi.org/10.1002/2015jc011231)
- Danièle Hauser (2023). Satellite Remote Sensing of Surface Winds, Waves, and Currents: Where are we Now?. *Surveys in Geophysics*. [doi:10.1007/s10712-023-09771-2](https://doi.org/10.1007/s10712-023-09771-2)
- Kathleen Bailey (2019). Coastal Mooring Observing Networks and Their Data Products: Recommendations for the Next Decade. *Frontiers in Marine Science*. [doi:10.3389/fmars.2019.00180](https://doi.org/10.3389/fmars.2019.00180)
- Damien Sous (2019). Wave transformation over a barrier reef. *Continental Shelf Research*. [doi:10.1016/j.csr.2019.07.010](https://doi.org/10.1016/j.csr.2019.07.010)
- V. Van Lancker (2015). Wave Glider Monitoring of Sediment Transport and Dredge Plumes in a Shallow Marine Sandbank Environment. *PLoS ONE*. [doi:10.1371/journal.pone.0128948](https://doi.org/10.1371/journal.pone.0128948)
- Guillaume Fromant (2021). Suspended sediment concentration field quantified from a calibrated MultiBeam EchoSounder. *Applied Acoustics*. [doi:10.1016/j.apacoust.2021.108107](https://doi.org/10.1016/j.apacoust.2021.108107)
- Klemas (2015). Coastal and Environmental Remote Sensing from Unmanned Aerial Vehicles: An Overview. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-15-00005.1](https://doi.org/10.2112/jcoastres-d-15-00005.1)
- Vincent Vuik (2016). Nature-based flood protection: The efficiency of vegetated foreshores for reducing wave loads on coastal dikes. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.06.001](https://doi.org/10.1016/j.coastaleng.2016.06.001)
- Philip D. Osborne (1992). Frequency dependent cross-shore suspended sediment transport. 1. A non-barred shoreface. *Marine Geology*. [doi:10.1016/0025-3227(92)90052-j](https://doi.org/10.1016/0025-3227(92)90052-j)
- Irene Delgado‐Fernández (2010). Meso-scale aeolian sediment input to coastal dunes: The nature of aeolian transport events. *Geomorphology*. [doi:10.1016/j.geomorph.2010.11.005](https://doi.org/10.1016/j.geomorph.2010.11.005)
- Glen Gawarkiewicz (2007). Observing Larval Transport Processes Affecting Population Connectivity: Progress and Challenges. *Oceanography*. [doi:10.5670/oceanog.2007.28](https://doi.org/10.5670/oceanog.2007.28)
- Irene Delgado‐Fernández (2011). Meso-scale modelling of aeolian sediment input to coastal dunes. *Geomorphology*. [doi:10.1016/j.geomorph.2011.04.001](https://doi.org/10.1016/j.geomorph.2011.04.001)
- Troels Aagaard (2002). Cross-shore suspended sediment transport in the surf zone: a field-based parameterization. *Marine Geology*. [doi:10.1016/s0025-3227(02)00193-7](https://doi.org/10.1016/s0025-3227(02)00193-7)
- Davide Bonaldo (2018). Integrating multidisciplinary instruments for assessing coastal vulnerability to erosion and sea level rise: lessons and challenges from the Adriatic Sea, Italy. *Journal of Coastal Conservation*. [doi:10.1007/s11852-018-0633-x](https://doi.org/10.1007/s11852-018-0633-x)
- Carlo Ruzzo (2021). Scaling strategies for multi-purpose floating structures physical modeling: state of art and new perspectives. *Applied Ocean Research*. [doi:10.1016/j.apor.2020.102487](https://doi.org/10.1016/j.apor.2020.102487)
- Sjoerd Groeskamp (2011). Observations of estuarine circulation and solitary internal waves in a highly energetic tidal channel. *Ocean Dynamics*. [doi:10.1007/s10236-011-0455-y](https://doi.org/10.1007/s10236-011-0455-y)
- Davide Wüthrich (2021). Strong free-surface turbulence in breaking bores: a physical study on the free-surface dynamics and air–water interfacial features. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2021.614](https://doi.org/10.1017/jfm.2021.614)
- Hongbin Hao (2022). Wind turbine model-test method for achieving similarity of both model- and full-scale thrusts and torques. *Applied Ocean Research*. [doi:10.1016/j.apor.2022.103444](https://doi.org/10.1016/j.apor.2022.103444)
- Alejandro J. Souza (2001). Tidal mixing modulation of sea-surface temperature and diatom abundance in Southern California. *Continental Shelf Research*. [doi:10.1016/s0278-4343(00)00105-9](https://doi.org/10.1016/s0278-4343(00)00105-9)
- KAWANISHI (2007). Effects of Wind on Salinity Intrusion and Sediment Transport in Ohtagawa Estuary. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.54.396](https://doi.org/10.2208/proce1989.54.396)
