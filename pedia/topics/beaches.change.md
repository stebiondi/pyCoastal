# Shoreline change

`beaches.change` | Retreat, advance, and variability.

Parent: [Beaches and shoreline evolution](beaches.md)

Papers: 21. Claims: 15. Equations: 2.

Used by pyCoastal design modules: Beach nourishment.

## Synthesis

**Well established.** Beach change is spatially and temporally variable: shoreline indicators respond to waves, water level, sediment supply, morphology and engineering, while erosion at one interval or transect can coexist with accretion nearby or later.

**Governing physics.** Cross-shore storm erosion and recovery redistribute profile sediment, alongshore transport gradients rotate or translate shorelines, inlets and headlands reorganize cells, and nourishment or construction alters sediment budgets; waterline position also moves instantaneously with tide, runup and setup.

**Dimensionless parameters.** Controls include shoreline displacement relative to positional uncertainty, observation duration relative to storm and recovery cycles, beach width normalized by wave runup, sediment-budget imbalance, closure-depth ratio, wave obliquity, nourishment volume per shoreline length and erosion/accretion cluster significance.

**Major equations.** Change metrics fit shoreline position versus time for endpoint or linear-regression rates and uncertainty, compute transect displacement and area or volume budgets, and relate gradients in alongshore transport to shoreline movement through one-line continuity; probabilistic methods characterize indicator and classification error.

**Typical methods.** Workflows define a repeatable shoreline proxy, harmonize imagery and datums, correct tide or waterline effects, quantify georeferencing and classification uncertainty, cast stable transects, calculate rates and confidence intervals, detect clusters or change points, validate against surveys and interpret results with forcing and interventions.

**Numerical models.** The reviewed set emphasizes satellite classification and statistical change analysis, including fuzzy c-means and spatial clustering. Hybrid two-dimensional/one-line, moment and climate-response shoreline models remain in the lawful-full-text queue.

**Experimental datasets.** Reviewed evidence includes 769 Haikou images from 1986-2023, Iztuzu transects and clusters for 2013-2022, national cross-mission remote sensing, northwest Ireland waterlines from 1999-2024 and fuzzy-classified northern Java change from 1994-2000.

**Validated ranges.** Findings cover selected urban, nourished, storm-affected, dissipative, reflective and deltaic coasts over years to decades. Reported rates and intervention associations are site-, proxy-, resolution- and interval-specific.

**Recent advances.** Recent advances combine cross-mission optical and SAR imagery, subpixel and probabilistic classification, lidar and video validation, cloud-scale transect analysis, Bayesian change points, physics-informed shoreline models and explicit propagation of waterline and geolocation uncertainty.

**Disagreements.** Different shoreline proxies—instantaneous waterline, wet/dry line, vegetation line or modeled datum contour—can yield different trends. Linear rates can conceal episodic storms, recovery and interventions, and apparent accretion need not imply positive subaqueous sediment volume.

**Limitations.** Clouds, pixel size, georegistration, tidal stage, runup, datum mismatch, proxy migration, sparse ground truth, short or uneven sampling, anthropogenic confounding and absent profile volume limit attribution. Random positional error does not capture all systematic bias.

**Open questions.** Priorities include globally consistent uncertainty-aware shoreline products, separation of waterline and morphology, profile-volume assimilation, intervention causal inference, storm-recovery memory, sediment-cell closure, compound drivers and forecast validation under nonstationary climate and management.

**Seminal papers.** Repeated beach profiles and aerial-photo transects established quantitative shoreline monitoring; sediment-budget and one-line theory linked transport gradients to movement, while satellite archives and automated extraction enabled dense regional and global time series.

## Equations

### Net shoreline movement

$$
NSM=d_{t_2}-d_{t_1}
$$

Regime: Each shore-normal DSAS transect between two georeferenced shoreline dates.

Variables: `d_t2` shoreline position at the youngest date; `d_t1` shoreline position at the oldest date

Source: (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))

### End point shoreline-change rate

$$
EPR=\frac{d_{t_2}-d_{t_1}}{t_2-t_1}
$$

Regime: Endpoint trend at an Iztuzu DSAS transect; ignores intermediate shorelines.

Variables: `d_t2` youngest shoreline position; `d_t1` oldest shoreline position; `t2-t1` elapsed time

Source: (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))

## Claims

- **C113.** Between 2013 and 2022, Iztuzu Zones II-IV were predominantly erosional, whereas Zones I and V contained the strongest accretion, with substantial variation among subperiods. *Regime: Manually digitized Google Earth shorelines at 18 dates along Iztuzu Beach; shoreline-position uncertainty from water level and image timing remains..* [direct_finding, field] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C115.** Of 819 Iztuzu shoreline transects, 287 points (35%) belonged to statistically significant erosion or deposition clusters, with erosion clusters concentrated mainly in Zone II and deposition clusters in Zone V. *Regime: 2013-2022 NSM-based hotspot analysis at 5 m transect spacing; results depend on manual shoreline extraction and neighborhood definition..* [direct_finding, field] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C148.** Fuzzy c-means shoreline classification at the northern Java site achieved kappa values of 0.86-0.96 and represented both boundary position and pixel-level change uncertainty, including 739 ha converted to water in 1994-2000. *Regime: The 1994-2015 optical images, t=0.5 membership threshold, and northern Java class definitions..* [direct_finding, field] (Dewi 2016, [doi:10.3390/rs8030190](https://doi.org/10.3390/rs8030190))
- **C152.** Across 769 Haikou images from 1986-2023, artificial-island construction and five nourishment projects were mainly associated with accretion, with a 4.9 m random waterline-position error. *Regime: Haikou Beach, its engineering chronology, and satellite mean-waterline proxy; association is not universal causation..* [direct_finding, field] (Hu 2024, [doi:10.3390/rs16132469](https://doi.org/10.3390/rs16132469))
- **C154.** Over 1999-2024, two broad dissipative northwest Ireland beaches remained comparatively stable or accreting under consistent extreme-waterline trends, whereas the narrower reflective beach showed the greatest variability and landward retreat. *Regime: The three undisturbed northwest Ireland beaches and their satellite waterline proxies..* [direct_finding, field] (Riaz 2026, [doi:10.1016/j.coastaleng.2025.104843](https://doi.org/10.1016/j.coastaleng.2025.104843))
- **C1355.** In an 18-year Tairua blind test, 19 process and machine-learning shoreline models lost skill on unseen 2014–2017 data and fast extremes; an ensemble outperformed individual models and exposed architecture uncertainty. *Regime: Blind testing of shoreline evolution models.* [direct_finding, mixed] (Jennifer Montaño 2020, [doi:10.1038/s41598-020-59018-y](https://doi.org/10.1038/s41598-020-59018-y))
- **C1357.** Satellite analysis for 1984–2016 estimates sandy beaches comprise 31% of ice-free shoreline; 24% erode faster than 0.5 m/yr, 28% accrete and 48% are stable. *Regime: The State of the World’s Beaches.* [direct_finding, mixed] (Arjen Luijendijk 2018, [doi:10.1038/s41598-018-24630-6](https://doi.org/10.1038/s41598-018-24630-6))
- **C1376.** Mekong delta shoreline analysis links rapid erosion to human-driven reductions and redistribution of river sediment rather than coastal forcing alone. *Regime: Linking rapid erosion of the Mekong River delta to human activities.* [direct_finding, mixed] (Edward J. Anthony 2015, [doi:10.1038/srep14745](https://doi.org/10.1038/srep14745))
- **C1377.** A shoreline-prediction review identifies nonstationary forcing, multiscale processes, data limitations and model uncertainty as central barriers to reliable coastal forecasts. *Regime: Challenges and Opportunities in Coastal Shoreline Prediction.* [literature_review_statement, review] (Splinter 2021, [doi:10.3389/fmars.2021.788657](https://doi.org/10.3389/fmars.2021.788657))
- **C1378.** Multitemporal remote sensing at Sayung documents spatially variable shoreline erosion and accretion suitable for diagnosing coastal change and management priorities. *Regime: Dynamics of shoreline changes in the coastal region of Sayung, Indonesia.* [direct_finding, mixed] (Ratna Dewi 2019, [doi:10.1016/j.ejrs.2019.09.001](https://doi.org/10.1016/j.ejrs.2019.09.001))
- **C1379.** Global long-term satellite observations quantify coastal erosion and accretion patterns and demonstrate that shoreline change is geographically heterogeneous rather than uniformly erosional. *Regime: Global long-term observations of coastal erosion and accretion.* [direct_finding, mixed] (Lorenzo Mentaschi 2018, [doi:10.1038/s41598-018-30904-w](https://doi.org/10.1038/s41598-018-30904-w))
- **C1401.** An ensemble Kalman filter improves shoreline modeling by assimilating observations and representing nonstationary future wave climates and associated forecast uncertainty. *Regime: Enhanced Coastal Shoreline Modeling Using an Ensemble Kalman Filter to Include Nonstationarity in Future Wave Climates.* [direct_finding, numerical] (Ibaceta 2020, [doi:10.1029/2020gl090724](https://doi.org/10.1029/2020gl090724))
- **C1511.** Remote surveys quantify rapid erosion of ice-rich Tuktoyaktuk Island and connect thermal-mechanical degradation to loss of a natural harbor barrier. *Regime: Mechanisms, volumetric assessment, and prognosis for rapid coastal erosion of Tuktoyaktuk Island, an important natural barrier for the harbour and community.* [direct_finding, field] (Dustin Whalen 2022, [doi:10.1139/cjes-2021-0101](https://doi.org/10.1139/cjes-2021-0101))
- **C1756.** Across 54 river deltas, multi-decadal shoreline response to diminished fluvial sediment supply was heterogeneous and often delayed, but eroding deltas experienced roughly twice the sediment-load reduction of stable or advancing deltas, indicating that sediment supply chiefly sustains resilience to marine forcing, subsidence, and sea-level rise rather than guaranteeing immediate shoreline advance. *Regime: Subaerial shorelines of 54 large and small river deltas worldwide, evaluated mainly from 1972-2015 satellite imagery and pre-/post-1970 river sediment-load evidence..* [direct_finding, mixed] (Manon Besset 2019, [doi:10.1016/j.earscirev.2019.04.018](https://doi.org/10.1016/j.earscirev.2019.04.018))
- **C1772.** Integrated 1947-2018 shoreline, elevation, stratigraphic, and ground-ice evidence shows that exposed-shore recession at Tuktoyaktuk Island accelerated from 1.58±0.05 to 1.80±0.02 m/year; erosion comprises 88% of island volume change (about 9,200 m3/year), and post-2000 rates project breach of the natural harbour barrier by 2044 or sooner. *Regime: Ice-rich permafrost barrier island protecting Tuktoyaktuk Harbour, western Canadian Arctic, with thermo-abrasional cliff undercutting, block failure, storm waves and surge, rising relative sea level, and an expanding open-water season..* [direct_finding, field] (Dustin Whalen 2022, [doi:10.1139/cjes-2021-0101](https://doi.org/10.1139/cjes-2021-0101))

## Papers

- Arjen Luijendijk (2018). The State of the World’s Beaches. *Scientific Reports*. [doi:10.1038/s41598-018-24630-6](https://doi.org/10.1038/s41598-018-24630-6) [published version, CC BY](https://www.nature.com/articles/s41598-018-24630-6.pdf)
- Lorenzo Mentaschi (2018). Global long-term observations of coastal erosion and accretion. *Scientific Reports*. [doi:10.1038/s41598-018-30904-w](https://doi.org/10.1038/s41598-018-30904-w) [published version, CC BY](https://www.nature.com/articles/s41598-018-30904-w.pdf)
- Edward J. Anthony (2015). Linking rapid erosion of the Mekong River delta to human activities. *Scientific Reports*. [doi:10.1038/srep14745](https://doi.org/10.1038/srep14745) [published version, CC BY](https://www.nature.com/articles/srep14745.pdf)
- Manon Besset (2019). Multi-decadal variations in delta shorelines and their relationship to river sediment supply: An assessment and review. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2019.04.018](https://doi.org/10.1016/j.earscirev.2019.04.018) [published version, read only](https://www.sciencedirect.com/science/article/am/pii/S0012825218306895?via%3Dihub)
- Jennifer Montaño (2020). Blind testing of shoreline evolution models. *Scientific Reports*. [doi:10.1038/s41598-020-59018-y](https://doi.org/10.1038/s41598-020-59018-y) [published version, CC BY](https://www.nature.com/articles/s41598-020-59018-y.pdf)
- Ibaceta (2020). Enhanced Coastal Shoreline Modeling Using an Ensemble Kalman Filter to Include Nonstationarity in Future Wave Climates. *Geophysical Research Letters*. [doi:10.1029/2020gl090724](https://doi.org/10.1029/2020gl090724) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2020GL090724)
- Splinter (2021). Challenges and Opportunities in Coastal Shoreline Prediction. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.788657](https://doi.org/10.3389/fmars.2021.788657) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2021.788657/pdf)
- Ratna Dewi (2019). Dynamics of shoreline changes in the coastal region of Sayung, Indonesia. *The Egyptian Journal of Remote Sensing and Space Science*. [doi:10.1016/j.ejrs.2019.09.001](https://doi.org/10.1016/j.ejrs.2019.09.001) [published version, CC BY-NC-ND](https://www.sciencedirect.com/science/article/pii/S1110982318302722/pdf)
- Dustin Whalen (2022). Mechanisms, volumetric assessment, and prognosis for rapid coastal erosion of Tuktoyaktuk Island, an important natural barrier for the harbour and community. *Canadian Journal of Earth Sciences*. [doi:10.1139/cjes-2021-0101](https://doi.org/10.1139/cjes-2021-0101) [published version, CC BY](https://doi.org/10.1139/cjes-2021-0101)
- Hu (2024). Satellite-Derived Shoreline Changes of an Urban Beach and Their Relationship to Coastal Engineering. *Remote Sensing*. [doi:10.3390/rs16132469](https://doi.org/10.3390/rs16132469) [published version, CC BY](https://www.mdpi.com/2072-4292/16/13/2469/pdf)
- Riaz (2026). Remote sensing techniques for exploring waterline influence on shoreline stability in Northwest Ireland. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104843](https://doi.org/10.1016/j.coastaleng.2025.104843) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383925001486?httpAccept=text/xml)
- Kılar (2025). Wave storm impacts on shoreline evolution: A case study of Iztuzu beach. *Ocean &amp; Coastal Management*. [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748) [published version, read only](https://acikerisim.uludag.edu.tr/bitstreams/c85bd685-4a66-457d-88b3-ab395a726911/download)
- Dongxian Kong (2014). Evolution of the Yellow River Delta and its relationship with runoff and sediment load from 1983 to 2011. *Journal of Hydrology*. [doi:10.1016/j.jhydrol.2014.09.038](https://doi.org/10.1016/j.jhydrol.2014.09.038) [accepted manuscript, read only](https://www.pure.ed.ac.uk/ws/files/17962644/Evolution_of_the_Yellow_River_Delta_and_its_relationship_with_runoff_and_sediment_load_from_1983_to_2011_2014_Journal_of_Hydrology.pdf)
- Michael R. Phillips (2005). Erosion and tourism infrastructure in the coastal zone: Problems, consequences and management. *Tourism Management*. [doi:10.1016/j.tourman.2005.10.019](https://doi.org/10.1016/j.tourman.2005.10.019) [accepted manuscript, read only](https://repository.uwtsd.ac.uk/id/eprint/694/1/Phillips%20and%20Jones%20-%20Tourism%20Management%20mss%2006-083.pdf)
- A. Toimil (2020). Climate change-driven coastal erosion modelling in temperate sandy beaches: Methods and uncertainty treatment. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2020.103110](https://doi.org/10.1016/j.earscirev.2020.103110) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0012825219303861)
- J.E.A. Storms (2008). Coastal dynamics under conditions of rapid sea-level rise: Late Pleistocene to Early Holocene evolution of barrier–lagoon systems on the northern Adriatic shelf (Italy). *Quaternary Science Reviews*. [doi:10.1016/j.quascirev.2008.02.009](https://doi.org/10.1016/j.quascirev.2008.02.009) [accepted manuscript, read only](https://archimer.ifremer.fr/doc/00000/4473/3984.pdf)
- Emma McAllister (2022). Multispectral satellite imagery and machine learning for the extraction of shoreline indicators. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104102](https://doi.org/10.1016/j.coastaleng.2022.104102) [accepted manuscript, read only](https://www.pure.ed.ac.uk/ws/portalfiles/portal/324587081/Manuscript_v1.pdf)
- Gonéri Le Cozannet (2016). Uncertainties in Sandy Shorelines Evolution under the Bruun Rule Assumption. *Frontiers in Marine Science*. [doi:10.3389/fmars.2016.00049](https://doi.org/10.3389/fmars.2016.00049) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2016.00049/pdf)
- Dewi (2016). Fuzzy Classification for Shoreline Change Monitoring in a Part of the Northern Coastal Area of Java, Indonesia. *Remote Sensing*. [doi:10.3390/rs8030190](https://doi.org/10.3390/rs8030190) [published version, CC BY](https://www.mdpi.com/2072-4292/8/3/190/pdf)
- Tsai (2024). Nation-scale multidecadal shoreline extraction and coastal spatio-temporal change monitoring using cross-mission remote sensing data. *Ocean &amp; Coastal Management*. [doi:10.1016/j.ocecoaman.2024.107136](https://doi.org/10.1016/j.ocecoaman.2024.107136) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0964569124001212?httpAccept=text/xml)
- Ye (2026). Coastal risk assessment and hazard forecast analysis via a Bayesian network. *Natural Hazards*. [doi:10.1007/s11069-026-08335-y](https://doi.org/10.1007/s11069-026-08335-y) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s11069-026-08335-y.pdf)
